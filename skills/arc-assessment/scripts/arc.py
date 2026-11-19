#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Query the ARC risk register for an assessment.

Fetches the register YAML from the official repository at a release tag (the
latest release unless --version is given), or reads an organisation's own
contextualised register with --register (a local directory or a base URL with
the same file layout as arc-risk-register/).

Commands:
  elements                      components, design elements and capabilities, with definitions
  assess --capabilities IDS     applicable risks and their controls for a system
  show ID [ID ...]              full text of risks or controls (e.g. RISK-034 CTRL-0062)
  template                      the ARC assessment template (Markdown)

Examples:
  python arc.py elements
  python arc.py assess --capabilities CAP-03,CAP-07,CAP-11
  python arc.py --version 1.3.0 assess --capabilities CAP-10 --format json
  python arc.py --register ./our-arc-register assess --capabilities CAP-02,CAP-06
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("arc.py needs PyYAML: run `pip install pyyaml` (or `uv run arc.py ...`).")

REPO_RAW = "https://raw.githubusercontent.com/govtech-responsibleai/agentic-risk-capability-framework"
SITE = "https://govtech-responsibleai.github.io/agentic-risk-capability-framework/"
REGISTER_FILES = ("register", "risks", "controls", "capabilities", "components", "design", "hazards")
TEMPLATE_PATH = "docs/implementation/assessment-template.md"
CACHE_DIR = Path(os.environ.get("ARC_CACHE_DIR", Path.home() / ".cache" / "arc-assessment"))
LEVELS = {0: "Level 0 · Cardinal", 1: "Level 1 · Standard", 2: "Level 2 · Best Practice"}


# ---------------------------------------------------------------- fetching

def _http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "arc-assessment-skill"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _cached_get(url, ref, name, refresh):
    """Release tags are immutable, so their files are cached; anything else is fetched fresh."""
    cacheable = ref.startswith("v")
    path = CACHE_DIR / ref / name
    if cacheable and path.exists() and not refresh:
        return path.read_text()
    text = _http_get(url)
    if cacheable:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return text


def resolve_official_ref(version):
    """The git ref to read: v<version>, defaulting to the latest release recorded on main."""
    if version:
        return "v" + version.lstrip("v")
    latest = yaml.safe_load(_http_get(f"{REPO_RAW}/main/arc-risk-register/register.yaml"))
    return f"v{latest['version']}"


def load_register(args):
    """Return (register dict of the seven files, human-readable source description, git ref for the template)."""
    data = {}
    if args.register:
        src = args.register
        for name in REGISTER_FILES:
            if src.startswith(("http://", "https://")):
                try:
                    data[name] = yaml.safe_load(_http_get(f"{src.rstrip('/')}/{name}.yaml"))
                except urllib.error.HTTPError:
                    data[name] = None
            else:
                p = Path(src) / f"{name}.yaml"
                data[name] = yaml.safe_load(p.read_text()) if p.exists() else None
        missing = [n for n in REGISTER_FILES if data[n] is None and n != "hazards" and n != "register"]
        if missing:
            sys.exit(f"{src} is missing {', '.join(f'{m}.yaml' for m in missing)}; "
                     "an organisation's register must use the same file layout as arc-risk-register/.")
        data["hazards"] = data["hazards"] or {}
        data["register"] = data["register"] or {"version": "unversioned", "released": ""}
        return data, f"organisation register at {src}", None

    ref = resolve_official_ref(args.version)
    for name in REGISTER_FILES:
        url = f"{REPO_RAW}/{ref}/arc-risk-register/{name}.yaml"
        try:
            data[name] = yaml.safe_load(_cached_get(url, ref, f"{name}.yaml", args.refresh))
        except urllib.error.HTTPError as e:
            if e.code == 404 and name == "register" and not args.version:
                sys.exit(f"Release tag {ref} not found in the ARC repository; pass --version to choose one.")
            if e.code == 404:
                sys.exit(f"{url} not found; check that --version names a released register version.")
            raise
    return data, f"official ARC register, tag {ref}", ref


# ---------------------------------------------------------------- register logic

def element_index(reg):
    idx = {}
    for kind, key in (("Component", "components"), ("Design", "design"), ("Capability", "capabilities")):
        for eid, e in (reg[key] or {}).items():
            idx[eid] = {"id": eid, "kind": kind, "name": e.get("name", ""), "category": e.get("category", ""),
                        "description": (e.get("description") or "").strip()}
    return idx


def is_capability(eid, elements):
    return elements.get(eid, {}).get("kind") == "Capability"


def applicable_risks(reg, capabilities):
    """Risks that apply to a system with the given capabilities, grouped as the ARC developer guide does.

    A risk applies when all the elements it arises from are present. Components and design elements are
    present in every agentic system, so a risk arising only from them is a baseline risk; a risk that
    lists capabilities applies only when the system has all of them.
    """
    elements = element_index(reg)
    selected = set(capabilities)
    baseline, single, combination = [], [], []
    for rid, r in reg["risks"].items():
        if r.get("superseded_by"):
            continue
        ids = r.get("element_ids") or ([r["element_id"]] if r.get("element_id") else [])
        needed = {e for e in ids if is_capability(e, elements)}
        if not needed:
            baseline.append(rid)
        elif needed <= selected:
            (combination if len(ids) > 1 else single).append(rid)
    return baseline, single, combination


def risk_record(reg, rid, elements, detail=False):
    r = reg["risks"][rid]
    ids = r.get("element_ids") or ([r["element_id"]] if r.get("element_id") else [])
    hazards = reg["hazards"] or {}
    controls = []
    for cid in r.get("controls", []) or []:
        c = reg["controls"].get(cid)
        if not c:
            continue
        rec = {"id": cid, "level": c.get("level"), "statement": c.get("statement", "")}
        if detail:
            rec["recommendations"] = (c.get("recommendations") or "").strip()
        controls.append(rec)
    return {
        "id": rid,
        "statement": r.get("statement", ""),
        "description": (r.get("description") or "").strip(),
        "elements": [f"{elements[e]['kind']}: {elements[e]['name']} ({e})" if e in elements else e for e in ids],
        "failure_mode": r.get("failure_mode", ""),
        "type": r.get("type", []),
        "hazards": [f"{hazards[h]['name']} ({h})" if h in hazards else h for h in r.get("hazards", []) or []],
        "controls": controls,
    }


# ---------------------------------------------------------------- commands

def cmd_elements(reg, source, args):
    elements = element_index(reg)
    v = reg["register"].get("version")
    if args.format == "json":
        print(json.dumps({"register_version": v, "source": source, "elements": list(elements.values())}, indent=2))
        return
    print(f"# ARC elements (register {v}; {source})\n")
    print("Components and design elements are present in every agentic system. Capabilities are what the system "
          "can do; a system has a capability if any of its agents has it.\n")
    for kind, title in (("Component", "Components"), ("Design", "Design elements"), ("Capability", "Capabilities")):
        print(f"## {title}\n")
        for e in elements.values():
            if e["kind"] == kind:
                cat = f" — {e['category']}" if e["category"] else ""
                print(f"- **{e['id']} {e['name']}**{cat}: {e['description']}\n")


def cmd_assess(reg, source, args):
    elements = element_index(reg)
    caps = [c.strip().upper() for c in args.capabilities.split(",") if c.strip()] if args.capabilities else []
    unknown = [c for c in caps if not is_capability(c, elements)]
    if unknown:
        valid = ", ".join(f"{e['id']} {e['name']}" for e in elements.values() if e["kind"] == "Capability")
        sys.exit(f"Unknown capability ID(s): {', '.join(unknown)}. Valid: {valid}")
    baseline, single, combination = applicable_risks(reg, caps)
    groups = [("Baseline risks (components and design elements)", baseline),
              ("Capability risks", single),
              ("Risks from combinations of elements", combination)]
    records = {rid: risk_record(reg, rid, elements, detail=args.detail) for _, ids in groups for rid in ids}

    level0 = {}
    for rid, rec in records.items():
        for c in rec["controls"]:
            if c["level"] == 0:
                level0.setdefault(c["id"], {"statement": c["statement"], "risks": []})["risks"].append(rid)

    v = reg["register"].get("version")
    if args.format == "json":
        print(json.dumps({
            "register_version": v, "source": source, "capabilities": caps,
            "risks": {"baseline": [records[r] for r in baseline], "capability": [records[r] for r in single],
                      "combination": [records[r] for r in combination]},
            "level0_controls": [{"id": k, **val} for k, val in level0.items()],
        }, indent=2))
        return

    total = len(baseline) + len(single) + len(combination)
    cap_names = ", ".join(f"{c} {elements[c]['name']}" for c in caps) or "none"
    print(f"# ARC applicable risks (register {v}; {source})\n")
    print(f"**Capabilities:** {cap_names}\n")
    print(f"**{total} applicable risks:** {len(baseline)} baseline, {len(single)} from single capabilities, "
          f"{len(combination)} from combinations of elements. They carry {len(level0)} distinct Level 0 controls.\n")
    print(f"Control levels are defined at {SITE}arc_framework/controls/#control-levels; "
          f"each entry's full text is at {SITE}arc_framework/register-full-text/#<ID> or via `arc.py show <ID>`.\n")
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
    if level0:
        print("## Level 0 controls across all applicable risks\n")
        print("Each Level 0 control once, with the applicable risks it addresses:\n")
        for cid, val in sorted(level0.items()):
            print(f"- {cid} {val['statement']} — {', '.join(val['risks'])}")


def cmd_show(reg, source, args):
    elements = element_index(reg)
    out = []
    for raw_id in args.ids:
        eid = raw_id.upper()
        if eid in reg["risks"]:
            out.append(risk_record(reg, eid, elements, detail=True) | {"sources": reg["risks"][eid].get("sources", [])})
        elif eid in reg["controls"]:
            c = reg["controls"][eid]
            out.append({"id": eid, "level": c.get("level"), "statement": c.get("statement", ""),
                        "recommendations": (c.get("recommendations") or "").strip(), "risks": c.get("risks", []),
                        "references": c.get("references") or []})
        else:
            sys.exit(f"{raw_id} is not a risk or control in this register.")
    if args.format == "json":
        print(json.dumps({"register_version": reg["register"].get("version"), "source": source, "entries": out}, indent=2))
        return
    for e in out:
        if "controls" in e:
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


def cmd_template(reg, source, args, ref):
    ref = ref or resolve_official_ref(None)
    print(_cached_get(f"{REPO_RAW}/{ref}/{TEMPLATE_PATH}", ref, "assessment-template.md", args.refresh))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", help="official register version to use, e.g. 1.3.0 (default: latest release)")
    parser.add_argument("--register", help="an organisation's own register: a directory or base URL with the "
                                           "same file layout as arc-risk-register/")
    parser.add_argument("--refresh", action="store_true", help="re-download cached release files")
    fmt = argparse.ArgumentParser(add_help=False)
    fmt.add_argument("--format", choices=("md", "json"), default="md", help="output format (default: md)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("elements", parents=[fmt], help="list components, design elements and capabilities with definitions")
    p_assess = sub.add_parser("assess", parents=[fmt], help="list applicable risks and their controls")
    p_assess.add_argument("--capabilities", default="", help="comma-separated capability IDs, e.g. CAP-03,CAP-07")
    p_assess.add_argument("--detail", action="store_true", help="include each control's implementation guidance")
    p_show = sub.add_parser("show", parents=[fmt], help="full text of risks or controls")
    p_show.add_argument("ids", nargs="+")
    sub.add_parser("template", help="print the ARC assessment template")
    args = parser.parse_args(argv)

    if args.register and args.version:
        parser.error("--register and --version are alternatives")
    reg, source, ref = load_register(args)
    if args.command == "elements":
        cmd_elements(reg, source, args)
    elif args.command == "assess":
        cmd_assess(reg, source, args)
    elif args.command == "show":
        cmd_show(reg, source, args)
    else:
        cmd_template(reg, source, args, ref)


if __name__ == "__main__":
    main()
