# Controls for agentic systems

Controls are essential to mitigate risks to an acceptable level. Within the **Risk Register**, each risk comes with a set of **recommended technical controls** that aim to either:

1. **Reduce the potential impact** by limiting the scope or severity of a failure, or
2. **Decrease the likelihood** of a specific failure mode occurring.

Below we provide some examples to illustrate how technical controls satisfy either goal.

??? example "Examples of reducing impact" 

    **Example 1: Sandboxing tool access**

    * **Scenario:** An agentic research agent accidentally deletes files.
    * **Control:** Run all file operations in a sandboxed or read-only directory.
    * **Effect:** The failure still happens, but it can’t harm real systems → *reduces impact*.

    **Example 2: Data encryption and backup**

    * **Scenario:** A system breach exposes internal data.
    * **Control:** Encrypt stored data and maintain regular backups.
    * **Effect:** Attackers can’t read stolen data, and recovery is fast → *reduces impact*.

??? example "Examples of decreasing likelihood"

    **Example 1: Input validation and allow-listing**

    * **Scenario:** A prompt injection tries to trick the agent.
    * **Control:** Filter and validate all external inputs; only allow trusted URLs or commands.
    * **Effect:** Reduces chances that malicious inputs even reach the agent → *lowers likelihood*.

    **Example 2: Authentication and least-privilege access**

    * **Scenario:** A compromised account triggers unauthorised actions.
    * **Control:** Enforce strong authentication and give each agent minimal necessary permissions.
    * **Effect:** Makes successful misuse much harder → *lowers likelihood*.

---

## Controls in the Risk Register

Identifying the wide range of risks from agentic systems is only just the start - the next part is curating a list of effective technical controls to mitigate these risks. This section describes how to develop controls for the Risk Register.

### Guiding principles

To ensure controls remain relevant, meaningful, and effective for tackling agentic risks, we outline three key guiding principles for developing controls: 

1. **Make controls actionable, composable, and measurable.** Controls must clearly state what actions are to be taken on what, by whom, and by when. Each control also needs to be written modularly, so they can be combined with other controls, and be easy to validate when it is implemented correctly. Writing controls in an active voice and using imperatives will help.
2. **Map each control to at least one risk in the Risk Register.** Controls must be useful in mitigating the identified risks in the Risk Register. Even general hygiene controls should be linked to the appropriate baseline risks (either from the components or design of the agentic system). 
3. **Build or recommend tools for implementing these controls.** Controls are useful in defining what standards need to be met, but they can also be very onerous on developers. Tools help to reduce the compliance workload, and recommending suitable open-source tools can make these controls more tolerable.

??? question "Is it possible to have a risk without a control in the Risk Register?"

    Yes! This is to document novel risks where there are no known effective controls, and to ensure that these risks are accounted for in the agentic system's risk assessment. As there are no recommended controls, development teams must decide whether the residual risk (see below) is too much to accept.

??? question "Is it possible for a single control to tackle multiple risks?"

    Yes! This is because several risks may share the same failure mode. For example, prompt injection guardrails are likely to be useful to deal with prompt injection attacks from the memory component, website, or internal files.

### Developing controls

First, we start by analysing the risk for its failure mode and hazard, and consider how to address the risk by reducing either its likelihood of occurring or the adverse impact if it does occur. Some helpful questions for brainstorming possible controls include:

* How can we **limit the blast radius** by restricting the resources the agent or system has access to?
* How can we **blunt the effectiveness of attacks** by preventively blocking potential attacks?
* How can we **make failures more detectable** so we can catch errors early before it cascades or escalates?
* How can we **deter attackers from probing our system** for potential weaknesses?

It is helpful to read up on the literature on AI safety and security to understand what the common mitigation measures are and how effective they are in managing agentic risks.

Next, we categorise the control into three levels based on its criticality:

* **Level 0: Cardinal control** - fundamental requirement that cannot be waived, must be adopted as is
* **Level 1: Standard control** - adopt or adapt meaningfully and sensibly
* **Level 2: Best practice control** - good to consider, especially for high-risk systems

??? example "Example of controls targeting a specific risk"

    **Risk:** “Opening vulnerabilities to prompt injection attacks via malicious websites” → **Security and safety risk (all)** caused by **external manipulation** of the **Internet & Search Access capability.**

    **Recommended Controls:**

    1. [Level 1] Implement input guardrails to detect prompt injection or adversarial attacks → *reduces likelihood of prompt injection attack succeeding*
    2. [Level 1] Implement escape filtering before including web content into prompts → *reduces likelihood of prompt injection attack succeeding*
    3. [Level 2] Use structured retrieval APIs for searching the web rather than through web scraping → *reduces likelihood of prompt injection attack occurring*

In our draft Risk Register, we also provide a **tentative list of recommended controls** for each risk to help organizations get started.

---

## Residual Risks

Agentic AI and LLMs are evolving rapidly, and no list of technical controls can credibly claim to eliminate all potential threats. It is therefore crucial to evaluate the **residual risk** — the remaining risk after controls have been applied — to uncover gaps and assess the overall level of risk in the agentic system. If the residual risk is deemed unacceptable, further measures, both **technical** and **organisational**, must be implemented to reduce it to an acceptable level.

However, identifying residual risks is inherently difficult, as it depends heavily on the specifics of the agentic system. Common sources include:

* **Inherent weaknesses** of technical controls (e.g., prompt-injection guardrails trained on past jailbreaks may not generalize to novel attacks).
* **Composite risks** that emerge from the interaction of two or more capabilities within the system.