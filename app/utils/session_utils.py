"""Session state management utilities."""

import streamlit as st
from models.schemas import SessionKeys


def initialize_session_state():
    """Initialize all session state variables with default values."""
    # Core application state
    if SessionKeys.PAGE not in st.session_state:
        st.session_state[SessionKeys.PAGE] = "application_assessment"
    
    if SessionKeys.EDIT_MODE not in st.session_state:
        st.session_state[SessionKeys.EDIT_MODE] = False
    
    # Form field defaults
    if SessionKeys.FORM_DATA_CLASSIFICATION not in st.session_state:
        st.session_state[SessionKeys.FORM_DATA_CLASSIFICATION] = 'Public/Open'
    
    if SessionKeys.FORM_PUBLIC_FACING not in st.session_state:
        st.session_state[SessionKeys.FORM_PUBLIC_FACING] = 'Yes'
    
    if SessionKeys.FORM_DEPLOYMENT_TYPE not in st.session_state:
        st.session_state[SessionKeys.FORM_DEPLOYMENT_TYPE] = 'SaaS'
    
    if SessionKeys.FORM_CRITICALITY not in st.session_state:
        st.session_state[SessionKeys.FORM_CRITICALITY] = 'Medium'
    
    # Risk assessment state
    if SessionKeys.RISK_ASSESSMENTS not in st.session_state:
        st.session_state[SessionKeys.RISK_ASSESSMENTS] = {}
    
    if SessionKeys.SELECTED_CAPABILITIES not in st.session_state:
        st.session_state[SessionKeys.SELECTED_CAPABILITIES] = []

    # Repository analysis defaults
    if SessionKeys.REPO_URL not in st.session_state:
        st.session_state[SessionKeys.REPO_URL] = ""
    if SessionKeys.REPO_ANALYSIS not in st.session_state:
        st.session_state[SessionKeys.REPO_ANALYSIS] = ""
    
    # Threshold defaults
    if SessionKeys.LIKELIHOOD_THRESHOLD not in st.session_state:
        st.session_state[SessionKeys.LIKELIHOOD_THRESHOLD] = 4
    
    if SessionKeys.IMPACT_THRESHOLD not in st.session_state:
        st.session_state[SessionKeys.IMPACT_THRESHOLD] = 4


def initialize_control_implementation(risk_id: str, control_id: str, 
                                   default_text: str = "I did not implement this control. I accept all residual risk."):
    """Initialize implementation status for a specific control.
    
    Args:
        risk_id: The ID of the risk
        control_id: The ID of the control
        default_text: Default text for unimplemented controls
    """
    control_key = f"control_implementation_{risk_id}_{control_id}"
    if control_key not in st.session_state:
        st.session_state[control_key] = default_text
