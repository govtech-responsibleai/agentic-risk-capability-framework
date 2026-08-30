"""Data loading utilities.

ARCvisor reads the ARC risk register directly from ``arc-risk-register/`` at the
repository root, so the app can never drift from the published framework. Set
``ARC_REGISTER_DIR`` to point elsewhere (e.g. in a container that copies the
register to a different path).
"""

import os
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
import yaml

REGISTER_DIR_ENV = "ARC_REGISTER_DIR"
REGISTER_FILES = ("capabilities", "risks", "controls", "components", "design")

# Element ID prefixes used in the register (CAP-01, CMP-01, DSN-01, ...)
KIND_BY_PREFIX = {"CAP": "capability", "CMP": "component", "DSN": "design"}
KIND_LABELS = {"capability": "Capability", "component": "Component", "design": "Design"}

CONTROL_LEVEL_LABELS = {
    0: "Level 0 · Cardinal",
    1: "Level 1 · Standard",
    2: "Level 2 · Best Practice",
}

Register = Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]
_EMPTY: Register = ({}, {}, {}, {}, {})


def get_register_dir() -> str:
    """Directory holding the register YAML files."""
    override = os.environ.get(REGISTER_DIR_ENV)
    if override:
        return override
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # app/
    return os.path.join(os.path.dirname(app_dir), "arc-risk-register")


def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


@st.cache_data
def load_data() -> Register:
    """Load the register.

    Returns:
        Tuple of (capabilities, risks, controls, components, design) dictionaries,
        keyed by element/risk/control ID exactly as in the YAML files. All five are
        empty if any file is missing or invalid.
    """
    register_dir = get_register_dir()
    loaded: Dict[str, Dict[str, Any]] = {}
    for name in REGISTER_FILES:
        path = os.path.join(register_dir, f"{name}.yaml")
        try:
            data = _load_yaml(path)
        except FileNotFoundError:
            st.error(
                f"Register file not found: {path}. "
                f"Run the app from the repository root, or set {REGISTER_DIR_ENV} "
                "to the directory containing the ARC risk register."
            )
            return _EMPTY
        except yaml.YAMLError as e:
            st.error(f"Error parsing {path}: {e}")
            return _EMPTY
        if not data:
            st.error(f"Register file is empty: {path}")
            return _EMPTY
        loaded[name] = data
    return tuple(loaded[name] for name in REGISTER_FILES)  # type: ignore[return-value]


@st.cache_data
def load_sample_data() -> Dict[str, Any]:
    """Load the sample application used by the "Try Sample" button."""
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(app_dir, "sample_data.yaml")
    try:
        sample_data = _load_yaml(path)
    except FileNotFoundError:
        st.error("Sample data file not found. Please ensure sample_data.yaml exists")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing sample_data.yaml: {e}")
        return {}
    if "sample_application" not in sample_data:
        st.error("Invalid sample data format. Please check sample_data.yaml")
        return {}
    return sample_data["sample_application"]


# --- Element helpers ---------------------------------------------------------

def element_kind(element_id: str) -> str:
    """'capability', 'component', or 'design' for a register element ID."""
    prefix = (element_id or "").split("-")[0]
    return KIND_BY_PREFIX.get(prefix, "unknown")


def is_baseline_risk(risk: Dict[str, Any]) -> bool:
    """Component and design risks apply to every agentic system."""
    return element_kind(risk.get("element_id", "")) in ("component", "design")


def get_element(element_id: str, capabilities: Dict[str, Any],
                components: Dict[str, Any], design: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Look up the element (capability, component, or design) a risk arises from."""
    kind = element_kind(element_id)
    source = {"capability": capabilities, "component": components, "design": design}.get(kind, {})
    return source.get(element_id)


def describe_risk_element(risk: Dict[str, Any], capabilities: Dict[str, Any],
                          components: Dict[str, Any], design: Dict[str, Any]) -> str:
    """Human-readable origin of a risk, e.g. 'Capability: Tool Use (Cognitive)'."""
    element_id = risk.get("element_id", "")
    kind = element_kind(element_id)
    element = get_element(element_id, capabilities, components, design)
    if not element:
        return element_id or "Unknown element"
    label = f"{KIND_LABELS.get(kind, 'Element')}: {element.get('name', element_id)}"
    if kind == "capability" and element.get("category"):
        label += f" ({element['category']})"
    return label


def get_applicable_risk_ids(risks: Dict[str, Any], selected_capabilities: List[str]) -> List[str]:
    """All baseline (component/design) risks plus the risks of the selected capabilities.

    Order follows the register: baseline risks first, then capability risks.
    """
    baseline = [rid for rid, r in risks.items() if is_baseline_risk(r)]
    capability = [
        rid for rid, r in risks.items()
        if element_kind(r.get("element_id", "")) == "capability"
        and r.get("element_id") in selected_capabilities
    ]
    return baseline + capability


def control_level_label(level: Any) -> str:
    try:
        return CONTROL_LEVEL_LABELS[int(level)]
    except (KeyError, TypeError, ValueError):
        return f"Level {level}"


def get_controls_for_risk(risk_id: str, risks: Dict[str, Any],
                          controls: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Controls recommended for a risk, in register order.

    Returns:
        List of dicts with id, statement, recommendations, level, level_label, references.
    """
    risk = risks.get(risk_id)
    if risk is None:
        st.warning(f"Risk {risk_id} not found in the register")
        return []

    risk_controls = []
    for ctrl_id in risk.get("controls", []) or []:
        control = controls.get(ctrl_id)
        if control is None:
            st.warning(f"Control {ctrl_id} (for {risk_id}) not found in the register")
            continue
        risk_controls.append({
            "id": ctrl_id,
            "statement": control.get("statement", ""),
            "recommendations": control.get("recommendations") or "",
            "level": control.get("level"),
            "level_label": control_level_label(control.get("level")),
            "references": control.get("references") or [],
        })
    return risk_controls
