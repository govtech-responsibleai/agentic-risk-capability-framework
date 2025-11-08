# For Governance Teams

In this section, we outline a step-by-step approach for applying the ARC Framework for your organisation and provide two worked examples to illustrate how it can be applied.

## Applying the ARC Framework

### Step 1: Review the capability taxonomy

Although we designed [our capability taxonomy](../capability/index.md) to be comprehensive in capturing the wide gamut of agentic capabilities today, we also recognise that there may be very niche capabilities which are especially relevant for specific domains. For example, companies operating in the intersection of agentic AI systems and robotics may have a whole umbrella of capabilities relating to hardware interaction, such as physical movement or object manipulation, while fintech companies may want more granularity for the capability to perform transactions by distinguishing between different types of transactions (e.g. cash, stocks, bonds).

**Governance teams should begin by reviewing the capability taxonomy and identifying the key capabilities which are intuitively most relevant to the organisation, and consider breaking out more specific second-level categories if the first-level categories are insufficient.** We generally do not recommend organisations to drop any of the existing capabilities in the taxonomy, even if they are unlikely to be used, as this may hurt the taxonomy's generalisability across different verticals within the organisation (e.g. manufacturing, finance, or legal).

### Step 2: Contextualise the risk mapping

Each organisation has a different risk profile, and contextualising the risk mapping is important to ensure tight alignment between the organisation's risk management needs and the ARC Framework. For example, while the ARC Framework describes hallucination as a general risk for the capability of Natural Language Communication, it is more significant for a law firm rather than a social companion chatbot. 

**Governance teams should go through the list of risks associated with each capability and apply the organisation's context (be it country- or industry-specific)** to help the organisation and its internal AI development teams better understand the potential harms that could arise from such a capability. This is necessary if the capability taxonomy has been updated, since the current risk mapping is valid only for the present taxonomy.

### Step 3: Adapt the controls

Similar to capabilities and risks, the technical controls themselves also require adaptation to the organisation's operating context and technical stack. For example, a fact-checking system operating in the European Union must comply with GDPR's strict data protection requirements, which might necessitate additional privacy controls beyond what's specified in the framework. Moreover, some controls may require specific technical expertise or infrastructure that is not available to all organisations, necessitating alternative approaches that achieve similar risk mitigation outcomes.

**Governance teams should systematically map their jurisdiction's AI and data protection requirements against the ARC Framework controls and conduct technical readiness assessments before mandating specific controls.** For smaller teams, focusing initial efforts on controls that address the highest-impact risks within the organisation's regulatory and technical constraints may be more fruitful. Implementing audits which evaluate both compliance and efficacy will help to identify controls which may need to be adjusted and ensure that the framework stays relevant in the longer run.

### Step 4: Define relevance criteria

Not all risks are equally relevant, especially given the diversity of domains and use cases even within an organisation. For example, the risk of "generating controversial content" is minimal for an internal document processing system but represents a critical concern for a public-facing fact-checking platform that could influence public opinion. Relevance criteria provide a structured filter to help developers focus their limited time and resources on risks that actually matter for their specific system and use case.

Under the ARC Framework, we recommend setting two main relevance criteria: **impact** (the magnitude of potential consequences) and **likelihood** (the probability of risk materialising). Each criterion is set along a five-point scale, and the final score is calculated by multiplying the two values together. This simplicity makes implementation easier. 

**Governance teams should then calibrate these criteria to their organisation's context and risk appetite, and provide guidance on what score is required for a risk to be considered as "relevant".**  For instance, a conservative financial institution might consider any risk scoring 6 or above (3x2 or 2x3) as relevant and requiring mandatory controls, while a technology startup might set the threshold at 9 or above (3x3). The calibration should also account for regulatory requirements - risks with direct compliance implications may be deemed relevant regardless of their calculated score. Additionally, governance teams should establish review periods to reassess these thresholds as the organisation's risk profile and business context evolve.

### Step 5: Standardise and scale

Rolling out the ARC Framework - capability taxonomy, risk mapping, and technical controls - will not be an overnight feat, and requires significant change management and training across multiple departments. **Governance teams should look to streamline the reporting process by providing a simple form or checklist for AI developers to declare their system's capabilities, relevant risks, and technical controls.** As more data points for different systems start to stream in, governance teams will get a better organisation-wide view of system capabilities, risk exposures, and control adoption rates, which in turn will enhance the governance design process.

Beyond the day-to-day operations of validating compliance to the framework, governance teams should leverage the framework to deliver more agile governance for agentic AI systems. For example, when new threats emerge or regulatory requirements change, **governance teams can efficiently update the framework by adjusting impact levels, adding new risks, or enhancing control specifications, with changes automatically propagating to all systems** through the next assessment cycle. This transforms AI governance from a reactive, project-by-project exercise into a proactive, portfolio-level capability that scales with organisational AI adoption and maintains effectiveness as both technology and threat landscapes evolve.

## Example: Domain-specific adaptations

In this subsection, we provide two fictional examples of how an organisation can adapt the ARC Framework to their operating context. 

### Healthcare Organisation

**Step 1: Review the capability taxonomy**

Healthcare organisations should expand the "Natural Language Communication" capability to distinguish between patient-facing communications and clinical decision support, as these may carry different regulatory implications (such as FDA medical device regulations and Singapore's Health Sciences Authority ("HSA") medical device guidelines). They may also need to add specific capabilities for medical image analysis under "Multimodal Understanding & Generation" and create subcategories for different types of clinical data access under "File & Data Management" (e.g., accessing electronic health records vs. medical literature databases). The "Transactions" capability should be refined to include medication ordering, appointment scheduling, and insurance claim processing, each with distinct risk profiles under healthcare regulations.

**Step 2: Contextualise the risk mapping**

Risk contextualisation must emphasize patient safety and data protection compliance. "Generating unqualified advice in specialised domains" becomes a critical risk requiring FDA medical device approval pathways or HSA therapeutic product registration rather than just disclaimer implementation. "Regurgitating personally identifiable information" takes on heightened significance due to HIPAA requirements in the US and Singapore's Personal Data Protection Act (PDPA) for healthcare data, with potential criminal penalties in both jurisdictions. "Generating hallucinated content" in clinical contexts could lead to patient harm, making this a patient safety issue under FDA guidelines. The organisation should map each risk against specific healthcare regulations (such as HIPAA, FDA 21 CFR Part 820, Joint Commission standards, HSA medical device regulations, MOH clinical practice guidelines) and patient safety frameworks.

**Step 3: Adapt the controls**

Controls must align with healthcare quality management systems and clinical workflows in both jurisdictions. "Implement output guardrails" becomes "Implement clinical decision support alerts with physician override capabilities and audit trails compliant with prevailing regulations", such as FDA 21 CFR Part 820 and HSA quality management system requirements. "Require human approval" transforms into "Require licensed clinician review with documented clinical reasoning". The organisation must integrate controls with existing clinical governance structures, electronic health record systems, and medical staff credentialing processes. Controls should also address clinical validation requirements, with mandatory testing against clinical datasets and integration with hospital incident reporting systems that in accordance with local requirements, be it the US Joint Commission sentinel event reporting or Singapore's MOH adverse event reporting requirements.

**Step 4: Define relevance criteria**

Healthcare organizations typically operate with very low risk tolerance due to patient safety implications and regulatory scrutiny in both the US and Singapore. The relevance threshold should be set conservatively - any risk scoring 4 or above (2x2) should be considered relevant given the potential for patient harm. Impact criteria must consider patient safety outcomes, regulatory compliance, and malpractice liability. Likelihood assessments should account for the clinical environment's high-stress conditions where users may over-rely on AI recommendations. All risks with direct patient safety implications should be deemed relevant regardless of calculated scores, especially for healthcare organisations in Singapore given Singapore's emphasis on healthcare quality through the National Healthcare Quality and Safety Framework.

**Step 5: Standardise and scale**

The rollout must integrate with existing clinical governance structures, including medical staff committees, quality assurance programs, and clinical informatics teams. Training should be incorporated into medical staff orientation and continuing education requirements. The framework should align with hospital accreditation standards and integrate with existing clinical audit processes. 

### Manufacturing Company

**Step 1: Review the capability taxonomy**

Manufacturing organisations should significantly expand operational capabilities to include industrial equipment control, sensor data processing, and supply chain coordination. Under "System Management," they may need subcategories for industrial control systems, supervisory control and data acquisition systems, and manufacturing execution systems. The "Transactions" capability should be refined to distinguish between procurement, inventory management, and supplier communications, particularly important given Singapore's role as a regional manufacturing and logistics hub. They may also need to add capabilities for predictive maintenance, quality control analysis, and production optimization under a new "Industrial Operations" category.

**Step 2: Contextualise the risk mapping**

Risk contextualisation must emphasize operational safety, production continuity, and supply chain security. "Misconfiguring system resources" becomes critical as it could shut down production lines or damage expensive equipment, violating standards like OSHA's safety standards and Singapore's Workplace Safety and Health Act. "Executing malicious code" takes on heightened significance in industrial environments where cyberattacks could cause physical damage or safety incidents, subject to frameworks like NIST's cybersecurity frameworks or Singapore's Cybersecurity Act requirements for critical information infrastructure. Risks should be mapped against industrial safety standards (ISO 45001, OSHA regulations, Singapore's WSH Act), quality management systems (ISO 9001), and cybersecurity frameworks for industrial control systems (IEC 62443, NIST, Singapore's Cybersecurity Agency guidelines).

**Step 3: Adapt the controls**

Controls must integrate with existing industrial safety and quality management systems under both jurisdictions. "Scope system privileges strictly" becomes "Implement role-based access control aligned with safety integrity levels and functional safety requirements". "Monitor system health metrics" transforms into "Integrate with plant-wide distributed control systems with automatic failsafe mechanisms compliant with prevailing regulations". Controls should align with manufacturing execution systems, integrate with existing maintenance management systems, and comply with industrial cybersecurity standards. Safety-critical systems may require redundant control mechanisms and fail-safe designs to meet the requisite safety standards.

**Step 4: Define relevance criteria**

Manufacturing organisations must balance operational efficiency with safety and continuity requirements under both regulatory environments. Risk tolerance varies significantly between safety-critical systems (very low tolerance) and optimisation systems (moderate tolerance). The relevance threshold should be set at 6 or above (3x2 or 2x3) for most systems, but any risk affecting safety-critical operations should be relevant regardless of score. Impact criteria must consider production downtime costs, equipment damage potential, worker safety implications, and supply chain disruption effects. Likelihood assessments should account for the industrial environment's complexity and the potential for cascading physical failures.

**Step 5: Standardise and scale**

The rollout must integrate with existing plant engineering, maintenance, and safety management systems, and training should be incorporated into existing safety training programs and technical competency development. The framework should align with manufacturing quality management systems and integrate with existing operational risk management processes, with regular reviews coinciding with planned maintenance shutdowns and safety audit cycles, thereby ensuring that AI governance becomes part of standard operational excellence programs.


