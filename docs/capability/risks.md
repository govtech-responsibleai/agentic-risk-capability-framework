# Risks

Similar to what we did for baseline components and risks, we identify safety and security risks that may arise from the specific [capabilities identified in the previous section](../capabilities/index.md). For each risk, we provide an academic paper, case study, or article which provides more details about the nature of the risk.

| First-level | Second-level | Risk |
|---|---|---|
| Cognitive | Reasoning & Problem-Solving | Becoming ineffective, inefficient, or unsafe due to overthinking[^1] |
| Cognitive | Reasoning & Problem-Solving | Engaging in deceptive behaviour through pursuing or prioritising other goals[^2] |
| Cognitive | Planning & Goal Management | Devising plans that are not effective in meeting the user's requirements[^3] |
| Cognitive | Planning & Goal Management | Devising plans that do not adhere to common sense or implicit assumptions about the user's instructions[^4] |
| Cognitive | Tool Use & Delegation | Assigning tasks incorrectly to other agents[^5] |
| Cognitive | Tool Use & Delegation | Attempting to use other agents maliciously[^6] |
| Cognitive | Tool Use & Delegation | Choosing the wrong tool for the given action or task[^7] |
| Interaction | Natural Language Communication | Generating undesirable content (e.g. toxic, hateful, sexual)[^8] |
| Interaction | Natural Language Communication | Generating unqualified advice in specialised domains (e.g. medical, financial, legal)[^9] |
| Interaction | Natural Language Communication | Generating controversial content (e.g. political, competitors)[^10] |
| Interaction | Natural Language Communication | Regurgitating personally identifiable information[^11] |
| Interaction | Natural Language Communication | Generating non-factual or hallucinated content[^12] |
| Interaction | Natural Language Communication | Generating copyrighted content[^13] |
| Interaction | Multimodal Understanding & Generation | Generating undesirable content (e.g. toxic, hateful, sexual)[^14] |
| Interaction | Multimodal Understanding & Generation | Generating unqualified advice in specialised domains (e.g. medical, financial, legal)[^15] |
| Interaction | Multimodal Understanding & Generation | Generating controversial content (e.g. political, competitors)[^16] |
| Interaction | Multimodal Understanding & Generation | Regurgitating personally identifiable information[^17] |
| Interaction | Multimodal Understanding & Generation | Generating non-factual or hallucinated content[^18] |
| Interaction | Multimodal Understanding & Generation | Generating copyrighted content[^19] |
| Interaction | Official Communications | Making inaccurate promises or statements to the public[^20] |
| Interaction | Official Communications | Sending undesirable content to recipients[^21] |
| Interaction | Official Communications | Sending malicious content to recipients[^22] |
| Interaction | Official Communications | Misleading recipients about the authorship of the communications[^23] |
| Interaction | Official Communications | Sending personally identifiable or sensitive data[^24] |
| Interaction | Agent Communication | Communicating insecurely resulting in man-in-the-middle attacks[^25] |
| Interaction | Agent Communication | Misinterpreting inter-agent messages due to poor formatting or weak protocols[^26] |
| Interaction | Agent Communication | Passing on prompt injection attacks across agents[^27] |
| Interaction | Transactions | Allowing unauthorised transactions[^28] |
| Interaction | Transactions | Increasing the system's vulnerability to attackers exfiltrating credentials for transactions through the agent[^29] |
| Interaction | Internet & Search Access | Opening vulnerabilities to prompt injection attacks via malicious websites[^30] |
| Interaction | Internet & Search Access | Returning unreliable information or websites[^31] |
| Interaction | Computer Use | Opening vulnerabilities to prompt injection attacks[^32] |
| Interaction | Computer Use | Accessing personally identifiable or sensitive data[^33] |
| Operational | Code Execution | Executing poor code[^34] |
| Operational | Code Execution | Executing vulnerable or malicious code[^35] |
| Operational | File & Data Management | Overwriting or deleting database tables or files[^36] |
| Operational | File & Data Management | Overwhelming the database with poor, inefficient, or repeated queries[^37] |
| Operational | File & Data Management | Exposing personally identifiable or sensitive data from databases or files[^38] |
| Operational | File & Data Management | Opening vulnerabilities to prompt injection attacks via malicious data or files[^39] |
| Operational | System Management | Escalating the agent's own privileges[^40] |
| Operational | System Management | Misconfiguring system resources, compromising system integrity and availability[^41] |
| Operational | System Management | Overwhelming the system with poor, inefficient, or repeated requests[^42] |

[^1]: [arXiv:2502.08235](https://arxiv.org/pdf/2502.08235) (arXiv, 2025)
[^2]: [Reasoning Models Dont Say Think](https://www.anthropic.com/research/reasoning-models-dont-say-think) (Anthropic, 2025)
[^3]: [ACL Anthology 2025.naacl-long.93.pdf](https://aclanthology.org/2025.naacl-long.93.pdf) (ACL Anthology, 2025); [arXiv:2402.01622v4](https://arxiv.org/pdf/2402.01622v4) (arXiv, 2024)
[^4]: [Ai Still Lacks Common Sense 70 Years](https://garymarcus.substack.com/p/ai-still-lacks-common-sense-70-years) (Substack COM, 2025)
[^5]: [arXiv:2503.13657](https://arxiv.org/pdf/2503.13657) (arXiv, 2025)
[^6]: [arXiv:2507.06850](https://arxiv.org/html/2507.06850) (arXiv, 2025)
[^7]: [arXiv:2411.13547v2](https://arxiv.org/pdf/2411.13547v2) (arXiv, 2024)
[^8]: [arXiv:2402.04249v2](https://arxiv.org/abs/2402.04249v2?utm_source=chatgpt.com) (arXiv, 2024)
[^9]: [Ai Privacy Risks And Mitigations In Llms](https://www.edpb.europa.eu/system/files/2025-04/ai-privacy-risks-and-mitigations-in-llms.pdf) (Europa EU, 2025)
[^10]: [Ai Models Llms Chatgpt Claude Gemini Partisan Bias Research Study](https://news.stanford.edu/stories/2025/05/ai-models-llms-chatgpt-claude-gemini-partisan-bias-research-study) (Stanford News, 2025)
[^11]: [Ai Privacy Risks And Mitigations In Llms](https://www.edpb.europa.eu/system/files/2025-04/ai-privacy-risks-and-mitigations-in-llms.pdf) (Europa EU, 2025)
[^12]: [arXiv:2309.01219](https://arxiv.org/pdf/2309.01219) (arXiv, 2023)
[^13]: [arXiv:2407.07087](https://arxiv.org/abs/2407.07087) (arXiv, 2024)
[^14]: [arXiv:2311.17600](https://arxiv.org/abs/2311.17600) (arXiv, 2023)
[^15]: [ACL Anthology 2025.findings-acl.981.pdf](https://aclanthology.org/2025.findings-acl.981.pdf) (ACL Anthology, 2025)
[^16]: [S0167268125000241](https://www.sciencedirect.com/science/article/pii/S0167268125000241) (Sciencedirect COM, 2025)
[^17]: [arXiv:2301.13188](https://arxiv.org/abs/2301.13188) (arXiv, 2023)
[^18]: [arXiv:2404.18930](https://arxiv.org/abs/2404.18930) (arXiv, 2024)
[^19]: [arXiv:2301.13188](https://arxiv.org/abs/2301.13188) (arXiv, 2023)
[^20]: [People Buy Brand New Chevrolets For 1 From A Chatgpt Chatbot](https://the-decoder.com/people-buy-brand-new-chevrolets-for-1-from-a-chatgpt-chatbot/?utm_source=chatgpt.com) (The-decoder COM, 2025)
[^21]: [Grok Ai Elon Musk Antisemitism](https://www.washingtonpost.com/technology/2025/07/11/grok-ai-elon-musk-antisemitism/?utm_source=chatgpt.com) (Washingtonpost COM, 2025)
[^22]: [Ai Agent Attacks](https://www.security.com/threat-intelligence/ai-agent-attacks) (Security COM, 2025)
[^23]: [Customer Support Ai Cursor Went Rogue](https://fortune.com/article/customer-support-ai-cursor-went-rogue/) (Fortune COM, 2025)
[^24]: [Ai Privacy Risks And Mitigations In Llms](https://www.edpb.europa.eu/system/files/2025-04/ai-privacy-risks-and-mitigations-in-llms.pdf) (Europa EU, 2025)
[^25]: [arXiv:2502.14847](https://arxiv.org/pdf/2502.14847) (arXiv, 2025)
[^26]: [arXiv:2506.19676](https://arxiv.org/html/2506.19676) (arXiv, 2025)
[^27]: [arXiv:2506.23260](https://arxiv.org/html/2506.23260) (arXiv, 2025)
[^28]: [Ai Agents Vulnerable Financial Attacks](https://www.emergingtechbrew.com/stories/2025/05/29/ai-agents-vulnerable-financial-attacks?utm_source=chatgpt.com) (Emergingtechbrew COM, 2025)
[^29]: [arXiv:2506.01055](https://arxiv.org/pdf/2506.01055) (arXiv, 2025)
[^30]: [Agentic Ai Threats](https://unit42.paloaltonetworks.com/agentic-ai-threats/) (Paloaltonetworks COM, 2025)
[^31]: [Googles Ai Overviews Are Often So Confidently Wrong That Ive Lost All Trust In Them](https://www.techradar.com/computing/artificial-intelligence/googles-ai-overviews-are-often-so-confidently-wrong-that-ive-lost-all-trust-in-them?utm_source=chatgpt.com) (Techradar COM, 2025)
[^32]: [arXiv:2505.13076v1](https://arxiv.org/html/2505.13076v1) (arXiv, 2025); [Indirect Prompt Injection Of Claude Computer Use](https://hiddenlayer.com/innovation-hub/indirect-prompt-injection-of-claude-computer-use/?utm_source=chatgpt.com) (Hiddenlayer COM, 2025)
[^33]: [arXiv:2506.00618v3](https://arxiv.org/html/2506.00618v3) (arXiv, 2025)
[^34]: [Sec25Cycle1 Prepub 742 Spracklen](https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-742-spracklen.pdf) (USENIX, 2025); [2025 07 10 Early 2025 Ai Experienced Os Dev Study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/?utm_source=chatgpt.com) (METR, 2025); [Bfd082C452Dffb450D5A5202B0419205 Paper Datasets_And_Benchmarks_Track](https://proceedings.neurips.cc/paper_files/paper/2024/file/bfd082c452dffb450d5a5202b0419205-Paper-Datasets_and_Benchmarks_Track.pdf?utm_source=chatgpt.com) (NeurIPS Proceedings, 2024)
[^35]: [arXiv:2504.21205v1](https://arxiv.org/html/2504.21205v1) (arXiv, 2025); [arXiv:2501.08200](https://arxiv.org/pdf/2501.08200) (arXiv, 2025)
[^36]: [Pedro_Icse25](https://syssec.dpss.inesc-id.pt/papers/pedro_icse25.pdf) (Inesc-id PT, 2025)
[^37]: [Which Llm Writes The Best Sql](https://www.tinybird.co/blog-posts/which-llm-writes-the-best-sql?utm_source=chatgpt.com) (Tinybird CO, 2025)
[^38]: [Microsoft 365 Copilot Zeroclick Ai](https://www.infosecurity-magazine.com/news/microsoft-365-copilot-zeroclick-ai/?utm_source=chatgpt.com) (Infosecurity-magazine COM, 2025)
[^39]: [Cve 2025 32711 Echoleak Copilot Vulnerability](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability?utm_source=chatgpt.com) (Hackthebox COM, 2025); [Here Come The Ai Worms](https://www.wired.com/story/here-come-the-ai-worms/?utm_source=chatgpt.com) (Wired COM, 2025)
[^40]: [arXiv:2503.15547v1](https://arxiv.org/html/2503.15547v1?utm_source=chatgpt.com) (arXiv, 2025)
[^41]: [97835](https://neurips.cc/virtual/2024/poster/97835?utm_source=chatgpt.com) (NeurIPS, 2024); [arXiv:2507.10584v1](https://arxiv.org/html/2507.10584v1?utm_source=chatgpt.com) (arXiv, 2025)
[^42]: [arXiv:2407.20859v1](https://arxiv.org/html/2407.20859v1) (arXiv, 2085); [Llm102025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/?utm_source=chatgpt.com) (OWASP GenAI, 2025)

| First-level | Second-level | Risk |
| ------ | ------ | ------ |
| Cognitive   | Reasoning & Problem-Solving           | Becoming ineffective, inefficient, or unsafe due to overthinking                                                     |
| Cognitive   | Reasoning & Problem-Solving           | Engaging in deceptive behaviour through pursuing or prioritising other goals                                         |
| Cognitive   | Planning & Goal Management            | Devising plans that are not effective in meeting the user's requirements                                             |
| Cognitive   | Planning & Goal Management            | Devising plans that d...on sense or implicit assumptions about the user's instructions                               |
| Cognitive   | Tool Use & Delegation                 | Assigning tasks incorrectly to other agents                                                                          |
| Cognitive   | Tool Use & Delegation                 | Attempting to use other agents maliciously                                                                           |
| Cognitive   | Tool Use & Delegation                 | Choosing the wrong tool for the given action or task                                                                 |
| Interaction | Natural Language Communication        | Generating undesirable content (e.g. toxic, hateful, sexual)                                                         |
| Interaction | Natural Language Communication        | Generating unqu...advice in specialised domains (e.g. medical, financial, legal)                                     |
| Interaction | Natural Language Communication        | Generating controversial content (e.g. political, competitors)                                                       |
| Interaction | Natural Language Communication        | Regurgitating personally identifiable information                                                                    |
| Interaction | Natural Language Communication        | Generating non-factual or hallucinated content                                                                       |
| Interaction | Natural Language Communication        | Generating copyrighted content                                                                                       |
| Interaction | Multimodal Understanding & Generation | Generating undesirable content (e.g. toxic, hateful, sexual)                                                         |
| Interaction | Multimodal Understanding & Generation | Generating misinformation or non-factual content                                                                     |
| Interaction | Multimodal Understanding & Generation | Generating copyrighted content                                                                                       |
| Interaction | Multimodal Understanding & Generation | Regurgitating personally identifiable information                                                                    |
| Interaction | Transactions                          | Conducting unauthorized transactions                                                                                 |
| Interaction | Transactions                          | Imposing difficult-to-reverse commitments                                                                            |
| Interaction | Transactions                          | Disclosing sensitive data during transactions                                                                        |
| Interaction | Transactions                          | Increasing the system's vulnerability to external actors exfiltrating credentials for transactions through the agent |
| Interaction | Internet & Search Access              | Opening vulnerabilities to prompt injection attacks via malicious websites                                           |
| Interaction | Internet & Search Access              | Returning unreliable information or websites                                                                         |
| Interaction | Computer Use                          | Opening vulnerabilities to prompt injection attacks                                                                  |
| Interaction | Computer Use                          | Accessing personally identifiable or sensitive data                                                                  |
| Operational | Code Execution                        | Executing poor code                                                                                                  |
| Operational | Code Execution                        | Executing vulnerable or malicious code                                                                               |
| Operational | File & Data Management                | Overwriting or deleting database tables or files                                                                     |
| Operational | File & Data Management                | Overwhelming the database with poor, inefficient, or repeated queries                                                |
| Operational | File & Data Management                | Exposing personally identifiable or sensitive data from databases or files                                           |
| Operational | File & Data Management                | Opening vulnerabilities to prompt injection attacks via malicious data or files                                      |
| Operational | System Management                     | Escalating the agent's own privileges                                                                                |
| Operational | System Management                     | Misconfiguring system resources, compromising system integrity and availability                                      |
| Operational | System Management                     | Overwhelming the system with poor, inefficient, or repeated requests                                                 |
