# :simple-lightning: Why the ARC Framework?

In this section, we explain why we developed the ARC framework, how it fits into the existing literature, and why we chose to focus on capabilities specifically.

## Motivation

OpenAI dubbed 2025 the "year of the AI agent”,[^1] a prediction which quickly proved prescient. Within the first few months, major companies launched increasingly powerful systems that allow large language model (LLM) agents to reason, plan, and autonomously execute tasks.[^2] However, this surge in agent-driven AI innovation also brought renewed scrutiny to these systems' safety and security risks. Recent research has shown that LLM agents are often more prone to unsafe behaviors than their base models,[^3] partly due to their growing autonomy and expanded capabilities through tool integration. As the ecosystem for agentic systems, including frameworks like Model Context Protocol[^4], continues to mature, there is greater urgency to establish robust governance mechanisms. 

## Existing literature

While regulatory frameworks such as the EU AI Act[^5] and NIST Risk Management Framework[^6] provide overarching principles and guidelines to manage AI risks, they are too high-level and conceptual for organizations to meaningful translate into governance policies.

To measure agentic AI risks, task-based frameworks have emerged to evaluate the ability of LLMs to execute malicious tasks. Benchmarks like CVEBench,[^7] CyBench,[^8] AgentHarm,[^9] and AgentDojo[^10] help to assess whether LLMs can complete cybersecurity attacks or harmful tasks like fraud. In these settings, agentic systems are required to not only comply with but also complete multi-step malicious requests. However, the ever-evolving landscape of attack scenarios make it difficult for organizations to constantly maintain a collection of harmful tasks and test their systems against them. This is also impractical when organizations deploy several agentic AI systems with differing goals.

Other works focus on evaluating the risks of individual tools that agents have access to. Tool-based benchmarks, like APIBench,[^11] ToolSword,[^12], and ToolEmu[^13], evaluate the performance and safety of LLMs in utilizing and interacting with tools like `bash`. However, as more tools are developed, tool-based approaches are too granular and difficult to maintain and operationalize at the organization level. 

 A potential middle ground could be to conduct risk evaluations of agents themselves. OpenAI breaks down an agent into three design choices - model, tools, and instructions, recommending interventions at each of these levels, including best practices like constraining the agent's action spaces, setting default behaviors and ensuring attributabilty.[^14] Similarly, Progent introduces a language for flexibly expressing privilege control policies applied during execution for each agent,[^15] while the UK AI Security Institute proposes a framework for evaluating each agent's capability profile across different dimensions.[^16] However, identifying risk at the individual agent level makes it difficult for organizations to prescriptively and preemptively manage risks across many different teams and systems. Hence, we build on these frameworks and introduce a structured taxonomy of ***capabilities*** that agents can acquire. This enables organizations to operationalize agentic risk management by establishing and maintaining a taxonomy of risk categories and controls at the capabilities level, while giving teams the flexibility in how to implement the controls. 

 <!--- Footnotes below --->

[^1]: Hamilton, E. 2025 is the year of ai agents, OpenAI CPO says. Axios, January 2025. URL <https://www.axios.com/2025/01/23/davos-2025-ai-agents>. Accessed: 2025-05-11.
[^2]: d
[^3]: See the following articles: (i) Chiang et al. Harmful helper: Perform malicious tasks? web AI agents might help. In ICLR 2025 Workshop on Building Trust in Language Models and Applications, 2025. URL <https://openreview.net/forum?id=4KoMbO2RJ9>, (ii) Kumar et al. Aligned LLMs are not aligned browser agents. In The Thirteenth International Conference on Learning Representations, 2025. URL <https://openreview.net/forum?id=NsFZZU9gvk>, (iii) Yu, C. and Papakyriakopoulos, O. Safety devolution in AI agents. In ICLR 2025 Workshop on Human-AI Coevolution, 2025. URL <https://openreview.net/forum?id=7nJmuFFkWd>.
[^4]: Anthropic. Model Context Protocol (MCP). <https://docs.anthropic.com/en/docs/agents-and-tools/mcp>, 2024. Accessed: 2025-05-11.
[^5]: European Parliament and Council of the European Union. Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 Laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). <https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng>, 2024. Accessed: 2025- 05-11.
[^6]: National Institute of Standards and Technology. NIST AI Risk Management Framework Playbook. <https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook>, 2023. Accessed: 2025-05-11.
[^7]: Zhu et al. CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities . <https://arxiv.org/abs/2503.17332>, 2025. Accessed: 2025-05-11.
[^8]: cybench
[^9]: agentharm
[^10]: agentdojo
[^11]: Patil et al. Gorilla: Large Language Model Connected with Massive APIs. <https://arxiv.org/abs/2305.15334>, 2023. Accessed: 2025-05-11.
[^12]: Ye et al. ToolSword: Unveiling Safety Issues of Large Language Models in Tool Learning Across Three Stages. <https://arxiv.org/abs/2402.10753>, 2024. Accessed: 2025-05-11.
[^13]: Ruan et al. Identifying the Risks of LM Agents with an LM-Emulated Sandbox. <https://arxiv.org/abs/2309.15817>, 2023. Accessed: 2025-05-11.
[^14]: OpenAI. A practical guide to building agents. Technical report, OpenAI, 2025a. URL <https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf>. Accessed: 2025-05-11.
[^15]: Shi et al. Progent: Programmable Privilege Control for LLM Agents. <https://arxiv.org/abs/2504.11703>, 2025. Accessed: 2025-05-11.
[^16]: Korbak et al. How to evaluate control measures for LLM agents? A trajectory from today to superintelligence. <https://arxiv.org/abs/2504.05259>, 2025. Accessed: 2025-05-11.