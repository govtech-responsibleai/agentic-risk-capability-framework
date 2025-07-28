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

