"""Headless smoke test for ARCvisor against the real ARC risk register.

Runs without a browser or LLM access: the LLM calls are patched with canned
results derived from the register, and Streamlit's AppTest drives all four
pages plus the Word export.

    python app/tests/test_smoke.py      # or: pytest app/tests
"""
import os
import sys
from unittest import mock

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(APP_DIR)
sys.path.insert(0, APP_DIR)

from utils import data_loader as dl  # noqa: E402
from models.schemas import CapabilityAnalysis, RiskAnalysis, RiskAssessment, ScoreAssessment  # noqa: E402
from utils.session_utils import NOT_IMPLEMENTED_TEXT  # noqa: E402

SELECTED = ["CAP-07", "CAP-11"]  # Internet & Search Access, File & Data Management


def test_loader_helpers():
    caps, risks, controls, comps, design = dl.load_data()
    assert caps and risks and controls and comps and design, "register failed to load"
    assert all(dl.element_kind(eid) != "unknown" for r in risks.values() for eid in r.get("element_ids") or [])

    baseline = [rid for rid in risks if dl.is_baseline_risk(risks[rid])]
    assert baseline, "no baseline risks found"
    ids = dl.get_applicable_risk_ids(risks, SELECTED)
    assert ids[:len(baseline)] == baseline
    assert all(set(risks[r].get("element_ids") or []) <= set(SELECTED) for r in ids[len(baseline):])
    # RISK-047 arises from a combination rule, which web access and file management complete between them
    assert "RISK-047" in ids and dl.describe_risk_element(risks["RISK-047"], caps, comps, design) == \
        "Combination: Lethal trifecta"

    assert dl.describe_risk_element(risks["RISK-034"], caps, comps, design) == \
        "Capability: Internet and Search Access (Interaction)"
    assert dl.describe_risk_element(risks["RISK-001"], caps, comps, design) == "Component: LLM"

    ctrls = dl.get_controls_for_risk("RISK-034", risks, controls)
    assert [c["id"] for c in ctrls] == risks["RISK-034"]["controls"]
    assert all(c["statement"] and c["level_label"].startswith("Level") for c in ctrls)

    # Level 0 attaches on applicability; scoring governs Levels 1 and 2 only
    below = dl.controls_in_scope(ctrls, meets_threshold=False)
    assert below and all(dl.is_level0(c) for c in below)
    assert len(below) < len(ctrls), "RISK-034 should have Level 1-2 controls too"
    assert dl.controls_in_scope(ctrls, meets_threshold=True) == ctrls
    in_scope = dict(dl.controls_by_risk(["RISK-034", "RISK-001"], ["RISK-001"], risks, controls))
    assert in_scope["RISK-034"] == below
    assert in_scope["RISK-001"] == dl.get_controls_for_risk("RISK-001", risks, controls)

    from utils.llm_utils import format_risks_for_prompt
    text = format_risks_for_prompt(["RISK-034"], risks, caps, comps, design)
    assert risks["RISK-034"]["statement"] in text and "Failure mode:" in text


def _fake_capability_analysis(app_info, capabilities):
    return CapabilityAnalysis(applicable_capabilities=SELECTED, reasoning="canned")


BELOW_THRESHOLD = "RISK-034"  # scored low, so only its Level 0 controls should be shown


def _fake_risk_analysis(app_info, selected, capabilities, risks, components, design, applicable_risk_ids=None):
    ids = applicable_risk_ids or dl.get_applicable_risk_ids(risks, selected)
    return RiskAnalysis(
        applicable_risks=ids,
        risk_assessments={
            rid: RiskAssessment(context=f"context for {rid}",
                                likelihood=ScoreAssessment(score=1 if rid == BELOW_THRESHOLD else 5,
                                                           reasoning="likelihood"),
                                impact=ScoreAssessment(score=5, reasoning="impact"))
            for rid in ids
        },
        reasoning="canned",
    )


def test_app_flow():
    from streamlit.testing.v1 import AppTest

    _, risks, controls, _, _ = dl.load_data()
    expected_ids = dl.get_applicable_risk_ids(risks, SELECTED)

    with mock.patch("utils.llm_utils.get_llm_capability_analysis", _fake_capability_analysis), \
         mock.patch("utils.llm_utils.get_llm_risk_analysis", _fake_risk_analysis), \
         mock.patch("utils.llm_utils.get_application_description", lambda info: "generated description"):
        at = AppTest.from_file(os.path.join(APP_DIR, "app.py"), default_timeout=120)
        at.run()
        assert not at.exception, at.exception

        at.session_state["application_info"] = {
            "description": "A research agent that browses the web and reads internal files",
            "data_classification": "Internal", "human_in_loop": "reviewer approves reports",
            "public_facing": "No", "criticality": "Medium", "pii_data": "No",
            "components": "browser tool, file tool",
        }
        at.session_state["application_description"] = "generated description"

        # Step 2: capability identification (first run triggers analysis + rerun)
        at.session_state["page"] = "capability_identification"
        at.run(); assert not at.exception, at.exception
        at.run(); assert not at.exception, at.exception
        assert at.session_state["selected_capabilities"] == SELECTED

        # Step 3: risk assessment
        at.session_state["page"] = "risk_assessment"
        at.run(); assert not at.exception, at.exception
        at.run(); assert not at.exception, at.exception
        body = " ".join(m.value for m in at.markdown)
        assert risks["RISK-034"]["statement"] in body, "capability risk not rendered"
        assert risks["RISK-001"]["statement"] in body, "baseline risk not rendered"
        assert "Component: LLM" in body and "Unknown" not in body
        assert at.session_state["high_priority_risks"] == [r for r in expected_ids if r != BELOW_THRESHOLD]

        # Step 4: controls
        at.session_state["page"] = "controls"
        at.run(); assert not at.exception, at.exception
        body = " ".join(m.value for m in at.markdown) + " " + " ".join(e.label for e in at.expander)
        assert "Level 0 · Cardinal" in body, "control level badge missing"
        assert "No specific controls found" not in body

        # A risk below the thresholds still carries its Level 0 controls, and only those
        boxes = {t.key: t.value for t in at.text_area if t.key.startswith("implementation_text_")}
        shown = {k.split("_", 3)[3] for k in boxes if k.startswith(f"implementation_text_{BELOW_THRESHOLD}_")}
        level0 = {c for c in risks[BELOW_THRESHOLD]["controls"] if controls[c]["level"] == 0}
        assert shown == level0, (shown, level0)
        # Level 0 starts blank (implemented, or waived only if its subject is absent); Levels 1-2 keep the explicit "not implemented" default
        for key, value in boxes.items():
            ctrl = key.split("_", 3)[3]
            assert value == ("" if controls[ctrl]["level"] == 0 else NOT_IMPLEMENTED_TEXT), (key, value)
        assert any("Level 0 control entries have no implementation described" in w.value for w in at.warning)

        # Every applicable risk with a Level 0 control appears, whatever its score
        for rid in expected_ids:
            for ctrl in risks[rid]["controls"]:
                if controls[ctrl]["level"] == 0:
                    assert f"implementation_text_{rid}_{ctrl}" in boxes, (rid, ctrl)

        # Export
        export_button = [b for b in at.button if "Export" in b.label][0]
        export_button.click().run()
        assert not at.exception, at.exception
        assert not at.error, [e.value for e in at.error]
        assert any("Download Word Document" in d.label for d in at.get("download_button"))


if __name__ == "__main__":
    test_loader_helpers()
    print("✓ loader helpers")
    test_app_flow()
    print("✓ app flow + export")
    print("ALL PASSED")
