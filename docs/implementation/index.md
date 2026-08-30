# Implementing the ARC Framework

!!! info "Quick Navigation"

    **Getting Started**:
    [Governance Teams](#for-governance-teams) •
    [AI Developers](#for-ai-developers)

    **Detailed Guides**:
    [Complete Governance Guide](for-governance-teams.md) •
    [Complete Developer Guide](for-ai-developers.md)

    **Resources**:
    [Framework Elements](../arc_framework/elements.md) •
    [Risk Register](../arc_framework/risk-register.md) •
    [Controls](../arc_framework/controls.md) •
    [ARCvisor Tool](../resources/index.md#arcvisor)

[A well-known adage in the Singapore civil service is "Policy is implementation and implementation is policy"](https://www.psd.gov.sg/files/opening-address-by-mr-peter-ho-at-2010-administrative-service-dinner-and-promotion-ceremony.pdf), and this is resoundingly true for AI governance. The ARC framework aims to go beyond academic novelty to practical value by providing a clear implementation plan that organisations can adopt from day 1.

---

## From General Framework to Organisational Practice

**The ARC framework is designed as a general-purpose tool that organisations should adapt to their specific context before applying it to individual systems.** This process is typically led by the organisation's central AI governance team or Chief AI Officer. Their role is to translate the baseline ARC framework into an organisation-specific version that reflects local laws, sector regulations, internal policies, and the technical infrastructure and capabilities available within the company. 
    
Once the governance team has created this contextualised framework, the organisation enters **a trial phase where the adapted framework is applied to a small number of diverse agentic systems**. These pilot applications test whether the relevance thresholds, control recommendations, and documentation requirements are appropriately calibrated, whether the framework is genuinely usable by AI developers in their day-to-day work, and where additional training or support tools may be needed—allowing the governance team to refine both the framework content and change management approach before wider rollout.

This two-stage approach — organisational contextualisation followed by pilot-based calibration — ensures that the ARC framework evolves from a general methodology into a practical, organisation-specific governance tool. In this section, we provide more detailed guidance for how this can be achieved.

??? question "Is contextualisation necessary?"

    The baseline Risk Register we provide should cover most of the general risks of using agentic systems. If you want to start with something simple without much effort, you can skip the contextualisation steps first.
    
    However, **contextualisation adjusts the baseline Risk Register to account for variations in regulatory jurisdiction, industry-specific risks, organisational risk appetite, and technical infrastructure**. For example, a law firm operating in London will need to tailor the framework quite differently from a manufacturing multinational in the United States — the former might emphasize data privacy regulations under UK GDPR and client confidentiality risks, while the latter focuses on operational safety controls and supply chain security requirements. 
    
    As such, contextualisation helps to ensure you get the maximum benefit from the framework, but is not strictly necessary.

---

## Getting Started

There is a lot to unpack in the ARC framework. To help you along, we provide resources and detailed walkthroughs for two roles: (1) governance teams and (2) AI developers. 

### For Governance Teams
**Your Goal:** Understand how to implement the ARC framework for your organisation

**How to get started:**

1. Adapt capability taxonomy for your domain
2. Contextualise risk mappings to your jurisdiction and industry
3. Map controls to your technical infrastructure
4. Define risk relevance criteria matching your risk appetite
5. Pilot with real systems and gather feedback
6. Roll out organisation-wide with training and templates

→ [Complete organisational adoption guide](for-governance-teams.md)

### For AI Developers
**Your Goal:** Understand how to apply ARC Framework to your agentic AI system

**How to get started:**

1. Identify capabilities by mapping your system's autonomous functions
2. Evaluate risks using the framework's risk register and relevance criteria
3. Implement controls by contextualising recommended technical controls
4. Assess residual risks and document remaining mitigation strategies

→ [Complete system assessment guide](for-ai-developers.md)