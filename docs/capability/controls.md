# Controls

| Control ID | Risk | Technical Controls |
|------------|------|--------------------|
| Thinking-Delegating-R1-M1 | <a name="risk-assigning-tasks-incorrectly-to-other-agents"></a>Assigning tasks incorrectly to other agents | Prompt the agent to self-reflect and assess the suitability of delegating the tasks to specific agents |
| Thinking-Delegating-R2-M1 | <a name="risk-attempting-to-use-other-agents-maliciously"></a>Attempting to use other agents maliciously | Log all task assignments by the agent to other agents |
| Thinking-Planning-R1-M1 | <a name="risk-devising-plans-that-do-not-adhere-to-the-user-s-instructions"></a>Devising plans that do not adhere to the user's instructions | Prompt the agent to self-reflect on the adherence of the plan to the user's instructions |
| Thinking-Planning-R1-M2 | Devising plans that do not adhere to the user's instructions | Require the user to approve the plan in high- impact cases |
| Thinking-Planning-R2-M1 | <a name="risk-devising-plans-that-do-not-adhere-to-common-sense-or-implicit-assumptions-about-the-user-s-instructions"></a>Devising plans that do not adhere to common sense or implicit assumptions about the user's instructions | Prompt the agent to self-reflect on whether the plan is sensible from a layperson's perspective |
| Thinking-Reasoning-R1-M1 | <a name="risk-becoming-stuck-in-a-reasoning-loop-due-to-overthinking"></a>Becoming stuck in a reasoning loop due to overthinking | Enforce time or token limits for agents' reasoning |
| Thinking-Reasoning-R1-M2 | Becoming stuck in a reasoning loop due to overthinking | Rigorously test different variations of the prompt to estimate likelihood of overthinking |
| Thinking-Reasoning-R1-M3 | Becoming stuck in a reasoning loop due to overthinking | Adjust short-term and long-term memory options for the agent |
| Thinking-Reasoning-R2-M1 | <a name="risk-engaging-in-deceptive-behaviour-through-pursuing-or-prioritising-other-goals"></a>Engaging in deceptive behaviour through pursuing or prioritising other goals | Provide access to a scratchpad for agents to use to record its inner thoughts |
| Searching-Databases-R1-M1 | <a name="risk-overwriting-or-deleting-tables-in-the-database"></a>Overwriting or deleting tables in the database | No write access to tables in the database unless strictly required |
| Searching-Databases-R1-M2 | Overwriting or deleting tables in the database | Require human approval for any changes to the database or table schema |
| Searching-Databases-R2-M1 | <a name="risk-overwhelming-the-database-with-poor-inefficient-or-repeated-queries"></a>Overwhelming the database with poor, inefficient, or repeated queries | Limit the number of concurrent queries to the database from the agent |
| Searching-Databases-R2-M2 | Overwhelming the database with poor, inefficient, or repeated queries | Analyse past database queries to identify repeated or inefficient queries |
| Searching-Databases-R3-M1 | <a name="risk-exposing-personally-identifiable-or-sensitive-data-from-databases"></a>Exposing personally identifiable or sensitive data from databases | Implement input guardrails to detect personally identifiable information in the web content |
| Searching-Databases-R3-M2 | Exposing personally identifiable or sensitive data from databases | Do not allow access to personally identifiable data or sensitive data unless strictly required |
| Searching-Databases-R3-M3 | Exposing personally identifiable or sensitive data from databases | Log all database queries in production |
| Searching-Files-R1-M1 | <a name="risk-opening-vulnerabilities-to-prompt-injection-attacks-via-malicious-files"></a>Opening vulnerabilities to prompt injection attacks via malicious files | Implement input guardrails to detect prompt injection or adversarial attacks |
| Searching-Files-R1-M2 | Opening vulnerabilities to prompt injection attacks via malicious files | Disallow unknown or external files unless it is scanned |
| Searching-Files-R2-M1 | <a name="risk-exposing-personally-identifiable-or-sensitive-data-from-files"></a>Exposing personally identifiable or sensitive data from files | Implement input guardrails to detect personally identifiable information in the web content |
| Searching-Files-R2-M2 | Exposing personally identifiable or sensitive data from files | Include a denylist for files known to host personal or sensitive data |
| Searching-Web-R1-M1 | <a name="risk-opening-vulnerabilities-to-prompt-injection-attacks-via-malicious-websites"></a>Opening vulnerabilities to prompt injection attacks via malicious websites | Implement input guardrails to detect prompt injection or adversarial attacks |
| Searching-Web-R1-M2 | Opening vulnerabilities to prompt injection attacks via malicious websites | Implement escape filtering before including web content into prompts |
| Searching-Web-R1-M3 | Opening vulnerabilities to prompt injection attacks via malicious websites | Use structured retrieval APIs for searching the web rather than through web scraping |
| Searching-Web-R2-M1 | <a name="risk-scraping-and-regurgitating-personally-identifiable-information-for-websites"></a>Scraping and regurgitating personally identifiable information for websites | Implement input guardrails to detect personally identifiable information in the content |
| Searching-Web-R2-M2 | Scraping and regurgitating personally identifiable information for websites | Include a denylist for websites known to host personal data |
| Searching-Web-R3-M1 | <a name="risk-returning-unreliable-information-or-websites"></a>Returning unreliable information or websites | Prioritise results from verified, high-quality domains (e.g. .gov, .edu, well-known publishers) |
| Searching-Web-R3-M2 | Returning unreliable information or websites | Require cross-source validation for some of the claims made |
| Generating-Audio-R1-M1 | <a name="risk-generating-undesirable-content-e-g-toxic-hateful-sexual"></a>Generating undesirable content (e.g. toxic, hateful, sexual) | Implement output audio or multimodal safety guardrails for the output to detect if undesirable content is being generated |
| Generating-Audio-R2-M1 | <a name="risk-generating-unqualified-advice-in-specialised-domains-e-g-medical-financial-legal"></a>Generating unqualified advice in specialised domains (e.g. medical, financial, legal) | Implement input audio or multimodal guardrails to detect if the question is related to one of the specialised domains, and if so, to decline answering the question |
| Generating-Audio-R3-M1 | <a name="risk-generating-controversial-content-e-g-political-competitors"></a>Generating controversial content (e.g. political, competitors) | Implement input audio or multimodal guardrails to detect instructions to generate content that is controversial according to the organisation's policies |
| Generating-Audio-R4-M1 | <a name="risk-regurgitating-personally-identifiable-information"></a>Regurgitating personally identifiable information | Implement output audio or multimodal guardrails to detect personally identifiable information in the LLM's outputs before it reaches the user |
| Generating-Audio-R5-M1 | <a name="risk-generating-non-factual-or-hallucinated-content"></a>Generating non-factual or hallucinated content | Implement methods to reduce hallucination rates (e.g. retrieval-augmented generation) |
| Generating-Audio-R5-M2 | Generating non-factual or hallucinated content | Implement UI/UX cues to highlight the risk of hallucination to the user |
| Generating-Audio-R5-M3 | Generating non-factual or hallucinated content | Implement features to enable users to easily verify the generated answer against the original content |
| Generating-Audio-R6-M1 | <a name="risk-generating-copyrighted-content"></a>Generating copyrighted content | Implement input guardrails to detect instructions to generate copyrighted content |
| Generating-Images-R1-M1 | Generating undesirable content (e.g. toxic, hateful, sexual) | Implement output multimodal safety guardrails for the output to detect if undesirable content is being generated |
| Generating-Images-R2-M1 | Generating unqualified advice in specialised domains (e.g. medical, financial, legal) | Implement input multimodal guardrails to detect if the instruction is related to one of the specialised domains, and if so, to decline fulfilling the instruction |
| Generating-Images-R3-M1 | Generating controversial content (e.g. political, competitors) | Implement input multimodal guardrails to detect instructions to generate content that is controversial according to the organisation's policies |
| Generating-Images-R4-M1 | Regurgitating personally identifiable information | Implement output multimodal guardrails to detect personally identifiable information in the LLM's outputs before it reaches the user |
| Generating-Images-R5-M1 | Generating copyrighted content | Implement input guardrails to detect instructions to generate copyrighted content |
| Generating-Text-R1-M1 | Generating undesirable content (e.g. toxic, hateful, sexual) | Implement output safety guardrails to detect if undesirable content is being generated |
| Generating-Text-R2-M1 | Generating unqualified advice in specialised domains (e.g. medical, financial, legal) | Implement input guardrails to detect if the question is related to one of the specialised domains, and if so, to decline answering the question |
| Generating-Text-R3-M1 | Generating controversial content (e.g. political, competitors) | Implement input guardrails to detect instructions to generate content that is controversial according to the organisation's policies |
| Generating-Text-R4-M1 | Regurgitating personally identifiable information | Implement output guardrails to detect personally identifiable information in the LLM's outputs before it reaches the user |
| Generating-Text-R5-M1 | Generating non-factual or hallucinated content | Implement methods to reduce hallucination rates (e.g. retrieval-augmented generation) |
| Generating-Text-R5-M2 | Generating non-factual or hallucinated content | Implement UI/UX cues to highlight the risk of hallucination to the user |
| Generating-Text-R5-M3 | Generating non-factual or hallucinated content | Implement features to enable users to easily verify the generated answer against the original content |
| Generating-Text-R6-M1 | Generating copyrighted content | Implement input guardrails to detect instructions to generate copyrighted content |
| Generating-Videos-R1-M1 | Generating undesirable content (e.g. toxic, hateful, sexual) | Implement output multimodal safety guardrails for the output to detect if undesirable content is being generated |
| Generating-Videos-R2-M1 | Generating unqualified advice in specialised domains (e.g. medical, financial, legal) | Implement input multimodal guardrails to detect if the instruction is related to one of the specialised domains, and if so, to decline fulfilling the instruction |
| Generating-Videos-R3-M1 | Generating controversial content (e.g. political, competitors) | Implement input multimodal guardrails to detect instructions to generate content that is controversial according to the organisation's policies |
| Generating-Videos-R4-M1 | Regurgitating personally identifiable information | Implement output multimodal guardrails to detect personally identifiable information in the LLM's outputs before it reaches the user |
| Generating-Videos-R5-M1 | Generating copyrighted content | Implement input guardrails to detect instructions to generate copyrighted content |
| Executing-Code-R1-M1 | <a name="risk-executing-poor-code"></a>Executing poor code | Use code linters to screen for bad practices, anti-patterns, unused variables, or poor syntax |
| Executing-Code-R1-M2 | Executing poor code | Use static code analysers to detect problems with the code |
| Executing-Code-R1-M3 | Executing poor code | Run code only in virtually isolated compute environments (e.g. Docker containers) |
| Executing-Code-R1-M4 | Executing poor code | Ensure monitoring of code runtime and memory consumption |
| Executing-Code-R1-M5 | Executing poor code | Ensure proper versioning of code to allow rollbacks |
| Executing-Code-R2-M1 | <a name="risk-executing-vulnerable-or-malicious-code"></a>Executing vulnerable or malicious code | Use static code analysers to identify dangerous patterns in the code before execution |
| Executing-Code-R2-M2 | Executing vulnerable or malicious code | Conduct CVE scanning and block execution if any High or Critical CVEs are detected |
| Executing-Code-R2-M3 | Executing vulnerable or malicious code | Block all inward and outward network access by default |
| Executing-Code-R2-M4 | Executing vulnerable or malicious code | Scope execution privileges strictly only to what is necessary |
| Executing-Code-R2-M5 | Executing vulnerable or malicious code | Do not grant admin or sudo privileges |
| Executing-Communications-R1-M1 | <a name="risk-giving-incorrect-or-unclear-instructions-to-others"></a>Giving incorrect or unclear instructions to others | Limit the communications to standard processes, where communication templates are available |
| Executing-Communications-R1-M2 | Giving incorrect or unclear instructions to others | Require human approval for communications for more sensitive matters |
| Executing-Communications-R1-M3 | Giving incorrect or unclear instructions to others | Provide alternate channels for users to clarify communications or give feedback |
| Executing-Communications-R2-M1 | <a name="risk-sending-undesirable-content-to-users"></a>Sending undesirable content to users | Implement output safety guardrails to detect if undesirable content is in the communications before it is sent to the user |
| Executing-Communications-R3-M1 | <a name="risk-sending-malicious-content-to-users"></a>Sending malicious content to users | Check for adherence to communication templates prior to sending email |
| Executing-Communications-R3-M2 | Sending malicious content to users | Validate all links and attachments prior to sending them to users |
| Executing-Communications-R4-M1 | <a name="risk-misleading-users-about-the-authorship-of-the-communications"></a>Misleading users about the authorship of the communications | Declare upfront that the communications are generated by an AI system |
| Executing-Communications-R5-M1 | <a name="risk-sending-personally-identifiable-or-sensitive-data"></a>Sending personally identifiable or sensitive data | Implement output guardrails to detect personally identifiable information in the communications before it is sent to the user |
| Executing-ComputerUse-R1-M1 | <a name="risk-opening-vulnerabilities-to-prompt-injection-attacks"></a>Opening vulnerabilities to prompt injection attacks | Scope agent privileges strictly only to what is necessary to run the tasks |
| Executing-ComputerUse-R1-M2 | Opening vulnerabilities to prompt injection attacks | Do not grant admin privileges to agents |
| Executing-ComputerUse-R1-M3 | Opening vulnerabilities to prompt injection attacks | Do not allow agents to modify privileges |
| Executing-ComputerUse-R2-M1 | <a name="risk-accessing-personally-identifiable-or-sensitive-data"></a>Accessing personally identifiable or sensitive data | Ensure "take over" mode is activated when keying in sensitive data (e.g. passwords, API keys) |
| Executing-ComputerUse-R2-M2 | Accessing personally identifiable or sensitive data | Limit scope of computer use to specific software |
| Executing-Files-R1-M1 | <a name="risk-overwriting-or-deleting-required-files"></a>Overwriting or deleting required files | Require user confirmation before overwriting or deleting any files |
| Executing-Files-R1-M2 | Overwriting or deleting required files | Keep separate copy of original files |
| Executing-Files-R2-M1 | <a name="risk-making-unauthorised-changes-to-files"></a>Making unauthorised changes to files | Require user confirmation before executing each change to a file |
| Executing-Systems-R1-M1 | <a name="risk-escalating-the-agent-s-own-privileges"></a>Escalating the agent's own privileges | Scope system privileges strictly only to what is necessary |
| Executing-Systems-R1-M2 | Escalating the agent's own privileges | Do not grant admin privileges to agents |
| Executing-Systems-R1-M3 | Escalating the agent's own privileges | Do not allow agents to modify privileges |
| Executing-Systems-R2-M1 | <a name="risk-misconfiguring-system-resources-compromising-system-integrity-and-availability"></a>Misconfiguring system resources, compromising system integrity and availability | Only grant agents privileges to modify system resources if strictly necessary for completion of tasks |
| Executing-Systems-R2-M2 | Misconfiguring system resources, compromising system integrity and availability | Set minimum and maximum limits to what the agent can modify within a given system resource |
| Executing-Systems-R2-M3 | Misconfiguring system resources, compromising system integrity and availability | Ensure logging of system health metrics and automated alerts to the developer team if any metrics are abnormal |
| Executing-Systems-R3-M1 | <a name="risk-overwhelming-external-systems-with-poor-inefficient-or-repeated-requests"></a>Overwhelming external systems with poor, inefficient, or repeated requests | Limit the number of concurrent queries to external systems from the agent |
| Executing-Systems-R3-M2 | Overwhelming external systems with poor, inefficient, or repeated requests | Log all queries to external systems from the agent |
| Executing-Transactions-R1-M1 | <a name="risk-allowing-unauthorised-transactions"></a>Allowing unauthorised transactions | Require human validation for high-impact transactions |
| Executing-Transactions-R1-M2 | Allowing unauthorised transactions | Logging all requests leading up to the transaction |
| Executing-Transactions-R1-M3 | Allowing unauthorised transactions | Apply fraud detection models or heuristics to the agent's own decisions |
| Executing-Transactions-R2-M1 | <a name="risk-increasing-the-system-s-vulnerability-to-attackers-exfiltrating-credentials-for-transactions-through-the-agent"></a>Increasing the system's vulnerability to attackers exfiltrating credentials for transactions through the agent | Ensure virtual isolation for agents carrying out transactions |
| Executing-Transactions-R2-M2 | Increasing the system's vulnerability to attackers exfiltrating credentials for transactions through the agent | Do not share credentials with the agent directly, require the agent to use a separate service for authentication and transactions |







This section outlines the governance mechanisms, technical safeguards, and operational procedures for managing agentic AI systems.

## Overview

AI agent controls are systematic approaches to managing and mitigating risks while ensuring safe and effective operation of autonomous AI systems.

## Control Categories

### Technical Controls
- Access controls and authentication
- Monitoring and logging systems
- Fail-safe mechanisms

### Governance Controls
- Policies and procedures
- Risk management frameworks
- Compliance monitoring

### Operational Controls
- Human oversight requirements
- Performance monitoring
- Incident response procedures

### Design Controls
- Safety by design principles
- Robustness testing
- Alignment mechanisms

## Implementation Framework

Coming soon...

---

*Part of the Agentic Risk & Capability Framework* 