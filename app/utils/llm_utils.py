"""LLM utility functions for API calls and response handling."""

import streamlit as st
import json
import re
import requests
from typing import Dict, List, Any, Tuple
from litellm import completion
from models.schemas import CapabilityAnalysis, CapabilityEvaluation, RiskAnalysis, SessionKeys


def get_llm_capability_analysis(application_info: Dict[str, Any], capabilities: Dict[str, Any]) -> CapabilityAnalysis:
    """Use LiteLLM to identify applicable capabilities for the application.
    
    Args:
        application_info: Dictionary containing application details
        capabilities: Dictionary of available capabilities
        
    Returns:
        CapabilityAnalysis object with applicable capabilities and reasoning
    """
    # Prepare capabilities list for the prompt with detailed information
    capabilities_text = ""
    capability_ids = []
    for cap_id, cap_data in capabilities.items():
        capability_ids.append(cap_id)
        capabilities_text += f"\n{cap_id}:\n"
        capabilities_text += f"  Name: {cap_data['name']}\n"
        capabilities_text += f"  Category: {cap_data['category']}\n"
        if 'description' in cap_data:
            capabilities_text += f"  Description: {cap_data['description']}\n"

    prompt = f"""You are an expert in AI system analysis. You must systematically evaluate EACH capability listed below to determine if it applies to this application.

Application Information:
- What does your application do? {application_info.get('description', 'Not provided')}
- Data classification: {application_info.get('data_classification', 'Not provided')}
- Human in the loop: {application_info.get('human_in_loop', 'Not provided')}
- Public facing: {application_info.get('public_facing', 'Not provided')}
- Criticality: {application_info.get('criticality', 'Not provided')}
- PII data: {application_info.get('pii_data', 'Not provided')}
- Components: {application_info.get('components', 'Not provided')}

INSTRUCTIONS:
1. Go through EACH of the {len(capability_ids)} capabilities listed below ONE BY ONE
2. For EACH capability, decide: Does this capability apply to this specific application?
3. For EACH capability, provide reasoning for your decision

Capabilities to Evaluate ({len(capability_ids)} total):
{capabilities_text}

CRITICAL: You MUST evaluate ALL {len(capability_ids)} capabilities listed above. Do not skip any.

Return your response as a JSON object with this EXACT structure:
{{
    "evaluations": [
        {{
            "capability_id": "CAP-XXX",
            "applies": true,
            "reasoning": "This capability applies because..."
        }},
        {{
            "capability_id": "CAP-YYY",
            "applies": false,
            "reasoning": "This does not apply because..."
        }}
    ]
}}

The "evaluations" array must contain exactly {len(capability_ids)} objects, one for each capability.
"""

    try:
        # Show progress indicator
        message_placeholder = st.empty()

        response = completion(
            model="gpt-4o",  # Use more capable model for systematic evaluation
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0  # Deterministic for consistency
        )

        message_placeholder.empty()
        result = json.loads(response.choices[0].message.content)

        # Parse evaluations
        evaluations = result.get('evaluations', [])

        # Extract applicable capabilities
        applicable_capabilities = []
        evaluation_details = []

        for eval_data in evaluations:
            try:
                evaluation = CapabilityEvaluation(**eval_data)
                evaluation_details.append(evaluation)
                if evaluation.applies:
                    applicable_capabilities.append(evaluation.capability_id)
            except Exception as e:
                st.warning(f"Could not parse evaluation: {eval_data}. Error: {str(e)}")
                continue

        # Generate overall reasoning
        reasoning = f"Evaluated {len(evaluations)} capabilities. {len(applicable_capabilities)} found to be applicable based on the application's characteristics."

        return CapabilityAnalysis(
            applicable_capabilities=applicable_capabilities,
            reasoning=reasoning
        )
    except Exception as e:
        st.error(f"Error calling LLM: {str(e)}")
        return CapabilityAnalysis(applicable_capabilities=[], reasoning="Error occurred during analysis")


def get_llm_risk_analysis(application_info: Dict[str, Any], selected_capabilities: List[str],
                         capabilities: Dict[str, Any], risks: Dict[str, Any],
                         components: Dict[str, Any], design: Dict[str, Any],
                         applicable_risk_ids: List[str] = None) -> RiskAnalysis:
    """Use LiteLLM to provide contextualized explanations for specified risks.

    Args:
        application_info: Dictionary containing application details
        selected_capabilities: List of selected capability IDs
        capabilities: Dictionary of available capabilities
        risks: Dictionary of available risks
        components: Dictionary of component categories
        design: Dictionary of design categories
        applicable_risk_ids: List of risk IDs to assess (if None, will determine from capabilities)

    Returns:
        RiskAnalysis object with risk assessments
    """
    # If no risk IDs provided, determine them (fallback to old behavior)
    if applicable_risk_ids is None:
        # Get ALL component and design risks
        component_design_risk_ids = []
        for risk_id, risk_data in risks.items():
            # Risks with 'components' or 'design' fields (but not 'capabilities')
            if (risk_data.get('components') or risk_data.get('design')) and not risk_data.get('capabilities'):
                component_design_risk_ids.append(risk_id)

        # Get ALL capability-specific risks for selected capabilities
        capability_risk_ids = []
        for risk_id, risk_data in risks.items():
            if risk_data.get('capabilities'):
                risk_capabilities = risk_data.get('capabilities', [])
                if any(cap_id in selected_capabilities for cap_id in risk_capabilities):
                    capability_risk_ids.append(risk_id)

        applicable_risk_ids = component_design_risk_ids + capability_risk_ids
    
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
            if risk_data.get('components'):
                risks_text += f"  Components: {', '.join(risk_data['components'])}\n"
            if risk_data.get('design'):
                risks_text += f"  Design: {', '.join(risk_data['design'])}\n"
            risks_text += "\n"
    
    prompt = f"""You are an expert in agentic AI risk assessment. Based on the following application information and selected capabilities, assess the risks and provide detailed likelihood and impact scores.

Application Information:
- What does your application do? {application_info.get('description', 'Not provided')}
- Data classification: {application_info.get('data_classification', 'Not provided')}
- Human in the loop: {application_info.get('human_in_loop', 'Not provided')}
- Public facing: {application_info.get('public_facing', 'Not provided')}
- Criticality: {application_info.get('criticality', 'Not provided')}
- PII data: {application_info.get('pii_data', 'Not provided')}
- Components: {application_info.get('components', 'Not provided')}

Selected Capabilities:
{capabilities_text}

Risks to Assess (you MUST assess ALL {len(applicable_risk_ids)} risks):
{risks_text}

CRITICAL INSTRUCTIONS:
1. You MUST assess ALL {len(applicable_risk_ids)} risks listed above. Do not skip any.
2. For each risk, provide specific context referencing the application details. Where possible, reference the specific component of the application that is at risk, and how the risk materializes into specific failure modes and hazards.
3. Scores MUST be integers between 1 and 5 (inclusive).
4. All text fields (context, reasoning) MUST be non-empty strings.

Return ONLY a valid JSON object with this EXACT structure (no additional text):
{{
    "applicable_risks": {json.dumps(applicable_risk_ids)},
    "risk_assessments": {{
        "RISK-001": {{
            "context": "string: 1-2 sentences explaining how this specific risk applies to this application",
            "likelihood": {{
                "score": 3,
                "reasoning": "string: Brief explanation of this likelihood score"
            }},
            "impact": {{
                "score": 4,
                "reasoning": "string: Brief explanation of this impact score"
            }}
        }}
    }},
    "reasoning": "string: 1-2 sentences explaining overall approach"
}}

Remember:
- All scores must be integers 1-5
- All text fields must be non-empty strings
- Include ALL {len(applicable_risk_ids)} risks in risk_assessments
"""

    try:
        # Show progress indicator
        message_placeholder = st.empty()

        response = completion(
            model="gpt-5",  # Use more capable model for better structured output reliability
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
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
        
        # Validate and fix nested structures
        for risk_id, assessment in result['risk_assessments'].items():
            if not isinstance(assessment, dict):
                st.warning(f"Invalid assessment structure for {risk_id}, creating default")
                result['risk_assessments'][risk_id] = {
                    "context": "Invalid assessment structure - please review manually",
                    "likelihood": {"score": 3, "reasoning": "Default assessment"},
                    "impact": {"score": 3, "reasoning": "Default assessment"}
                }
                continue

            # Ensure context exists and is a string
            if 'context' not in assessment or not assessment.get('context'):
                assessment['context'] = "Context missing - please review manually"
            elif not isinstance(assessment['context'], str):
                assessment['context'] = str(assessment['context'])

            # Validate likelihood structure
            if 'likelihood' not in assessment or not isinstance(assessment['likelihood'], dict):
                assessment['likelihood'] = {"score": 3, "reasoning": "Default assessment"}
            else:
                # Validate score
                if 'score' not in assessment['likelihood']:
                    assessment['likelihood']['score'] = 3
                else:
                    try:
                        score = int(assessment['likelihood']['score'])
                        # Clamp score between 1 and 5
                        assessment['likelihood']['score'] = max(1, min(5, score))
                    except (ValueError, TypeError):
                        st.warning(f"Invalid likelihood score for {risk_id}, using default")
                        assessment['likelihood']['score'] = 3

                # Validate reasoning
                if 'reasoning' not in assessment['likelihood'] or not assessment['likelihood'].get('reasoning'):
                    assessment['likelihood']['reasoning'] = "Reasoning not provided"
                elif not isinstance(assessment['likelihood']['reasoning'], str):
                    assessment['likelihood']['reasoning'] = str(assessment['likelihood']['reasoning'])

            # Validate impact structure
            if 'impact' not in assessment or not isinstance(assessment['impact'], dict):
                assessment['impact'] = {"score": 3, "reasoning": "Default assessment"}
            else:
                # Validate score
                if 'score' not in assessment['impact']:
                    assessment['impact']['score'] = 3
                else:
                    try:
                        score = int(assessment['impact']['score'])
                        # Clamp score between 1 and 5
                        assessment['impact']['score'] = max(1, min(5, score))
                    except (ValueError, TypeError):
                        st.warning(f"Invalid impact score for {risk_id}, using default")
                        assessment['impact']['score'] = 3

                # Validate reasoning
                if 'reasoning' not in assessment['impact'] or not assessment['impact'].get('reasoning'):
                    assessment['impact']['reasoning'] = "Reasoning not provided"
                elif not isinstance(assessment['impact']['reasoning'], str):
                    assessment['impact']['reasoning'] = str(assessment['impact']['reasoning'])
        
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


def _parse_github_repo(repo_url: str) -> Tuple[str, str]:
    """Extract owner and repository name from a GitHub URL."""
    pattern = r"github\.com[:/](?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)(?:\.git)?/?"
    match = re.search(pattern, repo_url)
    if not match:
        raise ValueError("Please provide a valid GitHub repository URL")
    owner = match.group("owner")
    repo = match.group("repo")
    return owner, repo


def _fetch_repo_snapshot(repo_url: str, max_files: int = 15, max_bytes_per_file: int = 3500, max_total_chars: int = 18000) -> Tuple[List[Dict[str, str]], str]:
    """Fetch a lightweight snapshot of a public GitHub repo for LLM analysis."""
    owner, repo = _parse_github_repo(repo_url)
    meta_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}", timeout=10)
    meta_resp.raise_for_status()
    default_branch = meta_resp.json().get("default_branch", "main")

    tree_resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1",
        timeout=10,
    )
    tree_resp.raise_for_status()
    tree = tree_resp.json().get("tree", [])

    # Prioritize security-relevant files
    priority_paths = [
        "README", "README.md", "SECURITY", "SECURITY.md", "docs/", "config", "infra", "deploy", "helm", "k8s", "docker", "compose",
        "api/", "apps/", "services/", "server/", "agents/", "tools/", "prompts/", "memory/", "vector/", "db/"
    ]
    # Anything that handles ingress/egress of data or requests is a threat vector
    data_io_keywords = [
        "api/", "apis/", "routes", "router", "controller", "handler", "webhook", "callback",
        "client", "http", "https", "fetch", "axios", "request", "response", "grpc", "rpc",
        "socket", "websocket", "ws/", "queue", "kafka", "sns", "sqs", "pubsub", "mq", "worker",
        "ingest", "upload", "download", "import", "export", "data/", "dataset", "csv", "parquet",
        "sql", "mongo", "db/", "database", "redis", "cache", "vector", "pinecone", "weaviate", "milvus", "chroma", "opensearch", "elastic", "s3", "gcs", "azureblob", "minio",
        "prompt", "prompts", "chat", "message", "llm", "model", "openai", "anthropic", "vertex", "bedrock", "mcp", "tool"
    ]
    preferred_exts = (".py", ".ts", ".tsx", ".js", ".go", ".rs", ".java", ".cs", ".rb", ".yaml", ".yml", ".json", ".env", "Dockerfile", ".http", ".sql", ".sh", ".md")

    def _score_path(path: str) -> int:
        score = 0
        for p in priority_paths:
            if path.startswith(p):
                score += 3
        for kw in data_io_keywords:
            if kw in path:
                score += 3
        for ext in preferred_exts:
            if path.endswith(ext):
                score += 2
        if "/tests" in path or path.startswith("tests/"):
            score -= 2
        return score

    blobs = [entry for entry in tree if entry.get("type") == "blob"]
    blobs.sort(key=lambda x: _score_path(x.get("path", "")), reverse=True)

    selected_files = []
    total_chars = 0

    for blob in blobs:
        if len(selected_files) >= max_files or total_chars >= max_total_chars:
            break

        path = blob.get("path", "")
        size = blob.get("size", 0)
        if size and size > max_bytes_per_file * 2:
            continue  # avoid very large files

        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/{path}"
        try:
            raw_resp = requests.get(raw_url, timeout=10)
            raw_resp.raise_for_status()
            content = raw_resp.text[:max_bytes_per_file]
        except Exception:
            continue

        selected_files.append({"path": path, "content": content})
        total_chars += len(content)

    if not selected_files:
        raise RuntimeError("Could not fetch any files from the repository. Ensure it is public and reachable.")

    return selected_files, default_branch


def analyze_public_repo(repo_url: str, stream_target=None, status_placeholder=None) -> Tuple[str, List[Dict[str, str]]]:
    """Pull a code snapshot from a public GitHub repo and summarize key application components.

    If stream_target is provided, stream partial text into that placeholder as the LLM responds.
    If status_placeholder is provided, it will be cleared once streaming starts.
    """
    try:
        files, branch = _fetch_repo_snapshot(repo_url)
    except Exception as fetch_error:
        if status_placeholder:
            status_placeholder.empty()
        st.error(f"Repository fetch failed: {fetch_error}")
        return "", []

    # Build compact context for the LLM
    file_blurbs = "".join([f"\n### {f['path']}\n{f['content']}\n" for f in files])

    prompt = f"""
You are a coding-focused architect. Given selected files from a public repository, produce a concise natural-language summary of the application so the user can drop it directly into their system description.

Repository: {repo_url} (branch: {branch})
Files (truncated):
{file_blurbs}

Provide a concise report (<=200 words) with these sections:
- Application Summary: 2 sentences on the purpose and main stack.
- Architecture & Components: 4-7 bullets covering services, agents, tools/connectors, MCP servers, data stores, model/LLM usage, runtime surfaces (APIs, queues, schedulers), and deployment artifacts.
- Data Flow & Config: 3-5 bullets on where data enters/exits, storage layers, notable config/secrets patterns, and observability/logging if present.

Be specific to the observed files. If something is not evident, state the assumption explicitly.
"""

    try:
        response = completion(
            model="gpt-5.1-codex",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        summary = ""
        placeholder = stream_target or st.empty()
        first_chunk = True
        for chunk in response:
            if chunk.choices[0].delta.content:
                # Clear status message on first chunk (when streaming starts)
                if first_chunk and status_placeholder:
                    status_placeholder.empty()
                    first_chunk = False
                summary += chunk.choices[0].delta.content
                placeholder.markdown(summary)
        return summary, files
    except Exception as e:
        if status_placeholder:
            status_placeholder.empty()
        st.error(f"Error analyzing repository with LLM: {e}")
        return "", []


def get_application_description(application_info: Dict[str, Any]) -> str:
    """Use LiteLLM to generate a comprehensive application description.
    
    Args:
        application_info: Dictionary containing application details
        
    Returns:
        Generated application description string
    """
    prompt = f"""
You are an expert in system architecture and application analysis. Based on the following application information, provide a concise description that will be used for risk assessment.

Application Information:
- What does your application do? {application_info.get('description', 'Not provided')}
- Data classification: {application_info.get('data_classification', 'Not provided')}
- Human in the loop: {application_info.get('human_in_loop', 'Not provided')}
- Public facing: {application_info.get('public_facing', 'Not provided')}
- Criticality: {application_info.get('criticality', 'Not provided')}
- PII data: {application_info.get('pii_data', 'Not provided')}
- Components: {application_info.get('components', 'Not provided')}
- Repo URL: {application_info.get('repo_url', 'Not provided')}
- Repo codebase summary: {application_info.get('repo_analysis', 'Not provided')}

Write a crisp description (target 120-150 words) with three parts:
1) Overview (2-3 sentences): what the system does, sensitivity level, public-facing status, criticality.
2) Architecture (3-5 short bullets): key frontend/backends, data stores, AI/LLM usage, integrations/tools/MCP servers, where PII flows if any.
3) User flow (3-5 short bullets): how users interact, key steps, human-in-loop points.

Keep language tight and avoid repetition. Do not add a title or headings in the output—just the paragraphs/bullets.
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
