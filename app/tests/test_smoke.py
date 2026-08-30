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

SELECTED = ["CAP-07", "CAP-11"]  # Internet & Search Access, File & Data Management


def test_loader_helpers():
    caps, risks, controls, comps, design = dl.load_data()
    assert caps and risks and controls and comps and design, "register failed to load"
    assert all(dl.element_kind(eid) != "unknown" for r in risks.values() for eid in r["element_ids"])

    baseline = [rid for rid in risks if dl.is_baseline_risk(risks[rid])]
    assert baseline, "no baseline risks found"
    ids = dl.get_applicable_risk_ids(risks, SELECTED)
    assert ids[:len(baseline)] == baseline
    assert all(set(risks[r]["element_ids"]) <= set(SELECTED) for r in ids[len(baseline):])

    assert dl.describe_risk_element(risks["RISK-034"], caps, comps, design) == \
        "Capability: Internet and Search Access (Interaction)"
    assert dl.describe_risk_element(risks["RISK-001"], caps, comps, design) == "Component: LLM"

    ctrls = dl.get_controls_for_risk("RISK-034", risks, controls)
    assert [c["id"] for c in ctrls] == risks["RISK-034"]["controls"]
    assert all(c["statement"] and c["level_label"].startswith("Level") for c in ctrls)

    from utils.llm_utils import format_risks_for_prompt
    text = format_risks_for_prompt(["RISK-034"], risks, caps, comps, design)
    assert risks["RISK-034"]["statement"] in text and "Failure mode:" in text


def _fake_capability_analysis(app_info, capabilities):
    return CapabilityAnalysis(applicable_capabilities=SELECTED, reasoning="canned")


def _fake_risk_analysis(app_info, selected, capabilities, risks, components, design, applicable_risk_ids=None):
    ids = applicable_risk_ids or dl.get_applicable_risk_ids(risks, selected)
    return RiskAnalysis(
        applicable_risks=ids,
        risk_assessments={
            rid: RiskAssessment(context=f"context for {rid}",
                                likelihood=ScoreAssessment(score=5, reasoning="likelihood"),
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
        assert at.session_state["high_priority_risks"] == expected_ids

        # Step 4: controls
        at.session_state["page"] = "controls"
        at.run(); assert not at.exception, at.exception
        body = " ".join(m.value for m in at.markdown) + " " + " ".join(e.label for e in at.expander)
        first_control = controls[risks["RISK-034"]["controls"][0]]["statement"]
        assert f"Control 1: {first_control}" in body
        assert "Level 0 · Cardinal" in body, "control level badge missing"
        assert "No specific controls found" not in body

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
