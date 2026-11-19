"""Offline test for the ARC assessment skill's script against this repository's register.

    python skills/tests/test_arc_assessment.py      # or: pytest skills/tests
"""
import contextlib
import io
import json
import shutil
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
    out = json.loads(run("--register", str(REGISTER), "show", "RISK-034", "CTRL-0062", "--format", "json"))
    assert [e["id"] for e in out["entries"]] == ["RISK-034", "CTRL-0062"]
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


if __name__ == "__main__":
    test_applicability_matches_register_rules()
    test_show_and_elements()
    test_organisation_register_with_single_element_id()
    print("ALL PASSED")
