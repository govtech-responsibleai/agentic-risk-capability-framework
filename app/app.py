"""Agentic Risk Capability Framework - Streamlit Application"""

import streamlit as st
from dotenv import load_dotenv
import os

# Import our modules
from models.schemas import SessionKeys, RiskAssessment, ScoreAssessment
from utils.data_loader import load_data, load_sample_data, get_controls_for_risk
from utils.llm_utils import get_llm_capability_analysis, get_llm_risk_analysis, get_application_description
from utils.session_utils import initialize_session_state, initialize_control_implementation
# Import will be done inside the function to avoid relative import issues
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agentic Risk Capability Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def application_assessment_page():
    """First page: Application Assessment"""
    st.title("🤖 Agentic Risk Capability Framework")
    st.markdown("### Step 1: Tell us about your application")
    
    # Load all data for LLM analysis
    capabilities, risks, controls, baseline = load_data()
    
    # Check if data loading failed
    if not capabilities or not risks or not controls or not baseline:
        st.error("Failed to load required data files. Please check that all YAML files exist and are valid.")
        st.stop()
    
    # Create two columns for the panels
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Header with Try Sample button
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.subheader("📝 Application Details")
        with header_col2:
            if st.button("📋 Try Sample", help="Auto-fill form with sample application data", key="try_sample_btn"):
                try:
                    sample_data = load_sample_data()
                    if sample_data:
                        # Store sample data directly in widget session state using the keys
                        st.session_state.purpose_text = sample_data.get('description', '')
                        st.session_state.components_text = sample_data.get('components', '')
                        st.session_state.form_data_classification = sample_data.get('data_classification', 'Public/Open')
                        st.session_state.form_public_facing = sample_data.get('public_facing', 'Yes')
                        st.session_state.form_deployment_type = sample_data.get('deployment_type', 'SaaS')
                        st.session_state.form_criticality = sample_data.get('criticality', 'Medium')
                        st.session_state.pii_text = sample_data.get('pii_data', '')
                        st.session_state.human_in_loop_text = sample_data.get('human_in_loop', '')
                        st.rerun()
                    else:
                        st.warning("Sample data not available. Please check sample_data.yaml file.")
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")
        
        # Application information form
        with st.form("application_form"):
            # Form field defaults are initialized in initialize_session_state()
            
            description = st.text_area(
                "What does your application do?",
                placeholder="Describe the main functionality and purpose of your agentic AI application, as well as how a user interacts with it...",
                height=140,
                key="purpose_text"
            )
            
            components = st.text_area(
                "Describe the components of your application",
                placeholder="Describe the technical components, architecture, tools, MCP servers, integrations, and data flows...",
                height=140,
                key="components_text"
            )
            
            data_classification = st.selectbox(
                "What data classification is your application?",
                options=["Public/Open", "Internal", "Confidential", "Restricted"],
                key="form_data_classification"
            )
            
            deployment_type = st.radio(
                "What is your application's deployment type?",
                options=["SaaS", "Custom", "Platform"],
                key="form_deployment_type"
            )
            
            human_in_loop = st.text_area(
                "Is there any human in the loop?",
                placeholder="Describe any human oversight, review, or intervention in your application...",
                height=100,
                key="human_in_loop_text"
            )
            
            public_facing = st.selectbox(
                "Is the application public facing?",
                options=["Yes", "No"],
                key="form_public_facing"
            )
            
            criticality = st.selectbox(
                "How critical is this application to your operations?",
                options=["Low", "Medium", "High", "Critical"],
                key="form_criticality"
            )
            
            pii_data = st.text_area(
                "Is there PII data? If so, how is it used?",
                placeholder="Describe any personally identifiable information collected, processed, or stored...",
                height=100,
                key="pii_text"
            )
            
            submitted = st.form_submit_button("Generate Application Description", type="primary", use_container_width=True, key="generate_desc_btn")
    
    with col2:
        # Header with edit button
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.subheader("📋 Generated Application Description")
        with header_col2:
            # Edit button will be shown here after generation
            pass
        
        if submitted:
            if not description.strip():
                st.error("Please provide a description of your application.")
            else:
                # Store application info in session state
                st.session_state.application_info = {
                    'description': description,
                    'data_classification': data_classification,
                    'deployment_type': deployment_type,
                    'human_in_loop': human_in_loop,
                    'public_facing': public_facing,
                    'criticality': criticality,
                    'pii_data': pii_data,
                    'components': components
                }
                
                # Clear form data after form submission
                for key in [SessionKeys.PURPOSE_TEXT, SessionKeys.COMPONENTS_TEXT, 
                           SessionKeys.FORM_DATA_CLASSIFICATION, SessionKeys.FORM_PUBLIC_FACING,
                           SessionKeys.FORM_DEPLOYMENT_TYPE, SessionKeys.FORM_CRITICALITY,
                           SessionKeys.PII_TEXT, SessionKeys.HUMAN_IN_LOOP_TEXT]:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Generate comprehensive application description
                application_description = get_application_description(st.session_state.application_info)
                st.session_state.application_description = application_description
        
        # Display the generated description
        if 'application_description' in st.session_state:
            # Update edit button in the header
            with header_col2:
                if st.session_state.edit_mode:
                    if st.button("✅ Done", key="edit_toggle_btn"):
                        # Save changes and exit edit mode
                        if 'final_description_display' in st.session_state:
                            st.session_state.application_description = st.session_state.final_description_display
                        st.session_state.edit_mode = False
                        st.rerun()
                else:
                    if st.button("✏️ Edit", key="edit_toggle_btn"):
                        # Enter edit mode
                        st.session_state.edit_mode = True
                        st.rerun()
            
            # Display content based on edit mode
            if st.session_state.edit_mode:
                # Editable text area
                st.text_area(
                    "",
                    value=st.session_state.application_description,
                    height=700,
                    disabled=False,
                    key="final_description_display"
                )
            else:
                # Markdown display
                st.markdown(st.session_state.application_description)
            
            # Button to proceed to capability identification
            if st.button("Continue to Capability Identification", type="primary", use_container_width=True, key="continue_capability_btn"):
                # Use the current description (whether edited or not)
                current_description = st.session_state.application_description
                st.session_state.page = "capability_identification"
                st.rerun()


def capability_identification_page():
    """Second page: Capability Identification"""
    st.title("🤖 Agentic Risk Capability Framework")
    
    # Add back button
    if st.button("← Back to Application Assessment"):
        st.session_state.page = "application_assessment"
        st.rerun()
    
    st.markdown("### Step 2: Identify Applicable Capabilities")
    
    # Load data
    capabilities, risks, controls, baseline = load_data()
    
    # Check if data loading failed
    if not capabilities or not risks or not controls or not baseline:
        st.error("Failed to load required data files. Please check that all YAML files exist and are valid.")
        st.stop()
    
    # Show application summary
    if 'application_info' in st.session_state:
        with st.expander("📋 Application Summary", expanded=False):
            info = st.session_state.application_info
            st.write(f"**Description:** {info['description']}")
            st.write(f"**Data Classification:** {info['data_classification']}")
            st.write(f"**Deployment Type:** {info['deployment_type']}")
            st.write(f"**Public Facing:** {info['public_facing']}")
            st.write(f"**Criticality:** {info['criticality']}")
            st.write(f"**PII Data:** {info['pii_data']}")
            st.write(f"**Human in Loop:** {info['human_in_loop']}")
            st.write(f"**Components:** {info['components']}")
    
    # Initialize capability analysis if not done
    if SessionKeys.CAPABILITY_ANALYSIS not in st.session_state:
        st.info("🔍 Analyzing application to identify applicable capabilities...")
        analysis_result = get_llm_capability_analysis(st.session_state.application_info, capabilities)
        st.session_state[SessionKeys.CAPABILITY_ANALYSIS] = analysis_result
        st.session_state[SessionKeys.SELECTED_CAPABILITIES] = analysis_result.applicable_capabilities.copy()
        st.rerun()
    
    # Show AI reasoning
    if SessionKeys.CAPABILITY_ANALYSIS in st.session_state:
        st.markdown("**Analysis of System Capabilities:**")
        st.info(st.session_state[SessionKeys.CAPABILITY_ANALYSIS].reasoning)
    
    # Capability selection interface
    st.markdown("**📋 Select Applicable Capabilities:**")
    
    # Group capabilities by category
    capability_categories = {}
    for cap_id, cap_data in capabilities.items():
        category = cap_data['category']
        if category not in capability_categories:
            capability_categories[category] = []
        capability_categories[category].append((cap_id, cap_data))
    
    # Display capabilities by category
    for category, caps in capability_categories.items():
        with st.expander(f"**{category}** ({len(caps)} capabilities)", expanded=True):
            for cap_id, cap_data in caps:
                col1, col2, col3 = st.columns([1, 2, 5])
                with col1:
                    is_selected = st.checkbox(
                        "",
                        value=cap_id in st.session_state[SessionKeys.SELECTED_CAPABILITIES],
                        key=f"cap_{cap_id}"
                    )
                with col2:
                    st.write(f"**{cap_id}**: {cap_data['name']}")
                with col3:
                    description = cap_data.get('description', '')
                    if description:
                        st.write(description)
                    else:
                        st.write("*No description available*")
                
                if is_selected:
                    if cap_id not in st.session_state[SessionKeys.SELECTED_CAPABILITIES]:
                        st.session_state[SessionKeys.SELECTED_CAPABILITIES].append(cap_id)
                else:
                    if cap_id in st.session_state[SessionKeys.SELECTED_CAPABILITIES]:
                        st.session_state[SessionKeys.SELECTED_CAPABILITIES].remove(cap_id)
    
    # Baseline risks section
    st.markdown("---")
    st.markdown("**📋 Baseline Risks (Always Included):**")
    
    # Get all baseline risks
    baseline_risks = []
    for risk_id, risk_data in risks.items():
        if risk_data.get('baseline') and not risk_data.get('capabilities'):
            baseline_risks.append((risk_id, risk_data))
    
    if baseline_risks:
        with st.expander(f"**Baseline Risks** ({len(baseline_risks)} risks) - All selected by default", expanded=False):
            for risk_id, risk_data in baseline_risks:
                col1, col2, col3 = st.columns([1, 2, 5])
                with col1:
                    # Baseline risks are always selected
                    st.checkbox(
                        "",
                        value=True,
                        disabled=True,
                        key=f"baseline_{risk_id}"
                    )
                with col2:
                    st.write(f"**{risk_id}**: {risk_data['name']}")
                with col3:
                    description = risk_data.get('description', '')
                    if description:
                        st.write(description)
                    else:
                        st.write("*No description available*")
        
        st.info(f"✅ All {len(baseline_risks)} baseline risks will be included in the risk assessment.")
    
    # Show selected capabilities summary
    if st.session_state[SessionKeys.SELECTED_CAPABILITIES]:
        st.markdown(f"**Selected {len(st.session_state[SessionKeys.SELECTED_CAPABILITIES])} capabilities:**")
        selected_caps_text = ", ".join(st.session_state[SessionKeys.SELECTED_CAPABILITIES])
        st.info(selected_caps_text)
    
    # Continue button
    if st.button("Continue to Risk Assessment", type="primary", use_container_width=True, key="continue_risk_btn"):
        st.session_state.page = "risk_assessment"
        st.rerun()


def risk_assessment_page():
    """Third page: Risk Assessment and Controls"""
    st.title("🤖 Agentic Risk Capability Framework")
    
    # Add back button
    if st.button("← Back to Capability Identification"):
        st.session_state.page = "capability_identification"
        st.rerun()
    
    st.markdown("### Step 3: Risk Assessment & Controls")
    
    # Load data
    capabilities, risks, controls, baseline = load_data()
    
    # Check if data loading failed
    if not capabilities or not risks or not controls or not baseline:
        st.error("Failed to load required data files. Please check that all YAML files exist and are valid.")
        st.stop()
    
    # Determine applicable risks based on selected capabilities
    if SessionKeys.APPLICABLE_RISKS not in st.session_state:
        # Get ALL baseline risks
        baseline_risk_ids = []
        for risk_id, risk_data in risks.items():
            if risk_data.get('baseline') and not risk_data.get('capabilities'):
                baseline_risk_ids.append(risk_id)
        
        # Get ALL capability-specific risks for selected capabilities
        capability_risk_ids = []
        for risk_id, risk_data in risks.items():
            if risk_data.get('capabilities'):
                # Check if any of the risk's capabilities are in the selected capabilities
                risk_capabilities = risk_data.get('capabilities', [])
                if any(cap_id in st.session_state[SessionKeys.SELECTED_CAPABILITIES] for cap_id in risk_capabilities):
                    capability_risk_ids.append(risk_id)
        
        # Combine all applicable risks
        all_applicable_risks = baseline_risk_ids + capability_risk_ids
        st.session_state[SessionKeys.APPLICABLE_RISKS] = all_applicable_risks
        
        
        # Now get LLM contextualization for all these risks
        st.info("🔍 Analyzing risks and generating contextualization... This can take up to a couple of minutes.")
        analysis_result = get_llm_risk_analysis(
            st.session_state.application_info, 
            st.session_state[SessionKeys.SELECTED_CAPABILITIES],
            capabilities, 
            risks, 
            baseline,
            all_applicable_risks
        )
        st.session_state[SessionKeys.RISK_ASSESSMENTS] = analysis_result.risk_assessments
        st.session_state.analysis_reasoning = analysis_result.reasoning
        st.rerun()
    
    # Risk Assessment Interface
    if SessionKeys.APPLICABLE_RISKS in st.session_state and st.session_state[SessionKeys.APPLICABLE_RISKS]:
        # Organize risks by type (baseline vs capability-specific)
        baseline_risks = []
        capability_risks = []
        
        for risk_id in st.session_state[SessionKeys.APPLICABLE_RISKS]:
            if risk_id in risks:
                risk_data = risks[risk_id]
                # Store both risk_id and risk_data as a tuple
                risk_info = (risk_id, risk_data)
                if risk_data.get('baseline') and not risk_data.get('capabilities'):
                    baseline_risks.append(risk_info)
                else:
                    capability_risks.append(risk_info)
        
        # Show AI reasoning
        if 'analysis_reasoning' in st.session_state:
            st.markdown("**Risk Analysis Approach:**")
            st.info(st.session_state.analysis_reasoning)
        
        # Capability-specific risks
        if capability_risks:
            with st.expander(f"### Capability-Specific Risks ({len(capability_risks)} risks)", expanded=True):
                for risk_id, risk_data in capability_risks:
                    risk_category_info = "Unknown"
                    for cap_id in risk_data.get('capabilities', []):
                        if cap_id in capabilities:
                            cap_data = capabilities[cap_id]
                            risk_category_info = f"{cap_data['category']} - {cap_data['name']}"
                            break
                
                    with st.container():
                        st.markdown("---")
                        col_risk, col_likelihood, col_impact = st.columns([1, 1, 1])
                        
                        with col_risk:
                            st.markdown(f"**{risk_data['name']}** ({risk_category_info})")
                            st.caption(risk_data['description'])
                            if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                if hasattr(assessment, 'context'):
                                    st.info(f"💡 {assessment.context}")
                        
                        with col_likelihood:
                            st.markdown("**Likelihood**")
                            if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                likelihood_score = assessment.likelihood.score
                                likelihood_reasoning = assessment.likelihood.reasoning
                                
                                new_likelihood_score = st.selectbox(
                                    "Score",
                                    options=[1, 2, 3, 4, 5],
                                    index=likelihood_score-1,
                                    key=f"likelihood_score_{risk_id}",
                                    format_func=lambda x: f"{['🟢', '🟡', '🟠', '🔴', '🔴'][x-1]} {x} - {['Very Low', 'Low', 'Medium', 'High', 'Very High'][x-1]}"
                                )
                                new_likelihood_reasoning = st.text_area(
                                    "Reasoning",
                                    value=likelihood_reasoning,
                                    height=80,
                                    key=f"likelihood_reasoning_{risk_id}"
                                )
                                
                                # Update session state if changed
                                if new_likelihood_score != likelihood_score or new_likelihood_reasoning != likelihood_reasoning:
                                    if SessionKeys.RISK_ASSESSMENTS not in st.session_state:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS] = {}
                                    if risk_id not in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=assessment.context,
                                            likelihood=ScoreAssessment(score=new_likelihood_score, reasoning=new_likelihood_reasoning),
                                            impact=assessment.impact
                                        )
                                    else:
                                        # Update existing assessment
                                        existing = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=existing.context,
                                            likelihood=ScoreAssessment(score=new_likelihood_score, reasoning=new_likelihood_reasoning),
                                            impact=ScoreAssessment(score=existing.impact.score, reasoning=existing.impact.reasoning)
                                        )
                        
                        with col_impact:
                            st.markdown("**Impact**")
                            if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                impact_score = assessment.impact.score
                                impact_reasoning = assessment.impact.reasoning
                                
                                new_impact_score = st.selectbox(
                                    "Score",
                                    options=[1, 2, 3, 4, 5],
                                    index=impact_score-1,
                                    key=f"impact_score_{risk_id}",
                                    format_func=lambda x: f"{['🟢', '🟡', '🟠', '🔴', '🔴'][x-1]} {x} - {['Very Low', 'Low', 'Medium', 'High', 'Very High'][x-1]}"
                                )
                                new_impact_reasoning = st.text_area(
                                    "Reasoning",
                                    value=impact_reasoning,
                                    height=80,
                                    key=f"impact_reasoning_{risk_id}"
                                )
                                
                                # Update session state if changed
                                if new_impact_score != impact_score or new_impact_reasoning != impact_reasoning:
                                    if SessionKeys.RISK_ASSESSMENTS not in st.session_state:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS] = {}
                                    if risk_id not in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=assessment.context,
                                            likelihood=assessment.likelihood,
                                            impact=ScoreAssessment(score=new_impact_score, reasoning=new_impact_reasoning)
                                        )
                                    else:
                                        # Update existing assessment
                                        existing = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=existing.context,
                                            likelihood=ScoreAssessment(score=existing.likelihood.score, reasoning=existing.likelihood.reasoning),
                                            impact=ScoreAssessment(score=new_impact_score, reasoning=new_impact_reasoning)
                                        )
        
        # Baseline risks
        if baseline_risks:
            with st.expander(f"### Baseline Risks ({len(baseline_risks)} risks)", expanded=True):
                for risk_id, risk_data in baseline_risks:
                    with st.container():
                        st.markdown("---")
                        col_risk, col_likelihood, col_impact = st.columns([1, 1, 1])
                    
                        with col_risk:
                            st.markdown(f"**{risk_data['name']}** (Baseline)")
                            st.caption(risk_data['description'])
                            if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                if hasattr(assessment, 'context'):
                                    st.info(f"💡 {assessment.context}")
                    
                        with col_likelihood:
                            st.markdown("**Likelihood**")
                            if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                likelihood_score = assessment.likelihood.score
                                likelihood_reasoning = assessment.likelihood.reasoning
                                
                                new_likelihood_score = st.selectbox(
                                    "Score",
                                    options=[1, 2, 3, 4, 5],
                                    index=likelihood_score-1,
                                    key=f"likelihood_score_{risk_id}",
                                    format_func=lambda x: f"{['🟢', '🟡', '🟠', '🔴', '🔴'][x-1]} {x} - {['Very Low', 'Low', 'Medium', 'High', 'Very High'][x-1]}"
                                )
                                new_likelihood_reasoning = st.text_area(
                                    "Reasoning",
                                    value=likelihood_reasoning,
                                    height=80,
                                    key=f"likelihood_reasoning_{risk_id}"
                                )
                                
                                # Update session state if changed
                                if new_likelihood_score != likelihood_score or new_likelihood_reasoning != likelihood_reasoning:
                                    if SessionKeys.RISK_ASSESSMENTS not in st.session_state:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS] = {}
                                    if risk_id not in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=assessment.context,
                                            likelihood=ScoreAssessment(score=new_likelihood_score, reasoning=new_likelihood_reasoning),
                                            impact=assessment.impact
                                        )
                                    else:
                                        # Update existing assessment
                                        existing = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=existing.context,
                                            likelihood=ScoreAssessment(score=new_likelihood_score, reasoning=new_likelihood_reasoning),
                                            impact=ScoreAssessment(score=existing.impact.score, reasoning=existing.impact.reasoning)
                                        )
                        
                        with col_impact:
                            st.markdown("**Impact**")
                            if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                impact_score = assessment.impact.score
                                impact_reasoning = assessment.impact.reasoning
                                
                                new_impact_score = st.selectbox(
                                    "Score",
                                    options=[1, 2, 3, 4, 5],
                                    index=impact_score-1,
                                    key=f"impact_score_{risk_id}",
                                    format_func=lambda x: f"{['🟢', '🟡', '🟠', '🔴', '🔴'][x-1]} {x} - {['Very Low', 'Low', 'Medium', 'High', 'Very High'][x-1]}"
                                )
                                new_impact_reasoning = st.text_area(
                                    "Reasoning",
                                    value=impact_reasoning,
                                    height=80,
                                    key=f"impact_reasoning_{risk_id}"
                                )
                                
                                # Update session state if changed
                                if new_impact_score != impact_score or new_impact_reasoning != impact_reasoning:
                                    if SessionKeys.RISK_ASSESSMENTS not in st.session_state:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS] = {}
                                    if risk_id not in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=assessment.context,
                                            likelihood=assessment.likelihood,
                                            impact=ScoreAssessment(score=new_impact_score, reasoning=new_impact_reasoning)
                                        )
                                    else:
                                        # Update existing assessment
                                        existing = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                                        st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id] = RiskAssessment(
                                            context=existing.context,
                                            likelihood=ScoreAssessment(score=existing.likelihood.score, reasoning=existing.likelihood.reasoning),
                                            impact=ScoreAssessment(score=new_impact_score, reasoning=new_impact_reasoning)
                                        )
        
        # Control Thresholds
        st.markdown("---")
        st.markdown("### Control Thresholds")
        col_likelihood, col_impact = st.columns(2)
        
        with col_likelihood:
            likelihood_threshold = st.slider(
                "Minimum Likelihood Score for Controls",
                min_value=1,
                max_value=5,
                value=st.session_state.get('likelihood_threshold', 4),
                help="Risks with likelihood scores at or above this threshold will be considered for controls"
            )
        
        with col_impact:
            impact_threshold = st.slider(
                "Minimum Impact Score for Controls",
                min_value=1,
                max_value=5,
                value=st.session_state.get('impact_threshold', 4),
                help="Risks with impact scores at or above this threshold will be considered for controls"
            )
        
        # Calculate high-priority risks
        high_priority_risks = []
        for risk_id in st.session_state[SessionKeys.APPLICABLE_RISKS]:
            if risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                if (assessment.likelihood.score >= likelihood_threshold and 
                    assessment.impact.score >= impact_threshold):
                    high_priority_risks.append(risk_id)
        
        # Display summary
        st.info(f"**{len(high_priority_risks)} out of {len(st.session_state[SessionKeys.APPLICABLE_RISKS])} risks** meet the threshold criteria and will be analyzed for controls.")
        
        # Store thresholds in session state
        st.session_state.likelihood_threshold = likelihood_threshold
        st.session_state.impact_threshold = impact_threshold
        st.session_state.high_priority_risks = high_priority_risks
        
        # Continue to Controls button
        if st.button("Continue to Controls", type="primary", use_container_width=True, key="continue_to_controls_btn"):
            st.session_state.page = "controls"
            st.rerun()
        

def controls_page():
    """Fourth page: Controls"""
    st.title("🤖 Agentic Risk Capability Framework")
    
    # Header with back button and export button
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        if st.button("← Back to Risk Assessment"):
            st.session_state.page = "risk_assessment"
            st.rerun()
    with header_col2:
        if st.button("📄 Export Assessment", type="secondary"):
            try:
                # Import here to avoid relative import issues
                from utils.export_utils import export_assessment_to_word
                doc = export_assessment_to_word()
                if doc is None:
                    st.error("Failed to create document. Please try again.")
                    return
                
                # Save to bytes
                from io import BytesIO
                doc_buffer = BytesIO()
                doc.save(doc_buffer)
                doc_buffer.seek(0)
                
                # Download button
                st.download_button(
                    label="Download Word Document",
                    data=doc_buffer.getvalue(),
                    file_name=f"risk_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Error generating document: {str(e)}")
                st.error("Please ensure all required data is available and try again.")
    
    st.markdown("### Step 4: Controls & Mitigation")
    
    # Load data
    capabilities, risks, controls, baseline = load_data()
    
    # Check if data loading failed
    if not capabilities or not risks or not controls or not baseline:
        st.error("Failed to load required data files. Please check that all YAML files exist and are valid.")
        st.stop()
    
    # Risk selection interface
    if 'high_priority_risks' in st.session_state and st.session_state.high_priority_risks:
        # Show threshold summary
        st.info(f"Showing controls for **{len(st.session_state.high_priority_risks)} high-priority risks** (Likelihood ≥ {st.session_state.get('likelihood_threshold', 4)} AND Impact ≥ {st.session_state.get('impact_threshold', 4)})")
        
        # Display all high-priority risks in a list
        st.subheader("📋 High-Priority Risks Requiring Controls")
        
        for risk_id in st.session_state.high_priority_risks:
            if risk_id in risks:
                risk_data = risks[risk_id]
                
                # Create expandable section for each risk
                with st.expander(f"**{risk_id}: {risk_data['name']}**", expanded=False):
                    st.write(f"**Description:** {risk_data['description']}")
                    
                    # Show risk assessment if available
                    if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                        assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                        if hasattr(assessment, 'context'):
                            st.info(f"💡 **For your application:** {assessment.context}")
                        
                        # Show current scores
                        col_likelihood, col_impact = st.columns(2)
                        with col_likelihood:
                            likelihood_score = assessment.likelihood.score
                            st.metric("Current Likelihood", f"{likelihood_score}/5")
                        with col_impact:
                            impact_score = assessment.impact.score
                            st.metric("Current Impact", f"{impact_score}/5")
                    
                    # Get and display controls for this risk
                    risk_controls = get_controls_for_risk(risk_id, risks, controls)
                    
                    if risk_controls:
                        st.write(f"**{len(risk_controls)} Control(s) Available:**")
                        for i, control in enumerate(risk_controls, 1):
                            with st.expander(f"Control {i}: {control['name']}"):
                                # Two-column layout: control info on left, implementation on right
                                col_control_info, col_implementation = st.columns([1, 1])
                                
                                with col_control_info:
                                    st.write(f"**{control['id']}**")
                                    st.write(control['description'])
                                
                                with col_implementation:
                                    # Editable text box for control implementation
                                    control_key = f"control_implementation_{risk_id}_{control['id']}"
                                    default_text = "I did not implement this control. I accept all residual risk."
                                    
                                    # Initialize session state for this control if not exists
                                    initialize_control_implementation(risk_id, control['id'], default_text)
                                    
                                    st.write("**Your Implementation Status:**")
                                    implementation_text = st.text_area(
                                        f"Describe how you have implemented this control and remaining residual risks.",
                                        value=st.session_state[control_key],
                                        height=150,
                                        key=f"implementation_text_{risk_id}_{control['id']}",
                                        help="Describe what you have implemented for this control, or leave the default text if not implemented."
                                    )
                                    
                                    # Update session state when text changes
                                    if implementation_text != st.session_state[control_key]:
                                        st.session_state[control_key] = implementation_text
                    else:
                        st.warning("No specific controls found for this risk.")
        
        # Controls selection interface
        st.markdown("---")
        st.subheader("🔍 Browse All Controls")
        
        # Create controls dropdown
        control_options = {}
        for control_id, control_data in controls.items():
            control_options[control_id] = f"{control_id}: {control_data['name']}"
        
        selected_control_id = st.selectbox(
            "Select a control to view its details:",
            options=list(control_options.keys()),
            format_func=lambda x: control_options[x],
            key="control_selector"
        )
        
        if selected_control_id:
            control_data = controls[selected_control_id]
            st.subheader(f"Control Details: {control_data['name']}")
            st.write(f"**Control ID:** {selected_control_id}")
            st.write(f"**Description:** {control_data['description']}")
            
            # Find which risks this control applies to
            applicable_risks = []
            for risk_id, risk_data in risks.items():
                if 'controls' in risk_data and selected_control_id in risk_data['controls']:
                    applicable_risks.append((risk_id, risk_data))
            
            if applicable_risks:
                st.write(f"**This control applies to {len(applicable_risks)} risk(s):**")
                for risk_id, risk_data in applicable_risks:
                    with st.expander(f"Risk: {risk_id} - {risk_data['name']}"):
                        st.write(f"**Description:** {risk_data['description']}")
                        
                        # Show risk assessment if available
                        if SessionKeys.RISK_ASSESSMENTS in st.session_state and risk_id in st.session_state[SessionKeys.RISK_ASSESSMENTS]:
                            assessment = st.session_state[SessionKeys.RISK_ASSESSMENTS][risk_id]
                            if hasattr(assessment, 'context'):
                                st.info(f"💡 **For your application:** {assessment.context}")
                            
                            # Show current scores
                            col_likelihood, col_impact = st.columns(2)
                            with col_likelihood:
                                likelihood_score = assessment.likelihood.score
                                st.metric("Current Likelihood", f"{likelihood_score}/5")
                            with col_impact:
                                impact_score = assessment.impact.score
                                st.metric("Current Impact", f"{impact_score}/5")
            else:
                st.info("This control is not directly associated with any specific risks in the current framework.")
    else:
        if SessionKeys.APPLICABLE_RISKS in st.session_state and st.session_state[SessionKeys.APPLICABLE_RISKS]:
            st.info("No risks meet the current threshold criteria for controls. Adjust the thresholds in the Risk Assessment page to see controls for lower-priority risks.")
        else:
            st.info("Please complete the risk assessment to view controls.")


def main():
    """Main application entry point."""
    
    # Initialize session state
    initialize_session_state()
    
    # Route to appropriate page
    if st.session_state.page == "application_assessment":
        application_assessment_page()
    elif st.session_state.page == "capability_identification":
        capability_identification_page()
    elif st.session_state.page == "risk_assessment":
        risk_assessment_page()
    elif st.session_state.page == "controls":
        controls_page()


if __name__ == "__main__":
    main()