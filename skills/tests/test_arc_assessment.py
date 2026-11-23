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


def assess(caps, register=REGISTER):
    return json.loads(run("--register", str(register), "assess", "--capabilities", ",".join(caps), "--format", "json"))


def test_applicability_matches_register_rules():
    risks = yaml.safe_load((REGISTER / "risks.yaml").read_text())
    controls = yaml.safe_load((REGISTER / "controls.yaml").read_text())
    is_cap = lambda e: e.startswith("CAP-")
    baseline = [r for r, v in risks.items() if not any(is_cap(e) for e in v["element_ids"])]

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

    # Every capability's own risks appear when it is selected, with their Level 0 controls summarised once
    all_caps = sorted(yaml.safe_load((REGISTER / "capabilities.yaml").read_text()))
    everything = assess(all_caps)
    listed = {r["id"] for g in everything["risks"].values() for r in g}
    assert listed == set(risks), set(risks) ^ listed
    level0 = {c["id"] for c in everything["level0_controls"]}
    assert level0 == {c for c, v in controls.items() if v["level"] == 0 and set(v["risks"]) & listed}


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
            if len(v["element_ids"]) == 1:
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
    expected = {c for rid in applicable for c in risks[rid]["controls"]
                if controls[c]["level"] == 0 or rid in priority}
    assert {c["id"] for c in out["controls_in_scope"]} == expected
    assert len(out["controls_in_scope"]) == len(expected), "each control in scope should appear once"


def _register():
    reg, _, _ = arc.load_register(argparse.Namespace(register=str(REGISTER), version=None, refresh=False))
    return reg


def test_combination_check():
    """The lethal trifecta check: verdicts follow the marks in combinations.yaml."""
    reg = _register()
    combo = yaml.safe_load((REGISTER / "combinations.yaml").read_text())["lethal-trifecta"]
    caps = sorted(reg["capabilities"])

    def expected(selected):
        legs = [{leg["capabilities"][c]["mark"] for c in selected if c in leg["capabilities"]}
                for leg in combo["legs"].values()]
        if not all(legs):
            return "not present"
        return "present" if all("yes" in marks for marks in legs) else "possible"

    for n in range(len(caps) + 1):
        for subset in itertools.combinations(caps, n):
            (check,) = arc.combination_checks(reg, list(subset))
            assert check["verdict"] == expected(subset), subset
            assert arc.combination_advice(check)

    # The verdicts quoted on the Capability combinations page and in the developer guide's examples
    examples = {
        ("CAP-04",): "not present",
        ("CAP-01", "CAP-02", "CAP-03", "CAP-04", "CAP-07", "CAP-11"): "present",    # fact checker
        ("CAP-01", "CAP-02", "CAP-03", "CAP-04", "CAP-10", "CAP-11"): "possible",   # coding assistant
        ("CAP-01", "CAP-02", "CAP-04", "CAP-06", "CAP-09", "CAP-11"): "possible",   # call assistant
        ("CAP-04", "CAP-05", "CAP-09", "CAP-11"): "possible",                       # email agent
    }
    for subset, verdict in examples.items():
        assert arc.combination_checks(reg, list(subset))[0]["verdict"] == verdict, subset

    out = assess(["CAP-04", "CAP-05", "CAP-09", "CAP-11"])
    (check,) = out["combinations"]
    assert check["control"]["id"] == "CTRL-0097" and check["control"]["level"] == 0
    assert "RISK-055" in check["control_listed_by"]
    assert [leg["status"] for leg in check["legs"]] == ["maybe", "yes", "yes"]
    text = run("--register", str(REGISTER), "assess", "--capabilities", "CAP-07,CAP-12")
    assert "### Lethal trifecta: present" in text
    assert "None of this system's applicable risks lists CTRL-0097" in text  # caught by the check, not by a risk


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
        input=json.dumps({"combination": reg["combinations"]["lethal-trifecta"], "subsets": subsets}),
        capture_output=True, text=True, check=True)
    assert json.loads(result.stdout) == [arc.combination_checks(reg, s)[0]["verdict"] for s in subsets]


def test_template_is_plain_markdown():
    page = (REPO / "docs" / "implementation" / "assessment-template.md").read_text()
    plain = arc.plain_markdown(page)
    assert "!!!" not in plain and "???" not in plain
    assert "](../" not in plain and ".md)" not in plain
    assert arc.SITE + "arc_framework/changelog/" in plain


if __name__ == "__main__":
    test_applicability_matches_register_rules()
    test_show_and_elements()
    test_organisation_register_with_single_element_id()
    test_builtin_yaml_parser_matches_pyyaml()
    test_runs_without_pyyaml()
    test_priority_lists_controls_in_scope()
    test_combination_check()
    test_register_without_combinations()
    test_site_check_matches_script()
    test_template_is_plain_markdown()
    print("ALL PASSED")
