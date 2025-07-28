# For Governance Teams


## Desiderata for agentic AI governance

In this subsection, we explain the five desiderata (or desired characteristics) for a good agentic AI governance framework. 

|#| Desiderata | What it means | Why this is important |
| -: | ---- | ---- | ---- |
|  1 | Map out the risk landscape clearly and with flexibility                     | The framework should provide a clear structure for understanding agentic AI risks while being adaptable to future developments in the agentic AI space. | Technology in the AI space is evolving rapidly, with new capabilities and risks emerging frequently. Organisations need a stable governance foundation that will not become obsolete quickly, while remaining adaptable enough to accommodate innovation and technological changes without requiring complete framework overhauls.                                           |
|  2 | Apply to all types of AI systems, agentic or otherwise                      | The framework should work across different AI applications, not just agentic AI systems.                                                                | Organisations typically deploy multiple types of AI systems across different use cases, and having separate governance frameworks for each type creates complexity, inconsistency, gaps, and training overhead that hinders effective risk management and organisational agility.                                                                                                                 |
|  3 | Distinguish between safer and riskier AI systems                            | The framework should differentiate risk levels and apply proportional controls.                                                                         | Applying uniform controls across all agentic AI systems wastes resources on low-risk applications while potentially under-protecting high-risk systems, making proportional governance essential for building stakeholder confidence, enabling appropriate innovation, and effectively prioritising organisational resources.                                                                     |
|  4 | Recommend useful, concrete, proportional, and practical mitigation measures | Controls should be specific, implementable, appropriately scaled to risk, and feasible for teams to execute.                                            | Vague guidance leads to inconsistent implementation and security theatre rather than real risk reduction, while impractical or disproportionate controls either create excessive burden or inadequate protection. Concrete, actionable measures are essential for effective governance that protect the organisation from safety and security risks while not hindering legitimate AI deployment. |
|  5 | Scale easily to manage and govern many AI systems                           | The framework should be efficient for organizations to implement across multiple AI systems without excessive overhead.                                 | Teams may start rapidly deploying multiple agentic AI systems within an organisation, and manual case-by-case governance assessments creates bottlenecks, inconsistencies, and vulnerabilities while preventing the organisation from scaling AI adoption safely and efficiently across different teams and use cases.                                                                            |


## Impact Levels in the Framework

### What Are Impact Levels?

The framework uses a three-tier impact classification system (Low/Medium/High) that determines which technical controls are required for each AI system. Teams must select the **highest impact level** across any of the three criteria:

**Current Criteria:**
- **Data Classification:** Open data (Low) → Staff-only circulation (Medium) → Confidential (High)
- **Domain:** All other use cases (Low) → Health/safety/compliance use cases (Medium) → National interest (High)
- **Target Audience:** Internal-facing (Low) → Public facing (Medium) → Critical infrastructure (High)

### Importance in the Framework

**1. Proportional Risk Management**
Impact levels ensure that more sensitive or critical AI systems receive appropriately stringent controls. For example, a simple internal chatbot (Low impact) might only need basic output filtering, while an AI system handling confidential national security data (High impact) would require comprehensive monitoring, human approval workflows, and regular audits.

**2. Resource Optimization**
By scaling control requirements with impact level, organizations avoid over-engineering low-risk systems while ensuring adequate protection for high-risk applications. This prevents governance from becoming a barrier to innovation on routine use cases.

**3. Control Activation Logic**
Controls are tagged with impact level requirements:
- **LMH:** Required for all systems (fundamental protections)
- **MH:** Required only for Medium and High impact systems (enhanced protections)
- **H:** Required only for High impact systems (maximum protections)

**4. Scalable Decision-Making**
Impact levels provide a clear, objective way to determine control requirements without requiring case-by-case governance review, enabling the framework to scale across many AI systems efficiently.

## Domain-Specific Adaptations

Different organizations can adapt the impact level criteria to reflect their unique risk profiles and regulatory environments. Here are examples:

### Healthcare Organization

**Criteria Adaptation:**
- **Patient Data Sensitivity:** De-identified research data (Low) → Individual patient records (Medium) → Genetic/psychiatric data (High)
- **Clinical Decision Impact:** Administrative support (Low) → Clinical decision support (Medium) → Autonomous treatment recommendations (High)
- **Regulatory Scope:** Internal research (Low) → FDA-regulated devices (Medium) → Life-critical interventions (High)

**Rationale:** Healthcare organizations face unique risks around patient privacy (HIPAA), clinical safety, and medical device regulations that don't map well to generic "confidential data" categories.

### Financial Services Institution

**Criteria Adaptation:**
- **Financial Impact:** <$10K exposure (Low) → $10K-$1M exposure (Medium) → >$1M exposure (High)
- **Regulatory Classification:** Internal operations (Low) → Customer-facing services (Medium) → Trading/market-making systems (High)
- **Data Sensitivity:** Public market data (Low) → Customer PII (Medium) → Trading algorithms/positions (High)

**Rationale:** Financial institutions need to consider market impact, systemic risk, and specific financial regulations (SOX, Basel III) that require different thresholds than general government classifications.

### Manufacturing Company

**Criteria Adaptation:**
- **Safety Impact:** Quality control (Low) → Equipment optimization (Medium) → Safety-critical systems (High)
- **Operational Scope:** Single facility (Low) → Regional operations (Medium) → Global supply chain (High)
- **Environmental Impact:** No environmental risk (Low) → Reportable emissions (Medium) → Hazardous materials (High)

**Rationale:** Manufacturing faces physical safety risks, environmental regulations, and supply chain vulnerabilities that don't align with information-centric government criteria.

### Technology Platform Company

**Criteria Adaptation:**
- **User Scale:** Internal tools (Low) → <1M users (Medium) → >1M users (High)
- **Content Impact:** Feature functionality (Low) → Content moderation (Medium) → Algorithmic feed ranking (High)
- **Platform Criticality:** Optional features (Low) → Core functionality (Medium) → Trust & safety systems (High)

**Rationale:** Tech platforms face unique risks around user manipulation, content amplification, and platform integrity that require scale-based and algorithmic impact considerations.

### Academic Research Institution

**Criteria Adaptation:**
- **Research Sensitivity:** Published research (Low) → Pre-publication findings (Medium) → Human subjects research (High)
- **Institutional Impact:** Individual projects (Low) → Department-wide tools (Medium) → Institution-wide systems (High)
- **Ethical Considerations:** No human impact (Low) → Indirect human impact (Medium) → Direct human subjects (High)

**Rationale:** Academic institutions must balance research freedom with ethical obligations, institutional reputation, and varying levels of research sensitivity.

## Key Adaptation Principles

When adapting impact level criteria, organizations should consider:

1. **Regulatory Environment:** What specific laws and regulations apply to your domain?
2. **Stakeholder Impact:** Who could be harmed and how severely?
3. **Organizational Risk Tolerance:** What level of risk is acceptable for different types of operations?
4. **Operational Context:** What makes an AI system more or less critical in your specific environment?
5. **Measurability:** Can the criteria be objectively assessed and consistently applied?

The flexibility to adapt impact level criteria while maintaining the same control structure allows the framework to be broadly applicable across different domains while respecting the unique risk profiles and regulatory requirements each organization faces.






**How the framework meets it:** 

* Uses a hierarchical taxonomy with exhaustive Level 1 capabilities (Cognitive, Interaction, Operational) and extensible Level 2 capabilities beneath them
* This structure helps organise discussions about different capabilities while allowing flexibility to add or remove specific capabilities as technology evolves
* For example, new capabilities like hardware control (e.g. embodied AI) could be added under Interaction without restructuring the entire framework

**How the framework meets it:**

* AI systems can be described through combinations of capabilities regardless of their domain or use case. There is no defined threshold for when a system is "agentic" - it simply depends on the capabilities.
* Everything from simple LLM chatbots (like ChatGPT) to more advanced agentic coding assistants (like Cursor, V0, or Replit) can be adequately described and managed using the ARC Framework.

**How the framework meets it:**

* Systems with more and riskier capabilities automatically have more risks and controls assigned under the ARC Framework - proportionality is an intrinsic part of the design
* Impact levels (Low / Medium / High) based on data classification, domain, and target audience determine which controls apply
* Clear progression shown: Pair Assistant (8 risks, 12 controls) → AI Bots (11 risks, 18 controls) → Spaceship (20 risks, 43 controls)
* Controls are tagged with levels (LMH, MH, H) indicating which impact systems require them

**How the framework meets it:**
- Controls are written with minimal ambiguity (e.g., "Limit communications to standard processes where communication templates are available")
- Controls are easily verifiable rather than vague statements
- Proportional application - sensitive controls only required for medium/high impact systems
- Covers both cybersecurity and responsible AI considerations
- Consider practical implementation constraints

**How the framework meets it:**
- Simple compliance assessment: check that teams correctly identified capabilities and implemented required controls
- Central governance teams can focus on maintaining the taxonomy, risk mapping, and control definitions rather than assessing each system individually
- Easy to adjust overall risk posture by modifying impact levels or adding risks
- Standardized approach allows consistent evaluation across all AI systems in an organization

