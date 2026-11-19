# Introducing the ARC Framework

!!! abstract "Page Summary"

    This page explains the design rationale and theoretical foundation of the ARC Framework, including its positioning within existing AI governance and agentic AI safety literature. It covers the framework's motivation, the capability-based approach, and comparison to related work in the field.

## Overview of the ARC Framework

The diagram below provides a conceptual overview of the entire ARC Framework, which we will go through in detail in the following sections.

<figure style="text-align: center;">
  <img src="../../assets/arc-overview.png" alt="ARC Overview" style="width: min(900px, 80%); display: block; margin: 0 auto;">
</figure>


---

## Governing agentic systems

Since 2025, major AI providers have deployed **LLM agents with autonomous reasoning, planning, and task execution capabilities**. Examples include [OpenAI's GPT-5.2](https://openai.com/index/introducing-gpt-5-2/) (achieving state-of-the-art results on SWE-Bench Pro and Terminal-Bench 2.0 for software engineering), [Google's Gemini 3 Pro](https://www.itpro.com/technology/artificial-intelligence/google-launches-flagship-gemini-3-model-and-google-antigravity-a-new-agentic-ai-development-platform) (reaching top scores across major AI benchmarks in multimodal reasoning), [Anthropic's Claude Opus 4.5](https://www.itpro.com/technology/artificial-intelligence/anthropic-announces-claude-opus-4-5-the-new-ai-coding-frontrunner) (scoring 80.9% on SWE-Bench Verified), and Singapore-based [Manus](https://en.wikipedia.org/wiki/Manus_%28AI_agent%29) (among the first fully autonomous AI agents capable of independent reasoning and dynamic planning). 

Because agentic systems can **plan and execute actions via tools (not just generate text)**, they introduce distinct safety and security risks and a harder governance problem for organisations deploying them. Concretely, autonomy + tool access shifts the risk profile from “bad text output” to **real-world actions**:

- **Destructive or unauthorised actions**: agents can take irreversible operational steps (e.g., deleting or modifying critical resources) when permissions are broad or approvals are bypassed (case study: [Replit’s AI coding assistant reportedly wiped a production database during a code freeze](https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-coding-platform-goes-rogue-during-code-freeze-and-deletes-entire-company-database-replit-ceo-apologizes-after-ai-engine-says-it-made-a-catastrophic-error-in-judgment-and-destroyed-all-production-data)).
- **Command misinterpretation at the system boundary**: agents operating terminals/filesystems can translate ambiguous intent into catastrophic OS-level commands (case study: [an “Antigravity” agent reportedly deleted a developer’s D: drive while “clearing cache”](https://www.techradar.com/ai-platforms-assistants/googles-antigravity-ai-deleted-a-developers-drive-and-then-apologized)).
- **Adversarial manipulation of agent tool-use**: attackers can shape what tools an agent calls (or how it interprets tool interfaces), causing harmful downstream decisions (case study: [FuncPoison—poisoning function/tool libraries to hijack multi-agent behaviour](https://arxiv.org/abs/2509.24408)).

Governing agentic systems presents unique challenges — their autonomy to execute diverse actions introduces substantially broader risk profiles. **The space of possible tool calls, action sequences, and environment interactions is large and often context-dependent, making failure modes harder to anticipate and audit than for text-only systems**. Whilst in-depth risk assessments for each system are possible, doing so for every deployment, configuration change, and new capability does not scale. 

The **Agentic Risk & Capability (ARC) framework addresses this challenge as a technical governance framework for identifying, assessing, and mitigating safety and security risks in agentic systems**. The framework examines where and how risks emerge, contextualises risks given domain and use case, and recommends technical controls for mitigation. Whilst not comprehensive, it provides a systematic, scalable foundation for managing agentic AI risks.

??? note "Existing Literature on Agentic AI Governance"

    **High-level regulatory frameworks**, such as the [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) and [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook), are effective at outlining key principles for managing AI risks and provide a shared vocabulary and baseline expectations across organisations, but they lack specific focus on agentic AI and actionable technical measures for risk identification, assessment, and management.

    We position ARC within **technical AI governance**: developing practical analysis and tools that support effective governance (see [Reuel et al., 2025](https://arxiv.org/abs/2407.14981)). Closely related work includes *TRiSM for agentic AI* ([Raza et al., 2025](https://arxiv.org/abs/2506.04133)) and *dimensional governance* ([Engin & Hand, 2025](https://arxiv.org/abs/2505.11579)), which frames oversight along decision authority, process autonomy, and accountability.
 
    **Cybersecurity-oriented frameworks** ([MAESTRO](https://arxiv.org/abs/2408.00989v3), [OWASP Agentic AI – Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/), [NVIDIA: Agentic Autonomy Levels and Security](https://developer.nvidia.com/blog/agentic-autonomy-levels-and-security)) apply threat modelling to agentic systems (e.g., data poisoning, tool compromise, agent impersonation). While useful and comprehensive, they can be complex for developers untrained in cybersecurity and often assume substantial human oversight.

    More broadly, technical AI governance is supported by a growing toolkit of **benchmarks** and **engineering controls**—and we aim to be consistent with this wider ecosystem:

    - **Benchmarks (evaluation support)**: safety/security suites such as [Agent Security Bench](https://arxiv.org/abs/2410.02644), [CVE-Bench](https://arxiv.org/abs/2503.17332), [RedCode](https://proceedings.neurips.cc/paper_files/paper/2024/hash/bfd082c452dffb450d5a5202b0419205-Abstract-Datasets_and_Benchmarks_Track.html), [AgentHarm](https://arxiv.org/abs/2410.09024), and [AgentDojo](https://arxiv.org/abs/2406.13352); and tool-use benchmarks such as [Gorilla/APIBench](https://arxiv.org/abs/2305.15334), [ToolSword](https://arxiv.org/abs/2402.10753), and [ToolEmu](https://arxiv.org/abs/2309.15817).
    - **Controls (mitigation support)**: *AI control* approaches emphasise monitoring and oversight (see [Greenblatt et al., 2024](https://arxiv.org/abs/2312.06942)); policy/enforcement mechanisms like [Progent](https://arxiv.org/abs/2504.11703) and [AgentSpec](https://arxiv.org/abs/2503.18666); control-evaluation trajectories (see [Korbak et al., 2025](https://arxiv.org/abs/2504.05259)); and practitioner guidance from [OpenAI](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf), [Google](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/), and prompt-injection defences (see [Beurer-Kellner et al., 2025](https://arxiv.org/abs/2506.08837)).

    ARC Framework complements these approaches by offering a scalable way to identify relevant risks and select appropriate controls based on an agent's **capabilities** and deployment context. For a more detailed literature review, please read our [technical paper](../assets/ARC_Framework-Paper-IASEAI_2026.pdf). For entry-by-entry mappings between the ARC register and the OWASP Top 10 for Agentic Applications, the CSA Securing Agentic AI Addendum, and IMDA's Model AI Governance Framework for Agentic AI, see [Crosswalks](crosswalks.md).

---

## What are Capabilities?

**Capabilities refer to actions an agentic system can autonomously execute using available tools and resources** — they represent the **combination of both the action itself and the specific tool or resource that enables it**. For example, "running code" is a capability that pairs the action (executing) with the tool (a Python interpreter or terminal access); "searching the Internet" pairs the action (querying) with the tool (web search APIs like Google SERP or Perplexity); "modifying documents" pairs the action (editing) with the resource (filesystem access or document APIs like Google Docs). 

A capability only exists when both the action and the enabling tool/resource are present — an agent with terminal access but no permission to execute commands, or with search APIs but no network connectivity, lacks the corresponding capability. 

??? question "How does this relate to affordances?"

    You can see capabilities as a complement for *affordances* ([Gaver, 1991](https://doi.org/10.1145/108844.108856)), which are environmental properties enabling actions. Loosely speaking, in the ARC Framework, components and design are affordances, whilst executing code or altering permissions are capabilities. Addressing both is essential for effective governance.

## Why capabilities?

Effective governance requires distinguishing between safer and riskier systems to implement differentiated management. Beyond analysing agent *components* (LLM, instructions, tools, memory) and *design* (architecture, access controls, monitoring), the **ARC Framework adopts the novel approach of analysing systems by their capabilities**.

Three advantages of adopting a **capability lens** in agentic AI governance:

1. **Capabilities offer a more holistic unit of analysis than individual tools.**
   Numerous tools facilitate similar actions (e.g., Google SERP, Serper, SerpAPI, Perplexity Search API), whilst single tools enable diverse actions (e.g., GitHub's MCP server can commit code or read pull requests). Given MCP diversity and rapid evolution, prescribing tool-specific controls risks becoming obsolete, inconsistent, or overly restrictive.

2. **A capability lens enables scalable, differentiated treatment.**
   Systems with more capabilities are inherently riskier and require more stringent controls, especially for capabilities with significant operational or safety impacts. Capability decomposition ensures riskier systems receive greater scrutiny whilst low-risk systems are governed lightly.

3. **A capability-based framing is intuitive and accessible.**
   Risks from *actions* are easier to grasp than technical abstractions, improving risk contextualisation and communication across organisations. The capability lens enables flexible adaptation to new developments and emerging risks.