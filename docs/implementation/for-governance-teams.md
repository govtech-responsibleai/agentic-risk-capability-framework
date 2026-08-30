# For Governance Teams

!!! abstract "Page Summary"

    This page guides organisational-level adoption and contextualisation of the ARC Framework through a six-phase methodology. Governance teams adapt the baseline framework to their organisation's context (jurisdiction, industry, technical stack, risk appetite) over 6-12 months, producing an organisation-specific capability taxonomy, risk register, adapted controls, and implementation toolkit.

This guide is for governance teams responsible for adopting the ARC framework across the organisation. Your goal is to contextualise the baseline framework to your organisation's specific needs, creating a standardised approach that all developers will use when building agentic AI systems.

**What you'll accomplish:**

- Adapt capability taxonomy for your domain
- Contextualise risk mappings to your jurisdiction and industry
- Map controls to your technical infrastructure
- Define risk relevance criteria matching your risk appetite
- Pilot with real systems and gather feedback
- Roll out organisation-wide with training and templates

---

## Customisation Steps

In this section, we explain the steps that governance teams need to take to contextualise the ARC framework for your organisation.

### Step 1: Customise the Capability Taxonomy

The [baseline capability taxonomy](../arc_framework/elements.md#capabilities) is a good start, but domain-specific capabilities may be needed. For example, healthcare organisations may need to distinguish "patient-facing communication" from "clinical decision support" due to regulatory differences, while manufacturing companies may need capabilities for "physical equipment control" or "sensor data processing."

**Review the baseline taxonomy, identify organisation-relevant capabilities, and consider adding domain-specific subcategories.** Retain all existing capabilities even if unlikely to be used — this preserves applicability across organisational verticals.

!!! tip "When to Customise the Capability Taxonomy"
    Consider adding domain-specific subcategories when:

    - **High Regulatory Scrutiny:** Healthcare needs to distinguish patient interactions from clinical decisions due to FDA/HSA regulations
    - **Fine-Grained Risk Profiles:** Finance needs to separate stock trading from bond trading from currency exchange
    - **Industry-Specific Operations:** Manufacturing needs capabilities for equipment control, sensor processing, supply chain coordination

    You should **keep the baseline taxonomy intact** even if certain capabilities seem irrelevant — future teams may need them.

### Step 2: Contextualise Risk Mapping

Risks can vary significantly across organisations. For example, hallucination risk is significantly more critical for law firms (where incorrect legal precedents could lead to malpractice) than for social companion chatbots (where occasional inaccuracies are tolerable). Contextualising risk mapping ensures alignment between organisational risk management needs and the ARC Framework. 

**Review risks associated with each capability and apply organisational context** (jurisdiction, industry, regulatory environment) to help development teams understand potential harms in your specific setting.

!!! example "Examples of Contextualised Risks"

    1. **Generic Risk:** "Exposing personally identifiable information from databases"  
    **Healthcare (Singapore):** "Exposing patient health records violating PDPA healthcare provisions and MOH data protection standards; potential criminal liability under Healthcare Services Act; mandatory breach notification to PDPC within 3 days"

    2. **Generic Risk:** "Executing unauthorised transactions"  
    **Financial Services (US):** "Processing unauthorised securities trades violating SEC Rule 15c3-3 (Customer Protection Rule); potential market manipulation under Securities Exchange Act; immediate FINRA reporting required; exposure to class action lawsuits"

!!! tip "Contextualising Risks for your Organisation"
    **Geographic context** matters significantly when contextualising risks. **US organisations** should map risks to state and federal regulations such as HIPAA, CCPA, and sector-specific requirements. **Singapore-based organisations** should align risks with the PDPA, Cybersecurity Act, and sectoral guidelines from regulators like MAS, MOH, and IMDA. **Organisations with a presence in the EU** must contextualise risks for GDPR compliance and emerging AI Act requirements.

    **Industry context** shapes risk prioritisation and impact assessment. **Healthcare organisations** should elevate all risks involving patient safety and medical information due to regulatory scrutiny and potential harm. **Financial services firms** must emphasize transaction integrity, market manipulation risks, and financial crime prevention. **Legal firms** should highlight risks to attorney-client privilege and professional liability. **Manufacturing companies** need to focus on safety-critical operations and operational continuity risks.

### Step 3: Adapt Controls

Technical controls require adaptation to the organisation's existing technical stack and capabilities. Some controls may require specific infrastructure, tools, or expertise that are not available in all organisations — for example, advanced guardrail systems may require dedicated ML infrastructure, or automated monitoring may depend on existing observability platforms. When standard controls are not feasible, organisations need to develop alternative approaches that achieve similar risk mitigation using available resources.

**Governance teams should conduct technical readiness assessments to understand what infrastructure, tools, and expertise are available** before mandating specific controls, and work with technical teams to adapt controls to what is practically achievable within current constraints.

!!! example "Examples of Adapted Controls"

    ???+ example "Example 1: Adapting to Different Logging Infrastructure"
        **Baseline Control (CTRL-0007):** "Log all LLM inputs and outputs for regular review using a centralised logging system (e.g., ELK stack, Datadog, CloudWatch)"

        - **Adapted for AWS-based Organisation:** "Log all LLM inputs and outputs to CloudWatch Logs with 90-day retention; use CloudWatch Insights for query analysis; export critical logs to S3 for long-term compliance retention"
        - **Adapted for Small Organisation Without Centralised Logging:** "Log all LLM inputs and outputs to structured JSON files with daily rotation; implement weekly manual review process by security team; escalate to cloud logging system when budget allows"
    
    ??? example "Example 2: Adapting Approval Workflows to Organisational Context"
        **Baseline Control (CTRL-0006):** "Require human approval before executing high-impact actions"
        
        - **Adapted for Enterprise with Slack:** "Require manager approval via Slack workflow for transactions >$1,000 or data modifications affecting >100 records; auto-approve lower-risk actions with notification; escalate to director approval for transactions >$10,000"
        - **Adapted for Financial Services Firm:** "Require dual approval (originator + supervisor) via internal workflow system for all transactions; implement out-of-band SMS confirmation for transactions >$50,000; maintain immutable audit trail in compliance database"

    ??? example "Example 3: Adapting Safety Guardrails to Available Tool"        
        **Baseline Control (CTRL-0044):** "Implement output safety guardrails to detect and prevent generation of undesirable content"
        
        - **Adapted for Organisation with Azure Infrastructure:** "Use Azure AI Content Safety API with toxicity threshold >0.7, sexual content threshold >0.6; block flagged outputs and log violations to Application Insights; review flagged content weekly"
        - **Adapted for Organisation Without Commercial Safety APIs:** "Implement keyword-based filtering for high-priority harmful content categories (profanity, violence, hate speech); use open-source detectors (e.g., Detoxify) for toxicity scoring; plan migration to commercial API in Q3 when budget available"


### Step 4: Define Relevance Criteria

Not all risks are equally relevant across systems and use cases. Relevance criteria provide a structured filter to help developers focus on risks that matter for their specific system. Under the ARC framework, we recommend two main criteria: **impact** (magnitude of potential consequences) and **likelihood** (probability of risk materialising), scored on five-point scales.

??? info "Five-Point Scoring Scales"
    
    We use a five-point scale to provide sufficient granularity for risk assessment while avoiding the analysis paralysis that comes with overly detailed scoring systems. Note that these scales should be calibrated to your organisational context.
    
    <table style="table-layout: fixed; width: 100%;">
      <thead>
        <tr style="background-color: #e3f2fd;">
          <th style="width: 50%;">Impact Scale</th>
          <th style="width: 50%;">Likelihood Scale</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>5 - Catastrophic:</strong> Financial loss >$1M; major irreversible physical or economic harm to people; severe regulatory violations; criminal liability<br><br><strong>4 - Severe:</strong> Financial loss $100K-$1M; some reversible harm to people (e.g., temporary health impact, significant financial loss); major reputational damage; significant compliance issues<br><br><strong>3 - Moderate:</strong> Financial loss $10K-$100K; minor reversible harm (e.g., temporary inconvenience, stress); customer dissatisfaction; moderate business impact<br><br><strong>2 - Minor:</strong> Financial loss <$10K; no harm to people; internal inefficiency; limited user frustration<br><br><strong>1 - Negligible:</strong> Minimal to no consequences; no harm to people</td>
          <td><strong>5 - Very High:</strong> Almost certain to occur; happens regularly in similar systems; requires only basic access or common conditions (e.g., public internet connection, standard user input)<br><br><strong>4 - High:</strong> Likely to occur; observed in comparable systems; requires commonly available capabilities or tools<br><br><strong>3 - Moderate:</strong> May occur under certain circumstances; requires specific but achievable conditions or moderate attacker sophistication<br><br><strong>2 - Low:</strong> Unlikely but possible; requires specific conditions, insider knowledge, or elevated attacker capabilities to materialize<br><br><strong>1 - Very Low:</strong> Rare; requires highly unlikely combination of factors, multiple zero-day exploits, or extraordinary attacker resources</td>
        </tr>
      </tbody>
    </table>

**Governance teams should calibrate these criteria to organisational context and risk appetite, and provide guidance on what score is required for a risk to be considered "relevant."** For instance, a conservative financial institution might consider any risk with Impact ≥ 3 AND Likelihood ≥ 2 as relevant, while a technology startup might set the threshold at Impact ≥ 4 AND Likelihood ≥ 2.

!!! tip "Setting Relevance Thresholds"

    Calibrating the threshold can be a tricky affair - we provide some illustrative examples of a conservative, moderate, and aggressive stance below to highlight how different levels of risk appetite may affect the threshold. 

    **Conservative** (Healthcare, Finance, Legal, Government):
    - **Threshold:** Impact ≥ 3 AND Likelihood ≥ 3 OR Impact ≥ 4 (regardless of likelihood)
    - **Rationale:** Patient safety, financial integrity, regulatory compliance require low risk tolerance

    **Moderate Organizations** (E-commerce, SaaS, Professional Services):
    - **Threshold:** Impact ≥ 3 AND Likelihood ≥ 3
    - **Rationale:** Balance innovation speed with customer trust and compliance

    **Aggressive Organizations** (Internal Tools, Early-Stage Startups):
    - **Threshold:** Impact ≥ 4 AND Likelihood ≥ 3 OR Impact ≥ 5 (regardless of likelihood)
    - **Rationale:** Maximize innovation speed; acceptable to have incidents on internal systems

### Step 5: Pilot with Real Systems and Gather Feedback

Before rolling out the contextualised framework organisation-wide, validate it with 2-3 pilot systems representing different use cases, complexity levels, and business units. These pilot applications test whether your relevance thresholds are appropriately calibrated, reveal whether control recommendations are practical, and identify where documentation or guidance needs clarification.

!!! tip "Selecting Effective Pilot Systems"
    Choose 2-3 diverse pilots to stress-test the framework:
    
    - **One simple system** (few capabilities, internal-facing) - Ensures the framework isn't overly burdensome for straightforward use cases
    - **One complex system** (many capabilities, customer-facing) - Tests if the framework scales to complexity without becoming unmanageable
    - **One novel use case** (new domain or capability) - Verifies the framework is flexible enough for emerging applications
    
    Have developers apply the complete framework — capability identification till the residual risk assessment — while you observe their process, collect detailed feedback, and track how long each step takes.

**Use pilot insights to refine your framework before scaling**. If developers consistently struggle with certain risk definitions, clarify the language or add examples. If recommended controls prove infeasible with your infrastructure, document alternative approaches. If relevance thresholds miss critical risks or flag too many trivial ones, recalibrate the criteria. Document these refinements and create case studies from your pilots — these become invaluable training materials for the broader rollout, showing developers exactly how to apply the framework to real systems in your organisation.

### Step 6: Scale Organisation-Wide

With your pilots complete and the framework refined based on real-world feedback, you are now ready to roll out organisation-wide. Scaling requires significant change management and training—developers need to understand not just the mechanics of filling out forms, but the underlying risk thinking and how to apply contextualised controls to their specific systems.

!!! tip "Making It Easy for Developers"
    Focus your initial efforts on reducing developer friction:
    
    **1. Create a developer self-service toolkit** including pre-filled templates, decision trees for risk scoring, and concrete examples from your pilot projects. This enables developers to complete assessments without constant governance support.
    
    **2. Develop standardised assessment templates** that auto-populate with your organisation's contextualised risks, controls, and relevance thresholds. Developers should be able to select from dropdowns rather than writing from scratch.
    
    **3. Implement automated tooling where possible** such as risk scoring calculators, control recommendation engines, or integration with [ARCvisor](../resources/index.md#arcvisor) for guided workflows. Automation reduces assessment time and ensures consistency.
    
    Developers who can complete assessments quickly and confidently are far more likely to embrace the framework than those who face lengthy, ambiguous processes.

As more agentic systems are assessed across the organisation, **governance teams gain valuable organisation-level visibility** into capabilities deployed, risk exposures, and control adoption rates. This aggregated view enables strategic decisions about where to invest in additional safeguards, which risks are most prevalent across systems, and where developer support is most needed. 

Crucially, governance teams should **treat the framework as a living document** — when new threats emerge or regulations change, update the contextualised framework by adjusting impact levels, adding new risks, or enhancing controls, with changes propagating to all future assessments.
