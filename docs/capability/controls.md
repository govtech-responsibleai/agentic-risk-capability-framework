# Controls

For each capability and risk combination identified in the previous sections, we provide a list of technical controls that may be useful in mitigating those safety or security risks. Due to the rapid developments in the agentic AI space, this list provides a simple starting point and is far from complete or thorough.

| First-level | Second-level | Risks | Technical Controls |
|---|---|---|---|
| Cognitive | Planning & Goal Management | Devising plans that do not adhere to the user's instructions | Prompt the agent to self-reflect on the adherence of the plan to the user's instructions |
| Cognitive | Planning & Goal Management | Devising plans that do not adhere to the user's instructions | Require the user to approve the plan in high-impact cases |
| Cognitive | Planning & Goal Management | Devising plans that do not adhere to common sense or implicit assumptions about the user's instructions | Prompt the agent to self-reflect on whether the plan is sensible and reasonable, given the user's original request |
| Cognitive | Planning & Goal Management | Devising plans that do not adhere to common sense or implicit assumptions about the user's instructions | Ensure important assumptions about feasibility, scope, and cost, where relevant, are included in the system prompt |
| Cognitive | Reasoning & Problem-Solving | Becoming ineffective, inefficient, or unsafe due to overthinking | Enforce time or token limits for agents' reasoning |
| Cognitive | Reasoning & Problem-Solving | Becoming ineffective, inefficient, or unsafe due to overthinking | Test different variations of the prompt to estimate likelihood of overthinking |
| Cognitive | Reasoning & Problem-Solving | Becoming ineffective, inefficient, or unsafe due to overthinking | Adjust short-term and long-term memory options for the agent |
| Cognitive | Reasoning & Problem-Solving | Engaging in deceptive behaviour through pursuing or prioritising other goals | Provide access to a scratchpad for agents to use to record its inner thoughts |
| Cognitive | Tool Use & Delegation | Assigning tasks incorrectly to other agents | Apply guardrails to limit the scope of tasks that can be assigned to specialised agents |
| Cognitive | Tool Use & Delegation | Attempting to use other agents maliciously | Log all task assignments by the agent to other agents |
| Cognitive | Tool Use & Delegation | Attempting to use other agents maliciously | Conduct rigorous adversarial testing on centralised planning agents |
| Interaction | Agent Communication | Impersonation of planning agent to use other agents maliciously | Ensure all cross-agent authentication and message validation, and encryption where necessary |
| Interaction | Agent Communication | Enabling the exfiltration of sensitive data | Implement a whitelist approach for outward network access, including API requests |
| Interaction | Agent Communication | Enabling the exfiltration of sensitive data | Ensure that sensitive data is not passed and leaked between agents by using appropriate guardrails |
| Interaction | Computer Use | Opening vulnerabilities to prompt injection attacks | Ensure computer use protocol or application provides immediate interruptability |
| Interaction | Computer Use | Opening vulnerabilities to prompt injection attacks | Limit computer use to accessing only safe resources on the computer |
| Interaction | Computer use | Accessing personally identifiable or sensitive data | Ensure "take over" mode is activated when keying in sensitive data (e.g. passwords, API keys) |
| Interaction | Internet & Search Access | Opening vulnerabilities to prompt injection attacks via malicious websites | Implement input guardrails to detect prompt injection or adversarial attacks |
| Interaction | Internet & Search Access | Opening vulnerabilities to prompt injection attacks via malicious websites | Implement escape filtering before including web content into prompts |
| Interaction | Internet & Search Access | Opening vulnerabilities to prompt injection attacks via malicious websites | Use structured retrieval APIs for searching the web rather than through web scraping |
| Interaction | Internet & Search Access | Returning unreliable information or websites | Prioritise results from verified, high-quality domains (e.g. .gov, .edu, well-known publishers) |
| Interaction | Internet & Search Access | Returning unreliable information or websites | Require cross-source validation for some of the claims made |
| Interaction | Multimodal Understanding & Generation | Generating undesirable content (e.g. toxic, hateful, sexual) | Implement output multimodal safety guardrails for the output to detect if undesirable content is being generated |
| Interaction | Multimodal Understanding & Generation | Generating unqualified advice in specialised domains (e.g. medical, financial, legal) | Implement input multimodal guardrails to detect if the instruction is related to one of the specialised domains, and if so, to decline fulfilling the instruction |
| Interaction | Multimodal Understanding & Generation | Generating controversial content (e.g. political, competitors) | Implement input multimodal guardrails to detect instructions to generate content that is controversial according to the organisation's policies |
| Interaction | Multimodal Understanding & Generation | Regurgitating personally identifiable information | Implement output multimodal guardrails to detect personally identifiable information in the LLM's outputs before it reaches the user |
| Interaction | Multimodal Understanding & Generation | Generating copyrighted content | Implement input guardrails to detect instructions to generate copyrighted content |
| Interaction | Natural Language Communication | Generating undesirable content (e.g. toxic, hateful, sexual) | Implement output safety text guardrails to detect if undesirable content is being generated |
| Interaction | Natural Language Communication | Generating unqualified advice in specialised domains (e.g. medical, financial, legal) | Implement input text guardrails to detect if the question is related to one of the specialised domains, and if so, to decline answering the question |
| Interaction | Natural Language Communication | Generating controversial content (e.g. political, competitors) | Implement input text guardrails to detect instructions to generate content that is controversial according to the organisation's policies |
| Interaction | Natural Language Communication | Regurgitating personally identifiable information | Implement output text guardrails to detect personally identifiable information in the LLM's outputs before it reaches the user |
| Interaction | Natural Language Communication | Generating non-factual or hallucinated content | Implement methods to reduce hallucination rates (e.g. retrieval-augmented generation) |
| Interaction | Natural Language Communication | Generating non-factual or hallucinated content | Implement UI/UX cues to highlight the risk of hallucination to the user |
| Interaction | Natural Language Communication | Generating non-factual or hallucinated content | Implement features to enable users to easily verify the generated answer against the original content |
| Interaction | Natural Language Communication | Generating copyrighted content | Implement input text guardrails to detect instructions to generate copyrighted content |
| Interaction | Official Communications | Making inaccurate promises or statements to the public | Limit the communications to standard processes, where communication templates are available |
| Interaction | Official Communications | Making inaccurate promises or statements to the public | Require human approval for communications for more sensitive matters |
| Interaction | Official Communications | Making inaccurate promises or statements to the public | Provide alternate channels for users to clarify communications or give feedback |
| Interaction | Official Communications | Sending undesirable content to recipients | Implement output safety guardrails to detect if undesirable content is in the communications before it is sent to the user |
| Interaction | Official Communications | Sending malicious content to recipients | Check for adherence to communication templates prior to sending email |
| Interaction | Official Communications | Sending malicious content to recipients | Validate all links and attachments prior to sending them to users |
| Interaction | Official Communications | Misleading recipients about the authorship of the communications | Declare upfront that the communications are generated by an AI system |
| Interaction | Official Communications | Sending personally identifiable or sensitive data | Implement output guardrails to detect personally identifiable information in the communications before it is sent to the user |
| Interaction | Transactions | Allowing unauthorised transactions | Require human validation for high-impact transactions |
| Interaction | Transactions | Allowing unauthorised transactions | Logging all requests leading up to the transaction |
| Interaction | Transactions | Allowing unauthorised transactions | Apply fraud detection models or heuristics to the agent's own decisions |
| Interaction | Transactions | Increasing the system's vulnerability to attackers exfiltrating credentials for transactions through the agent | Ensure virtual isolation for agents carrying out transactions |
| Interaction | Transactions | Increasing the system's vulnerability to attackers exfiltrating credentials for transactions through the agent | Do not share credentials with the agent directly, require the agent to use a separate service for authentication and transactions |
| Operational | Code Execution | Executing poor code | Use code linters to screen for bad practices, anti-patterns, unused variables, or poor syntax |
| Operational | Code Execution | Executing poor code | Use static code analysers to detect problems with the code |
| Operational | Code Execution | Executing poor code | Run code only in virtually isolated compute environments (e.g. Docker containers) |
| Operational | Code Execution | Executing poor code | Ensure monitoring of code runtime and memory consumption |
| Operational | Code Execution | Executing vulnerable or malicious code | Use static code analysers to identify dangerous patterns in the code before execution |
| Operational | Code Execution | Executing vulnerable or malicious code | Conduct CVE scanning and block execution if any High or Critical CVEs are detected |
| Operational | Code Execution | Executing vulnerable or malicious code | Block all inward and outward network access by default |
| Operational | Code Execution | Executing vulnerable or malicious code | Scope execution privileges strictly only to what is necessary, ensuring that privileges are customised to each agent within a system |
| Operational | Code Execution | Executing vulnerable or malicious code | Do not grant admin or sudo privileges |
| Operational | Code Execution | Executing vulnerable or malicious code | Sanitise all inputs |
| Operational | Code Execution | Executing vulnerable or malicious code | Implement a whitelist approach for inward network access |
| Operational | Code Execution | Executing vulnerable or malicious code | Review all code generated by agents, including shell scripts, before execution |
| Operational | Code Execution | Executing vulnerable or malicious code | Create a Deny list of commands that agents are not allowed to run autonomously |
| Operational | File & Data Management | Overwriting or deleting database tables or files | No write access to tables in the database unless strictly required |
| Operational | File & Data Management | Overwriting or deleting database tables or files | Require human approval for any changes to the database, table, or file |
| Operational | File & Data Management | Overwhelming the database with poor, inefficient, or repeated queries | Limit the number of concurrent queries to the database from the agent |
| Operational | File & Data Management | Overwhelming the database with poor, inefficient, or repeated queries | Analyse past database queries to identify repeated or inefficient queries |
| Operational | File & Data Management | Exposing personally identifiable or sensitive data from databases or files | Implement input guardrails to detect personally identifiable information |
| Operational | File & Data Management | Exposing personally identifiable or sensitive data from databases or files | Do not allow access to personally identifiable data or sensitive data unless strictly required |
| Operational | File & Data Management | Exposing personally identifiable or sensitive data from databases or files | Log all database queries in production |
| Operational | File & Data Management | Opening vulnerabilities to prompt injection attacks via malicious data or files | Validate new data used to supplement RAG databases or training data |
| Operational | File & Data Management | Opening vulnerabilities to prompt injection attacks via malicious data or files | Implement input guardrails to detect prompt injection or adversarial attacks |
| Operational | File & Data Management | Opening vulnerabilities to prompt injection attacks via malicious data or files | Disallow unknown or external files unless it is scanned |
| Operational | File & Data Management | Overwriting or deleting required files | Require user confirmation before overwriting or deleting any files |
| Operational | File & Data Management | Overwriting or deleting required files | Keep separate copy of original files |
| Operational | File & Data Management | Overwriting or deleting required files | Ensure second copy of database is not changed until a pre-specified amount of time has passed / ensure database versioning |
| Operational | File & Data Management | Making unauthorised changes to files | Require user confirmation before executing each change to a file |
| Operational | System Management | Escalating the agent's own privileges | Scope system privileges strictly only to what is necessary |
| Operational | System Management | Escalating the agent's own privileges | Do not grant admin privileges to agents |
| Operational | System Management | Escalating the agent's own privileges | Do not allow agents to modify privileges |
| Operational | System Management | Misconfiguring system resources, compromising system integrity and availability | Only grant agents privileges to modify system resources if strictly necessary for completion of tasks |
| Operational | System Management | Misconfiguring system resources, compromising system integrity and availability | Set minimum and maximum limits to what the agent can modify within a given system resource |
| Operational | System Management | Misconfiguring system resources, compromising system integrity and availability | Ensure logging of system health metrics and automated alerts to the developer team if any metrics are abnormal |
| Operational | System Management | Overwhelming the system with poor, inefficient, or repeated requests | Limit the number of concurrent queries to external systems from the agent |
| Operational | System Management | Overwhelming the system with poor, inefficient, or repeated requests | Log all queries to external systems from the agent |