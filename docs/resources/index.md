# Resources

Beyond the [technical governance framework](../arc_framework/introduction.md) and [implementation guide](../implementation/index.md), we have also developed additional tools and resources to help organisations understand and get started with using the ARC framework to govern their agentic AI systems. 

| Resource | Target Audience | Description |
| --- | --- | --- |
| [ARCvisor Tool](#arcvisor) | AI governance teams, developers | Web-based risk assessment workflow with 50%+ time savings |
| [Technical Paper](../assets/ARC_Framework-Paper-IASEAI_2026.pdf) | AI governance teams, academia | In-depth technical details and research foundations |
| [Baseline Risk Register](../arc_framework/risk-register.md) | AI governance teams, developers | Interactive exploration of 54 risks and 94 controls ([YAML sources](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/arc-risk-register); [machine-readable JSON](../assets/risk_register_data.json)) |
| [Assessment Template](../implementation/assessment-template.md) | AI developers, governance teams | Record of a per-system assessment: capabilities, applicable risks, controls with evidence, residual risks, sign-off |
| [Changelog](../arc_framework/changelog.md) | Everyone using the register | What changed in each register version, and the versioning policy |
| Presentation slides (pending) | General AI-literate audience | High-level overview of the ARC framework |

## ARCvisor 🤖✨

ARCvisor is an AI-powered assistant that makes risk assessment for agentic AI systems actually enjoyable. By combining LLMs with structured knowledge representation, ARCvisor turns the tedious process of risk identification and control selection into an interactive conversation.

[Try Live Demo :material-play-circle:](https://agentic-risk-assessment.app.tc1.airbase.sg){ .md-button .md-button--primary } [View on GitHub :fontawesome-brands-github:](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/app){ .md-button }

### 🚀 Key Features

- **Automated risk identification**: Identifies relevant risks based on system descriptions
- **Control recommendations**: Suggests appropriate controls for specific deployment contexts
- **Documentation generation**: Produces structured risk mitigation documentation
- **Conversational interface**: Natural language interaction for describing agentic systems
- **Improved Efficiency**: Reduces time required for manual risk assessment workflows

### 📚 Learn More

Want to dive deeper into how ARCvisor works? Check out the [ARCvisor preprint paper](../assets/ARCvisor-Preprint_2025.pdf) for technical details on the architecture, evaluation results, and real-world case studies.
## Contributing to the register 🤝

The register is a living document and we welcome proposals for new risks, new controls, corrections, and crosswalks. The bar is the same one we hold ourselves to: a risk must be supported by academic research or a documented industry incident, and a control must be actionable, composable, and measurable. See [CONTRIBUTING.md](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/blob/main/CONTRIBUTING.md) for the entry format, the validator, and the pull-request flow, or [open an issue](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/issues) if you would rather describe the proposal and let us draft it.
