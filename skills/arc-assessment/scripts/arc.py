#!/usr/bin/env python3
"""Query the ARC risk register for an assessment. Needs only Python 3.9+.

Fetches the register YAML from the official repository at a release tag (the
latest release unless --version is given), or reads an organisation's own
contextualised register with --register (a local directory or a base URL with
the same file layout as arc-risk-register/). Uses PyYAML if installed and a
built-in parser for the register's YAML otherwise.

Commands:
  elements                       components, design elements and capabilities, with definitions
  assess --capabilities IDS      applicable risks and their controls for a system, and a check for
         [--components IDS]      capability combinations such as the lethal trifecta; --components names
                                 the conditional components the system has (e.g. CMP-04 for persistent memory)
         [--priority IDS|all]    ...and the controls in scope once priority risks are known
  show ID [ID ...]               full text of risks, controls or elements (RISK-034, CTRL-0062, CAP-07)
  template                       the ARC assessment template (Markdown)

Examples:
  python3 arc.py elements
  python3 arc.py assess --capabilities CAP-03,CAP-07,CAP-11
  python3 arc.py --version 1.3.0 assess --capabilities CAP-03,CAP-07 --priority RISK-034,RISK-044 --format json
  python3 arc.py --register ./our-arc-register assess --capabilities CAP-02,CAP-06

Environment:
  ARC_CACHE_DIR   where release files are cached (default ~/.cache/arc-assessment;
                  caching is skipped if the directory can't be written)
"""

import argparse
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
    """Return (register dict, human-readable source, git ref of the official release or None)."""
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

def element_index(reg):
    idx = {}
    for kind, key in (("Component", "components"), ("Design", "design"), ("Capability", "capabilities")):
        for eid, e in (reg[key] or {}).items():
            idx[eid] = {"id": eid, "kind": kind, "name": e.get("name", ""), "category": e.get("category", ""),
                        "description": (e.get("description") or "").strip(),
                        "present_when": (e.get("present_when") or "").strip()}
    return idx


def risk_elements(r):
    return r.get("element_ids") or ([r["element_id"]] if r.get("element_id") else [])


def is_chosen(element):
    """True for an element that only some systems have: a capability, or a conditional component or design element."""
    return element.get("kind") == "Capability" or bool(element.get("present_when"))


def applicable_risks(reg, present):
    """Risks that apply to a system with the given capabilities and conditional components.

    A risk applies when all the elements it arises from are present. Most components and design elements
    are present in every agentic system, so a risk arising only from them is a baseline risk. A capability,
    or a component that states when it is present (`present_when`), must be named in `present`; a risk
    that lists such elements applies only when the system has all of them.
    """
    elements = element_index(reg)
    selected = set(present)
    baseline, single, combination = [], [], []
    for rid, r in reg["risks"].items():
        if r.get("superseded_by"):
            continue
        ids = risk_elements(r)
        needed = {e for e in ids if is_chosen(elements.get(e, {}))}
        if not needed:
            baseline.append(rid)
        elif needed <= selected:
            (combination if len(ids) > 1 else single).append(rid)
    return baseline, single, combination


def risk_record(reg, rid, elements, detail=False):
    r = reg["risks"][rid]
    hazards = reg["hazards"] or {}
    controls = []
    for cid in r.get("controls", []) or []:
        c = reg["controls"].get(cid)
        if c:
            rec = {"id": cid, "level": c.get("level"), "statement": c.get("statement", "")}
            if detail:
                rec["recommendations"] = (c.get("recommendations") or "").strip()
            controls.append(rec)
    return {
        "id": rid,
        "statement": r.get("statement", ""),
        "description": (r.get("description") or "").strip(),
        "elements": [f"{elements[e]['kind']}: {elements[e]['name']} ({e})" if e in elements else e
                     for e in risk_elements(r)],
        "failure_mode": r.get("failure_mode", ""),
        "type": r.get("type", []),
        "hazards": [f"{hazards[h]['name']} ({h})" if h in hazards else h for h in r.get("hazards", []) or []],
        "controls": controls,
    }


def combination_checks(reg, capabilities):
    """Check the system's capabilities against each combination the register defines (combinations.yaml).

    Each combination has legs; a capability supplies a leg always ("yes") or only in some deployments
    ("maybe"). The combination is present when every leg has a "yes" capability, possible when every leg
    is supplied but at least one only by "maybe" capabilities, and not present otherwise. The verdict
    decides whether the combination's control is implemented or waived; it does not change which risks apply.
    """
    elements = element_index(reg)
    applicable = [rid for group in applicable_risks(reg, capabilities) for rid in group]
    out = []
    for combo_id, combo in (reg.get("combinations") or {}).items():
        legs = []
        for leg_id, leg in (combo.get("legs") or {}).items():
            marks = leg.get("capabilities") or {}
            suppliers = [{"id": c, "name": elements.get(c, {}).get("name", ""), "mark": marks[c].get("mark"),
                          "note": marks[c].get("note", "")} for c in capabilities if c in marks]
            status = "yes" if any(s["mark"] == "yes" for s in suppliers) else ("maybe" if suppliers else "none")
            legs.append({"id": leg_id, "name": leg.get("name", leg_id), "description": leg.get("description", ""),
                         "question": leg.get("question", ""), "status": status, "capabilities": suppliers})
        statuses = [leg["status"] for leg in legs]
        verdict = ("not present" if "none" in statuses or not legs
                   else "present" if all(s == "yes" for s in statuses) else "possible")
        cid = combo.get("control")
        control = reg["controls"].get(cid) or {}
        out.append({
            "id": combo_id, "name": combo.get("name", combo_id), "description": combo.get("description", ""),
            "verdict": verdict, "legs": legs,
            "control": {"id": cid, "level": control.get("level"), "statement": control.get("statement", "")},
            "control_listed_by": [rid for rid in applicable if cid in (reg["risks"][rid].get("controls") or [])],
        })
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
    if check["verdict"] != "not present" and not check["control_listed_by"]:
        advice += (f" None of this system's applicable risks lists {cid} in this register version, so record it "
                   "with the combination check.")
    return advice


def parse_ids(text):
    return [x.strip().upper() for x in (text or "").split(",") if x.strip()]


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
    caps = parse_ids(args.capabilities)
    unknown = [c for c in caps if elements.get(c, {}).get("kind") != "Capability"]
    if unknown:
        valid = ", ".join(f"{e['id']} {e['name']}" for e in elements.values() if e["kind"] == "Capability")
        raise ArcError(f"unknown capability ID(s): {', '.join(unknown)}. Valid: {valid}")
    components = parse_ids(getattr(args, "components", "") or "")
    conditional = {e["id"]: e for e in elements.values() if e["present_when"]}
    stray = [c for c in components if c not in conditional]
    if stray:
        valid = ", ".join(f"{e['id']} {e['name']}" for e in conditional.values()) or "none in this register"
        raise ArcError(f"not a conditional component: {', '.join(stray)}. Conditional components: {valid}")
    baseline, single, combination = applicable_risks(reg, caps + components)
    applicable = baseline + single + combination
    groups = [("Baseline risks (components and design elements)", baseline),
              ("Risks from capabilities and conditional components", single),
              ("Risks from combinations of elements", combination)]
    records = {rid: risk_record(reg, rid, elements, detail=args.detail) for rid in applicable}

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

    combinations = combination_checks(reg, caps)
    v = reg["register"].get("version")
    if args.format == "json":
        out = {"register_version": v, "source": source, "capabilities": caps, "components": components,
               "conditional_components": [{"id": e["id"], "name": e["name"], "present_when": e["present_when"],
                                           "present": e["id"] in components} for e in conditional.values()],
               "risks": {"baseline": [records[r] for r in baseline], "capability": [records[r] for r in single],
                         "combination": [records[r] for r in combination]},
               "level0_controls": [{"id": k, **val} for k, val in level0.items()],
               "combinations": [{**c, "advice": combination_advice(c)} for c in combinations]}
        if in_scope is not None:
            out["priority_risks"] = priority
            out["controls_in_scope"] = [{"id": k, **val} for k, val in in_scope.items()]
        print(json.dumps(out, indent=2))
        return

    cap_names = ", ".join(f"{c} {elements[c]['name']}" for c in caps) or "none"
    by_level = lambda d: ", ".join(f"{sum(1 for x in d.values() if x['level'] == lv)} at Level {lv}" for lv in (0, 1, 2))
    print(f"# ARC applicable risks (register {v}; {source})\n")
    print(f"**Capabilities:** {cap_names}\n")
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
                print(f"- {c['id']} [{LEVELS.get(c['level'], c['level'])}] {c['statement']}")
                if args.detail and c.get("recommendations"):
                    print(f"  - Guidance: {c['recommendations']}")
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
        if eid in reg["risks"]:
            out.append({**risk_record(reg, eid, elements, detail=True), "sources": reg["risks"][eid].get("sources", [])})
        elif eid in reg["controls"]:
            c = reg["controls"][eid]
            out.append({"id": eid, "level": c.get("level"), "statement": c.get("statement", ""),
                        "recommendations": (c.get("recommendations") or "").strip(), "risks": c.get("risks", []),
                        "references": c.get("references") or []})
        elif eid in elements:
            e = elements[eid]
            out.append({**e, "risks": [rid for rid, r in reg["risks"].items() if eid in risk_elements(r)]})
        else:
            raise ArcError(f"{raw_id} is not a risk, control or element in this register")
    if args.format == "json":
        print(json.dumps({"register_version": reg["register"].get("version"), "source": source, "entries": out},
                         indent=2, default=str))
        return
    for e in out:
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
    parser.add_argument("--version", help="official register version to use, e.g. 1.3.0 (default: latest release)")
    parser.add_argument("--register", help="an organisation's own register: a directory or base URL with the "
                                           "same file layout as arc-risk-register/")
    parser.add_argument("--refresh", action="store_true", help="re-download cached release files")
    fmt = argparse.ArgumentParser(add_help=False)
    fmt.add_argument("--format", choices=("md", "json"), default="md", help="output format (default: md)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("elements", parents=[fmt], help="list components, design elements and capabilities")
    p_assess = sub.add_parser("assess", parents=[fmt], help="list applicable risks and their controls")
    p_assess.add_argument("--capabilities", default="", help="comma-separated capability IDs, e.g. CAP-03,CAP-07")
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
