# :material-shield-star: Agentic Risk & Capability Framework

<img src="assets/arc-banner.jpeg" alt="Robot" style="width: min(600px, 65%); display: block; margin: 0 auto;">

**The ARC Framework is a technical governance framework for identifying, assessing, and mitigating safety and security risks in agentic AI systems.** The framework provides:

- A hierarchical capability taxonomy for classifying agentic system capabilities
- A structured risk mapping distinguishing component, design, and capability-specific risks
- Technical control specifications with risk-to-control mappings
- An implementation methodology for organisational adoption and per-system assessment

!!! info "What's new — register v1.4 and v1.5, November 2026"

    - **Level 0 controls match their subject (v1.5)**: CVE scanning of agent-generated code applies only to systems that can execute code, tool authentication covers every remote tool rather than only MCP servers, and the memory-write controls concern persistent memory, so a system that keeps nothing beyond a session can waive them
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
- **[Risk Register](arc_framework/risk-register.md)** — 54 component, design, and capability-specific risks with their hazards and 94 recommended controls at three levels, filterable and searchable
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