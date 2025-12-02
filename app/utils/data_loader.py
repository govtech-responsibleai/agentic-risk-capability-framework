"""Data loading utilities with comprehensive error handling."""

import streamlit as st
import yaml
import os
from typing import Dict, Any, Tuple, List


@st.cache_data
def load_data() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Load all YAML data files with error handling.

    Returns:
        Tuple of (capabilities, risks, controls, components, design) dictionaries
    """
    # Get the directory of this file (app/utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to app/, then to data/
    data_dir = os.path.join(os.path.dirname(current_dir), '..', 'data')
    
    try:
        with open(os.path.join(data_dir, 'capabilities.yaml'), 'r') as f:
            capabilities = yaml.safe_load(f)
        if not capabilities:
            st.error("Failed to load capabilities data. Please check data/capabilities.yaml")
            return {}, {}, {}, {}, {}
    except FileNotFoundError:
        st.error("Capabilities file not found. Please ensure data/capabilities.yaml exists")
        return {}, {}, {}, {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing capabilities.yaml: {str(e)}")
        return {}, {}, {}, {}
    except Exception as e:
        st.error(f"Unexpected error loading capabilities: {str(e)}")
        return {}, {}, {}, {}
    
    try:
        with open(os.path.join(data_dir, 'risks.yaml'), 'r') as f:
            risks = yaml.safe_load(f)
        if not risks:
            st.error("Failed to load risks data. Please check data/risks.yaml")
            return capabilities, {}, {}, {}, {}, {}
    except FileNotFoundError:
        st.error("Risks file not found. Please ensure data/risks.yaml exists")
        return capabilities, {}, {}, {}, {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing risks.yaml: {str(e)}")
        return capabilities, {}, {}, {}, {}
    except Exception as e:
        st.error(f"Unexpected error loading risks: {str(e)}")
        return capabilities, {}, {}, {}, {}
    
    try:
        with open(os.path.join(data_dir, 'controls.yaml'), 'r') as f:
            controls = yaml.safe_load(f)
        if not controls:
            st.error("Failed to load controls data. Please check data/controls.yaml")
            return capabilities, risks, {}, {}, {}
    except FileNotFoundError:
        st.error("Controls file not found. Please ensure data/controls.yaml exists")
        return capabilities, risks, {}, {}, {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing controls.yaml: {str(e)}")
        return capabilities, risks, {}, {}, {}
    except Exception as e:
        st.error(f"Unexpected error loading controls: {str(e)}")
        return capabilities, risks, {}, {}, {}
    
    try:
        with open(os.path.join(data_dir, 'components.yaml'), 'r') as f:
            components = yaml.safe_load(f)
        if not components:
            st.error("Failed to load components data. Please check data/components.yaml")
            return capabilities, risks, controls, {}, {}
    except FileNotFoundError:
        st.error("Components file not found. Please ensure data/components.yaml exists")
        return capabilities, risks, controls, {}, {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing components.yaml: {str(e)}")
        return capabilities, risks, controls, {}, {}
    except Exception as e:
        st.error(f"Unexpected error loading components: {str(e)}")
        return capabilities, risks, controls, {}, {}

    try:
        with open(os.path.join(data_dir, 'design.yaml'), 'r') as f:
            design = yaml.safe_load(f)
        if not design:
            st.error("Failed to load design data. Please check data/design.yaml")
            return capabilities, risks, controls, components, {}
    except FileNotFoundError:
        st.error("Design file not found. Please ensure data/design.yaml exists")
        return capabilities, risks, controls, components, {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing design.yaml: {str(e)}")
        return capabilities, risks, controls, components, {}
    except Exception as e:
        st.error(f"Unexpected error loading design: {str(e)}")
        return capabilities, risks, controls, components, {}

    return capabilities, risks, controls, components, design


@st.cache_data
def load_sample_data() -> Dict[str, Any]:
    """Load sample application data with error handling.
    
    Returns:
        Dictionary containing sample application data
    """
    # Get the directory of this file (app/utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to app/
    app_dir = os.path.dirname(current_dir)
    
    try:
        with open(os.path.join(app_dir, 'sample_data.yaml'), 'r') as f:
            sample_data = yaml.safe_load(f)
        if not sample_data or 'sample_application' not in sample_data:
            st.error("Invalid sample data format. Please check sample_data.yaml")
            return {}
        return sample_data['sample_application']
    except FileNotFoundError:
        st.error("Sample data file not found. Please ensure sample_data.yaml exists")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing sample_data.yaml: {str(e)}")
        return {}
    except Exception as e:
        st.error(f"Unexpected error loading sample data: {str(e)}")
        return {}


def get_controls_for_risk(risk_id: str, risks: Dict[str, Any], controls: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get controls for a specific risk with error handling.
    
    Args:
        risk_id: The ID of the risk to get controls for
        risks: Dictionary of risk data
        controls: Dictionary of control data
        
    Returns:
        List of control dictionaries for the specified risk
    """
    risk_controls = []
    
    try:
        if not risks:
            st.warning("No risks data available to find controls")
            return []
        
        if risk_id in risks:
            control_ids = risks[risk_id].get('controls', [])
            for ctrl_id in control_ids:
                if ctrl_id in controls:
                    risk_controls.append({
                        'id': ctrl_id,
                        'name': controls[ctrl_id]['name'],
                        'description': controls[ctrl_id]['description']
                    })
                else:
                    st.warning(f"Control {ctrl_id} not found in controls data")
        else:
            st.warning(f"Risk {risk_id} not found in risks data")
        
        return risk_controls
        
    except Exception as e:
        st.error(f"Unexpected error looking up controls: {str(e)}")
        return []
