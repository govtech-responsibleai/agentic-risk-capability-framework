# Baseline Risks

In this section, we list the baseline risks from (i) the components of an agent and (ii) the design of an agentic system. Note that this list is meant as a reference and is not meant to be exhaustive. Clicking on any of the risks will bring you to the next page with the corresponding controls.

## List of Baseline Risks

| Origin | Risk |
|---------------|-------|
| <a name="llm-alignment-failure"></a>LLM | [Poorly aligned LLMs may pursue objectives which technically satisfy instructions but violate safety principles.](controls.md#llm-alignment-failure)[^1] |
| <a name="llm-unpredictable-performance"></a>LLM | [Weaker LLMs have a higher tendency to produce unpredictable outputs which make agent behaviour erratic.](controls.md#llm-unpredictable-performance)[^2] |
| <a name="llm-poor-safety-tuning"></a>LLM | [LLMs with poor safety tuning are more susceptible to prompt injection attacks and jailbreaking attempts.](controls.md#llm-poor-safety-tuning)[^3] |
| <a name="llm-data-contamination"></a>LLM | [Using LLMs trained on poisoned or biased data introduces manipulation risk, discriminatory decisions, or misinformation.](controls.md#llm-data-contamination)[^4] |
| <a name="tools-authentication-failure"></a>Tools | [Poorly implemented tools may not correctly verify user identity or permissions when executing privileged actions.](controls.md#tools-authentication-failure)[^5] |
| <a name="tools-rogue-malicious"></a>Tools | [Rogue tools that mimic legitimate ones can contain hidden malicious code that executes when loaded.](controls.md#tools-rogue-malicious)[^6] |
| <a name="tools-input-validation"></a>Tools | [Tools that do not properly sanitise or validate inputs can be exploited through prompt injection attacks.](controls.md#tools-input-validation)[^7] |
| <a name="tools-excessive-privileges"></a>Tools | [Tools that demand broader permissions than necessary create unnecessary attack surfaces for malicious actors.](controls.md#tools-excessive-privileges)[^8] |
| <a name="instructions-specification-gaming"></a>Instructions | [Simplistic instructions with narrow metrics and without broader constraints may result in agents engaging in specification gaming, resulting in poor performance or safety violations.](controls.md#instructions-specification-gaming)[^9] |
| <a name="instructions-underspecified"></a>Instructions | [Vague instructions may compel agents to attempt to fill in missing constraints, resulting in unpredictable actions or incorrect steps taken.](controls.md#instructions-underspecified)[^10] |
| <a name="instructions-hierarchy-confusion"></a>Instructions | [Instructions without a clear distinction between system prompts and user requests may confuse agents and result in greater vulnerability to prompt injection attacks.](controls.md#instructions-hierarchy-confusion)[^11] |
| <a name="memory-data-poisoning"></a>Memory | [Malicious actors can inject false or misleading facts into the knowledge base, resulting in the agent acting on incorrect data or facts.](controls.md#memory-data-poisoning)[^12] |
| <a name="memory-privacy-leakage"></a>Memory | [Agents may inadvertently store sensitive user or organisational data from prior interactions, resulting in data privacy risks.](controls.md#memory-privacy-leakage)[^13]|
| <a name="memory-hallucination-persistence"></a>Memory | [Agents may mistakenly save momentary glitches and hallucinations into memory, resulting in compounding mistakes when the agent relies on the incorrect information for its decision or actions.](controls.md#memory-hallucination-persistence)|
| <a name="architecture-error-propagation"></a>Agentic Architecture | [In linear agentic pipelines where each stage blindly trusts the previous stage, single early mistakes may be propagated and magnified.](controls.md#architecture-error-propagation)[^15] |
| <a name="architecture-single-point-failure"></a>Agentic Architecture | [In hub-and-spoke architectures which route all decisions through one controller agent, any bug or compromise may distributes faulty instructions across the entire system.](controls.md#architecture-single-point-failure)[^16]|
| <a name="architecture-decision-traceability"></a>Agentic Architecture | [More complex agentic architectures may make it difficult to fully reconstruct decision processes across multiple agents.](controls.md#architecture-decision-traceability)|
| <a name="access-role-impersonation"></a>Roles and Access Controls | [Unauthorised actors can impersonate agents and gain access to restricted resources.](controls.md/#access-role-impersonation)[^17] |
| <a name="access-misconfigured-roles"></a>Roles and Access Controls | [Agents may gain unauthorized access to restricted resources by exploiting misconfigured or overly permissive roles.](controls.md/#access-misconfigured-roles)[^18] |


<!-- footnotes -->

[^1]: [Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models (Denison et al, 2024)](https://arxiv.org/abs/2406.10162).
[^2]: [Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems (Zhang et al, 2025)](https://arxiv.org/abs/2505.00212).
[^3]: [Commercial LLM Agents Are Already Vulnerable to Simple Yet Dangerous Attacks (Li et al, 2025)](https://arxiv.org/pdf/2502.08586) and [Watch Out for Your Agents! Investigating Backdoor Threats to LLM-Based Agents (Yang et al, 2024)](https://arxiv.org/abs/2402.11208).
[^4]: [Scaling Trends for Data Poisoning in LLMs (Bowen et al, 2024)](https://arxiv.org/abs/2408.02946v6).
[^5]: [Enterprise-Grade Security for the Model Context Protocol (MCP): Frameworks and Mitigation Strategies (Vineeth Sai Narajala and Idan Habler, 2025)](https://arxiv.org/abs/2504.08623), [MCIP: Protecting MCP Safety via Model Contextual Integrity Protocol (Jing et al, 2025)](https://arxiv.org/abs/2505.14590), and [Model Context Protocol (MCP): Understanding security risks and controls (Florencio Cano Gabarda, 2025)](https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls)
[^6]: [MCP: Untrusted Servers and Confused Clients, Plus a Sneaky Exploit (Michael Bargury, 2025)](https://www.mbgsec.com/archive/2025-05-03-mcp-untrusted-servers-and-confused-clients-plus-a-sneaky-exploit-embrace-the-red/).
<!--[BadAgent: Inserting and Activating Backdoor Attacks in LLM Agents (Wang et al, 2024)](https://arxiv.org/abs/2406.03007) and [Composite Backdoor Attacks Against Large Language Models (Huang et al, 2024)](https://aclanthology.org/2024.findings-naacl.94/). -->
[^7]: [Multi-Agent Systems Execute Arbitrary Malicious Code (Triedman et al, 2025)](https://arxiv.org/abs/2503.12188v1). Also see [CVE-2024-7042](https://www.cve.org/CVERecord?id=CVE-2024-7042).
<!-- [Commercial LLM Agents Are Already Vulnerable to Simple Yet Dangerous Attacks (Li et al, 2025)](https://arxiv.org/pdf/2502.08586).-->
[^8]: [Plugin Vulnerabilities: Visit a Website and Have Your Source Code Stolen (Johann Rehberger, 2023)](https://embracethered.com/blog/posts/2023/chatgpt-plugin-vulns-chat-with-code/).
[^9]: [Demonstrating specification gaming in reasoning models (Bondarenko et al, 2025)](https://arxiv.org/abs/2502.13295).
[^10]: In [What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts](https://arxiv.org/abs/2505.13360v1), Yang et al (2025) show that underspecified prompts are two times more likely to regress over model or prompt changes, with accuracy drops exceeding 20% in some cases.
[^11]: See [Control Illusion: The Failure of Instruction Hierarchies in Large Language Models (Geng et al, 2025)](https://arxiv.org/abs/2502.15851v1) and [IHEval: Evaluating Language Models on Following the Instruction Hierarchy (Zhang et al, 2025)](https://aclanthology.org/2025.naacl-long.425.pdf).
[^12]: See [One Shot Dominance: Knowledge Poisoning Attack on Retrieval-Augmented Generation Systems (Chang et al, 2025)](https://arxiv.org/abs/2505.11548v2) and [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models (Zou et al, 2025)](https://arxiv.org/abs/2402.07867) for text-based knowledge bases; see [PoisonedEye: Knowledge Poisoning Attack on Retrieval-Augmented Generation based Large Vision-Language Models (Zhang et al, 2025)](https://openreview.net/pdf?id=6SIymOqJlc) for image-based knowledge bases.
[^13]: [SoK: The Privacy Paradox of Large Language Models: Advancements, Privacy Risks, and Mitigation (Shanmugarasa et al, 2025)](https://arxiv.org/abs/2506.12699v2)
[^15]: [On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents (Huang et al, 2025)](https://arxiv.org/abs/2408.00989v3)
[^16]: Peigné-Lefebvre et al. Multi-Agent Security Tax: Trading Off Security and Collaboration Capabilities in [^16]Multi-Agent Systems. arXiv preprint arXiv:2502.19145, 2025. <https://arxiv.org/pdf/2502.19145>, Accessed: 2025‑07‑27.
[^17]: Chen et al. AI Agents Are Here. So Are the Threats. Palo Alto Networks Unit 42 blog, May 1 2025. <https://unit42.paloaltonetworks.com/agentic-ai-threats/>, Accessed: 2025‑07‑27.
[^18]: Goutham A S. Escaping Reality: Privilege Escalation in Gen AI Admin Panel (aka The Chaos of a Misconfigured Admin Panel). Medium blog, Sept 23 2024. <https://cyberweapons.medium.com/escaping-reality-privilege-escalation-in-gen-ai-admin-panel-aka-the-chaos-of-a-misconfigured-b6ad73bf1b65>, Accessed: 2025‑07‑27.


---
