# Controls for agentic systems

!!! abstract "Page Summary"

    This page defines technical controls for mitigating risks in agentic systems, organised into three tiers: Cardinal (Level 0 - fundamental requirements), Standard (Level 1 - adopt or adapt), and Best Practice (Level 2 - good to consider, especially for high-risk systems). Each control aims to either reduce the potential impact of failures or decrease the likelihood of specific failures occurring.

Controls are essential to mitigate risks to an acceptable level. Within the **Risk Register**, each risk comes with a set of **recommended technical controls** that aim to either:

1. **Reduce the potential impact** by limiting the scope or severity of a failure, or
2. **Decrease the likelihood** of a specific failure occurring.

---

## Controls in the Risk Register

Identifying the wide range of risks from agentic systems is only just the start - the next part is curating a list of effective technical controls to mitigate these risks. This section describes how to develop controls for the Risk Register.

### 🧭 Guiding principles

To ensure controls remain relevant, meaningful, and effective for tackling agentic risks, we outline three key guiding principles for developing controls: 

1. **Make controls actionable, composable, and measurable.** Controls must clearly state what actions are to be taken on what, by whom, and by when. Each control also needs to be written modularly, so they can be combined with other controls, and be easy to validate when it is implemented correctly. Writing controls in an active voice and using imperatives will help.
2. **Map each control to at least one risk in the Risk Register.** Controls must be useful in mitigating the identified risks in the Risk Register. Even general hygiene controls should be linked to the appropriate baseline risks (either from the components or design of the agentic system). 
3. **Build or recommend tools for implementing these controls.** Controls are useful in defining what standards need to be met, but they can also be very onerous on developers. Tools help to reduce the compliance workload, and recommending suitable open-source tools can make these controls more tolerable.

??? question "Is it possible to have a risk without a control in the Risk Register?"

    Yes! This is to document novel risks where there are no known effective controls, and to ensure that these risks are accounted for in the agentic system's risk assessment. As there are no recommended controls, development teams must decide whether the residual risk (see below) is too much to accept.

??? question "Is it possible for a single control to tackle multiple risks?"

    Yes! This is because several risks may share the same failure cause. For example, prompt injection guardrails are likely to be useful to deal with prompt injection attacks from the memory component, website, or internal files.

### 🔨 Developing controls

First, we start by analysing the risk for its failure cause and harm, and consider how to address the risk by reducing either its likelihood of occurring or the adverse impact if it does occur. Some helpful questions for brainstorming possible controls include:

* How can we **limit the blast radius** by restricting the resources the agent or system has access to?
* How can we **blunt the effectiveness of attacks** by preventively blocking potential attacks?
* How can we **make failures more detectable** so we can catch errors early before it cascades or escalates?
* How can we **deter attackers from probing our system** for potential weaknesses?

It is helpful to read up on the literature on AI safety and security to understand what the common mitigation measures are and how effective they are in managing agentic risks.

### 📶 Control levels { #control-levels }

Next, we categorise the control into three levels based on its criticality:

* **Level 0: Cardinal control** - fundamental requirement that must be adopted as is; waived only when the capability or component it concerns is not present in the system
* **Level 1: Standard control** - adopt or adapt meaningfully and sensibly
* **Level 2: Best practice control** - good to consider, especially for high-risk systems

!!! info "When does a Level 0 control apply?"

    A Level 0 control is mandatory for every system in which its risk is **applicable**. A risk is applicable when what it arises from is present:

    - a **baseline** risk arises only from components and design elements that every agentic system has, so it always applies;
    - a risk that arises from a **conditional component** (Memory, Protocols) applies when the system has that component, and is assumed to apply when the assessment does not say;
    - a **capability** risk applies when the system has the capability, and, where the risk states a minimum authority, uses it at that authority or above;
    - a risk that arises from a **combination rule** applies when the rule is present or possible for the system's capabilities.

    Impact and likelihood scoring, which organisations use to prioritise effort, **never waives a Level 0 control**: a risk that scores below the relevance threshold still carries its Level 0 controls. Scoring governs Levels 1 and 2 only.

    Most of what used to need a waiver is now decided by the rules above. A Level 0 control can still be **waived when the specific thing it concerns is not present** in the system, for example a control on agent-generated code in a system that generates none, or the control of a combination rule when the assessor shows that one of its roles is absent. Record the waiver with the evidence. This is the single definition of the levels; the implementation guides restate it.

!!! info "What each control records"

    Besides its statement, level and guidance, every control in the register says:

    | Field | Meaning |
    | --- | --- |
    | **Enforced in** | Where the control bites: the *prompt* (instructions the model may not follow), the *model* or a model-based component, the *harness* (the code around the model, such as the tool layer and approval gates), the *infrastructure* beneath the agent (network, identity, sandboxes, storage, logging), or the *organisation* (people and process). One or two, the main one first |
    | **Owner** | The role that normally implements and maintains it: developer, platform, security, governance or business |
    | **Phase** | When in the lifecycle it is put in place or exercised: design, build, deploy, operate, retire |
    | **Evidence** | The artefact a reviewer can inspect to see that the control is in place |
    | **Test** | How to check that it works, as an action with an expected result |

    A control enforced only in the prompt is the weakest kind, because the model may not comply. A control enforced in the harness or the infrastructure can often be provided once by a shared platform; an organisation's [overlay](../implementation/for-governance-teams.md#keeping-your-version-as-an-overlay) marks those.

!!! info "Levels that depend on context"

    A control's level can be stricter when a capability is used with more authority. The register states this on the control (`level_when`). In register 2.0:

    - **CTRL-0042** (human confirmation before high-impact or irreversible tool actions) is Level 1, and Level 0 when a capability acts alone with effects that are irreversible and reach outside the organisation.
    - **CTRL-0043** (log all tool selection decisions and invocations) is Level 1, and Level 0 when a capability acts alone.

    See [how a capability is used](elements.md#context-how-a-capability-is-used) for the definitions. An organisation can add its own conditions when it contextualises the register.

??? example "Example of controls targeting a specific risk"

    **Risk:** RISK-034 "Prompt injection via malicious websites" → **Safety and security risk** caused by **external manipulation** of the **Internet and Search Access** capability.

    **Recommended Controls:**

    1. **CTRL-0060** [Level 1] Implement escape filtering before incorporating web content into prompts → *neutralises injected instructions before they reach the agent's context*
    2. **CTRL-0061** [Level 1] Use structured retrieval APIs for web searches rather than web scraping → *reduces exposure to malicious web content and injection vectors*
    3. **CTRL-0062** [Level 0] Implement input guardrails to detect prompt injection and adversarial attacks → *reduces likelihood of prompt injection attack succeeding*

Our [Interactive Risk Register](risk-register.md) provides **recommended controls** for each of the 66 documented risks to help organizations get started.

---

## Residual Risks

Agentic AI and LLMs are evolving rapidly, and no list of technical controls can credibly claim to eliminate all potential threats. It is therefore crucial to evaluate the **residual risk** — the remaining risk after controls have been applied — to uncover gaps and assess the overall level of risk in the agentic system. If the residual risk is deemed unacceptable, further measures, both **technical** and **organisational**, must be implemented to reduce it to an acceptable level.

However, identifying residual risks is inherently difficult, as it depends heavily on the specifics of the agentic system. Common sources include:

* **Inherent weaknesses** of technical controls (e.g., prompt-injection guardrails trained on past jailbreaks may not generalize to novel attacks).
* **Composite risks** that emerge from the interaction of two or more capabilities within the system.
* **Human factors** including social engineering attacks targeting developers or operators, credential compromise, or misconfiguration during deployment.
* **Context-specific risks** unique to the deployment domain (e.g., medical, financial, legal) that are not adequately addressed by general-purpose controls.

To adequately address residual risks, organisations can consider implementing a **layered risk management strategy** that combines technical controls with organisational measures. This includes establishing **human-in-the-loop oversight** for high-stakes decisions, implementing **continuous monitoring and anomaly detection** to identify unexpected behaviours, and fostering a **culture of responsible AI development** where teams proactively identify and escalate emerging risks. Additionally, organisations should stay informed about the evolving agentic AI landscape and periodically reassess their risk posture as capabilities, architectures, and deployment contexts change over time.