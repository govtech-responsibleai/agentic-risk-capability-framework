# Agentic Risk & Capability (ARC) Framework

[![CI](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**A technical governance framework for identifying, assessing, and mitigating safety and security risks in agentic AI systems**, developed by the Responsible AI team in GovTech Singapore's AI Practice.

**[Website](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/)** ·
**[Interactive risk register](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/risk-register/)** ·
**[Paper (IASEAI'26)](https://arxiv.org/abs/2512.22211)** ·
**[ARCvisor demo](https://agentic-risk-assessment.app.tc1.airbase.sg)** ·
**[Changelog](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/changelog/)**

## How ARC works

ARC starts from what an agent **can do**, not from a list of threats. Every agentic system is made of the same building blocks, and what it can do determines which risks it carries:

| Element | What it covers | Whose risks |
| --- | --- | --- |
| **Components** | LLM, instructions, tools, memory | every system (the *baseline*) |
| **Design** | agentic architecture, roles and access controls, monitoring and traceability | every system (the *baseline*) |
| **Capabilities** | 12 capabilities, e.g. code execution, internet and search access, official communication, business transactions | systems that have them |

Each risk arises from one or more elements, through one of three failure modes (agent failure, external manipulation, tool or resource malfunction), and results in safety or security hazards. A risk that lists several capabilities applies only when a system has all of them. Each risk maps to controls at three levels:

| Level | Meaning |
| --- | --- |
| **0 · Cardinal** | Must be adopted as is wherever the risk applies, whatever its score; waived only if the capability or component it concerns is not present |
| **1 · Standard** | Adopt or adapt meaningfully and sensibly; prioritised by impact and likelihood |
| **2 · Best practice** | Good to consider, especially for high-risk systems |

In practice, a governance team adapts the baseline register to its organisation, and each development team then assesses its own system: identify capabilities → list applicable risks → score them → implement controls → record residual risk. The [implementation guide](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/) walks through both, with worked examples and an [assessment template](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/assessment-template/).

**Register 1.5.0** has 19 elements, 55 risks and 95 controls. Every entry is crosswalked to the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), OWASP's agentic threat taxonomy, the [CSA Securing Agentic AI Addendum](https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/), and [IMDA's Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf). The CSA Addendum adopts ARC's twelve capabilities as its organising taxonomy.

## Using the register

- **Browse** the [interactive register](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/risk-register/), filterable by element, failure mode, risk type, and hazard, with full-text search.
- **Read or link** the [full-text register](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/register-full-text/): every risk and control as plain text, with a link per entry (e.g. `#RISK-034`). It needs no JavaScript, so agents and search engines can read it too.
- **Machine-readable:** the YAML in [`arc-risk-register/`](arc-risk-register/) *is* the register, and the format to build on. It is the single source for both the website and ARCvisor, with one file per kind of entry (risks, controls, elements, hazards, crosswalk references) cross-referenced by ID, and the version in `register.yaml`. The JSON the website loads is generated from it at build time for the interactive page; its shape may change, so don't depend on it.
- **Pin a version:** each release is tagged `v<version>` (e.g. `v1.5.0`). The [changelog](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/changelog/) explains the versioning policy and how to cite a specific version.

## ARCvisor

[ARCvisor](app/) is a Streamlit assistant that walks a team through an ARC assessment. It drafts a system description, identifies capabilities, contextualises and scores the applicable risks, and lists the controls to implement, with a Word export. It reads the register directly from `arc-risk-register/`, so it always matches the published framework. Try the [live demo](https://agentic-risk-assessment.app.tc1.airbase.sg), or see [`app/README.md`](app/README.md) to run it yourself.

## Agent skill

[`skills/arc-assessment`](skills/) is an [Agent Skill](https://agentskills.io) that lets a coding agent assess the system it is building with ARC: it identifies capabilities from the code, lists the applicable risks and controls from the register (fetched at a release tag, or your organisation's own version), checks which controls are implemented, and drafts the assessment. See [`skills/README.md`](skills/README.md) to install it.

## Repository layout

| Path | Contents |
| --- | --- |
| [`arc-risk-register/`](arc-risk-register/) | The register: risks, controls, elements, hazards, crosswalk references, and the register version |
| [`docs/`](docs/) | The website ([MkDocs Material](https://squidfunk.github.io/mkdocs-material/)) |
| [`scripts/`](scripts/) | Validator, and the MkDocs hook that generates the site's register JSON, Crosswalks page, and full-text register at build time |
| [`app/`](app/) | ARCvisor |
| [`skills/`](skills/) | The ARC assessment Agent Skill for coding agents |
| [`iaseai26.tex`](iaseai26.tex) | Source of the IASEAI'26 paper |
| [`archive/`](archive/) | Earlier versions of the site, kept for reference |
| `Dockerfile` | Container image for ARCvisor |

## Running locally

Website (Python 3.13):

```bash
pip install -r requirements.txt
mkdocs serve      # validates the register and generates its pages on every rebuild; http://127.0.0.1:8000
```

ARCvisor:

```bash
pip install -r app/requirements.txt
cp env.example .env                     # add an LLM provider API key
cd app && streamlit run app.py
```

## Contributing

We welcome new risks, new controls, corrections, better sources, and crosswalks to other frameworks. See [CONTRIBUTING.md](CONTRIBUTING.md) for the evidence bar, the entry format, and the checks CI runs. Pull requests go to the `dev` branch. If you'd rather describe a proposal than draft it, [open an issue](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/issues).

## Citation

The framework paper was published in the main track of IASEAI'26:

```bibtex
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

To cite the register itself, name the version, e.g. *GovTech Singapore (2026). Agentic Risk & Capability Framework, risk register v1.5.0.* followed by the website URL.

## License and contact

Released under the [Apache License 2.0](LICENSE). © GovTech Singapore.

Questions or feedback: use [this form](https://forms.gle/KoXecxDuPHf8izP2A) or [open an issue](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/issues).
