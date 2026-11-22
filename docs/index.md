# :material-shield-star: Agentic Risk & Capability Framework

<img src="assets/arc-banner.jpeg" alt="Robot" style="width: min(600px, 65%); display: block; margin: 0 auto;">

**The ARC Framework is a technical governance framework for identifying, assessing, and mitigating safety and security risks in agentic AI systems.** The framework provides:

- A hierarchical capability taxonomy for classifying agentic system capabilities
- A structured risk mapping distinguishing component, design, and capability-specific risks
- Technical control specifications with risk-to-control mappings
- An implementation methodology for organisational adoption and per-system assessment

!!! info "What's new — register v2.0 (draft)"

    Version 2.0 changes the model. An assessment or a contextualised register written against 1.x needs migrating; the [changelog](arc_framework/changelog.md#v2-0-0) says how.

    - **How a capability is used**: each capability that acts on the world is recorded with its [authority, reversibility and reach](arc_framework/elements.md#context-how-a-capability-is-used), so an assistant that drafts a payment and an agent that pays by itself no longer get the same risks and controls
    - **Protocols** is a fifth component, for connections to tool servers and agents that another party builds or operates; it and Memory are conditional, so their risks apply only to systems that have them
    - **Combination rules** bring a risk into scope whenever a system's capabilities can complete a [dangerous combination](arc_framework/capability-combinations.md), whichever capabilities supply the parts
    - **Six failure modes**, separating an agent's mistakes from goal-directed misbehaviour, and adding safeguard failure and misuse by the principal
    - **Twelve new risks**, written from a curated file of 366 incidents, covering instruction files, agent credentials, provider dependence, agents that work around their limits, and more
    - **Every control** says where it is enforced, who owns it, what evidence shows it is in place and how to test it, and cites its sources
    - **Overlays** let an organisation keep its own version as one file of changes
    - **Two more crosswalks**: MITRE ATLAS and the Five Eyes guidance on agentic AI

!!! info "Earlier — register v1.4 and v1.5, November 2026"

    - **Capability combinations (v1.5)**: a new [page](arc_framework/capability-combinations.md) on risks that arise only when capabilities are held together, with a check that reads a system's capabilities and reports whether the lethal trifecta (untrusted content, sensitive data, and an outbound channel) is present; a new Level 0 control, CTRL-0097, requires breaking that combination; and a new risk, RISK-055, covers data exfiltration by agents that handle messages, such as email assistants
    - **Human approval as a floor (v1.5)**: human approval of business transactions outside pre-authorised limits, of sensitive official communications, and of deletions that cannot be undone is now Level 0, together with least privilege and checking that approvals remain real decisions; copyright guardrails and code linters move to Level 1; and each Level 0 control now matches its subject, so CVE scanning applies only where code runs, tool authentication covers every remote tool, and the memory-write controls concern persistent memory
    - **Risks apply where they arise**: multi-agent risks now apply only to systems in which more than one agent works on a task, including agents operated by other organisations, and the sandbox-escape risk only to systems that can execute code, so simpler systems no longer carry Level 0 controls that cannot apply to them; and a Level 0 control is waived when the capability or component it concerns is not present
    - **Readable by AI agents**: a [full-text register](arc_framework/register-full-text.md) with a link for every risk and control, and an [`llms.txt`](llms.txt) index for agents
    - **ARC assessment skill**: an [Agent Skill](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/skills) that lets a coding agent assess the system it is building against the register

    Register v1.3 (November 2026) corrected and validated the register; defined Level 0 controls as unwaivable wherever their risk applies; introduced risks that arise from a combination of elements; added crosswalks to the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), OWASP's agentic threat taxonomy, the [CSA Securing Agentic AI Addendum](https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/), and [IMDA's Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf); added eight risks and eight controls from the 2026 evidence base; and recorded the hazards each risk results in. Each change is listed by version in the [Changelog](arc_framework/changelog.md).

    Earlier (December 2025): the [introduction](arc_framework/introduction.md) with design rationale and literature review, the unified [Elements](arc_framework/elements.md) page, the [interactive register](arc_framework/risk-register.md), the [ARCvisor](resources/index.md#arcvisor) tool, and the two technical papers in [Resources](resources/index.md).

## Navigation

On this website, you'll find all the resources you need to get started with understanding and applying the ARC Framework in your organisation.

### 📚 Reference Documentation
- **[Framework Introduction](arc_framework/introduction.md)** — Design rationale, literature review, and theoretical foundation
- **[Agentic System Elements](arc_framework/elements.md)** — Detailed examination of components, design, and capabilities
- **[Capability Taxonomy](arc_framework/elements.md#capabilities)** — Cognitive, interaction, and operational capability categories with definitions
- **[Risk Register](arc_framework/risk-register.md)** — 66 component, design, capability and combination risks with their hazards and 103 recommended controls at three levels, filterable and searchable
- **[Capability Combinations](arc_framework/capability-combinations.md)** — Risks that arise only when capabilities are held together, and the check for the lethal trifecta
- **[Crosswalks](arc_framework/crosswalks.md)** — Entry-level mappings to the OWASP Top 10 for Agentic Applications, OWASP's agentic threat taxonomy, the Cyber Security Agency of Singapore's Securing Agentic AI Addendum, and IMDA's Model AI Governance Framework for Agentic AI

### 🛠️ Implementation Guides
- **[Implementation Overview](implementation/index.md)** — How the framework goes from general methodology to organisational practice
- **[Organisational Adoption](implementation/for-governance-teams.md)** — Multi-phase rollout methodology for governance teams
- **[System Assessment](implementation/for-ai-developers.md)** — Per-system risk assessment process for developers

### 🧰 Tools & Resources
- **[ARCvisor Tool](resources/index.md#arcvisor)** — Open-source web application for automated risk assessment
- **[Resources](resources/index.md)** — Slide deck, paper, and code for implementing the ARC Framework for your organisation

## Referenced By

The ARC framework has been mentioned in:

* [Cyber Security Agency of Singapore's Securing Agentic AI — An Addendum to the Guidelines and Companion Guide on Securing AI Systems](https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/) (finalised 17 June 2026), which adopts ARC's twelve capabilities as its organising taxonomy
* [IMDA's Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf), which lists ARC under both risks and technical controls
* [Opening Address by Minister Josephine Teo at HLP (AI) on 22 Oct 2025](https://www.csa.gov.sg/news-events/speeches/opening-address-by-minister-josephine-teo-at-hlp--ai--on-22-oct-2025/#:~:text=20.%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%20First%2C%20we,can%20trust%20autonomy.)
* [AI Agents and Global Governance: Analyzing Foundational Legal, Policy, and Accountability Tools by Talita Dias (Partnership on AI)](https://partnershiponai.org/wp-content/uploads/2025/09/agents-policy-analysis.pdf?vgo_ee=uag8GfRQtHHxKE9ENGhTyS97XYF3rhM%3D%3AZ%2BYB5WRdklLrdWegdiC1Lb9RPOHzTLfW)
* [Engineering responsible AI: How Singapore builds trust in emerging technologies by GovTech Singapore](https://www.tech.gov.sg/technews/engineering-responsible-ai/)

## About the Authors

The ARC Framework is developed by the Responsible AI team in GovTech Singapore's AI Practice. We develop deep technical capabilities in Responsible AI to improve how the Singapore government develops, evaluates, deploys, and monitors AI systems in a safe, trustworthy, and ethical manner.

In developing this framework, we work closely with other teams in the Singapore government, such as the Ministry for Digital Development and Information, the Cybersecurity Agency of Singapore, and the Infocomm Media Development Authority. We are grateful for their feedback and contributions, which have helped to make this framework more effective, robust, and thorough.

To reach out to us, please fill out the Google form <a href="https://forms.gle/KoXecxDuPHf8izP2A" target="_blank">here</a>.

## Citation

The framework paper was published in the main track of IASEAI'26, the Second Conference of the International Association for Safe and Ethical Artificial Intelligence. To cite this work, please use the following BibTeX citation:

```
@inproceedings{khoo2026arc,
    title         = {With Great Capabilities Come Great Responsibilities: Introducing the Agentic Risk \& Capability Framework for Governing Agentic AI Systems},
    author        = {Khoo, Shaun and Foo, Jessica and Lee, Roy Ka-Wei},
    booktitle     = {Second Conference of the International Association for Safe and Ethical Artificial Intelligence (IASEAI'26)},
    note          = {Main track},
    year          = {2026},
    eprint        = {2512.22211},
    archivePrefix = {arXiv},
    url           = {https://arxiv.org/abs/2512.22211}
}
```

Alternatively, you may use the APA-formatted citation below:

> Khoo, S., Foo, J., & Lee, R. K.-W. (2026). With great capabilities come great responsibilities: Introducing the Agentic Risk & Capability Framework for governing agentic AI systems. In *Second Conference of the International Association for Safe and Ethical Artificial Intelligence (IASEAI'26)*, main track. <https://arxiv.org/abs/2512.22211>

To cite the framework website directly (e.g., for the Risk Register rather than the paper):

> GovTech Singapore (2025) Agentic Risk & Capability Framework. URL <https://govtech-responsibleai.github.io/agentic-risk-capability-framework/>

*This page was last updated on 20 Nov 2026*