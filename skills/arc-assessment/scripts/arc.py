#!/usr/bin/env python3
"""Query the ARC risk register for an assessment. Needs only Python 3.9+.

Fetches the register YAML from the official repository at a release tag (the
latest release unless --version is given), or reads an organisation's own
contextualised register with --register (a local directory or a base URL with
the same file layout as arc-risk-register/). With --overlay it applies an
organisation's overlay file on top: the organisation keeps only its own changes,
and the overlay names the register version it was written against. Uses PyYAML
if installed and a built-in parser for the register's YAML otherwise.

Commands:
  elements                       components, design elements and capabilities, with definitions
  assess --capabilities IDS      applicable risks and their controls for a system, and a check for
         [--components IDS]      capability combinations such as the lethal trifecta; --components names
                                 the conditional components the system has (e.g. CMP-04 for persistent memory)
         [--priority IDS|all]    ...and the controls in scope once priority risks are known
         [--profile FILE]        ...for a system described in a YAML file (capabilities with their
                                 authority, whether their effects are irreversible or external, and
                                 conditional components); see "Context" below
  show ID [ID ...]               full text of risks, controls or elements (RISK-034, CTRL-0062, CAP-07)
  template                       the ARC assessment template (Markdown)

Examples:
  python3 arc.py elements
  python3 arc.py assess --capabilities CAP-03,CAP-07,CAP-11
  python3 arc.py --version 2.0.0 assess --capabilities CAP-03,CAP-07 --priority RISK-034,RISK-044 --format json
  python3 arc.py --register ./our-arc-register assess --capabilities CAP-02,CAP-06
  python3 arc.py --overlay ./our-overlay.yaml assess --capabilities CAP-02,CAP-06

Context:
  A capability that acts on the world is used at an authority level: read, propose (a person carries
  out what the agent prepares), act-with-approval (the agent acts after a person approves each action)
  or act-alone. Give it inline, CAP-11=read, or in a profile file. Its effects may be irreversible and
  may reach outside the organisation; --reversible and --internal name the capabilities for which they
  do not. Anything left unstated is assumed to be the most cautious case, so no risk or stricter
  control level drops out until the context says it can.

Environment:
  ARC_CACHE_DIR   where release files are cached (default ~/.cache/arc-assessment;
                  caching is skipped if the directory can't be written)
"""

import argparse
import copy
import datetime
import http.client
import json
import os
import posixpath
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

REPO_RAW = "https://raw.githubusercontent.com/govtech-responsibleai/agentic-risk-capability-framework"
SITE = "https://govtech-responsibleai.github.io/agentic-risk-capability-framework/"
REGISTER_FILES = ("register", "risks", "controls", "capabilities", "components", "design", "hazards")
OPTIONAL_FILES = ("combinations",)  # older registers and organisation registers may lack them
TEMPLATE_PATH = "docs/implementation/assessment-template.md"
LEVELS = {0: "Level 0 · Cardinal", 1: "Level 1 · Standard", 2: "Level 2 · Best Practice"}
AUTHORITY = ("read", "propose", "act-with-approval", "act-alone")  # least to most


class ArcError(Exception):
    """A problem to report to the user without a traceback."""


def warn(msg):
    print(f"arc.py: {msg}", file=sys.stderr)


# ---------------------------------------------------------------- YAML

class MiniYAMLError(ValueError):
    pass


_BOOL = {**dict.fromkeys(("true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"), True),
         **dict.fromkeys(("false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF"), False)}


def _resolve(text):
    """Type a plain scalar the way PyYAML's safe loader does for the cases the register uses."""
    if text in ("", "~", "null", "Null", "NULL"):
        return None
    if text in _BOOL:
        return _BOOL[text]
    if re.fullmatch(r"[-+]?(0|[1-9][0-9_]*)", text):
        return int(text.replace("_", ""))
    if re.fullmatch(r"[-+]?([0-9][0-9_]*\.[0-9_]*|\.[0-9_]+)([eE][-+]?[0-9]+)?", text):
        return float(text.replace("_", ""))
    if re.fullmatch(r"\d{4}-\d\d-\d\d", text):
        return datetime.date.fromisoformat(text)
    return text


def mini_yaml_load(text):
    """Parse the YAML subset the ARC register uses: block mappings and sequences, plain and quoted
    (possibly multi-line) scalars, simple flow sequences and full-line comments. Used only when PyYAML
    isn't installed; CI checks it gives the same result as PyYAML on every register file."""
    lines = []
    for n, raw in enumerate(text.splitlines(), 1):
        body = raw.rstrip()
        stripped = body.lstrip(" ")
        if stripped.startswith("\t"):
            raise MiniYAMLError(f"line {n}: tab indentation")
        if stripped.startswith("#") or (not lines and stripped == "---"):
            continue
        lines.append((len(body) - len(stripped) if stripped else -1, stripped, n))

    def skip_blank(i):
        while i < len(lines) and lines[i][0] == -1:
            i += 1
        return i

    def is_item(s):
        return s == "-" or s.startswith("- ")

    def quoted(s, i, ind, q):
        """Read a quoted scalar starting at s (line i); return (value, rest_of_line, next_i)."""
        buf, j, k = s, i, 1
        while True:
            while k < len(buf):
                if buf[k] == q:
                    if q == "'" and k + 1 < len(buf) and buf[k + 1] == "'":
                        k += 2
                        continue
                    if q == '"' and buf[k - 1] == "\\" and not buf[k - 2:k] == "\\\\":
                        k += 1
                        continue
                    raw, rest = buf[1:k], buf[k + 1:].strip()
                    return _unquote(raw, q), rest, j + 1
                k += 1
            j += 1
            if j >= len(lines):
                raise MiniYAMLError(f"line {lines[i][2]}: unterminated quoted scalar")
            nxt = lines[j][1]
            buf += "\n" if lines[j][0] == -1 else (" " if not buf.endswith("\n") else "") + nxt

    def _unquote(raw, q):
        raw = re.sub(r" ?\n ?", "\n", raw)
        if q == "'":
            return raw.replace("''", "'")
        out, k = [], 0
        esc = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "/": "/", "0": "\0", "r": "\r", " ": " "}
        while k < len(raw):
            ch = raw[k]
            if ch == "\\" and k + 1 < len(raw):
                nx = raw[k + 1]
                if nx in esc:
                    out.append(esc[nx]); k += 2; continue
                if nx in "xuU":
                    width = {"x": 2, "u": 4, "U": 8}[nx]
                    out.append(chr(int(raw[k + 2:k + 2 + width], 16))); k += 2 + width; continue
                raise MiniYAMLError(f"unsupported escape \\{nx}")
            out.append(ch); k += 1
        return "".join(out)

    def flow_seq(s, i):
        if not s.endswith("]"):
            raise MiniYAMLError(f"line {lines[i][2]}: multi-line flow sequence")
        inner = s[1:-1].strip()
        if not inner:
            return []
        items, cur, q = [], "", None
        for ch in inner:
            if q:
                cur += ch
                if ch == q:
                    q = None
            elif ch in "'\"":
                q = ch; cur += ch
            elif ch == ",":
                items.append(cur.strip()); cur = ""
            else:
                cur += ch
        items.append(cur.strip())
        return [_unquote(x[1:-1], x[0]) if x[:1] in "'\"" else _resolve(x) for x in items]

    def scalar(s, i, ind):
        """Value starting with text s on line i, where the owning key/dash is at indent ind."""
        if s[:1] in ("'", '"'):
            val, rest, j = quoted(s, i, ind, s[0])
            if rest and not rest.startswith("#"):
                raise MiniYAMLError(f"line {lines[i][2]}: text after quoted scalar")
            return val, j
        if s.startswith("["):
            return flow_seq(s, i), i + 1
        if s.startswith("{"):
            if s == "{}":
                return {}, i + 1
            raise MiniYAMLError(f"line {lines[i][2]}: flow mappings are not supported")
        if s[:1] in "|>&*!":
            raise MiniYAMLError(f"line {lines[i][2]}: block scalars, anchors and tags are not supported")
        parts, j = [s], i + 1
        while True:
            k = skip_blank(j)
            if k < len(lines) and lines[k][0] > ind:
                parts.append("\n" * (k - j) if k > j else "")
                parts.append(lines[k][1]); j = k + 1
            else:
                break
        text_ = ""
        for p in parts:
            if p == "":
                continue
            if p.startswith("\n"):
                text_ += p
            else:
                text_ += (p if not text_ or text_.endswith("\n") else " " + p)
        text_ = re.split(r"\s#", text_, maxsplit=1)[0].strip()
        return _resolve(text_), j

    def split_key(s, n):
        if s[:1] in ("'", '"'):
            q, k = s[0], 1
            while k < len(s) and not (s[k] == q and (q == '"' or s[k + 1:k + 2] != "'")):
                k += 2 if (q == "'" and s[k:k + 2] == "''") else 1
            key, rest = _unquote(s[1:k], q), s[k + 1:].lstrip()
            if not rest.startswith(":"):
                raise MiniYAMLError(f"line {n}: expected ':' after quoted key")
            return key, rest[1:].strip()
        m = re.search(r":(\s|$)", s)
        if not m:
            raise MiniYAMLError(f"line {n}: expected 'key: value'")
        return _resolve(s[:m.start()].strip()), s[m.end():].strip()

    def node(i):
        i = skip_blank(i)
        if i >= len(lines):
            return None, i
        ind, s, _ = lines[i]
        return seq(i, ind) if is_item(s) else mapping(i, ind)

    def value_after_colon(rest, i, ind):
        if rest.startswith("#"):
            rest = ""
        if rest:
            return scalar(rest, i, ind)
        j = skip_blank(i + 1)
        if j < len(lines) and lines[j][0] > ind:
            return node(j)
        if j < len(lines) and lines[j][0] == ind and is_item(lines[j][1]):
            return seq(j, ind)
        return None, i + 1

    def mapping(i, ind):
        out = {}
        while True:
            i = skip_blank(i)
            if i >= len(lines) or lines[i][0] < ind:
                return out, i
            lind, s, n = lines[i]
            if lind > ind:
                raise MiniYAMLError(f"line {n}: unexpected indentation")
            if is_item(s):
                return out, i
            key, rest = split_key(s, n)
            out[key], i = value_after_colon(rest, i, ind)

    def seq(i, ind):
        out = []
        while True:
            i = skip_blank(i)
            if i >= len(lines) or lines[i][0] != ind or not is_item(lines[i][1]):
                return out, i
            s, n = lines[i][1], lines[i][2]
            rest = s[1:].lstrip()
            if not rest:
                j = skip_blank(i + 1)
                if j < len(lines) and lines[j][0] > ind:
                    val, i = node(j)
                else:
                    val, i = None, i + 1
            elif rest[:1] not in ("'", '"', "[", "{") and re.search(r":(\s|$)", rest):
                item_ind = ind + (len(s) - len(rest))
                lines[i] = (item_ind, rest, n)
                val, i = mapping(i, item_ind)
            else:
                val, i = scalar(rest, i, ind)
            out.append(val)

    value, end = node(0)
    if skip_blank(end) < len(lines):
        raise MiniYAMLError(f"line {lines[skip_blank(end)][2]}: could not parse")
    return value


def load_yaml_text(text, what):
    if yaml is not None:
        return yaml.safe_load(text)
    try:
        return mini_yaml_load(text)
    except MiniYAMLError as e:
        raise ArcError(f"couldn't parse {what} without PyYAML ({e}). Install it with `pip install pyyaml`.")


# ---------------------------------------------------------------- fetching

def cache_dir():
    return Path(os.environ.get("ARC_CACHE_DIR") or Path.home() / ".cache" / "arc-assessment")


def http_get(url, attempts=3):
    """GET a URL, retrying transient failures (dropped or truncated connections)."""
    req = urllib.request.Request(url, headers={"User-Agent": "arc-assessment-skill"})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, http.client.HTTPException, OSError) as e:
            if attempt == attempts:
                raise ArcError(f"couldn't reach {url.split('/')[2]} ({getattr(e, 'reason', e)!s}). Check network "
                               "access, or use --register with a local copy of the register.")
            time.sleep(attempt)


_cache_warned = False


def cached_get(url, ref, name, refresh):
    """Release tags don't change, so their files are cached; caching is skipped if the cache can't be written."""
    global _cache_warned
    path = cache_dir() / ref / name
    if ref.startswith("v") and path.exists() and not refresh:
        return path.read_text()
    text = http_get(url)
    if ref.startswith("v"):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        except OSError as e:
            if not _cache_warned:
                warn(f"not caching ({e}); set ARC_CACHE_DIR to a writable directory to cache release files")
                _cache_warned = True
    return text


def _version_key(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def resolve_official_ref(version):
    """The git ref to read: v<version>, defaulting to the latest release recorded on main.

    If main can't be reached, falls back to the newest release already in the cache."""
    if version:
        return "v" + version.lstrip("v")
    try:
        latest = load_yaml_text(http_get(f"{REPO_RAW}/main/arc-risk-register/register.yaml"), "register.yaml")
        return f"v{latest['version']}"
    except ArcError:
        cached = sorted((p.name for p in cache_dir().glob("v*")
                         if all((p / f"{n}.yaml").exists() for n in REGISTER_FILES)), key=_version_key)
        if not cached:
            raise
        warn(f"couldn't check for the latest release; using cached {cached[-1]}")
        return cached[-1]


def load_register(args):
    """Return (register dict, human-readable source, git ref of the official release or None).

    With --overlay, the base is the official register of the version the overlay names (or the
    register given with --register), and the overlay is applied on top of it.
    """
    overlay = read_overlay(args.overlay) if getattr(args, "overlay", None) else None
    if overlay and not args.register:
        base = str(overlay["overlay"]["base"])
        if args.version and args.version.lstrip("v") != base:
            warn(f"the overlay was written against register {base}; applying it to {args.version} as asked")
        else:
            args.version = base
    data, source, ref = load_base_register(args)
    if overlay:
        data, notes = apply_overlay(data, overlay)
        for note in notes:
            warn(note)
        meta = overlay["overlay"]
        source = f"{meta.get('name', 'overlay')} {meta.get('version', '')}".strip() + f", applied to {source}"
    return data, source, ref


def load_base_register(args):
    data = {}
    if args.register:
        src = args.register
        for name in REGISTER_FILES:
            if src.startswith(("http://", "https://")):
                try:
                    data[name] = load_yaml_text(http_get(f"{src.rstrip('/')}/{name}.yaml"), f"{name}.yaml")
                except urllib.error.HTTPError:
                    data[name] = None
            else:
                p = Path(src) / f"{name}.yaml"
                data[name] = load_yaml_text(p.read_text(), str(p)) if p.exists() else None
        missing = [n for n in REGISTER_FILES if data[n] is None and n not in ("hazards", "register")]
        if missing:
            raise ArcError(f"{src} is missing {', '.join(f'{m}.yaml' for m in missing)}; an organisation's "
                           "register must use the same file layout as arc-risk-register/.")
        data["hazards"] = data["hazards"] or {}
        data["register"] = data["register"] or {"version": "unversioned", "released": ""}
        for name in OPTIONAL_FILES:
            data[name] = None
            try:
                if src.startswith(("http://", "https://")):
                    data[name] = load_yaml_text(http_get(f"{src.rstrip('/')}/{name}.yaml"), f"{name}.yaml")
                elif (Path(src) / f"{name}.yaml").exists():
                    data[name] = load_yaml_text((Path(src) / f"{name}.yaml").read_text(), f"{name}.yaml")
            except (urllib.error.HTTPError, ArcError):
                pass
        return data, f"organisation register at {src}", None

    ref = resolve_official_ref(args.version)
    for name in REGISTER_FILES:
        url = f"{REPO_RAW}/{ref}/arc-risk-register/{name}.yaml"
        try:
            data[name] = load_yaml_text(cached_get(url, ref, f"{name}.yaml", args.refresh), f"{name}.yaml")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ArcError(f"release {ref} not found in the ARC repository"
                               + ("; check --version" if args.version else "; pass --version to choose one"))
            raise ArcError(f"couldn't fetch {url} (HTTP {e.code})")
    for name in OPTIONAL_FILES:
        url = f"{REPO_RAW}/{ref}/arc-risk-register/{name}.yaml"
        try:
            data[name] = load_yaml_text(cached_get(url, ref, f"{name}.yaml", args.refresh), f"{name}.yaml")
        except urllib.error.HTTPError as e:
            data[name] = None
            if e.code == 404 and ref.startswith("v"):  # this release predates the file; remember that
                try:
                    (cache_dir() / ref / f"{name}.yaml").write_text("{}\n")
                except OSError:
                    pass
        except ArcError:
            data[name] = None
    return data, f"official ARC register, tag {ref}", ref


# ---------------------------------------------------------------- register logic

# ---------------------------------------------------------------- overlays

NAMESPACED_ID = re.compile(r"^[A-Z][A-Z0-9]{1,7}-(RISK-\d{3}|CTRL-\d{4}|CAP-\d{2})$")
OVERLAY_SECTIONS = ("capabilities", "risks", "controls")


def apply_overlay(reg, overlay):
    """An organisation's effective register: the base register with its overlay applied by ID.

    An overlay can add entries (with a namespaced ID such as ORG-RISK-001), change fields of existing
    entries, and remove entries it does not use. Everything it does not mention is inherited from the
    base, so a new base version reaches the organisation without a merge. Returns (register, notes);
    raises ArcError listing every problem if the overlay cannot be applied.
    """
    reg = copy.deepcopy(reg)
    problems, notes, unlinked = [], [], set()
    part = lambda name, op: ((overlay.get(name) or {}).get(op) or {})

    for name in OVERLAY_SECTIONS:
        for eid, entry in part(name, "add").items():
            if not NAMESPACED_ID.match(str(eid)):
                problems.append(f"{eid}: an entry added by an overlay needs a namespaced ID, such as ORG-RISK-001")
            elif eid in reg[name]:
                problems.append(f"{eid}: already exists")
            else:
                reg[name][eid] = {**(entry or {}), "overlay": "added"}

    for name in OVERLAY_SECTIONS:
        for eid, changes in part(name, "change").items():
            base = reg[name].get(eid)
            if base is None or base.get("superseded_by"):
                problems.append(f"{eid}: the overlay changes it, but it is not in the base register"
                                + (f" (retired; see {base['superseded_by']})" if base else ""))
                continue
            for field, value in (changes or {}).items():
                if field.endswith("_append"):
                    target = field[:-len("_append")]
                    base[target] = f"{str(base.get(target) or '').rstrip()} {str(value).strip()}".strip()
                elif field in ("add_controls", "add_risks"):
                    key = field[len("add_"):]
                    base[key] = list(dict.fromkeys((base.get(key) or []) + list(value or [])))
                elif field in ("remove_controls", "remove_risks"):
                    key = field[len("remove_"):]
                    base[key] = [x for x in base.get(key) or [] if x not in (value or [])]
                    unlinked |= {(eid, x) if name == "risks" else (x, eid) for x in value or []}
                elif field == "level" and name == "controls" and base.get("level") == 0 and value != 0:
                    problems.append(f"{eid}: an overlay cannot lower a Level 0 control")
                else:
                    base[field] = value
            base["overlay"] = "changed"

    removed = {name: part(name, "remove") for name in OVERLAY_SECTIONS}
    for name, items in removed.items():
        for eid in items:
            if eid not in reg[name]:
                problems.append(f"{eid}: the overlay removes it, but it is not in the base register")
            else:
                del reg[name][eid]

    # A capability the organisation does not use takes its risks, and its part in any combination, with it
    for rid, r in list(reg["risks"].items()):
        gone = [e for e in risk_elements(r) if e in removed["capabilities"]]
        if gone:
            del reg["risks"][rid]
            notes.append(f"{rid} is left out because the overlay removes {', '.join(gone)}")
    combinations = reg.get("combinations") or {}
    for role in (combinations.get("roles") or {}).values():
        for cap in removed["capabilities"]:
            (role.get("capabilities") or {}).pop(cap, None)
    for cap in removed["capabilities"]:
        (combinations.get("implies") or {}).pop(cap, None)
    for implied in (combinations.get("implies") or {}).values():
        for cap in removed["capabilities"]:
            implied.pop(cap, None)

    # Risks and controls point at each other; make both directions agree after the changes
    risks = {r: v for r, v in reg["risks"].items() if not v.get("superseded_by")}
    controls = {c: v for c, v in reg["controls"].items() if not v.get("superseded_by")}
    for rid, r in risks.items():
        for cid in r.get("controls") or []:
            if cid not in controls and cid not in removed["controls"]:
                problems.append(f"{rid}: lists {cid}, which does not exist")
    for cid, c in controls.items():
        for rid in c.get("risks") or []:
            if rid not in risks and rid not in removed["risks"] and rid not in reg["risks"] \
                    and not any(note.startswith(rid + " ") for note in notes):
                problems.append(f"{cid}: lists {rid}, which does not exist")
    links = ({(r, c) for r, v in risks.items() for c in v.get("controls") or [] if c in controls}
             | {(r, c) for c, v in controls.items() for r in v.get("risks") or [] if r in risks}) - unlinked
    for rid, r in risks.items():
        mine = [c for c in r.get("controls") or [] if (rid, c) in links]
        r["controls"] = mine + sorted(c for (x, c) in links if x == rid and c not in mine)
        if not r["controls"]:
            problems.append(f"{rid}: no controls are left for this risk; remove the risk as well, or keep a control")
    for cid, c in controls.items():
        mine = [r for r in c.get("risks") or [] if (r, cid) in links]
        c["risks"] = mine + sorted(r for (r, x) in links if x == cid and r not in mine)
        if not c["risks"]:
            del reg["controls"][cid]
            notes.append(f"{cid} is left out because none of its risks remain")
    for rule_id, rule in (combinations.get("rules") or {}).items():
        rule["risks"] = [r for r in rule.get("risks") or [] if r in reg["risks"]]
        if rule.get("control") not in reg["controls"]:
            problems.append(f"combination rule {rule_id}: its control {rule.get('control')} is no longer in the register")

    if problems:
        raise ArcError("the overlay cannot be applied:\n  - " + "\n  - ".join(problems))
    meta = overlay.get("overlay") or {}
    reg["register"] = {**reg["register"], "overlay": {k: meta[k] for k in ("name", "version", "base") if k in meta}}
    return reg, notes


def read_overlay(path):
    overlay = load_yaml_text(Path(path).read_text(), path) or {}
    if not isinstance(overlay.get("overlay"), dict) or not overlay["overlay"].get("base"):
        raise ArcError(f"{path}: an overlay starts with `overlay:` giving its name, version and `base`, "
                       "the ARC register version it was written against")
    return overlay


def element_index(reg):
    idx = {}
    for kind, key in (("Component", "components"), ("Design", "design"), ("Capability", "capabilities")):
        for eid, e in (reg[key] or {}).items():
            idx[eid] = {"id": eid, "kind": kind, "name": e.get("name", ""), "category": e.get("category", ""),
                        "description": (e.get("description") or "").strip(),
                        "present_when": (e.get("present_when") or "").strip(),
                        "authority": e.get("authority") or [], "irreversible": e.get("irreversible"),
                        "external": e.get("external")}
    return idx


def risk_elements(r):
    return r.get("element_ids") or ([r["element_id"]] if r.get("element_id") else [])


def is_chosen(element):
    """True for an element that only some systems have: a capability, or a conditional component or design element."""
    return element.get("kind") == "Capability" or bool(element.get("present_when"))


def build_profile(reg, capabilities, authority=None, reversible=(), internal=()):
    """The context each capability is used in: {capability: {authority, irreversible, external}}.

    A capability that lists authority levels is taken to be used at the highest one unless `authority`
    says otherwise. Its effects are taken to be irreversible and external wherever the register leaves
    the question open ("ask"), unless the capability is named in `reversible` or `internal`. The cautious
    assumption keeps every risk and every stricter control level in scope until the context removes it.
    A register without context fields gives an empty context, and nothing changes.
    """
    elements = element_index(reg)
    profile = {}
    for cap in capabilities:
        e = elements[cap]
        context = {}
        if e["authority"]:
            given = (authority or {}).get(cap)
            if given and given not in e["authority"]:
                raise ArcError(f"{cap} {e['name']} can be used at: {', '.join(e['authority'])} (got {given!r})")
            context["authority"] = given or e["authority"][-1]
        for field, cleared in (("irreversible", reversible), ("external", internal)):
            if e[field] == "ask":
                context[field] = cap not in cleared
            elif e[field] in ("always", "never"):
                context[field] = e[field] == "always"
        if context.get("authority") == "read" and "irreversible" in context:
            context["irreversible"] = False   # reading changes nothing, so there is nothing to undo
        profile[cap] = context
    return profile


def below_authority(risk, profile):
    """(capability, level needed) if the system uses a capability below the authority this risk needs."""
    for cap, minimum in (risk.get("min_authority") or {}).items():
        used = (profile or {}).get(cap, {}).get("authority")
        if used and AUTHORITY.index(used) < AUTHORITY.index(minimum):
            return cap, minimum
    return None


def effective_level(control, profile):
    """A control's level in this system: its own, or a stricter one if a `level_when` context holds."""
    level = control.get("level")
    for condition in control.get("level_when") or []:
        for cap, context in (profile or {}).items():
            if condition.get("capabilities") and cap not in condition["capabilities"]:
                continue
            if "authority" in condition and (
                    not context.get("authority")
                    or AUTHORITY.index(context["authority"]) < AUTHORITY.index(condition["authority"])):
                continue
            if any(field in condition and context.get(field) != condition[field]
                   for field in ("irreversible", "external")):
                continue
            level = min(level, condition["level"])
    return level


def combination_rules(reg):
    """The register's combination rules as {rule_id: rule}, each with `legs`: {role_id: role}.

    Register 2.0 keeps shared `roles` and `rules` that name them; register 1.3 kept the legs inside each
    combination. Both are returned in the one shape.
    """
    data = reg.get("combinations") or {}
    if "rules" not in data:
        return {rule_id: rule for rule_id, rule in data.items() if isinstance(rule, dict) and rule.get("legs")}
    roles = data.get("roles") or {}
    return {rule_id: {**rule, "legs": {r: roles[r] for r in rule.get("roles") or [] if r in roles}}
            for rule_id, rule in (data.get("rules") or {}).items()}


def applicable_risks(reg, present, profile=None):
    """Risks that apply to a system with the given capabilities and conditional components.

    A risk applies when all the elements it arises from are present. Most components and design elements
    are present in every agentic system, so a risk arising only from them is a baseline risk. A capability,
    or a component that states when it is present (`present_when`), must be named in `present`; a risk
    that lists such elements applies only when the system has all of them.
    """
    elements = element_index(reg)
    selected = set(present)
    verdicts = {c["id"]: c["verdict"] for c in combination_checks(reg, present, profile)}
    baseline, single, combination = [], [], []
    for rid, r in reg["risks"].items():
        if r.get("superseded_by") or below_authority(r, profile):
            continue
        if r.get("combination"):   # arises from a rule, and applies unless the rule is ruled out
            if verdicts.get(r["combination"], "not present") != "not present":
                combination.append(rid)
            continue
        ids = risk_elements(r)
        needed = {e for e in ids if is_chosen(elements.get(e, {}))}
        if not needed:
            baseline.append(rid)
        elif needed <= selected:
            (combination if len(ids) > 1 else single).append(rid)
    return baseline, single, combination


def risk_record(reg, rid, elements, detail=False, profile=None):
    r = reg["risks"][rid]
    hazards = reg["hazards"] or {}
    controls = []
    for cid in r.get("controls", []) or []:
        c = reg["controls"].get(cid)
        if c:
            rec = {"id": cid, "level": effective_level(c, profile), "statement": c.get("statement", "")}
            if rec["level"] != c.get("level"):
                rec["level_outside_this_context"] = c.get("level")
            if c.get("provided_by"):   # an overlay marks controls that a shared platform implements
                rec["provided_by"] = c["provided_by"]
            if detail:
                rec["recommendations"] = (c.get("recommendations") or "").strip()
                rec.update({k: c[k] for k in ("enforcement", "owner", "phase", "evidence", "test") if c.get(k)})
            controls.append(rec)
    return {
        "id": rid,
        "statement": r.get("statement", ""),
        "description": (r.get("description") or "").strip(),
        "elements": ([f"Combination: {combination_rules(reg).get(r['combination'], {}).get('name', r['combination'])}"]
                     if r.get("combination") else
                     [f"{elements[e]['kind']}: {elements[e]['name']} ({e})" if e in elements else e
                      for e in risk_elements(r)]),
        "failure_mode": r.get("failure_mode", ""),
        "type": r.get("type", []),
        "hazards": [f"{hazards[h]['name']} ({h})" if h in hazards else h for h in r.get("hazards", []) or []],
        "controls": controls,
    }


def combination_checks(reg, capabilities, profile=None):
    """Check the system's capabilities against each combination rule the register defines.

    A rule names roles that must all be supplied. A capability supplies a role always ("yes") or only in
    some deployments ("maybe"), and some only from a certain authority upwards. The rule is present when
    every role has a "yes" capability, possible when every role is supplied but at least one only by
    "maybe" capabilities, and not present otherwise. A rule that is present or possible brings its risks
    into scope; its control is implemented unless the assessor shows that a role is absent.
    """
    elements = element_index(reg)

    def supplies(cap, entry):
        used = (profile or {}).get(cap, {}).get("authority")
        minimum = entry.get("min_authority")
        return not (used and minimum) or AUTHORITY.index(used) >= AUTHORITY.index(minimum)

    out = []
    for rule_id, rule in combination_rules(reg).items():
        legs = []
        for leg_id, leg in rule["legs"].items():
            marks = leg.get("capabilities") or {}
            suppliers = [{"id": c, "name": elements.get(c, {}).get("name", ""), "mark": marks[c].get("mark"),
                          "note": marks[c].get("note", "")}
                         for c in capabilities if c in marks and supplies(c, marks[c])]
            status = "yes" if any(s["mark"] == "yes" for s in suppliers) else ("maybe" if suppliers else "none")
            legs.append({"id": leg_id, "name": leg.get("name", leg_id), "description": leg.get("description", ""),
                         "question": leg.get("question", ""), "status": status, "capabilities": suppliers})
        statuses = [leg["status"] for leg in legs]
        verdict = ("not present" if "none" in statuses or not legs
                   else "present" if all(s == "yes" for s in statuses) else "possible")
        cid = rule.get("control")
        control = reg["controls"].get(cid) or {}
        out.append({
            "id": rule_id, "name": rule.get("name", rule_id), "description": rule.get("description", ""),
            "verdict": verdict, "legs": legs, "risks": rule.get("risks") or [],
            "control": {"id": cid, "level": control.get("level"), "statement": control.get("statement", "")},
        })
    return out


def implied_capabilities(reg, capabilities):
    """Capabilities the system has not declared but that its declared ones give it (`implies`)."""
    elements = element_index(reg)
    out = []
    for cap in capabilities:
        for other, entry in ((reg.get("combinations") or {}).get("implies") or {}).get(cap, {}).items():
            if other in capabilities:
                continue
            out.append({"from": cap, "from_name": elements.get(cap, {}).get("name", ""), "capability": other,
                        "name": elements.get(other, {}).get("name", "") if other != "any" else "any capability",
                        "mark": entry.get("mark"), "note": entry.get("note", "")})
    return out


def combination_advice(check):
    """What the assessor does with a combination verdict."""
    cid = check["control"]["id"]
    missing = [leg["name"].lower() for leg in check["legs"] if leg["status"] == "none"]
    unsure = [leg["name"].lower() for leg in check["legs"] if leg["status"] == "maybe"]
    if check["verdict"] == "present":
        advice = (f"Every leg is present. Implement {cid}. If your review of the system finds that a leg is absent "
                  f"in practice, record which one and the evidence, and record {cid} as waived — not applicable.")
    elif check["verdict"] == "possible":
        advice = (f"Whether this system has {' and '.join(unsure)} depends on how it is deployed. Answer each "
                  f"note marked maybe from the code and configuration. If every leg is confirmed, implement "
                  f"{cid}. If one is absent, record {cid} as waived — not applicable, with the evidence.")
    else:
        advice = (f"No capability of this system supplies {' or '.join(missing)}. Where {cid} is listed, record it "
                  "as waived — not applicable, with this as the evidence.")
    if check["verdict"] != "not present" and not check.get("control_listed_by", True):
        advice += (f" None of this system's applicable risks lists {cid} in this register version, so record it "
                   "with the combination check.")
    return advice


def parse_ids(text):
    return [x.strip().upper() for x in (text or "").split(",") if x.strip()]


def parse_capabilities(text):
    """'CAP-06=act-with-approval,CAP-11' -> (['CAP-06', 'CAP-11'], {'CAP-06': 'act-with-approval'})."""
    caps, authority = [], {}
    for item in (text or "").split(","):
        if not item.strip():
            continue
        cap, _, level = item.strip().partition("=")
        caps.append(cap.strip().upper())
        if level.strip():
            authority[caps[-1]] = level.strip().lower()
    return caps, authority


def read_profile(path):
    """A system profile file -> (capabilities, authority, reversible, internal, components)."""
    data = load_yaml_text(Path(path).read_text(), path) or {}
    entries = data.get("capabilities") or {}
    if isinstance(entries, list):
        entries = {cap: {} for cap in entries}
    caps = [str(c).upper() for c in entries]
    entries = {str(c).upper(): (v or {}) for c, v in entries.items()}
    authority = {c: str(v["authority"]).lower() for c, v in entries.items() if v.get("authority")}
    reversible = [c for c, v in entries.items() if v.get("irreversible") is False]
    internal = [c for c, v in entries.items() if v.get("external") is False]
    return caps, authority, reversible, internal, [str(c).upper() for c in data.get("components") or []]


def describe_context(context):
    parts = [context["authority"]] if context.get("authority") else []
    if "irreversible" in context:
        parts.append("irreversible" if context["irreversible"] else "reversible")
    if "external" in context:
        parts.append("external" if context["external"] else "internal")
    return ", ".join(parts)


# ---------------------------------------------------------------- commands

def cmd_elements(reg, source, args):
    elements = element_index(reg)
    v = reg["register"].get("version")
    if args.format == "json":
        print(json.dumps({"register_version": v, "source": source, "elements": list(elements.values())}, indent=2))
        return
    print(f"# ARC elements (register {v}; {source})\n")
    print("Components and design elements are present in every agentic system, except those marked conditional, "
          "which a system has only when the stated condition holds. Capabilities are what the system can do; a "
          "system has a capability if any of its agents has it. Go by each definition, not the name.\n")
    for kind, title in (("Component", "Components"), ("Design", "Design elements"), ("Capability", "Capabilities")):
        print(f"## {title}\n")
        for e in elements.values():
            if e["kind"] == kind:
                cat = f" ({e['category']})" if e["category"] else ""
                print(f"- **{e['id']} {e['name']}**{cat}: {e['description']}")
                if e["present_when"]:
                    print(f"  - Conditional. Present when: {e['present_when']}")
                print()


def cmd_assess(reg, source, args):
    elements = element_index(reg)
    caps, authority = parse_capabilities(args.capabilities)
    reversible, internal = parse_ids(args.reversible), parse_ids(args.internal)
    profile_components = []
    if args.profile:
        if caps:
            raise ArcError("--profile and --capabilities are alternatives")
        caps, authority, reversible, internal, profile_components = read_profile(args.profile)
    unknown = [c for c in caps if elements.get(c, {}).get("kind") != "Capability"]
    if unknown:
        valid = ", ".join(f"{e['id']} {e['name']}" for e in elements.values() if e["kind"] == "Capability")
        raise ArcError(f"unknown capability ID(s): {', '.join(unknown)}. Valid: {valid}")
    components = parse_ids(getattr(args, "components", "") or "") or profile_components
    profile = build_profile(reg, caps, authority, reversible, internal)
    too_low = {rid: below_authority(r, profile) for rid, r in reg["risks"].items() if below_authority(r, profile)}
    conditional = {e["id"]: e for e in elements.values() if e["present_when"]}
    stray = [c for c in components if c not in conditional]
    if stray:
        valid = ", ".join(f"{e['id']} {e['name']}" for e in conditional.values()) or "none in this register"
        raise ArcError(f"not a conditional component: {', '.join(stray)}. Conditional components: {valid}")
    baseline, single, combination = applicable_risks(reg, caps + components, profile)
    applicable = baseline + single + combination
    groups = [("Baseline risks (components and design elements)", baseline),
              ("Risks from capabilities and conditional components", single),
              ("Risks from combinations of elements", combination)]
    records = {rid: risk_record(reg, rid, elements, detail=args.detail, profile=profile) for rid in applicable}

    priority = None
    if args.priority:
        priority = applicable if args.priority.strip().lower() == "all" else parse_ids(args.priority)
        stray = [p for p in priority if p not in records]
        if stray:
            raise ArcError(f"not applicable to this system (check --capabilities): {', '.join(stray)}")

    def rollup(include):
        out = {}
        for rid in applicable:
            for c in records[rid]["controls"]:
                if include(rid, c):
                    out.setdefault(c["id"], {"level": c["level"], "statement": c["statement"], "risks": []})
                    out[c["id"]]["risks"].append(rid)
        return dict(sorted(out.items()))

    all_controls = rollup(lambda rid, c: True)
    level0 = rollup(lambda rid, c: c["level"] == 0)
    in_scope = rollup(lambda rid, c: c["level"] == 0 or rid in priority) if priority is not None else None

    combinations = combination_checks(reg, caps, profile)
    for check in combinations:
        check["control_listed_by"] = [rid for rid in applicable
                                      if check["control"]["id"] in (reg["risks"][rid].get("controls") or [])]
    implied = implied_capabilities(reg, caps)
    v = reg["register"].get("version")
    if args.format == "json":
        out = {"register_version": v, "source": source, "capabilities": caps, "components": components,
               "context": profile,
               "below_authority": [{"id": rid, "capability": cap, "needs": minimum}
                                   for rid, (cap, minimum) in too_low.items()],
               "conditional_components": [{"id": e["id"], "name": e["name"], "present_when": e["present_when"],
                                           "present": e["id"] in components} for e in conditional.values()],
               "risks": {"baseline": [records[r] for r in baseline], "capability": [records[r] for r in single],
                         "combination": [records[r] for r in combination]},
               "level0_controls": [{"id": k, **val} for k, val in level0.items()],
               "combinations": [{**c, "advice": combination_advice(c)} for c in combinations],
               "implied_capabilities": implied}
        if in_scope is not None:
            out["priority_risks"] = priority
            out["controls_in_scope"] = [{"id": k, **val} for k, val in in_scope.items()]
        print(json.dumps(out, indent=2))
        return

    cap_names = ", ".join(f"{c} {elements[c]['name']}" + (f" ({describe_context(profile[c])})" if profile[c] else "")
                          for c in caps) or "none"
    by_level = lambda d: ", ".join(f"{sum(1 for x in d.values() if x['level'] == lv)} at Level {lv}" for lv in (0, 1, 2))
    print(f"# ARC applicable risks (register {v}; {source})\n")
    print(f"**Capabilities:** {cap_names}\n")
    if any(profile.values()):
        print("The context in brackets is how each capability is used. Unstated context is assumed to be the most "
              "cautious case; give it with CAP-xx=<authority>, --reversible, --internal or --profile.\n")
    for rid, (cap, minimum) in too_low.items():
        print(f"**Left out:** {rid} {reg['risks'][rid].get('statement', '')}. It needs {cap} at {minimum} or above.\n")
    for e in conditional.values():
        state = "present" if e["id"] in components else "not present (its risks are left out; pass --components to include them)"
        print(f"**{e['id']} {e['name']}:** {state}. Present when: {e['present_when']}\n")
    print(f"**{len(applicable)} applicable risks:** {len(baseline)} baseline, {len(single)} from single "
          f"capabilities, {len(combination)} from combinations of elements. Between them they list "
          f"{len(all_controls)} distinct controls ({by_level(all_controls)}).\n")
    print(f"Control levels: {SITE}arc_framework/controls/#control-levels. Full text of any entry: "
          f"`arc.py show <ID>` or {SITE}arc_framework/register-full-text/#<ID>.\n")
    for title, ids in groups:
        if not ids:
            continue
        print(f"## {title}\n")
        for rid in ids:
            rec = records[rid]
            print(f"### {rid} · {rec['statement']}\n")
            print(f"Arises from: {' + '.join(rec['elements'])} · Failure mode: {rec['failure_mode']} · "
                  f"Hazards: {', '.join(rec['hazards'])}\n")
            print(f"{rec['description']}\n")
            for c in rec["controls"]:
                raised = (f"; Level {c['level_outside_this_context']} outside this context"
                          if "level_outside_this_context" in c else "")
                print(f"- {c['id']} [{LEVELS.get(c['level'], c['level'])}{raised}] {c['statement']}"
                      + (f" (provided by {c['provided_by'].get('platform', 'a shared platform')})"
                         if c.get("provided_by") else ""))
                if args.detail and c.get("recommendations"):
                    print(f"  - Guidance: {c['recommendations']}")
                if args.detail and c.get("evidence"):
                    print(f"  - Evidence that it is in place: {c['evidence']}")
                    print(f"  - Test that it works: {c['test']}")
            print()

    if implied:
        print("## Capabilities this system may also have\n")
        print("Some capabilities give a system others, whether or not they were declared. For each one below, add "
              "it to --capabilities and assess again, or record the evidence that it does not apply.\n")
        for i in implied:
            print(f"- {i['from']} {i['from_name']} gives {i['capability']} {i['name']} ({i['mark']}): {i['note']}")
        print()

    if combinations:
        print("## Capability combinations\n")
        print("Some capabilities create a risk only when a system holds them together. This check uses the "
              "capabilities alone. Persistent memory can carry untrusted content or sensitive data from one "
              f"session into another, so count it when answering. See {SITE}arc_framework/capability-combinations/.\n")
        for c in combinations:
            print(f"### {c['name']}: {c['verdict']}\n")
            print(f"{c['description']}\n")
            for leg in c["legs"]:
                if leg["status"] == "none":
                    print(f"- {leg['name']}: not supplied by any capability of this system")
                    continue
                print(f"- {leg['name']}: {leg['status']}")
                shown = [s for s in leg["capabilities"] if s["mark"] == "yes"] or leg["capabilities"]
                for s in shown:
                    print(f"  - {s['id']} {s['name']} ({s['mark']}): {s['note']}")
            print(f"\n{combination_advice(c)}\n")
            print(f"- {c['control']['id']} [{LEVELS.get(c['control']['level'], c['control']['level'])}] "
                  f"{c['control']['statement']}\n")

    def table(d):
        for cid, val in d.items():
            print(f"- {cid} [{LEVELS.get(val['level'], val['level'])}] {val['statement']} ({', '.join(sorted(val['risks']))})")

    if in_scope is not None:
        print(f"## Controls in scope ({len(in_scope)}: {by_level(in_scope)})\n")
        print(f"Level 0 controls of all {len(applicable)} applicable risks, and Level 1 and 2 controls of the "
              f"{len(priority)} priority risks. Each control appears once, with the risks it addresses:\n")
        table(in_scope)
    elif level0:
        print(f"## Level 0 controls across all applicable risks ({len(level0)})\n")
        print("Each Level 0 control once, with the applicable risks it addresses. Re-run with --priority once "
              "risks are scored to list every control in scope.\n")
        table(level0)


def cmd_show(reg, source, args):
    elements = element_index(reg)
    out = []
    for raw_id in args.ids:
        eid = raw_id.upper()
        retired = (reg["risks"].get(eid) or reg["controls"].get(eid) or {}).get("superseded_by")
        if retired:
            out.append({"id": eid, "statement": (reg["risks"].get(eid) or reg["controls"][eid]).get("statement", ""),
                        "superseded_by": retired})
        elif eid in reg["risks"]:
            out.append({**risk_record(reg, eid, elements, detail=True), "sources": reg["risks"][eid].get("sources", [])})
        elif eid in reg["controls"]:
            c = reg["controls"][eid]
            out.append({"id": eid, "level": c.get("level"), "statement": c.get("statement", ""),
                        "recommendations": (c.get("recommendations") or "").strip(), "risks": c.get("risks", []),
                        "references": c.get("references") or [],
                        **{k: c[k] for k in ("enforcement", "owner", "phase", "evidence", "test", "provided_by")
                           if c.get(k)}})
        elif eid in elements:
            e = elements[eid]
            out.append({**e, "risks": [rid for rid, r in reg["risks"].items()
                                       if eid in risk_elements(r) and not r.get("superseded_by")]})
        else:
            raise ArcError(f"{raw_id} is not a risk, control or element in this register")
    if args.format == "json":
        print(json.dumps({"register_version": reg["register"].get("version"), "source": source, "entries": out},
                         indent=2, default=str))
        return
    for e in out:
        if "superseded_by" in e:
            print(f"## {e['id']} · {e['statement']}\n\nRetired. Superseded by {e['superseded_by']}; "
                  f"run `arc.py show {e['superseded_by']}`.\n")
            continue
        if "kind" in e:
            print(f"## {e['id']} · {e['name']} ({e['kind']}{', ' + e['category'] if e['category'] else ''})\n\n"
                  f"{e['description']}\n\nRisks arising from it: {', '.join(e['risks']) or 'none'}")
        elif "controls" in e:
            print(f"## {e['id']} · {e['statement']}\n\nArises from: {' + '.join(e['elements'])} · Failure mode: "
                  f"{e['failure_mode']} · Hazards: {', '.join(e['hazards'])}\n\n{e['description']}\n")
            for c in e["controls"]:
                print(f"- {c['id']} [{LEVELS.get(c['level'], c['level'])}] {c['statement']}")
            if e.get("sources"):
                print("\nSources: " + ", ".join(map(str, e["sources"])))
        else:
            print(f"## {e['id']} · {e['statement']}\n\n{LEVELS.get(e['level'], e['level'])} · Mitigates: "
                  f"{', '.join(e['risks'])}\n\n{e['recommendations'] or '(no guidance recorded)'}")
            if e.get("enforcement"):
                print(f"\nEnforced in: {', '.join(e['enforcement'])} · Owner: {e.get('owner', '')} · "
                      f"Phase: {', '.join(e.get('phase') or [])}")
            if e.get("evidence"):
                print(f"\nEvidence that it is in place: {e['evidence']}\n\nTest that it works: {e['test']}")
            if e.get("provided_by"):
                print(f"\nProvided by: {e['provided_by'].get('platform', '')}. {e['provided_by'].get('evidence', '')}")
            if e["references"]:
                print("\nReferences: " + ", ".join(map(str, e["references"])))
        print()


def plain_markdown(page, page_dir="implementation"):
    """Turn MkDocs page source into portable Markdown: admonitions become quotes, links become absolute."""
    out, block = [], False
    for line in page.splitlines():
        m = re.match(r'^(!!!|\?\?\?\+?)\s+\w+(?:\s+"([^"]*)")?\s*$', line)
        if m:
            out.append(f"> **{m.group(2)}**" if m.group(2) else ">")
            block = True
            continue
        if block:
            if line.startswith("    ") or not line.strip():
                out.append(("> " + line[4:]).rstrip() if line.strip() else ">")
                continue
            block = False
        out.append(line)
    text = "\n".join(out).rstrip() + "\n"

    def absolute(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"^[a-z]+:|^#", target):
            return m.group(0)
        path, _, anchor = target.partition("#")
        path = posixpath.normpath(posixpath.join(page_dir, path))
        path = re.sub(r"(^|/)index\.md$", r"\1", path)
        path = re.sub(r"\.md$", "/", path)
        return f"[{label}]({SITE}{path}{'#' + anchor if anchor else ''})"
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", absolute, text)


def cmd_template(reg, source, args, ref):
    if args.file:
        print(plain_markdown(Path(args.file).read_text()))
        return
    ref = ref or resolve_official_ref(None)
    if ref and source.startswith("organisation"):
        warn(f"using the official ARC assessment template at {ref}; pass --file for your organisation's own")
    print(plain_markdown(cached_get(f"{REPO_RAW}/{ref}/{TEMPLATE_PATH}", ref, "assessment-template.md", args.refresh)))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", help="official register version to use, e.g. 2.0.0 (default: latest release)")
    parser.add_argument("--register", help="an organisation's own register: a directory or base URL with the "
                                           "same file layout as arc-risk-register/")
    parser.add_argument("--overlay", help="an organisation's overlay file, applied to the official register of the "
                                          "version it names (or to --register)")
    parser.add_argument("--refresh", action="store_true", help="re-download cached release files")
    fmt = argparse.ArgumentParser(add_help=False)
    fmt.add_argument("--format", choices=("md", "json"), default="md", help="output format (default: md)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("elements", parents=[fmt], help="list components, design elements and capabilities")
    p_assess = sub.add_parser("assess", parents=[fmt], help="list applicable risks and their controls")
    p_assess.add_argument("--capabilities", default="", help="comma-separated capability IDs, e.g. CAP-03,CAP-07")
    p_assess.add_argument("--reversible", default="", help="capabilities whose effects can be readily undone")
    p_assess.add_argument("--internal", default="", help="capabilities whose effects stay inside the organisation")
    p_assess.add_argument("--profile", help="a YAML file describing the system: capabilities (each with authority, "
                                            "irreversible, external) and components")
    p_assess.add_argument("--components", default="", help="comma-separated conditional components the system has, "
                                                           "e.g. CMP-04,CMP-05 (see `elements` for the conditions)")
    p_assess.add_argument("--priority", help="comma-separated priority risk IDs (or 'all'): also list every "
                                             "control in scope")
    p_assess.add_argument("--detail", action="store_true", help="include each control's implementation guidance")
    p_show = sub.add_parser("show", parents=[fmt], help="full text of risks, controls or elements")
    p_show.add_argument("ids", nargs="+")
    p_tpl = sub.add_parser("template", help="print the ARC assessment template as plain Markdown")
    p_tpl.add_argument("--file", help="use this template file (e.g. your organisation's) instead of ARC's")
    args = parser.parse_args(argv)

    if args.register and args.version:
        parser.error("--register and --version are alternatives")
    try:
        reg, source, ref = load_register(args)
        if args.command == "elements":
            cmd_elements(reg, source, args)
        elif args.command == "assess":
            cmd_assess(reg, source, args)
        elif args.command == "show":
            cmd_show(reg, source, args)
        else:
            cmd_template(reg, source, args, ref)
    except ArcError as e:
        sys.exit(f"arc.py: {e}")


if __name__ == "__main__":
    main()
