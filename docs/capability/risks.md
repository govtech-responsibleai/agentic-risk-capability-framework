# Risks

Similar to what we did for baseline components and risks, we identify safety and security risks that may arise from the specific [capabilities identified in the previous section](../capabilities/index.md). For each risk, we provide an academic paper, case study, or article which provides more details about the nature of the risk.

| First-level | Second-level | Risk |
|---|---|---|
| Cognitive | Reasoning & Problem-Solving | <a name="cognitive-reasoning-overthinking"></a>[Becoming ineffective, inefficient, or unsafe due to overthinking](controls.md#cognitive-reasoning-overthinking)[^1] |
| Cognitive | Reasoning & Problem-Solving | <a name="cognitive-reasoning-deceptive-behavior"></a>[Engaging in deceptive behaviour through pursuing or prioritising other goals](controls.md#cognitive-reasoning-deceptive-behavior)[^2] |
| Cognitive | Planning & Goal Management | <a name="cognitive-planning-ineffective-plans"></a>Devising plans that are not effective in meeting the user's requirements[^3] |
| Cognitive | Planning & Goal Management | <a name="cognitive-planning-common-sense"></a>[Devising plans that do not adhere to common sense or implicit assumptions about the user's instructions](controls.md#cognitive-planning-common-sense)[^4] |
| Cognitive | Tool Use & Delegation | <a name="cognitive-tools-incorrect-assignment"></a>[Assigning tasks incorrectly to other agents](controls.md#cognitive-tools-incorrect-assignment)[^5] |
| Cognitive | Tool Use & Delegation | <a name="cognitive-tools-malicious-use"></a>[Attempting to use other agents maliciously](controls.md#cognitive-tools-malicious-use)[^6] |
| Cognitive | Tool Use & Delegation | <a name="cognitive-tools-wrong-choice"></a>Choosing the wrong tool for the given action or task[^7] |
| Interaction | Natural Language Communication | <a name="interaction-nlc-undesirable-content"></a>[Generating undesirable content (e.g. toxic, hateful, sexual)](controls.md#interaction-nlc-undesirable-content)[^8] |
| Interaction | Natural Language Communication | <a name="interaction-nlc-unqualified-advice"></a>[Generating unqualified advice in specialised domains (e.g. medical, financial, legal)](controls.md#interaction-nlc-unqualified-advice)[^9] |
| Interaction | Natural Language Communication | <a name="interaction-nlc-controversial-content"></a>[Generating controversial content (e.g. political, competitors)](controls.md#interaction-nlc-controversial-content)[^10] |
| Interaction | Natural Language Communication | <a name="interaction-nlc-pii-regurgitation"></a>[Regurgitating personally identifiable information](controls.md#interaction-nlc-pii-regurgitation)[^11] |
| Interaction | Natural Language Communication | <a name="interaction-nlc-hallucination"></a>[Generating non-factual or hallucinated content](controls.md#interaction-nlc-hallucination)[^12] |
| Interaction | Natural Language Communication | <a name="interaction-nlc-copyright"></a>[Generating copyrighted content](controls.md#interaction-nlc-copyright)[^13] |
| Interaction | Multimodal Understanding & Generation | <a name="interaction-multimodal-undesirable-content"></a>[Generating undesirable content (e.g. toxic, hateful, sexual)](controls.md#interaction-multimodal-undesirable-content)[^14] |
| Interaction | Multimodal Understanding & Generation | <a name="interaction-multimodal-unqualified-advice"></a>[Generating unqualified advice in specialised domains (e.g. medical, financial, legal)](controls.md#interaction-multimodal-unqualified-advice)[^15] |
| Interaction | Multimodal Understanding & Generation | <a name="interaction-multimodal-controversial-content"></a>[Generating controversial content (e.g. political, competitors)](controls.md#interaction-multimodal-controversial-content)[^16] |
| Interaction | Multimodal Understanding & Generation | <a name="interaction-multimodal-pii-regurgitation"></a>[Regurgitating personally identifiable information](controls.md#interaction-multimodal-pii-regurgitation)[^17] |
| Interaction | Multimodal Understanding & Generation | <a name="interaction-multimodal-hallucination"></a>Generating non-factual or hallucinated content[^18] |
| Interaction | Multimodal Understanding & Generation | <a name="interaction-multimodal-copyright"></a>[Generating copyrighted content](controls.md#interaction-multimodal-copyright)[^19] |
| Interaction | Official Communications | <a name="interaction-official-inaccurate-statements"></a>[Making inaccurate promises or statements to the public](controls.md#interaction-official-inaccurate-statements)[^20] |
| Interaction | Official Communications | <a name="interaction-official-undesirable-content"></a>[Sending undesirable content to recipients](controls.md#interaction-official-undesirable-content)[^21] |
| Interaction | Official Communications | <a name="interaction-official-malicious-content"></a>[Sending malicious content to recipients](controls.md#interaction-official-malicious-content)[^22] |
| Interaction | Official Communications | <a name="interaction-official-authorship-deception"></a>[Misleading recipients about the authorship of the communications](controls.md#interaction-official-authorship-deception)[^23] |
| Interaction | Official Communications | <a name="interaction-official-sensitive-data"></a>[Sending personally identifiable or sensitive data](controls.md#interaction-official-sensitive-data)[^24] |
| Interaction | Agent Communication | <a name="interaction-agent-insecure-communication"></a>Communicating insecurely resulting in man-in-the-middle attacks[^25] |
| Interaction | Agent Communication | <a name="interaction-agent-message-misinterpretation"></a>Misinterpreting inter-agent messages due to poor formatting or weak protocols[^26] |
| Interaction | Agent Communication | <a name="interaction-agent-prompt-injection"></a>Passing on prompt injection attacks across agents[^27] |
| Interaction | Transactions | <a name="interaction-transactions-unauthorized"></a>[Allowing unauthorised transactions](controls.md#interaction-transactions-unauthorized)[^28] |
| Interaction | Transactions | <a name="interaction-transactions-credential-vulnerability"></a>[Increasing the system's vulnerability to attackers exfiltrating credentials for transactions through the agent](controls.md#interaction-transactions-credential-vulnerability)[^29] |
| Interaction | Internet & Search Access | <a name="interaction-internet-prompt-injection"></a>[Opening vulnerabilities to prompt injection attacks via malicious websites](controls.md#interaction-internet-prompt-injection)[^30] |
| Interaction | Internet & Search Access | <a name="interaction-internet-unreliable-info"></a>[Returning unreliable information or websites](controls.md#interaction-internet-unreliable-info)[^31] |
| Interaction | Computer Use | <a name="interaction-computer-prompt-injection"></a>[Opening vulnerabilities to prompt injection attacks](controls.md#interaction-computer-prompt-injection)[^32] |
| Interaction | Computer Use | <a name="interaction-computer-sensitive-access"></a>[Accessing personally identifiable or sensitive data](controls.md#interaction-computer-sensitive-access)[^33] |
| Operational | Code Execution | <a name="operational-code-poor-execution"></a>[Executing poor code](controls.md#operational-code-poor-execution)[^34] |
| Operational | Code Execution | <a name="operational-code-malicious-execution"></a>[Executing vulnerable or malicious code](controls.md#operational-code-malicious-execution)[^35] |
| Operational | File & Data Management | <a name="operational-files-overwrite-delete"></a>[Overwriting or deleting database tables or files](controls.md#operational-files-overwrite-delete)[^36] |
| Operational | File & Data Management | <a name="operational-files-query-overload"></a>[Overwhelming the database with poor, inefficient, or repeated queries](controls.md#operational-files-query-overload)[^37] |
| Operational | File & Data Management | <a name="operational-files-data-exposure"></a>[Exposing personally identifiable or sensitive data from databases or files](controls.md#operational-files-data-exposure)[^38] |
| Operational | File & Data Management | <a name="operational-files-prompt-injection"></a>[Opening vulnerabilities to prompt injection attacks via malicious data or files](controls.md#operational-files-prompt-injection)[^39] |
| Operational | System Management | <a name="operational-system-privilege-escalation"></a>[Escalating the agent's own privileges](controls.md#operational-system-privilege-escalation)[^40] |
| Operational | System Management | <a name="operational-system-misconfiguration"></a>[Misconfiguring system resources, compromising system integrity and availability](controls.md#operational-system-misconfiguration)[^41] |
| Operational | System Management | <a name="operational-system-request-overload"></a>[Overwhelming the system with poor, inefficient, or repeated requests](controls.md#operational-system-request-overload)[^42] |

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
