# Overview of the ARC Framework

## Introduction

OpenAI dubbed 2025 the “year of the AI agent” [^1], a prediction that quickly proved prescient. Major AI companies launched increasingly powerful systems that allowed large language model (LLM) agents to reason, plan, and autonomously execute tasks such as code development or web browsing. However, this surge in agent-driven AI innovation also brought renewed scrutiny to these systems’ safety and security risks.

Recent research [^2][^3][^4] demonstrated that LLM agents are more prone to unsafe behaviors than their base models. Moreover, governing agentic systems presents unique challenges compared to traditional LLM systems — they possess autonomy to execute a wide variety of actions, thereby introducing a significantly broader range of risks. This makes comprehensive identification, assessment, and mitigation more challenging, thus hindering effective organizational governance. Although conducting in-depth and customized risk assessments for each agentic system is possible as an interim measure, it is unsustainable in the long run.

The **Agentic Risk & Capability (ARC)** framework aims to tackle this problem as a **technical governance framework for identifying, assessing, and mitigating the safety and security risks of agentic systems**.

It examines **where and how risks may emerge**, **contextualizes the agentic system’s risks** given its domain, use case, and organizational context, and **recommends practical and technical controls** for mitigating these risks. While the ARC framework is not a panacea for the complex challenges of governing agentic systems, it offers a strong foundation upon which organizations can manage the plethora of risks in a systematic, scalable, and adaptable manner.

---

## Existing Literature on Agentic AI Governance

Although regulatory frameworks such as the **EU AI Act** [^5] and the **NIST Risk Management Framework** [^6] articulate clear overarching principles and guidelines for managing AI risks, they do not examine specific technical measures for identifying, assessing, and managing risks.
Our paper aims to contribute to the **technical AI governance** field by developing “technical analysis and tools for supporting the effective governance of AI” [^7].

For agentic AI, **Raza et al.** adapted the **AI Trust, Risk, and Security Management (TRiSM)** framework to LLM-based multi-agent systems [^8]. It provides generalized metrics and controls across a spectrum of risks but does not tackle the practical problems of contextualizing risks for a given agentic system to be deployed.

Another approach, proposed by **Engin and Hand**, is *dimensional governance*, which tracks AI systems along three dynamic axes — **decision authority**, **process autonomy**, and **accountability** — and introduces controls when systems shift across critical thresholds [^9]. While conceptually appealing, its effectiveness relies on accurately quantifying the dimensions and calibrating the thresholds, both of which are difficult to operationalize.

More cybersecurity-oriented frameworks include the **MAESTRO** framework [^10], **OWASP’s** white paper on agentic AI risks [^11], and **NVIDIA’s** taint-tracing approach [^12], which utilize threat modelling to uncover security threats such as data poisoning or agent impersonation. However, these are highly complex — especially for developers untrained in cybersecurity — and the controls rely heavily on human oversight.

### Benchmarks for Assessing Agentic Risks

Benchmarks help to assess how risky agentic systems are. Several **safety and security benchmarks** outline test scenarios or tasks that reveal specific risk behaviours of an agentic system. Examples include **Agent Security Bench** [^13], **CVE-Bench** [^14], **RedCode** [^15], **AgentHarm** [^16], and **AgentDojo** [^17]. These benchmarks assess whether LLMs can complete multi-step cybersecurity attacks or harmful tasks (e.g., fraud), but they do not help developers identify the full range of risks and attack scenarios for their specific applications.

**Tool-based benchmarks**, such as **Gorilla / APIBench** [^18], **ToolSword** [^19], and **ToolEmu** [^20], measure the performance and safety of LLMs in utilizing tools like `bash`, but omit risks unrelated to tool use (e.g., misaligned LLMs).

### Approaches for Mitigating Risks

For mitigating risks, **AI control** has emerged as a paradigm to prevent misaligned AI systems from causing harm [^21]. Rather than relying solely on training techniques to shape model behaviour, AI control focuses on designing mechanisms such as **monitoring** and **human oversight** to constrain AI systems.

Examples include:

* **Progent** and **AgentSpec**, which introduce languages for flexibly expressing privilege-control policies applied at runtime [^22][^23].
* The **UK AI Security Institute** advocates for *AI control levels*, derived from evaluating frontier LLMs’ threat-model-specific capabilities [^24].
* **OpenAI** shares best practices such as constraining the agent’s action spaces and ensuring attributability [^25].
* **Google** emphasizes a hybrid *defense-in-depth* strategy combining deterministic security measures with dynamic, reasoning-based defenses [^26].
* **Beurer-Kellner et al.** propose six design patterns for building AI agents with provable resistance to prompt injections [^27].

However, these works are either too narrow (specific to particular applications) or too broad (high-level, conceptual) to be effectively operationalized within organizations.

Here’s your **LaTeX section converted cleanly into Markdown**, following the same structure and stylistic conventions as your earlier sections — with in-text citations formatted for footnotes and clear typographic hierarchy.

---

## Capabilities of an Agentic System

Effective governance requires **distinguishing between safer and riskier systems** and implementing a differentiated approach to manage them. Applied to agentic AI governance, this means that beyond analyzing the *components* of an agent (i.e., the LLM, instructions, tools, and memory) and the *design* of the agentic system (i.e., architecture, access controls, and monitoring),
the **ARC framework** adopts the **novel approach of also analysing agentic AI systems by their capabilities.**

### Defining Capabilities

**Capabilities refer to the actions that an agentic system can autonomously execute using the tools and resources it has access to** — for example, running code, searching the Internet, or modifying documents. This concept complements that of affordances, as defined by *Gaver* [^28], which are the properties of the external environment that enable actions. In our view, the **components** and **design** of agentic systems are **affordances**, while executing code or altering agent permissions are **capabilities**. Addressing both affordances and capabilities is essential for the effective governance of agentic systems.

### Why the Capability Lens Matters

There are three key advantages of adopting a **capability lens** in agentic AI governance.

1. **Capabilities offer a more holistic unit of analysis than individual tools.**
   There are numerous tools that facilitate similar actions (e.g., Google SERP, Serper, SerpAPI, Perplexity Search API), and conversely, a single tool can enable a wide array of actions (e.g., GitHub’s Model Context Protocol (MCP) server, which can commit code or read pull requests). Given the diversity and rapid evolution of MCPs, **prescribing specific controls for each tool would be too granular and risk becoming obsolete, inconsistent, or overly restrictive**.

2. **A capability lens enables scalable, differentiated treatment.**
   Systems with more capabilities are inherently riskier and require more stringent controls, especially when those capabilities have significant operational or safety impacts.
   Deconstructing a system into its constituent capabilities ensures that **riskier systems receive greater scrutiny, while low-risk systems are governed with a lighter touch**.

3. **A capability-based framing is intuitive and accessible.**
   Risks arising from *actions* are easier for laypersons to grasp, improving the contextualisation and communication of risks across an organization. Technical approaches often risk being esoteric, which hampers adoption and limits flexibility. By being more accessible, **the capability lens empowers organizations to adapt governance frameworks more flexibly to new developments and emerging risks**.

## Overview of the ARC Framework

The diagram below provides a conceptual overview of the entire ARC Framework, which we will now go through in detail.

<img src="../../assets/arc-overview.png" alt="ARC Overview" style="width: min(900px, 80%); display: block; margin: 0 auto;">


[^1]: Hamilton, E. (2025, January). *2025 is the year of AI agents, OpenAI CPO says.* Axios. [https://www.axios.com/2025/01/23/davos-2025-ai-agents](https://www.axios.com/2025/01/23/davos-2025-ai-agents)

[^2]: Chiang, C.-H., et al. (2025). *Harmful Helper: Perform Malicious Tasks? Web AI Agents Might Help.* ICLR 2025 Workshop on Building Trust in Language Models and Applications. [https://openreview.net/forum?id=4KoMbO2RJ9](https://openreview.net/forum?id=4KoMbO2RJ9)

[^3]: Kumar, A., et al. (2025). *Aligned LLMs Are Not Aligned Browser Agents.* ICLR 2025. [https://openreview.net/forum?id=NsFZZU9gvk](https://openreview.net/forum?id=NsFZZU9gvk)

[^4]: Yu, C., & Papakyriakopoulos, O. (2025). *Safety Devolution in AI Agents.* ICLR 2025 Workshop on Human-AI Coevolution. [https://openreview.net/forum?id=7nJmuFFkWd](https://openreview.net/forum?id=7nJmuFFkWd)

[^5]: European Parliament & Council (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).* [https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)

[^6]: National Institute of Standards and Technology (2023). *NIST AI Risk Management Framework Playbook.* [https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook)

[^7]: Reuel, A., Bucknall, B., Casper, S., et al. (2025). *Open Problems in Technical AI Governance.* arXiv:2407.14981. [https://arxiv.org/abs/2407.14981](https://arxiv.org/abs/2407.14981)

[^8]: Raza, S., Sapkota, R., Karkee, M., & Emmanouilidis, C. (2025). *TRiSM for Agentic AI: A Review of Trust, Risk, and Security Management in LLM-based Agentic Multi-Agent Systems.* arXiv:2506.04133. [https://arxiv.org/abs/2506.04133](https://arxiv.org/abs/2506.04133)

[^9]: Engin, Z., & Hand, D. (2025). *Toward Adaptive Categories: Dimensional Governance for Agentic AI.* arXiv:2505.11579. [https://arxiv.org/abs/2505.11579](https://arxiv.org/abs/2505.11579)

[^10]: Huang, Y., et al. (2025). *On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents.* arXiv:2408.00989v3. [https://arxiv.org/abs/2408.00989v3](https://arxiv.org/abs/2408.00989v3)

[^11]: OWASP (2025). *Agentic AI – Threats and Mitigations.* [https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)

[^12]: Harang, R., et al. (2025). *Agentic Autonomy Levels and Security.* NVIDIA Developer Blog. [https://developer.nvidia.com/blog/agentic-autonomy-levels-and-security](https://developer.nvidia.com/blog/agentic-autonomy-levels-and-security/)

[^13]: Zhang, H., et al. (2025). *Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents.* arXiv:2410.02644. [https://arxiv.org/abs/2410.02644](https://arxiv.org/abs/2410.02644)

[^14]: Zhu, Y., et al. (2025). *CVE-Bench: A Benchmark for AI Agents’ Ability to Exploit Real-World Web Application Vulnerabilities.* arXiv:2503.17332. [https://arxiv.org/abs/2503.17332](https://arxiv.org/abs/2503.17332)

[^15]: Guo, Z., et al. (2024). *RedCode: Risky Code Execution and Generation Benchmark for Code Agents.* NeurIPS 2024 Datasets and Benchmarks. [https://proceedings.neurips.cc/paper_files/paper/2024/hash/bfd082c452dffb450d5a5202b0419205-Abstract-Datasets_and_Benchmarks_Track.html](https://proceedings.neurips.cc/paper_files/paper/2024/hash/bfd082c452dffb450d5a5202b0419205-Abstract-Datasets_and_Benchmarks_Track.html)

[^16]: Andriushchenko, M., et al. (2025). *AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents.* arXiv:2410.09024. [https://arxiv.org/abs/2410.09024](https://arxiv.org/abs/2410.09024)

[^17]: Debenedetti, E., et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* arXiv:2406.13352. [https://arxiv.org/abs/2406.13352](https://arxiv.org/abs/2406.13352)

[^18]: Patil, S. G., Zhang, T., Wang, X., & Gonzalez, J. E. (2023). *Gorilla: Large Language Model Connected with Massive APIs.* arXiv:2305.15334. [https://arxiv.org/abs/2305.15334](https://arxiv.org/abs/2305.15334)

[^19]: Ye, J., et al. (2024). *ToolSword: Unveiling Safety Issues of Large Language Models in Tool Learning Across Three Stages.* arXiv:2402.10753. [https://arxiv.org/abs/2402.10753](https://arxiv.org/abs/2402.10753)

[^20]: Ruan, Y., Dong, H., Wang, A., Pitis, S., Zhou, Y., Ba, J., Dubois, Y., Maddison, C. J., & Hashimoto, T. (2024). *Identifying the Risks of LM Agents with an LM-Emulated Sandbox.* arXiv:2309.15817. [https://arxiv.org/abs/2309.15817](https://arxiv.org/abs/2309.15817)

[^21]: Greenblatt, R., Shlegeris, B., Sachan, K., & Roger, F. (2024). *AI Control: Improving Safety Despite Intentional Subversion.* arXiv:2312.06942. [https://arxiv.org/abs/2312.06942](https://arxiv.org/abs/2312.06942)

[^22]: Shi, T., He, J., Wang, Z., Li, H., Wu, L., Guo, W., & Song, D. (2025). *Progent: Programmable Privilege Control for LLM Agents.* arXiv:2504.11703. [https://arxiv.org/abs/2504.11703](https://arxiv.org/abs/2504.11703)

[^23]: Wang, H., Poskitt, C. M., & Sun, J. (2025). *AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents.* arXiv:2503.18666. [https://arxiv.org/abs/2503.18666](https://arxiv.org/abs/2503.18666)

[^24]: Korbak, T., Balesni, M., Shlegeris, B., & Irving, G. (2025). *How to Evaluate Control Measures for LLM Agents? A Trajectory from Today to Superintelligence.* arXiv:2504.05259. [https://arxiv.org/abs/2504.05259](https://arxiv.org/abs/2504.05259)

[^25]: Shavit, Y., Agarwal, S., Brundage, M., Adler, S., O’Keefe, C., Campbell, R., Lee, T., Mishkin, P., Eloundou, T., Hickey, A., Slama, K., Ahmad, L., McMillan, P., Beutel, A., Passos, A., Robinson, D. G., and colleagues. (2025). *Practices for Governing Agentic AI Systems.* OpenAI. [https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf)

[^26]: Diaz, S., Kern, C., & Olive, K. (2025). *Google’s Approach for Secure AI Agents.* [https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)

[^27]: Beurer-Kellner, L., Buesser, B., Creţu, A.-M., Debenedetti, E., Dobos, D., Fabian, D., Fischer, M., Froelicher, D., Grosse, K., Naeff, D., Ozoani, E., Paverd, A., Tramèr, F., & Volhejn, V. (2025). *Design Patterns for Securing LLM Agents against Prompt Injections.* arXiv:2506.08837. [https://arxiv.org/abs/2506.08837](https://arxiv.org/abs/2506.08837)

[^28]: Gaver, W. W. (1991). *Technology Affordances.* In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '91)*, pp. 79–84. ACM. [https://doi.org/10.1145/108844.108856](https://doi.org/10.1145/108844.108856)