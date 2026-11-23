"""Offline test for the ARC assessment skill's script against this repository's register.

    python skills/tests/test_arc_assessment.py      # or: pytest skills/tests
"""
import argparse
import contextlib
import io
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
REGISTER = REPO / "arc-risk-register"
sys.path.insert(0, str(REPO / "skills" / "arc-assessment" / "scripts"))
import arc  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        arc.main(list(argv))
    return buf.getvalue()


def assess(present, register=REGISTER):
    """Assess a system that has the given capabilities and conditional components (CAP-.. and CMP-.. IDs)."""
    caps = [e for e in present if e.startswith("CAP-")]
    components = [e for e in present if not e.startswith("CAP-")]
    return json.loads(run("--register", str(register), "assess", "--capabilities", ",".join(caps),
                          "--components", ",".join(components), "--format", "json"))


def chosen_elements(register=REGISTER):
    """Elements only some systems have: capabilities, and components or design elements with `present_when`."""
    chosen = set(yaml.safe_load((register / "capabilities.yaml").read_text()))
    for name in ("components", "design"):
        chosen |= {e for e, v in yaml.safe_load((register / f"{name}.yaml").read_text()).items() if v.get("present_when")}
    return chosen


def test_applicability_matches_register_rules():
    risks = {r: v for r, v in yaml.safe_load((REGISTER / "risks.yaml").read_text()).items() if not v.get("superseded_by")}
    controls = yaml.safe_load((REGISTER / "controls.yaml").read_text())
    chosen = chosen_elements()
    is_cap = lambda e: e in chosen
    by_rule = {r for r, v in risks.items() if v.get("combination")}   # these arise from a rule, not from elements
    for v in risks.values():
        v.setdefault("element_ids", [])
    baseline = [r for r, v in risks.items() if r not in by_rule and not any(is_cap(e) for e in v["element_ids"])]

    none = assess([])
    assert [r["id"] for r in none["risks"]["baseline"]] == baseline
    assert none["risks"]["capability"] == [] and none["risks"]["combination"] == []

    # A risk listing several capabilities applies only when all are present
    multi = {r: {e for e in v["element_ids"] if is_cap(e)} for r, v in risks.items()
             if len({e for e in v["element_ids"] if is_cap(e)}) > 1}
    for rid, caps in multi.items():
        for missing in caps:
            partial = assess(sorted(caps - {missing}))
            assert rid not in {r["id"] for g in partial["risks"].values() for r in g}, (rid, missing)
        full = assess(sorted(caps))
        assert rid in {r["id"] for r in full["risks"]["combination"]}, rid

    # Every chosen element's own risks appear when it is selected, with their Level 0 controls summarised once
    everything = assess(sorted(chosen))
    listed = {r["id"] for g in everything["risks"].values() for r in g}
    assert listed == set(risks), set(risks) ^ listed
    # ...at the level each control has in the most cautious context, which is what an unstated context means
    reg = _register()
    cautious = arc.build_profile(reg, sorted(e for e in chosen if e.startswith("CAP-")))
    level0 = {c["id"] for c in everything["level0_controls"]}
    assert level0 == {c for c, v in controls.items()
                      if arc.effective_level(v, cautious) == 0 and set(v["risks"]) & listed}


def test_conditional_components():
    """A component with `present_when` contributes its risks only when the system is said to have it."""
    risks = yaml.safe_load((REGISTER / "risks.yaml").read_text())
    components = yaml.safe_load((REGISTER / "components.yaml").read_text())
    conditional = [c for c, v in components.items() if v.get("present_when")]
    assert conditional, "the register should define at least one conditional component"
    for cid in conditional:
        own = {r for r, v in risks.items() if v.get("element_ids") == [cid]}
        without = {r["id"] for g in assess([])["risks"].values() for r in g}
        with_it = {r["id"] for g in assess([cid])["risks"].values() for r in g}
        assert own and not (own & without) and own <= with_it, cid
    try:
        run("--register", str(REGISTER), "assess", "--capabilities", "CAP-04", "--components", "CMP-01")
    except SystemExit as e:
        assert "not a conditional component" in str(e)
    else:
        raise AssertionError("CMP-01 is always present and should be rejected by --components")


def test_context_changes_applicability_and_levels():
    """Authority, reversibility and reach: a risk can need a minimum authority, and a control can be stricter in context."""
    risks = yaml.safe_load((REGISTER / "risks.yaml").read_text())
    controls = yaml.safe_load((REGISTER / "controls.yaml").read_text())
    capabilities = yaml.safe_load((REGISTER / "capabilities.yaml").read_text())
    order = arc.AUTHORITY

    def run_json(*argv):
        return json.loads(run("--register", str(REGISTER), "assess", *argv, "--format", "json"))

    # A risk that needs a minimum authority is left out below it, and only below it
    gated = {r: v["min_authority"] for r, v in risks.items() if v.get("min_authority")}
    assert gated, "the register should gate at least one risk on authority"
    for rid, need in gated.items():
        (cap, minimum), = need.items()
        others = [e for e in risks[rid]["element_ids"] if e.startswith("CAP-") and e != cap]
        for level in capabilities[cap]["authority"]:
            out = run_json("--capabilities", ",".join([f"{cap}={level}"] + others))
            listed = {r["id"] for g in out["risks"].values() for r in g}
            assert (rid in listed) == (order.index(level) >= order.index(minimum)), (rid, level)
            assert (rid in {b["id"] for b in out["below_authority"]}) == (rid not in listed), (rid, level)

    # A control with level_when is stricter only in that context
    raised = {c: v for c, v in controls.items() if v.get("level_when")}
    assert raised, "the register should raise at least one control's level in context"
    reg = _register()
    for cid, control in raised.items():
        calm = arc.build_profile(reg, ["CAP-11"], {"CAP-11": "read"}, reversible=["CAP-11"], internal=["CAP-11"])
        assert arc.effective_level(control, calm) == control["level"], cid
        assert arc.effective_level(control, arc.build_profile(reg, ["CAP-09"])) < control["level"], cid

    # Unstated context is the most cautious; a profile file says the same thing as the flags
    assert run_json("--capabilities", "CAP-11")["context"]["CAP-11"] == \
        {"authority": "act-alone", "irreversible": True, "external": True}
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp) / "system.yaml"
        profile.write_text("capabilities:\n  CAP-06: {authority: act-with-approval}\n"
                           "  CAP-11: {authority: read, external: false}\ncomponents: [CMP-04]\n")
        from_file = run_json("--profile", str(profile))
    from_flags = run_json("--capabilities", "CAP-06=act-with-approval,CAP-11=read", "--internal", "CAP-11",
                          "--components", "CMP-04")
    assert from_file == from_flags
    assert from_file["context"]["CAP-11"] == {"authority": "read", "irreversible": False, "external": False}
    try:
        run("--register", str(REGISTER), "assess", "--capabilities", "CAP-05=read")
    except SystemExit as e:
        assert "can be used at" in str(e)
    else:
        raise AssertionError("CAP-05 has no read level")


def test_show_and_elements():
    out = json.loads(run("--register", str(REGISTER), "show", "RISK-034", "CTRL-0062", "CAP-07", "--format", "json"))
    assert [e["id"] for e in out["entries"]] == ["RISK-034", "CTRL-0062", "CAP-07"]
    assert "RISK-034" in out["entries"][2]["risks"]
    elements = json.loads(run("--register", str(REGISTER), "elements", "--format", "json"))
    assert sum(e["kind"] == "Capability" for e in elements["elements"]) == 12


def test_organisation_register_with_single_element_id():
    """An organisation's register may still use the older single `element_id` field."""
    with tempfile.TemporaryDirectory() as tmp:
        org = Path(tmp) / "org-register"
        shutil.copytree(REGISTER, org)
        risks = yaml.safe_load((org / "risks.yaml").read_text())
        for v in risks.values():
            if len(v.get("element_ids") or []) == 1:
                v["element_id"] = v.pop("element_ids")[0]
        (org / "risks.yaml").write_text(yaml.safe_dump(risks, sort_keys=False, allow_unicode=True))
        (org / "register.yaml").unlink()
        result = assess(["CAP-07", "CAP-11"], register=org)
        assert result["register_version"] == "unversioned"
        assert [r["id"] for r in result["risks"]["baseline"]] == [r["id"] for r in assess(["CAP-07", "CAP-11"])["risks"]["baseline"]]
        assert "RISK-034" in {r["id"] for r in result["risks"]["capability"]}


def test_builtin_yaml_parser_matches_pyyaml():
    """Without PyYAML the script uses its own parser; it must read every register file exactly as PyYAML does."""
    for f in sorted(REGISTER.glob("*.yaml")):
        if f.stem.endswith("-wog"):
            continue
        text = f.read_text()
        assert arc.mini_yaml_load(text) == yaml.safe_load(text), f.name


def test_runs_without_pyyaml():
    with_pyyaml = assess(["CAP-07", "CAP-11"])
    saved, arc.yaml = arc.yaml, None
    try:
        assert assess(["CAP-07", "CAP-11"]) == with_pyyaml
    finally:
        arc.yaml = saved


def test_priority_lists_controls_in_scope():
    risks = yaml.safe_load((REGISTER / "risks.yaml").read_text())
    controls = yaml.safe_load((REGISTER / "controls.yaml").read_text())
    caps = ["CAP-07", "CAP-11"]
    applicable = [r["id"] for g in assess(caps)["risks"].values() for r in g]
    priority = ["RISK-034"]
    out = json.loads(run("--register", str(REGISTER), "assess", "--capabilities", ",".join(caps),
                         "--priority", ",".join(priority), "--format", "json"))
    profile = arc.build_profile(_register(), caps)
    expected = {c for rid in applicable for c in risks[rid]["controls"]
                if arc.effective_level(controls[c], profile) == 0 or rid in priority}
    assert {c["id"] for c in out["controls_in_scope"]} == expected
    assert len(out["controls_in_scope"]) == len(expected), "each control in scope should appear once"


def _register():
    reg, _, _ = arc.load_register(argparse.Namespace(register=str(REGISTER), version=None, refresh=False))
    return reg


def test_combination_check():
    """Combination rules: verdicts follow the marks in combinations.yaml, and a rule brings its risks into scope."""
    reg = _register()
    trifecta = lambda checks: next(c for c in checks if c["id"] == "lethal-trifecta")
    data = yaml.safe_load((REGISTER / "combinations.yaml").read_text())
    rule = data["rules"]["lethal-trifecta"]
    roles = [data["roles"][r] for r in rule["roles"]]
    caps = sorted(reg["capabilities"])

    def expected(selected):   # the most cautious context, so every mark counts
        legs = [{role["capabilities"][c]["mark"] for c in selected if c in role["capabilities"]} for role in roles]
        if not all(legs):
            return "not present"
        return "present" if all("yes" in marks for marks in legs) else "possible"

    for n in range(len(caps) + 1):
        for subset in itertools.combinations(caps, n):
            check = trifecta(arc.combination_checks(reg, list(subset)))
            assert check["verdict"] == expected(subset), subset
            assert arc.combination_advice(check)
            # the rule's risk applies exactly when the rule is not ruled out
            applies = "RISK-047" in arc.applicable_risks(reg, list(subset))[2]
            assert applies == (check["verdict"] != "not present"), subset

    # The verdicts quoted on the Capability combinations page and in the developer guide's examples
    examples = {
        ("CAP-04",): "not present",
        ("CAP-01", "CAP-02", "CAP-03", "CAP-04", "CAP-07", "CAP-11"): "present",    # fact checker
        ("CAP-01", "CAP-02", "CAP-03", "CAP-04", "CAP-10", "CAP-11"): "possible",   # coding assistant
        ("CAP-01", "CAP-02", "CAP-04", "CAP-06", "CAP-09", "CAP-11"): "possible",   # call assistant
        ("CAP-04", "CAP-05", "CAP-09", "CAP-11"): "possible",                       # email agent
        ("CAP-07", "CAP-12"): "present",                                            # no composite risk covered this in 1.3
    }
    for subset, verdict in examples.items():
        assert trifecta(arc.combination_checks(reg, list(subset)))["verdict"] == verdict, subset

    out = assess(["CAP-07", "CAP-12"])
    check = trifecta(out["combinations"])
    assert check["control"]["id"] == "CTRL-0097" and check["control_listed_by"] == ["RISK-047"]
    assert "RISK-047" in {r["id"] for r in out["risks"]["combination"]}

    # A capability used below the authority a mark needs does not supply the role
    drafting = arc.build_profile(reg, ["CAP-05", "CAP-11"], {"CAP-05": "propose"})
    legs = {leg["id"]: leg["status"] for leg in trifecta(arc.combination_checks(reg, ["CAP-05", "CAP-11"], drafting))["legs"]}
    assert legs["outbound-channel"] == "none"
    sending = arc.build_profile(reg, ["CAP-05", "CAP-11"])
    legs = {leg["id"]: leg["status"] for leg in trifecta(arc.combination_checks(reg, ["CAP-05", "CAP-11"], sending))["legs"]}
    assert legs["outbound-channel"] == "yes"

    # Implied capabilities are reported until they are declared
    implied = {(i["from"], i["capability"]) for i in assess(["CAP-10"])["implied_capabilities"]}
    assert ("CAP-10", "CAP-11") in implied and ("CAP-10", "CAP-09") in implied
    assert not any(i["capability"] == "CAP-11" for i in assess(["CAP-10", "CAP-11"])["implied_capabilities"])

    # A rule with one role: an agent that can change what governs it. Reading is not enough to supply the role.
    oversight = lambda caps, **kw: next(c for c in arc.combination_checks(reg, caps, arc.build_profile(reg, caps, **kw))
                                        if c["id"] == "oversight-within-reach")
    assert oversight(["CAP-04"])["verdict"] == "not present"
    assert oversight(["CAP-12"])["verdict"] == "present"
    assert oversight(["CAP-11"])["verdict"] == "possible"
    assert oversight(["CAP-11"], authority={"CAP-11": "read"})["verdict"] == "not present"
    assert "RISK-062" in arc.applicable_risks(reg, ["CAP-12"])[2] and "RISK-062" not in arc.applicable_risks(reg, ["CAP-04"])[2]

    # A retired risk never applies, and `show` points to its successor
    everything = assess(sorted(chosen_elements()))
    assert "RISK-055" not in {r["id"] for g in everything["risks"].values() for r in g}
    assert "Superseded by RISK-047" in run("--register", str(REGISTER), "show", "RISK-055")


def test_register_without_combinations():
    """Older registers and organisation registers may have no combinations.yaml."""
    with tempfile.TemporaryDirectory() as tmp:
        org = Path(tmp) / "org-register"
        shutil.copytree(REGISTER, org)
        (org / "combinations.yaml").unlink()
        assert assess(["CAP-07", "CAP-11"], register=org)["combinations"] == []
        text = run("--register", str(org), "assess", "--capabilities", "CAP-07,CAP-11")
        assert "Capability combinations" not in text


def test_site_check_matches_script():
    """The website's interactive check (docs/assets/combination-check.js) gives the script's verdicts."""
    if shutil.which("node") is None:
        print("  (node not found; skipping the website check comparison)")
        return
    reg = _register()
    caps = sorted(reg["capabilities"])
    subsets = [list(s) for n in range(len(caps) + 1) for s in itertools.combinations(caps, n)]
    script = (
        "const {checkCombination} = require(process.argv[1]);"
        "const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
        "console.log(JSON.stringify(input.subsets.map((s) => checkCombination(input.combination, s).verdict)));"
    )
    result = subprocess.run(
        ["node", "-e", script, str(REPO / "docs" / "assets" / "combination-check.js")],
        input=json.dumps({"combination": arc.combination_rules(reg)["lethal-trifecta"], "subsets": subsets}),
        capture_output=True, text=True, check=True)
    assert json.loads(result.stdout) == [next(c for c in arc.combination_checks(reg, s) if c["id"] == "lethal-trifecta")["verdict"]
                                         for s in subsets]


def test_overlay():
    """An organisation's overlay is applied to the base register by ID, and what it does not mention is inherited."""
    reg = _register()
    example = REPO / "examples" / "overlay" / "example-agency.yaml"
    overlay = arc.read_overlay(str(example))
    effective, notes = arc.apply_overlay(reg, overlay)

    assert reg["controls"]["CTRL-0081"]["level"] == 1 and "CAP-08" in reg["capabilities"], "the base must not change"
    assert "CAP-08" not in effective["capabilities"]
    assert not any("CAP-08" in (r.get("element_ids") or []) for r in effective["risks"].values())
    assert any(n.startswith("RISK-036 ") for n in notes)
    assert effective["controls"]["CTRL-0081"]["level"] == 0 and effective["controls"]["CTRL-0081"]["overlay"] == "changed"
    assert effective["risks"]["RISK-043"]["description"].startswith(reg["risks"]["RISK-043"]["description"].strip())
    assert effective["risks"]["RISK-043"]["description"].endswith("data management policy.")
    assert effective["controls"]["CTRL-0007"]["provided_by"]["platform"] == "Agency agent platform"
    assert effective["risks"]["EXA-RISK-001"]["overlay"] == "added"
    assert "EXA-RISK-001" in effective["controls"]["CTRL-0047"]["risks"], "links are made in both directions"
    assert effective["risks"]["RISK-001"] == reg["risks"]["RISK-001"], "unmentioned entries are inherited unchanged"
    forward = {(r, c) for r, v in effective["risks"].items() for c in v.get("controls") or []}
    backward = {(r, c) for c, v in effective["controls"].items() for r in v.get("risks") or []}
    assert forward == backward

    out = json.loads(run("--register", str(REGISTER), "--overlay", str(example), "assess",
                         "--capabilities", "CAP-04,CAP-11", "--format", "json"))
    assert "Example Agency ARC register" in out["source"]
    assert "EXA-RISK-001" in {r["id"] for r in out["risks"]["capability"]}

    def refused(changes, expect):
        try:
            arc.apply_overlay(reg, {"overlay": {"base": "2.0.0"}, **changes})
        except arc.ArcError as e:
            assert expect in str(e), str(e)
        else:
            raise AssertionError(f"expected the overlay to be refused: {expect}")
    refused({"controls": {"change": {"CTRL-0062": {"level": 1}}}}, "cannot lower a Level 0 control")
    refused({"risks": {"add": {"RISK-900": {"statement": "x"}}}}, "namespaced ID")
    refused({"controls": {"remove": {"CTRL-0016": "x", "CTRL-0017": "x", "CTRL-0018": "x"}}}, "no controls are left")
    refused({"risks": {"change": {"RISK-055": {"description_append": "x"}}}}, "retired")
    refused({"controls": {"remove": {"CTRL-0097": "x"}}}, "combination rule")


def test_worked_examples_match_the_guide():
    """The developer guide quotes risk and Level 0 counts for its worked examples; they must be what the tool gives.

    Each example in the guide carries a marker such as
    `<!-- arc:example fact-checker risks=45 level0=28 lethal-trifecta=present -->`, and its profile is in
    examples/systems/. When the register changes these numbers, update the guide's prose and its marker together.
    """
    import re
    guide = (REPO / "docs" / "implementation" / "for-ai-developers.md").read_text()
    markers = re.findall(r"<!-- arc:example ([a-z-]+) (.+?) -->", guide)
    assert len(markers) >= 3, "the guide should mark each worked example"
    for name, fields in markers:
        quoted = dict(f.split("=") for f in fields.split())
        out = json.loads(run("--register", str(REGISTER), "assess", "--profile",
                             str(REPO / "examples" / "systems" / f"{name}.yaml"), "--format", "json"))
        actual = {"risks": str(sum(len(g) for g in out["risks"].values())), "level0": str(len(out["level0_controls"]))}
        actual.update({c["id"]: c["verdict"].replace(" ", "-") for c in out["combinations"]})
        assert quoted == {k: actual.get(k) for k in quoted}, (name, quoted, actual)
        # the prose must carry the same numbers as the marker
        paragraph = guide.split(f"<!-- arc:example {name} ")[1].split("\n")[1]
        assert f"This system has {quoted['risks']} applicable risks" in paragraph, name
        assert f"{quoted['level0']} Level 0 controls" in paragraph, name
    for profile in sorted((REPO / "examples" / "systems").glob("*.yaml")):   # every profile must be assessable
        run("--register", str(REGISTER), "assess", "--profile", str(profile), "--format", "json")


def test_template_is_plain_markdown():
    page = (REPO / "docs" / "implementation" / "assessment-template.md").read_text()
    plain = arc.plain_markdown(page)
    assert "!!!" not in plain and "???" not in plain
    assert "](../" not in plain and ".md)" not in plain
    assert arc.SITE + "arc_framework/changelog/" in plain


if __name__ == "__main__":
    test_applicability_matches_register_rules()
    test_conditional_components()
    test_context_changes_applicability_and_levels()
    test_show_and_elements()
    test_organisation_register_with_single_element_id()
    test_builtin_yaml_parser_matches_pyyaml()
    test_runs_without_pyyaml()
    test_priority_lists_controls_in_scope()
    test_combination_check()
    test_register_without_combinations()
    test_site_check_matches_script()
    test_overlay()
    test_worked_examples_match_the_guide()
    test_template_is_plain_markdown()
    print("ALL PASSED")
