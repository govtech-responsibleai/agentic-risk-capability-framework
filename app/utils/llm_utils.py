"""LLM utility functions for API calls and response handling."""

import streamlit as st
import json
from typing import Dict, List, Any
from litellm import completion
from models.schemas import CapabilityAnalysis, RiskAnalysis


def get_llm_capability_analysis(application_info: Dict[str, Any], capabilities: Dict[str, Any]) -> CapabilityAnalysis:
    """Use LiteLLM to identify applicable capabilities for the application.
    
    Args:
        application_info: Dictionary containing application details
        capabilities: Dictionary of available capabilities
        
    Returns:
        CapabilityAnalysis object with applicable capabilities and reasoning
    """
    # Prepare capabilities list for the prompt
    capabilities_text = ""
    for cap_id, cap_data in capabilities.items():
        capabilities_text += f"- {cap_id}: {cap_data['name']} ({cap_data['category']})\n"
    
    prompt = f"""
You are an expert in AI system analysis. Based on the following application information, identify which capabilities from the provided list are applicable to this application.

Application Information:
- What does your application do? {application_info.get('description', 'Not provided')}
- Data classification: {application_info.get('data_classification', 'Not provided')}
- Deployment type: {application_info.get('deployment_type', 'Not provided')}
- Human in the loop: {application_info.get('human_in_loop', 'Not provided')}
- Public facing: {application_info.get('public_facing', 'Not provided')}
- Criticality: {application_info.get('criticality', 'Not provided')}
- PII data: {application_info.get('pii_data', 'Not provided')}
- Components: {application_info.get('components', 'Not provided')}

Available Capabilities:
{capabilities_text}

Please analyze the application and return your response as a JSON object with the following structure:
{{
    "applicable_capabilities": ["CAP-001", "CAP-002", ...],
    "reasoning": "Brief explanation of why these capabilities were selected"
}}

Only include capabilities that are clearly relevant to this application. Be conservative - it's better to miss a capability than to include irrelevant ones.
"""

    try:
        # Show progress indicator
        message_placeholder = st.empty()
        
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        message_placeholder.empty()
        result = json.loads(response.choices[0].message.content)
        capability_analysis = CapabilityAnalysis(**result)
        return capability_analysis
    except Exception as e:
        st.error(f"Error calling LLM: {str(e)}")
        return CapabilityAnalysis(applicable_capabilities=[], reasoning="Error occurred during analysis")


def get_llm_risk_analysis(application_info: Dict[str, Any], selected_capabilities: List[str], 
                         capabilities: Dict[str, Any], risks: Dict[str, Any], 
                         baseline: Dict[str, Any], applicable_risk_ids: List[str] = None) -> RiskAnalysis:
    """Use LiteLLM to provide contextualized explanations for specified risks.
    
    Args:
        application_info: Dictionary containing application details
        selected_capabilities: List of selected capability IDs
        capabilities: Dictionary of available capabilities
        risks: Dictionary of available risks
        baseline: Dictionary of baseline categories
        applicable_risk_ids: List of risk IDs to assess (if None, will determine from capabilities)
        
    Returns:
        RiskAnalysis object with risk assessments
    """
    # If no risk IDs provided, determine them (fallback to old behavior)
    if applicable_risk_ids is None:
        # Get ALL baseline risks
        baseline_risk_ids = []
        for risk_id, risk_data in risks.items():
            if risk_data.get('baseline') and not risk_data.get('capabilities'):
                baseline_risk_ids.append(risk_id)
        
        # Get ALL capability-specific risks for selected capabilities
        capability_risk_ids = []
        for risk_id, risk_data in risks.items():
            if risk_data.get('capabilities'):
                risk_capabilities = risk_data.get('capabilities', [])
                if any(cap_id in selected_capabilities for cap_id in risk_capabilities):
                    capability_risk_ids.append(risk_id)
        
        applicable_risk_ids = baseline_risk_ids + capability_risk_ids
    
    # Prepare capabilities text
    capabilities_text = ""
    for cap_id in selected_capabilities:
        if cap_id in capabilities:
            cap_data = capabilities[cap_id]
            capabilities_text += f"- {cap_id}: {cap_data['name']} ({cap_data['category']})\n"
    
    # Prepare risks text for the specific risks we want to assess
    risks_text = ""
    for risk_id in applicable_risk_ids:
        if risk_id in risks:
            risk_data = risks[risk_id]
            risks_text += f"- {risk_id}: {risk_data['name']}\n"
            risks_text += f"  Description: {risk_data['description']}\n"
            if risk_data.get('capabilities'):
                risks_text += f"  Capabilities: {', '.join(risk_data['capabilities'])}\n"
            if risk_data.get('baseline'):
                risks_text += f"  Baseline: {', '.join(risk_data['baseline'])}\n"
            risks_text += "\n"
    
    prompt = f"""
You are an expert in agentic AI risk assessment. Based on the following application information and selected capabilities, assess the risks and provide detailed likelihood and impact scores.

Application Information:
- What does your application do? {application_info.get('description', 'Not provided')}
- Data classification: {application_info.get('data_classification', 'Not provided')}
- Deployment type: {application_info.get('deployment_type', 'Not provided')}
- Human in the loop: {application_info.get('human_in_loop', 'Not provided')}
- Public facing: {application_info.get('public_facing', 'Not provided')}
- Criticality: {application_info.get('criticality', 'Not provided')}
- PII data: {application_info.get('pii_data', 'Not provided')}
- Components: {application_info.get('components', 'Not provided')}

Selected Capabilities:
{capabilities_text}

Risks to Assess:
{risks_text}

For each risk listed above, provide:
1. A 1-2 line explanation of how this risk materializes for this specific application
2. A likelihood score (1-5) with reasoning
3. An impact score (1-5) with reasoning

IMPORTANT: You must assess ALL risks listed above - both capability-specific and baseline risks. Include every single risk in your response.

Return your response as a JSON object with the following structure:
{{
    "applicable_risks": ["RISK-001", "RISK-002", ...],
    "risk_assessments": {{
        "RISK-001": {{
            "context": "1-2 line explanation of how this risk materializes for this specific application",
            "likelihood": {{
                "score": 3,
                "reasoning": "Brief explanation of why this likelihood score was assigned"
            }},
            "impact": {{
                "score": 4,
                "reasoning": "Brief explanation of why this impact score was assigned"
            }}
        }},
        "RISK-002": {{
            "context": "1-2 line explanation of how this risk materializes for this specific application",
            "likelihood": {{
                "score": 2,
                "reasoning": "Brief explanation of why this likelihood score was assigned"
            }},
            "impact": {{
                "score": 3,
                "reasoning": "Brief explanation of why this impact score was assigned"
            }}
        }}
    }},
    "reasoning": "1-2 lines explaining the overall risk assessment approach and key considerations"
}}
"""

    try:
        # Show progress indicator
        message_placeholder = st.empty()
        
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Clear progress message
        message_placeholder.empty()
        
        # Parse with Pydantic model
        result = json.loads(response.choices[0].message.content)
        
        
        # Ensure we return the correct risk IDs (use the ones we determined, not what LLM returned)
        result['applicable_risks'] = applicable_risk_ids
        
        # Validate that we have risk assessments for all applicable risks
        if 'risk_assessments' not in result:
            st.warning("LLM response missing 'risk_assessments' field")
            result['risk_assessments'] = {}
        
        # Check if any risks are missing from the LLM response
        missing_risks = []
        for risk_id in applicable_risk_ids:
            if risk_id not in result['risk_assessments']:
                missing_risks.append(risk_id)
        
        if missing_risks:
            st.warning(f"LLM did not provide assessments for {len(missing_risks)} risks: {missing_risks}")
            # Create default assessments for missing risks
            for risk_id in missing_risks:
                result['risk_assessments'][risk_id] = {
                    "context": "Risk assessment not provided by LLM",
                    "likelihood": {"score": 3, "reasoning": "Default assessment - please review manually"},
                    "impact": {"score": 3, "reasoning": "Default assessment - please review manually"}
                }
        
        # Validate and fix score types (ensure they're integers)
        for risk_id, assessment in result['risk_assessments'].items():
            if isinstance(assessment, dict):
                # Fix likelihood score
                if 'likelihood' in assessment and isinstance(assessment['likelihood'], dict):
                    if 'score' in assessment['likelihood']:
                        try:
                            assessment['likelihood']['score'] = int(assessment['likelihood']['score'])
                        except (ValueError, TypeError):
                            st.warning(f"Invalid likelihood score for {risk_id}, using default")
                            assessment['likelihood']['score'] = 3
                
                # Fix impact score
                if 'impact' in assessment and isinstance(assessment['impact'], dict):
                    if 'score' in assessment['impact']:
                        try:
                            assessment['impact']['score'] = int(assessment['impact']['score'])
                        except (ValueError, TypeError):
                            st.warning(f"Invalid impact score for {risk_id}, using default")
                            assessment['impact']['score'] = 3
        
        # Ensure reasoning field exists
        if 'reasoning' not in result:
            result['reasoning'] = "Risk assessment completed with some default values"
        
        try:
            risk_analysis = RiskAnalysis(**result)
            return risk_analysis
        except Exception as validation_error:
            st.error(f"Pydantic validation error: {str(validation_error)}")
            # Return a minimal valid response
            return RiskAnalysis(
                applicable_risks=applicable_risk_ids,
                risk_assessments={},
                reasoning="Error in validation - please try again"
            )
    
    except Exception as e:
        st.error(f"Error calling LLM: {str(e)}")
        return RiskAnalysis(applicable_risks=applicable_risk_ids or [], risk_assessments={}, reasoning="Error occurred during analysis")


def get_application_description(application_info: Dict[str, Any]) -> str:
    """Use LiteLLM to generate a comprehensive application description.
    
    Args:
        application_info: Dictionary containing application details
        
    Returns:
        Generated application description string
    """
    prompt = f"""
You are an expert in system architecture and application analysis. Based on the following application information, provide a comprehensive description that will be used for risk assessment.

Application Information:
- What does your application do? {application_info.get('description', 'Not provided')}
- Data classification: {application_info.get('data_classification', 'Not provided')}
- Deployment type: {application_info.get('deployment_type', 'Not provided')}
- Human in the loop: {application_info.get('human_in_loop', 'Not provided')}
- Public facing: {application_info.get('public_facing', 'Not provided')}
- Criticality: {application_info.get('criticality', 'Not provided')}
- PII data: {application_info.get('pii_data', 'Not provided')}
- Components: {application_info.get('components', 'Not provided')}

Please provide a comprehensive description that includes:

1. **System Components**: Describe the high-level architecture including:
   - Frontend components (web interface, mobile app, API endpoints, etc.)
   - Backend services and their roles
   - Databases and data storage systems
   - External tools, MCP servers, or third-party integrations
   - AI/LLM components and their integration points

2. **User Flow**: Describe the complete user journey including:
   - How users interact with the system
   - What actions they can perform
   - How the AI/agent responds to user inputs
   - Any multi-step processes or workflows

3. **Additional Context**: Include any other relevant information such as:
   - Data flow and processing
   - Integration points with other systems

Provide a detailed, technical description that would help a risk assessor understand the complete system architecture and operation. Do not need to include a title.
"""

    try:
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        # Stream the response
        full_response = ""
        message_placeholder = st.empty()
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(f"{full_response}")
        
        # Clear the streaming message
        message_placeholder.empty()
        
        return full_response
    except Exception as e:
        st.error(f"Error generating application description: {str(e)}")
        return "Error occurred while generating description."
