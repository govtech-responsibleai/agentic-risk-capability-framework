# :material-shield-star: Agentic Risk & Capability Framework

<img src="assets/arc-banner.jpeg" alt="Robot" style="width: min(600px, 65%); display: block; margin: 0 auto;">

**The ARC Framework is a technical governance framework for identifying, assessing, and mitigating safety and security risks in agentic AI systems.** The framework provides:

- A hierarchical capability taxonomy for classifying agentic system capabilities
- A structured risk mapping distinguishing component, design, and capability-specific risks
- Technical control specifications with risk-to-control mappings
- An implementation methodology for organisational adoption and per-system assessment

!!! info "Major Update"

    We have significantly updated the ARC Framework since our initial release in August 2025. The main changes include:

    - **Updated theoretical foundations**: Added a comprehensive [introduction](arc_framework/introduction.md) with design rationale, literature review, real-world case studies (Replit, Antigravity incidents), as well as detailed justifications for the capability-based approach
    - **Restructured documentation**: Consolidated Components and Design elements together with the Capabilities element into a unified [Elements](arc_framework/elements.md) reference page with clearer taxonomy and detailed definitions
    - **Interactive Risk Register**: Introduced a [filterable, searchable risk register](arc_framework/risk-register.md) consolidating all 46 risks and 86 controls with risk-to-control mappings in a single interactive interface
    - **Framework positioning**: Added a [comparison table](arc_framework/comparison.md) benchmarking ARC against NIST AI RMF, EU AI Act, Dimensional Governance, OWASP Agentic AI, Google SAIF 2.0, CSA MAESTRO, and other governance frameworks
    - **Enhanced implementation guidance**: Updated implementation guides with more detailed methodologies for both organizational adoption and per-system assessment
    - **ARCvisor tool**: Launched [ARCvisor](resources/index.md#arcvisor), an AI-powered risk assessment assistant achieving 50%+ time savings with live demo and open-source repository
    - **Research publications**: Published two technical papers available in [Resources](resources/index.md) — the ARC Framework paper (accepted at IASEAI 2026) and the ARCvisor preprint

## Navigation

On this website, you'll find all the resources you need to get started with understanding and applying the ARC Framework in your organisation.

### 📚 Reference Documentation
- **[Framework Introduction](arc_framework/introduction.md)** — Design rationale, literature review, and theoretical foundation
- **[Agentic System Elements](arc_framework/elements.md)** — Detailed examination of components, design, and capabilities
- **[Capability Taxonomy](arc_framework/elements.md#capabilities)** — Cognitive, interaction, and operational capability categories with definitions
- **[Risk Register](arc_framework/risk-register.md)** — Component, design, and capability-specific risks with impact/likelihood assessment
- **[Comparison Table](arc_framework/comparison.md)** — Comparison to NIST AI RMF, EU AI Act, Dimensional Governance, OWASP Agentic AI, Google SAIF 2.0, and CSA MAESTRO

### 🛠️ Implementation Guides
- **[Implementation Overview](implementation/index.md)** — Macro and micro implementation levels, timelines, and resources
- **[Organisational Adoption](implementation/for-governance-teams.md)** — Multi-phase rollout methodology for governance teams
- **[System Assessment](implementation/for-ai-developers.md)** — Per-system risk assessment process for developers

### 🧰 Tools & Resources
- **[ARCvisor Tool](resources/index.md#arcvisor)** — Open-source web application for automated risk assessment
- **[Resources](resources/index.md)** — Slide deck, paper, and code for implementing the ARC Framework for your organisation

## Referenced By

The ARC framework has been mentioned in:

* [Cybersecurity Agency of Singapore's Securing Agentic AI — An Addendum to the Guidelines and Companion Guide on Securing AI Systems](https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/) (finalised 17 June 2026)
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

*This page was last updated on 12 Aug 2026*