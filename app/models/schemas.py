"""Pydantic models for structured LLM outputs and session state management."""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Union


class ScoreAssessment(BaseModel):
    """Model for likelihood and impact score assessments."""
    score: int = Field(ge=1, le=5, description="Score from 1 (Very Low) to 5 (Very High)")
    reasoning: str = Field(description="Explanation for the score assignment")
    
    @validator('score', pre=True)
    def convert_score_to_int(cls, v):
        """Convert score to int if it's a string or float."""
        if isinstance(v, str):
            try:
                return int(float(v))
            except (ValueError, TypeError):
                return 3  # Default to medium score
        elif isinstance(v, float):
            return int(v)
        return v
    
    @validator('reasoning', pre=True)
    def ensure_reasoning_is_string(cls, v):
        """Ensure reasoning is a string."""
        if v is None:
            return "No reasoning provided"
        return str(v)


class RiskAssessment(BaseModel):
    """Model for individual risk assessments."""
    context: str = Field(description="1-2 line explanation of how this risk materializes for this specific application")
    likelihood: ScoreAssessment = Field(description="Likelihood assessment")
    impact: ScoreAssessment = Field(description="Impact assessment")
    
    @validator('context', pre=True)
    def ensure_context_is_string(cls, v):
        """Ensure context is a string."""
        if v is None:
            return "No context provided"
        return str(v)


class CapabilityAnalysis(BaseModel):
    """Model for capability analysis results."""
    applicable_capabilities: List[str] = Field(description="List of applicable capability IDs")
    reasoning: str = Field(description="Brief explanation of why these capabilities were selected")


class RiskAnalysis(BaseModel):
    """Model for risk analysis results."""
    applicable_risks: List[str] = Field(description="List of applicable risk IDs")
    risk_assessments: Dict[str, RiskAssessment] = Field(description="Risk assessments for each applicable risk")
    reasoning: str = Field(description="Overall risk assessment approach and key considerations")


class SessionKeys:
    """Constants for session state keys to prevent typos and ensure consistency."""
    PAGE = "page"
    EDIT_MODE = "edit_mode"
    APPLICATION_INFO = "application_info"
    APPLICATION_DESCRIPTION = "application_description"
    CAPABILITY_ANALYSIS = "capability_analysis"
    SELECTED_CAPABILITIES = "selected_capabilities"
    APPLICABLE_RISKS = "applicable_risks"
    RISK_ASSESSMENTS = "risk_assessments"
    LIKELIHOOD_THRESHOLD = "likelihood_threshold"
    IMPACT_THRESHOLD = "impact_threshold"
    HIGH_PRIORITY_RISKS = "high_priority_risks"
    
    # Form field keys
    FORM_DATA_CLASSIFICATION = "form_data_classification"
    FORM_PUBLIC_FACING = "form_public_facing"
    FORM_CRITICALITY = "form_criticality"
    
    # Text area keys
    PURPOSE_TEXT = "purpose_text"
    COMPONENTS_TEXT = "components_text"
    PII_TEXT = "pii_text"
    HUMAN_IN_LOOP_TEXT = "human_in_loop_text"
    FINAL_DESCRIPTION_DISPLAY = "final_description_display"
    REPO_URL = "repo_url"
    REPO_ANALYSIS = "repo_analysis"
