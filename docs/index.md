# :material-shield-star: Agentic Risk & Capability Framework

<img src="assets/arc-banner.jpeg" alt="Robot" style="width: min(600px, 65%); display: block; margin: 0 auto;">

**The ARC Framework is a technical governance framework for identifying, assessing, and mitigating safety and security risks in agentic AI systems.** The framework provides:

- A hierarchical capability taxonomy for classifying agentic system capabilities
- A structured risk mapping distinguishing component, design, and capability-specific risks
- Technical control specifications with risk-to-control mappings
- An implementation methodology for organisational adoption and per-system assessment

!!! info "What's new — August 2026"

    The register and site have had their largest revision since the framework was published:

    - **Register corrected and validated**: the risk-to-control mappings were realigned, and every build now runs a validator so the register cannot regress silently
    - **Level 0 means unwaivable**: cardinal controls are those that must be adopted as-is wherever the risk applies; controls that could not meet that bar were re-tiered
    - **Composite risks**: a risk can arise from a *combination* of elements (e.g., data exfiltration through untrusted content + sensitive data + an outbound channel)
    - **Crosswalks**: every risk and control is mapped to the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), OWASP's agentic threat taxonomy, the [CSA Securing Agentic AI Addendum](https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/) (final, June 2026), and [IMDA's Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf) — see [Crosswalks](arc_framework/crosswalks.md)
    - **2026 risks and controls**: eight risks and eight controls from the 2026 evidence base (supply-chain compromise, sandbox escape, deception toward overseers, unsanctioned agent coordination, automation bias, third-party agents, insecure runtime defaults), and updated controls for the current MCP specification, agent identity, kill switches, and continuous testing
    - **Hazards recorded**: every risk now lists the safety or security hazards it results in, and the register can be filtered by hazard
    - **ARCvisor reads the same register** as this site, so assessments and the published framework can no longer drift apart

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

To cite this work, please use the following BibTeX citation:

```
@article{khoo2025arc,
    title   = {With Great Capabilities Come Great Responsibilities: Introducing the Agentic Risk & Capability Framework for Governing Agentic AI Systems},
    author  = {Khoo, Shaun and Foo, Jessica and Lee, Roy Ka-Wei},
    journal = {arXiv preprint arXiv:2512.22211},
    year    = {2025},
    url     = {https://arxiv.org/abs/2512.22211}
}
```

Alternatively, you may use the APA-formatted citation below:

> Khoo, S., Foo, J., & Lee, R. K.-W. (2025). With great capabilities come great responsibilities: Introducing the Agentic Risk & Capability Framework for governing agentic AI systems. *arXiv preprint arXiv:2512.22211*. <https://arxiv.org/abs/2512.22211>

To cite the framework website directly (e.g., for the Risk Register rather than the paper):

> GovTech Singapore (2025) Agentic Risk & Capability Framework. URL <https://govtech-responsibleai.github.io/agentic-risk-capability-framework/>

*This page was last updated on 30 Aug 2026*