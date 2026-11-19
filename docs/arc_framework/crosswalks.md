# Crosswalks to other frameworks

<!-- GENERATED FILE: edit arc-risk-register/*.yaml and run scripts/build_risk_register.py -->

!!! abstract "Page Summary"

    This page maps the ARC risk register to the external frameworks organisations are most likely to be
    using alongside it, so that an assessment done under one can be read in the vocabulary of another.
    Each mapping points to the *nearest corresponding entries*; it is not a claim of equivalence.

The crosswalks are maintained as a `crosswalks` field on every risk and control in the
[register YAML](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/arc-risk-register),
validated against `crosswalk_references.yaml`, and shown on each entry in the
[Interactive Risk Register](risk-register.md). This page is generated from the same data.

| Framework | Version | Maps to |
| --- | --- | --- |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 2026 (December 2025) | ARC risks and controls |
| [OWASP Agentic AI – Threats and Mitigations (threat taxonomy, as reproduced in CSA Addendum Annex A)](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | T1–T15 per CSA Addendum Annex A; T16–T17 per OWASP Top 10 Appendix A | ARC risks |
| [CSA Singapore – Securing Agentic AI, an Addendum to the Guidelines and Companion Guide on Securing AI Systems](https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/) | 1.0 (17 June 2026) | ARC controls |
| [IMDA – Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf) | 1.5 (May 2026) | ARC controls |

??? question "Why are some cells empty?"

    ARC covers both safety and security hazards. Its content-safety risks (undesirable, unqualified,
    controversial, or copyrighted content) have no counterpart in OWASP's security-focused agentic
    taxonomy, and are deliberately left unmapped rather than forced. CSA Addendum control 1.1 (conduct a
    risk assessment) is the assessment process that the ARC methodology itself implements, so no single
    ARC control corresponds to it.


## OWASP Top 10 for Agentic Applications 2026 → ARC risks

| OWASP ASI | ARC risks |
| --- | --- |
| **ASI01** Agent Goal Hijack | **RISK-008** Vague or underspecified instructions<br>**RISK-009** Unsanitised inputs in system instructions<br>**RISK-019** Generating plans that fail to meet the user's requirements<br>**RISK-020** Generating plans that overlook safety implications<br>**RISK-032** Unauthorised execution of business transactions<br>**RISK-034** Prompt injection via malicious websites<br>**RISK-036** Prompt injection risks through computer use<br>**RISK-044** Prompt injection via malicious files or data<br>**RISK-047** Data exfiltration through combined access to untrusted content, sensitive data, and an outbound channel |
| **ASI02** Tool Misuse and Exploitation | **RISK-004** Weak tool authentication and authorisation controls<br>**RISK-006** Tool poisoning by malicious actors<br>**RISK-007** Lack of input sanitisation<br>**RISK-023** Incorrect tool selection or misuse<br>**RISK-032** Unauthorised execution of business transactions<br>**RISK-037** Exposure of sensitive data<br>**RISK-038** Incorrect use of unfamiliar programmatic interfaces<br>**RISK-041** Unintended overwriting or deletion of files or data<br>**RISK-042** Database overload due to inefficient data operations<br>**RISK-043** Exposure of sensitive data through file or database access<br>**RISK-045** Misconfiguration of system resources<br>**RISK-046** System overload due to inefficient or excessive operations<br>**RISK-047** Data exfiltration through combined access to untrusted content, sensitive data, and an outbound channel |
| **ASI03** Identity and Privilege Abuse | **RISK-004** Weak tool authentication and authorisation controls<br>**RISK-005** Lack of proper role-based access control for tools<br>**RISK-011** Sensitive data leakage across memory contexts<br>**RISK-015** Overly permissive roles and permissions<br>**RISK-016** Unauthorised privilege escalation<br>**RISK-021** Incorrect task delegation between agents<br>**RISK-022** Malicious or manipulative use of delegated agents<br>**RISK-033** Leakage of transaction credentials<br>**RISK-043** Exposure of sensitive data through file or database access<br>**RISK-049** Escape from evaluation or sandbox containment onto live systems<br>**RISK-054** Insecure default configuration of agent frameworks and runtimes |
| **ASI04** Agentic Supply Chain Vulnerabilities | **RISK-001** Use of untrusted or compromised LLMs<br>**RISK-006** Tool poisoning by malicious actors<br>**RISK-048** Compromise through the tool, skill, and dependency supply chain<br>**RISK-053** Dependence on third-party agents as counterparties or delegates |
| **ASI05** Unexpected Code Execution (RCE) | **RISK-007** Lack of input sanitisation<br>**RISK-039** Production or execution of poor or ineffective code<br>**RISK-040** Production or execution of vulnerable or malicious code<br>**RISK-054** Insecure default configuration of agent frameworks and runtimes |
| **ASI06** Memory and Context Poisoning | **RISK-010** Poisoned memory<br>**RISK-011** Sensitive data leakage across memory contexts<br>**RISK-027** Regurgitating personally identifiable information<br>**RISK-035** Unreliable information or websites<br>**RISK-044** Prompt injection via malicious files or data |
| **ASI07** Insecure Inter-Agent Communication | **RISK-013** Man-in-the-middle attacks between agents<br>**RISK-051** Unsanctioned coordination between agents<br>**RISK-053** Dependence on third-party agents as counterparties or delegates |
| **ASI08** Cascading Failures | **RISK-003** Insufficient LLM capability and reliability<br>**RISK-012** Cascading errors in multi-agent architectures<br>**RISK-014** Feedback loops and runaway agent behaviour<br>**RISK-017** Delayed failure detection due to limited monitoring<br>**RISK-018** Inability to audit failures due to missing decision traces<br>**RISK-021** Incorrect task delegation between agents<br>**RISK-028** Generation of non-factual or hallucinated content<br>**RISK-045** Misconfiguration of system resources |
| **ASI09** Human-Agent Trust Exploitation | **RISK-030** Misrepresentation of authorship<br>**RISK-031** Inaccurate promises or statements in official communications<br>**RISK-050** Deceptive behaviour toward overseers<br>**RISK-052** Automation bias and erosion of human oversight |
| **ASI10** Rogue Agents | **RISK-002** Insufficient alignment of LLM behaviour<br>**RISK-014** Feedback loops and runaway agent behaviour<br>**RISK-018** Inability to audit failures due to missing decision traces<br>**RISK-020** Generating plans that overlook safety implications<br>**RISK-022** Malicious or manipulative use of delegated agents<br>**RISK-049** Escape from evaluation or sandbox containment onto live systems<br>**RISK-050** Deceptive behaviour toward overseers<br>**RISK-051** Unsanctioned coordination between agents |

## OWASP Agentic AI – Threats and Mitigations (threat taxonomy, as reproduced in CSA Addendum Annex A) → ARC risks

| OWASP threat | ARC risks |
| --- | --- |
| **T1** Memory poisoning | **RISK-010** Poisoned memory<br>**RISK-011** Sensitive data leakage across memory contexts<br>**RISK-027** Regurgitating personally identifiable information<br>**RISK-044** Prompt injection via malicious files or data |
| **T2** Tool misuse | **RISK-004** Weak tool authentication and authorisation controls<br>**RISK-006** Tool poisoning by malicious actors<br>**RISK-007** Lack of input sanitisation<br>**RISK-023** Incorrect tool selection or misuse<br>**RISK-032** Unauthorised execution of business transactions<br>**RISK-037** Exposure of sensitive data<br>**RISK-038** Incorrect use of unfamiliar programmatic interfaces<br>**RISK-041** Unintended overwriting or deletion of files or data<br>**RISK-043** Exposure of sensitive data through file or database access<br>**RISK-045** Misconfiguration of system resources<br>**RISK-047** Data exfiltration through combined access to untrusted content, sensitive data, and an outbound channel |
| **T3** Privilege compromise | **RISK-004** Weak tool authentication and authorisation controls<br>**RISK-005** Lack of proper role-based access control for tools<br>**RISK-011** Sensitive data leakage across memory contexts<br>**RISK-015** Overly permissive roles and permissions<br>**RISK-016** Unauthorised privilege escalation<br>**RISK-021** Incorrect task delegation between agents<br>**RISK-033** Leakage of transaction credentials<br>**RISK-043** Exposure of sensitive data through file or database access<br>**RISK-054** Insecure default configuration of agent frameworks and runtimes |
| **T4** Resource overload | **RISK-014** Feedback loops and runaway agent behaviour<br>**RISK-042** Database overload due to inefficient data operations<br>**RISK-046** System overload due to inefficient or excessive operations |
| **T5** Cascading hallucination attacks | **RISK-003** Insufficient LLM capability and reliability<br>**RISK-012** Cascading errors in multi-agent architectures<br>**RISK-014** Feedback loops and runaway agent behaviour<br>**RISK-028** Generation of non-factual or hallucinated content<br>**RISK-035** Unreliable information or websites |
| **T6** Intent breaking and goal manipulation | **RISK-008** Vague or underspecified instructions<br>**RISK-009** Unsanitised inputs in system instructions<br>**RISK-019** Generating plans that fail to meet the user's requirements<br>**RISK-032** Unauthorised execution of business transactions<br>**RISK-034** Prompt injection via malicious websites<br>**RISK-036** Prompt injection risks through computer use<br>**RISK-044** Prompt injection via malicious files or data<br>**RISK-047** Data exfiltration through combined access to untrusted content, sensitive data, and an outbound channel |
| **T7** Misaligned and deceptive behaviours | **RISK-002** Insufficient alignment of LLM behaviour<br>**RISK-020** Generating plans that overlook safety implications<br>**RISK-049** Escape from evaluation or sandbox containment onto live systems<br>**RISK-050** Deceptive behaviour toward overseers |
| **T8** Repudiation and untraceability | **RISK-017** Delayed failure detection due to limited monitoring<br>**RISK-018** Inability to audit failures due to missing decision traces |
| **T9** Identity spoofing and impersonation | **RISK-013** Man-in-the-middle attacks between agents |
| **T10** Overwhelming human in the loop | **RISK-052** Automation bias and erosion of human oversight |
| **T11** Unexpected RCE and code attacks | **RISK-007** Lack of input sanitisation<br>**RISK-039** Production or execution of poor or ineffective code<br>**RISK-040** Production or execution of vulnerable or malicious code<br>**RISK-054** Insecure default configuration of agent frameworks and runtimes |
| **T12** Agent communication poisoning | **RISK-013** Man-in-the-middle attacks between agents<br>**RISK-051** Unsanctioned coordination between agents |
| **T13** Rogue agents in multi-agent systems | **RISK-022** Malicious or manipulative use of delegated agents<br>**RISK-049** Escape from evaluation or sandbox containment onto live systems<br>**RISK-051** Unsanctioned coordination between agents<br>**RISK-053** Dependence on third-party agents as counterparties or delegates |
| **T14** Human attacks on multi-agent systems | **RISK-022** Malicious or manipulative use of delegated agents |
| **T15** Human manipulation | **RISK-030** Misrepresentation of authorship<br>**RISK-031** Inaccurate promises or statements in official communications |
| **T16** Insecure inter-agent protocol abuse | — |
| **T17** Supply chain compromise | **RISK-001** Use of untrusted or compromised LLMs<br>**RISK-006** Tool poisoning by malicious actors<br>**RISK-048** Compromise through the tool, skill, and dependency supply chain |

## CSA Singapore – Securing Agentic AI, an Addendum to the Guidelines and Companion Guide on Securing AI Systems → ARC controls

| CSA Addendum | ARC controls |
| --- | --- |
| **1.1** Conduct a risk assessment in accordance with relevant standards and best practices | — |
| **2.1** Supply chain security – ensure components are from trusted sources | **CTRL-0001** Use only LLMs from verified and trusted model developers<br>**CTRL-0002** Obtain legally binding no-training and no-logging agreements from LLM API service providers<br>**CTRL-0003** Use only established and verified model loaders in production environments<br>**CTRL-0004** Review the LLM's system card to inform risk assessment and model selection<br>**CTRL-0009** Use only MCP servers that implement robust authentication mechanisms in production environments<br>**CTRL-0014** Use only MCP servers from verified and trusted developers<br>**CTRL-0061** Use structured retrieval APIs for web searches rather than web scraping<br>**CTRL-0063** Prioritise search results from verified, high-quality domains<br>**CTRL-0083** Disallow unknown or external files unless they have been scanned for threats<br>**CTRL-0091** Require verified provenance for tools, skills, and dependencies, and re-verify them on every update<br>**CTRL-0095** Apply due diligence and technical bounds to third-party agents before delegating to them or transacting with them |
| **2.2** Consider model hardening | **CTRL-0005** Conduct structured evaluation of multiple LLMs for instruction-following, performance, and safety before deployment |
| **2.3** Harden the system beyond the model itself | **CTRL-0016** Define clearly the agent's role, scope, and non-goals in the system prompt<br>**CTRL-0017** Define clear success criteria for the agent's tasks<br>**CTRL-0096** Harden agent frameworks and runtimes before exposing them, and patch framework vulnerabilities promptly |
| **2.4** Identify, track and protect AI system assets | **CTRL-0039** Ensure each agent publishes standardised, machine-readable capability descriptors accessible to other agents<br>**CTRL-0041** Provide comprehensive descriptions for each tool including intended use, required inputs, and potential outputs<br>**CTRL-0067** Ensure proper documentation of programmatic interfaces for agent use<br>**CTRL-0091** Require verified provenance for tools, skills, and dependencies, and re-verify them on every update |
| **2.5** Have regular backups in the event of compromise | **CTRL-0077** Enable versioning or soft-delete for managed object stores to allow recovery from accidental modifications |
| **2.6** Implement authentication, authorisation and access controls | **CTRL-0010** Use only MCP servers that validate credentials on every inbound request<br>**CTRL-0011** Limit token scopes to the minimum privileges required and avoid broad or wildcard scopes<br>**CTRL-0021** Implement allowlists and denylists to restrict what categories of information can be written to agent memory<br>**CTRL-0025** Ensure all inter-agent communications are encrypted in transit and prohibit plaintext channels<br>**CTRL-0026** Require all agents to authenticate with verifiable, cryptographically signed identities before processing requests<br>**CTRL-0030** Assign each agent a unique, verifiable identity with no shared credentials<br>**CTRL-0031** Use only MCP servers that validate token provenance and prohibit unauthorised token passthrough<br>**CTRL-0089** Enforce default-deny network egress for agent runtimes, allowing only approved destinations |
| **2.7** Implement controls to limit what models or agents can access and generate | **CTRL-0021** Implement allowlists and denylists to restrict what categories of information can be written to agent memory<br>**CTRL-0024** Define formal schemas for inter-agent messages and validate all messages against these schemas before processing<br>**CTRL-0037** Require planning agents to include explicit safety constraints in all generated plans before execution<br>**CTRL-0040** Limit the scope of agent actions through predefined thresholds and baselines<br>**CTRL-0054** Limit agent communications to standard processes with predefined templates<br>**CTRL-0064** Limit computer use to accessing only safe and trusted resources<br>**CTRL-0073** Create a denylist of commands that agents are not permitted to execute<br>**CTRL-0082** Do not grant agents access to personally identifiable or sensitive data unless strictly required<br>**CTRL-0084** Set minimum and maximum limits on what agents can modify within system resources |
| **2.8** Apply least privilege; secure-by-default configurations | **CTRL-0011** Limit token scopes to the minimum privileges required and avoid broad or wildcard scopes<br>**CTRL-0029** Grant agents only the minimum permissions required for their designated tasks<br>**CTRL-0069** Run agent-generated code only in isolated compute environments with network access blocked by default<br>**CTRL-0075** Do not grant write access to agents unless strictly necessary<br>**CTRL-0082** Do not grant agents access to personally identifiable or sensitive data unless strictly required<br>**CTRL-0096** Harden agent frameworks and runtimes before exposing them, and patch framework vulnerabilities promptly |
| **2.9** Segregate environments and segment networks | **CTRL-0013** Test all untested MCP servers in a sandboxed environment before deploying to production<br>**CTRL-0020** Use a dedicated LLM to extract required fields from inputs and filter out extraneous text or embedded instructions<br>**CTRL-0058** Restrict agents to proposing transactions whilst using a separate transaction controller for execution<br>**CTRL-0069** Run agent-generated code only in isolated compute environments with network access blocked by default<br>**CTRL-0089** Enforce default-deny network egress for agent runtimes, allowing only approved destinations<br>**CTRL-0090** Enforce data-flow and capability policies at runtime with a deterministic policy layer that separates untrusted content from privileged actions<br>**CTRL-0092** Contain evaluations and red-team exercises so that agents cannot reach real systems, credentials, or people |
| **2.10** Implement model self-reflection before decisions | **CTRL-0018** Define default behaviour when the agent encounters ambiguous situations<br>**CTRL-0035** Require agents to decompose user goals into explicit sub-goals and validate necessity before proceeding<br>**CTRL-0037** Require planning agents to include explicit safety constraints in all generated plans before execution |
| **2.11** Implement controls to reduce the likelihood of hallucination | **CTRL-0048** Implement methods to reduce hallucination rates in agent outputs<br>**CTRL-0049** Implement UI/UX cues to communicate the risk of hallucination to users<br>**CTRL-0050** Implement features enabling users to verify generated answers against source content |
| **3.1** Ensure availability controls against disruption or failure | **CTRL-0040** Limit the scope of agent actions through predefined thresholds and baselines<br>**CTRL-0072** Monitor runtime and memory consumption of agent-generated code<br>**CTRL-0078** Enforce throttling or rate limits on agent-initiated database operations<br>**CTRL-0079** Validate agent-generated database queries for efficiency before execution against production databases<br>**CTRL-0080** Implement caching mechanisms to reduce repetitive database queries by agents<br>**CTRL-0086** Limit the number of concurrent queries to external systems by agents |
| **3.2** Conduct security testing | **CTRL-0005** Conduct structured evaluation of multiple LLMs for instruction-following, performance, and safety before deployment<br>**CTRL-0017** Define clear success criteria for the agent's tasks<br>**CTRL-0036** Regularly evaluate and test planning behaviour under representative workloads and failure scenarios<br>**CTRL-0038** Conduct safety verification with domain-relevant stress tests and adversarial scenarios before deployment and on a regular cadence afterwards<br>**CTRL-0092** Contain evaluations and red-team exercises so that agents cannot reach real systems, credentials, or people |
| **3.3** Secure the invocation of external tools (e.g. MCP servers) | **CTRL-0009** Use only MCP servers that implement robust authentication mechanisms in production environments<br>**CTRL-0012** Use only MCP servers that integrate with authorisation servers implementing per-client consent mechanisms<br>**CTRL-0014** Use only MCP servers from verified and trusted developers<br>**CTRL-0015** Treat all tool metadata and outputs as untrusted input requiring validation<br>**CTRL-0031** Use only MCP servers that validate token provenance and prohibit unauthorised token passthrough |
| **3.4** Implement security controls between agents | **CTRL-0024** Define formal schemas for inter-agent messages and validate all messages against these schemas before processing<br>**CTRL-0025** Ensure all inter-agent communications are encrypted in transit and prohibit plaintext channels<br>**CTRL-0026** Require all agents to authenticate with verifiable, cryptographically signed identities before processing requests<br>**CTRL-0039** Ensure each agent publishes standardised, machine-readable capability descriptors accessible to other agents<br>**CTRL-0093** Monitor agents for deceptive and collusive behaviour using an independent monitor<br>**CTRL-0095** Apply due diligence and technical bounds to third-party agents before delegating to them or transacting with them |
| **4.1** Validate inputs to models and agents | **CTRL-0015** Treat all tool metadata and outputs as untrusted input requiring validation<br>**CTRL-0019** Use delimiters to enclose untrusted inputs and instruct the LLM to treat delimited content as data only<br>**CTRL-0020** Use a dedicated LLM to extract required fields from inputs and filter out extraneous text or embedded instructions<br>**CTRL-0022** Implement content filtering on memory writes to detect and block known unsafe content patterns<br>**CTRL-0045** Implement input guardrails to detect and decline requests for specialised domain advice<br>**CTRL-0046** Implement input guardrails to detect and decline requests for controversial content that violates organisational policies<br>**CTRL-0051** Implement input guardrails to detect and decline requests to generate copyrighted content<br>**CTRL-0060** Implement escape filtering before incorporating web content into prompts<br>**CTRL-0062** Implement input guardrails to detect prompt injection and adversarial attacks<br>**CTRL-0081** Implement input guardrails to detect personally identifiable information in data accessed by agents<br>**CTRL-0083** Disallow unknown or external files unless they have been scanned for threats<br>**CTRL-0090** Enforce data-flow and capability policies at runtime with a deterministic policy layer that separates untrusted content from privileged actions |
| **4.2** Validate outputs from models and agents | **CTRL-0044** Implement output safety guardrails to detect and prevent generation of undesirable content<br>**CTRL-0047** Implement output guardrails to detect and redact personally identifiable information<br>**CTRL-0059** Apply fraud detection models or heuristics to agent-proposed transactions<br>**CTRL-0068** Use code linters to screen generated code for bad practices and poor syntax<br>**CTRL-0070** Review all agent-generated code before execution<br>**CTRL-0071** Use static code analysers to detect security vulnerabilities and code quality issues<br>**CTRL-0074** Conduct CVE scanning and block execution of code with High or Critical vulnerabilities |
| **4.3** Continuous monitoring and logging | **CTRL-0007** Log all LLM inputs and outputs for regular review<br>**CTRL-0008** Implement automated alerts when agent behaviour drifts from predefined thresholds<br>**CTRL-0023** Log all memory modifications with comprehensive source metadata for audit purposes<br>**CTRL-0027** Implement circuit breakers to prevent cascading failures in multi-agent systems<br>**CTRL-0028** Continuously monitor multi-agent systems for cascade failure indicators<br>**CTRL-0032** Centralise observability data collection in a unified backend system<br>**CTRL-0033** Standardise trace attributes for agent operations using consistent semantic conventions<br>**CTRL-0034** Conduct regular reviews of logs and traces to detect emergent issues in deployed agentic systems<br>**CTRL-0043** Log all tool selection decisions and invocations with comprehensive metadata<br>**CTRL-0085** Log system health metrics and implement automated alerts for abnormal conditions<br>**CTRL-0093** Monitor agents for deceptive and collusive behaviour using an independent monitor |
| **4.4** Ensure adequate human oversight | **CTRL-0006** Require human approval before executing high-impact actions<br>**CTRL-0042** Require explicit human confirmation before executing high-impact or irreversible tool actions<br>**CTRL-0053** Require human approval for communications on sensitive matters<br>**CTRL-0056** Require explicit user confirmation before initiating or committing any business transaction<br>**CTRL-0057** Require out-of-band confirmation when transaction risk signals are elevated<br>**CTRL-0065** Ensure every agent can be immediately paused or terminated by its operators<br>**CTRL-0070** Review all agent-generated code before execution<br>**CTRL-0076** Require human approval for any destructive changes to databases, tables, or files<br>**CTRL-0094** Measure the quality of human oversight and redesign approval steps that have become rubber stamps |
| **4.5** Establish a vulnerability disclosure process | **CTRL-0055** Provide alternative channels for users to clarify communications or provide feedback |

## IMDA – Model AI Governance Framework for Agentic AI → ARC controls

| IMDA MGF | ARC controls |
| --- | --- |
| **2.1.1** Determine suitable use cases | **CTRL-0004** Review the LLM's system card to inform risk assessment and model selection |
| **2.1.2** Bound risks through design (agent limits, agent identity) | **CTRL-0010** Use only MCP servers that validate credentials on every inbound request<br>**CTRL-0011** Limit token scopes to the minimum privileges required and avoid broad or wildcard scopes<br>**CTRL-0012** Use only MCP servers that integrate with authorisation servers implementing per-client consent mechanisms<br>**CTRL-0016** Define clearly the agent's role, scope, and non-goals in the system prompt<br>**CTRL-0017** Define clear success criteria for the agent's tasks<br>**CTRL-0026** Require all agents to authenticate with verifiable, cryptographically signed identities before processing requests<br>**CTRL-0029** Grant agents only the minimum permissions required for their designated tasks<br>**CTRL-0030** Assign each agent a unique, verifiable identity with no shared credentials<br>**CTRL-0031** Use only MCP servers that validate token provenance and prohibit unauthorised token passthrough<br>**CTRL-0037** Require planning agents to include explicit safety constraints in all generated plans before execution<br>**CTRL-0040** Limit the scope of agent actions through predefined thresholds and baselines<br>**CTRL-0054** Limit agent communications to standard processes with predefined templates<br>**CTRL-0058** Restrict agents to proposing transactions whilst using a separate transaction controller for execution<br>**CTRL-0061** Use structured retrieval APIs for web searches rather than web scraping<br>**CTRL-0064** Limit computer use to accessing only safe and trusted resources<br>**CTRL-0069** Run agent-generated code only in isolated compute environments with network access blocked by default<br>**CTRL-0073** Create a denylist of commands that agents are not permitted to execute<br>**CTRL-0075** Do not grant write access to agents unless strictly necessary<br>**CTRL-0077** Enable versioning or soft-delete for managed object stores to allow recovery from accidental modifications<br>**CTRL-0078** Enforce throttling or rate limits on agent-initiated database operations<br>**CTRL-0082** Do not grant agents access to personally identifiable or sensitive data unless strictly required<br>**CTRL-0084** Set minimum and maximum limits on what agents can modify within system resources<br>**CTRL-0086** Limit the number of concurrent queries to external systems by agents<br>**CTRL-0089** Enforce default-deny network egress for agent runtimes, allowing only approved destinations |
| **2.2.1** Clear allocation of responsibilities | **CTRL-0002** Obtain legally binding no-training and no-logging agreements from LLM API service providers<br>**CTRL-0095** Apply due diligence and technical bounds to third-party agents before delegating to them or transacting with them |
| **2.2.2** Design for meaningful human oversight | **CTRL-0006** Require human approval before executing high-impact actions<br>**CTRL-0042** Require explicit human confirmation before executing high-impact or irreversible tool actions<br>**CTRL-0053** Require human approval for communications on sensitive matters<br>**CTRL-0056** Require explicit user confirmation before initiating or committing any business transaction<br>**CTRL-0057** Require out-of-band confirmation when transaction risk signals are elevated<br>**CTRL-0070** Review all agent-generated code before execution<br>**CTRL-0076** Require human approval for any destructive changes to databases, tables, or files<br>**CTRL-0094** Measure the quality of human oversight and redesign approval steps that have become rubber stamps |
| **2.3.1** Technical controls during design and development | **CTRL-0001** Use only LLMs from verified and trusted model developers<br>**CTRL-0009** Use only MCP servers that implement robust authentication mechanisms in production environments<br>**CTRL-0014** Use only MCP servers from verified and trusted developers<br>**CTRL-0015** Treat all tool metadata and outputs as untrusted input requiring validation<br>**CTRL-0018** Define default behaviour when the agent encounters ambiguous situations<br>**CTRL-0019** Use delimiters to enclose untrusted inputs and instruct the LLM to treat delimited content as data only<br>**CTRL-0020** Use a dedicated LLM to extract required fields from inputs and filter out extraneous text or embedded instructions<br>**CTRL-0021** Implement allowlists and denylists to restrict what categories of information can be written to agent memory<br>**CTRL-0022** Implement content filtering on memory writes to detect and block known unsafe content patterns<br>**CTRL-0024** Define formal schemas for inter-agent messages and validate all messages against these schemas before processing<br>**CTRL-0025** Ensure all inter-agent communications are encrypted in transit and prohibit plaintext channels<br>**CTRL-0035** Require agents to decompose user goals into explicit sub-goals and validate necessity before proceeding<br>**CTRL-0039** Ensure each agent publishes standardised, machine-readable capability descriptors accessible to other agents<br>**CTRL-0041** Provide comprehensive descriptions for each tool including intended use, required inputs, and potential outputs<br>**CTRL-0044** Implement output safety guardrails to detect and prevent generation of undesirable content<br>**CTRL-0045** Implement input guardrails to detect and decline requests for specialised domain advice<br>**CTRL-0046** Implement input guardrails to detect and decline requests for controversial content that violates organisational policies<br>**CTRL-0047** Implement output guardrails to detect and redact personally identifiable information<br>**CTRL-0048** Implement methods to reduce hallucination rates in agent outputs<br>**CTRL-0051** Implement input guardrails to detect and decline requests to generate copyrighted content<br>**CTRL-0060** Implement escape filtering before incorporating web content into prompts<br>**CTRL-0062** Implement input guardrails to detect prompt injection and adversarial attacks<br>**CTRL-0063** Prioritise search results from verified, high-quality domains<br>**CTRL-0066** Ensure "take over" mode is activated when entering sensitive data<br>**CTRL-0067** Ensure proper documentation of programmatic interfaces for agent use<br>**CTRL-0068** Use code linters to screen generated code for bad practices and poor syntax<br>**CTRL-0071** Use static code analysers to detect security vulnerabilities and code quality issues<br>**CTRL-0074** Conduct CVE scanning and block execution of code with High or Critical vulnerabilities<br>**CTRL-0081** Implement input guardrails to detect personally identifiable information in data accessed by agents<br>**CTRL-0083** Disallow unknown or external files unless they have been scanned for threats<br>**CTRL-0090** Enforce data-flow and capability policies at runtime with a deterministic policy layer that separates untrusted content from privileged actions<br>**CTRL-0091** Require verified provenance for tools, skills, and dependencies, and re-verify them on every update<br>**CTRL-0096** Harden agent frameworks and runtimes before exposing them, and patch framework vulnerabilities promptly |
| **2.3.2** Test agents before deploying | **CTRL-0005** Conduct structured evaluation of multiple LLMs for instruction-following, performance, and safety before deployment<br>**CTRL-0013** Test all untested MCP servers in a sandboxed environment before deploying to production<br>**CTRL-0036** Regularly evaluate and test planning behaviour under representative workloads and failure scenarios<br>**CTRL-0038** Conduct safety verification with domain-relevant stress tests and adversarial scenarios before deployment and on a regular cadence afterwards<br>**CTRL-0092** Contain evaluations and red-team exercises so that agents cannot reach real systems, credentials, or people |
| **2.3.3** Continuously monitor and test when deploying | **CTRL-0007** Log all LLM inputs and outputs for regular review<br>**CTRL-0008** Implement automated alerts when agent behaviour drifts from predefined thresholds<br>**CTRL-0023** Log all memory modifications with comprehensive source metadata for audit purposes<br>**CTRL-0027** Implement circuit breakers to prevent cascading failures in multi-agent systems<br>**CTRL-0028** Continuously monitor multi-agent systems for cascade failure indicators<br>**CTRL-0032** Centralise observability data collection in a unified backend system<br>**CTRL-0033** Standardise trace attributes for agent operations using consistent semantic conventions<br>**CTRL-0034** Conduct regular reviews of logs and traces to detect emergent issues in deployed agentic systems<br>**CTRL-0043** Log all tool selection decisions and invocations with comprehensive metadata<br>**CTRL-0059** Apply fraud detection models or heuristics to agent-proposed transactions<br>**CTRL-0065** Ensure every agent can be immediately paused or terminated by its operators<br>**CTRL-0072** Monitor runtime and memory consumption of agent-generated code<br>**CTRL-0079** Validate agent-generated database queries for efficiency before execution against production databases<br>**CTRL-0085** Log system health metrics and implement automated alerts for abnormal conditions<br>**CTRL-0093** Monitor agents for deceptive and collusive behaviour using an independent monitor |
| **2.4.2** Users who interact with agents (transparency, disclosure, escalation) | **CTRL-0049** Implement UI/UX cues to communicate the risk of hallucination to users<br>**CTRL-0050** Implement features enabling users to verify generated answers against source content<br>**CTRL-0052** Declare upfront that communications are generated by an AI system<br>**CTRL-0055** Provide alternative channels for users to clarify communications or provide feedback |
| **2.4.3** Users who integrate agents | — |

## ARC risks → external frameworks

| ARC risk | OWASP ASI | OWASP threats |
| --- | --- | --- |
| **RISK-001** Use of untrusted or compromised LLMs | ASI04 | T17 |
| **RISK-002** Insufficient alignment of LLM behaviour | ASI10 | T7 |
| **RISK-003** Insufficient LLM capability and reliability | ASI08 | T5 |
| **RISK-004** Weak tool authentication and authorisation controls | ASI03, ASI02 | T3, T2 |
| **RISK-005** Lack of proper role-based access control for tools | ASI03 | T3 |
| **RISK-006** Tool poisoning by malicious actors | ASI04, ASI02 | T17, T2 |
| **RISK-007** Lack of input sanitisation | ASI02, ASI05 | T2, T11 |
| **RISK-008** Vague or underspecified instructions | ASI01 | T6 |
| **RISK-009** Unsanitised inputs in system instructions | ASI01 | T6 |
| **RISK-010** Poisoned memory | ASI06 | T1 |
| **RISK-011** Sensitive data leakage across memory contexts | ASI06, ASI03 | T1, T3 |
| **RISK-012** Cascading errors in multi-agent architectures | ASI08 | T5 |
| **RISK-013** Man-in-the-middle attacks between agents | ASI07 | T12, T9 |
| **RISK-014** Feedback loops and runaway agent behaviour | ASI08, ASI10 | T5, T4 |
| **RISK-015** Overly permissive roles and permissions | ASI03 | T3 |
| **RISK-016** Unauthorised privilege escalation | ASI03 | T3 |
| **RISK-017** Delayed failure detection due to limited monitoring | ASI08 | T8 |
| **RISK-018** Inability to audit failures due to missing decision traces | ASI08, ASI10 | T8 |
| **RISK-019** Generating plans that fail to meet the user's requirements | ASI01 | T6 |
| **RISK-020** Generating plans that overlook safety implications | ASI10, ASI01 | T7 |
| **RISK-021** Incorrect task delegation between agents | ASI03, ASI08 | T3 |
| **RISK-022** Malicious or manipulative use of delegated agents | ASI10, ASI03 | T13, T14 |
| **RISK-023** Incorrect tool selection or misuse | ASI02 | T2 |
| **RISK-024** Generation of undesirable content | — | — |
| **RISK-025** Generation of unqualified advice in specialised domains | — | — |
| **RISK-026** Generation of controversial or sensitive content | — | — |
| **RISK-027** Regurgitating personally identifiable information | ASI06 | T1 |
| **RISK-028** Generation of non-factual or hallucinated content | ASI08 | T5 |
| **RISK-029** Generation of copyrighted content | — | — |
| **RISK-030** Misrepresentation of authorship | ASI09 | T15 |
| **RISK-031** Inaccurate promises or statements in official communications | ASI09 | T15 |
| **RISK-032** Unauthorised execution of business transactions | ASI02, ASI01 | T2, T6 |
| **RISK-033** Leakage of transaction credentials | ASI03 | T3 |
| **RISK-034** Prompt injection via malicious websites | ASI01 | T6 |
| **RISK-035** Unreliable information or websites | ASI06 | T5 |
| **RISK-036** Prompt injection risks through computer use | ASI01 | T6 |
| **RISK-037** Exposure of sensitive data | ASI02 | T2 |
| **RISK-038** Incorrect use of unfamiliar programmatic interfaces | ASI02 | T2 |
| **RISK-039** Production or execution of poor or ineffective code | ASI05 | T11 |
| **RISK-040** Production or execution of vulnerable or malicious code | ASI05 | T11 |
| **RISK-041** Unintended overwriting or deletion of files or data | ASI02 | T2 |
| **RISK-042** Database overload due to inefficient data operations | ASI02 | T4 |
| **RISK-043** Exposure of sensitive data through file or database access | ASI02, ASI03 | T2, T3 |
| **RISK-044** Prompt injection via malicious files or data | ASI01, ASI06 | T6, T1 |
| **RISK-045** Misconfiguration of system resources | ASI02, ASI08 | T2 |
| **RISK-046** System overload due to inefficient or excessive operations | ASI02 | T4 |
| **RISK-047** Data exfiltration through combined access to untrusted content, sensitive data, and an outbound channel | ASI01, ASI02 | T6, T2 |
| **RISK-048** Compromise through the tool, skill, and dependency supply chain | ASI04 | T17 |
| **RISK-049** Escape from evaluation or sandbox containment onto live systems | ASI10, ASI03 | T13, T7 |
| **RISK-050** Deceptive behaviour toward overseers | ASI10, ASI09 | T7 |
| **RISK-051** Unsanctioned coordination between agents | ASI10, ASI07 | T13, T12 |
| **RISK-052** Automation bias and erosion of human oversight | ASI09 | T10 |
| **RISK-053** Dependence on third-party agents as counterparties or delegates | ASI04, ASI07 | T13 |
| **RISK-054** Insecure default configuration of agent frameworks and runtimes | ASI03, ASI05 | T3, T11 |

## ARC controls → external frameworks

| ARC control | CSA Addendum | IMDA MGF | OWASP ASI |
| --- | --- | --- | --- |
| **CTRL-0001** Use only LLMs from verified and trusted model developers | 2.1 | 2.3.1 | ASI04 |
| **CTRL-0002** Obtain legally binding no-training and no-logging agreements from LLM API service providers | 2.1 | 2.2.1 | ASI04 |
| **CTRL-0003** Use only established and verified model loaders in production environments | 2.1 | — | ASI04, ASI05 |
| **CTRL-0004** Review the LLM's system card to inform risk assessment and model selection | 2.1 | 2.1.1 | ASI10 |
| **CTRL-0005** Conduct structured evaluation of multiple LLMs for instruction-following, performance, and safety before deployment | 2.2, 3.2 | 2.3.2 | ASI10 |
| **CTRL-0006** Require human approval before executing high-impact actions | 4.4 | 2.2.2 | ASI01, ASI09 |
| **CTRL-0007** Log all LLM inputs and outputs for regular review | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0008** Implement automated alerts when agent behaviour drifts from predefined thresholds | 4.3 | 2.3.3 | ASI10 |
| **CTRL-0009** Use only MCP servers that implement robust authentication mechanisms in production environments | 2.1, 3.3 | 2.3.1 | ASI03, ASI04 |
| **CTRL-0010** Use only MCP servers that validate credentials on every inbound request | 2.6 | 2.1.2 | ASI03 |
| **CTRL-0011** Limit token scopes to the minimum privileges required and avoid broad or wildcard scopes | 2.6, 2.8 | 2.1.2 | ASI03 |
| **CTRL-0012** Use only MCP servers that integrate with authorisation servers implementing per-client consent mechanisms | 3.3 | 2.1.2 | ASI03 |
| **CTRL-0013** Test all untested MCP servers in a sandboxed environment before deploying to production | 2.9 | 2.3.2 | ASI04 |
| **CTRL-0014** Use only MCP servers from verified and trusted developers | 2.1, 3.3 | 2.3.1 | ASI04 |
| **CTRL-0015** Treat all tool metadata and outputs as untrusted input requiring validation | 4.1, 3.3 | 2.3.1 | ASI02, ASI04 |
| **CTRL-0016** Define clearly the agent's role, scope, and non-goals in the system prompt | 2.3 | 2.1.2 | ASI01 |
| **CTRL-0017** Define clear success criteria for the agent's tasks | 2.3, 3.2 | 2.1.2 | ASI01 |
| **CTRL-0018** Define default behaviour when the agent encounters ambiguous situations | 2.10 | 2.3.1 | ASI01 |
| **CTRL-0019** Use delimiters to enclose untrusted inputs and instruct the LLM to treat delimited content as data only | 4.1 | 2.3.1 | ASI01 |
| **CTRL-0020** Use a dedicated LLM to extract required fields from inputs and filter out extraneous text or embedded instructions | 4.1, 2.9 | 2.3.1 | ASI01 |
| **CTRL-0021** Implement allowlists and denylists to restrict what categories of information can be written to agent memory | 2.6, 2.7 | 2.3.1 | ASI06 |
| **CTRL-0022** Implement content filtering on memory writes to detect and block known unsafe content patterns | 4.1 | 2.3.1 | ASI06 |
| **CTRL-0023** Log all memory modifications with comprehensive source metadata for audit purposes | 4.3 | 2.3.3 | ASI06, ASI08 |
| **CTRL-0024** Define formal schemas for inter-agent messages and validate all messages against these schemas before processing | 2.7, 3.4 | 2.3.1 | ASI07 |
| **CTRL-0025** Ensure all inter-agent communications are encrypted in transit and prohibit plaintext channels | 3.4, 2.6 | 2.3.1 | ASI07 |
| **CTRL-0026** Require all agents to authenticate with verifiable, cryptographically signed identities before processing requests | 3.4, 2.6 | 2.1.2 | ASI03, ASI07 |
| **CTRL-0027** Implement circuit breakers to prevent cascading failures in multi-agent systems | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0028** Continuously monitor multi-agent systems for cascade failure indicators | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0029** Grant agents only the minimum permissions required for their designated tasks | 2.8 | 2.1.2 | ASI03 |
| **CTRL-0030** Assign each agent a unique, verifiable identity with no shared credentials | 2.6 | 2.1.2 | ASI03 |
| **CTRL-0031** Use only MCP servers that validate token provenance and prohibit unauthorised token passthrough | 3.3, 2.6 | 2.1.2 | ASI03 |
| **CTRL-0032** Centralise observability data collection in a unified backend system | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0033** Standardise trace attributes for agent operations using consistent semantic conventions | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0034** Conduct regular reviews of logs and traces to detect emergent issues in deployed agentic systems | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0035** Require agents to decompose user goals into explicit sub-goals and validate necessity before proceeding | 2.10 | 2.3.1 | ASI01 |
| **CTRL-0036** Regularly evaluate and test planning behaviour under representative workloads and failure scenarios | 3.2 | 2.3.2 | ASI01 |
| **CTRL-0037** Require planning agents to include explicit safety constraints in all generated plans before execution | 2.7, 2.10 | 2.1.2 | ASI01, ASI10 |
| **CTRL-0038** Conduct safety verification with domain-relevant stress tests and adversarial scenarios before deployment and on a regular cadence afterwards | 3.2 | 2.3.2 | ASI01, ASI10 |
| **CTRL-0039** Ensure each agent publishes standardised, machine-readable capability descriptors accessible to other agents | 2.4, 3.4 | 2.3.1 | ASI07 |
| **CTRL-0040** Limit the scope of agent actions through predefined thresholds and baselines | 2.7, 3.1 | 2.1.2 | ASI02, ASI08 |
| **CTRL-0041** Provide comprehensive descriptions for each tool including intended use, required inputs, and potential outputs | 2.4 | 2.3.1 | ASI02 |
| **CTRL-0042** Require explicit human confirmation before executing high-impact or irreversible tool actions | 4.4 | 2.2.2 | ASI02, ASI09 |
| **CTRL-0043** Log all tool selection decisions and invocations with comprehensive metadata | 4.3 | 2.3.3 | ASI02 |
| **CTRL-0044** Implement output safety guardrails to detect and prevent generation of undesirable content | 4.2 | 2.3.1 | — |
| **CTRL-0045** Implement input guardrails to detect and decline requests for specialised domain advice | 4.1 | 2.3.1 | — |
| **CTRL-0046** Implement input guardrails to detect and decline requests for controversial content that violates organisational policies | 4.1 | 2.3.1 | — |
| **CTRL-0047** Implement output guardrails to detect and redact personally identifiable information | 4.2 | 2.3.1 | — |
| **CTRL-0048** Implement methods to reduce hallucination rates in agent outputs | 2.11 | 2.3.1 | ASI08 |
| **CTRL-0049** Implement UI/UX cues to communicate the risk of hallucination to users | 2.11 | 2.4.2 | ASI09 |
| **CTRL-0050** Implement features enabling users to verify generated answers against source content | 2.11 | 2.4.2 | ASI09 |
| **CTRL-0051** Implement input guardrails to detect and decline requests to generate copyrighted content | 4.1 | 2.3.1 | — |
| **CTRL-0052** Declare upfront that communications are generated by an AI system | — | 2.4.2 | ASI09 |
| **CTRL-0053** Require human approval for communications on sensitive matters | 4.4 | 2.2.2 | ASI09 |
| **CTRL-0054** Limit agent communications to standard processes with predefined templates | 2.7 | 2.1.2 | ASI01 |
| **CTRL-0055** Provide alternative channels for users to clarify communications or provide feedback | 4.5 | 2.4.2 | ASI09 |
| **CTRL-0056** Require explicit user confirmation before initiating or committing any business transaction | 4.4 | 2.2.2 | ASI09, ASI02 |
| **CTRL-0057** Require out-of-band confirmation when transaction risk signals are elevated | 4.4 | 2.2.2 | ASI09 |
| **CTRL-0058** Restrict agents to proposing transactions whilst using a separate transaction controller for execution | 2.9 | 2.1.2 | ASI03 |
| **CTRL-0059** Apply fraud detection models or heuristics to agent-proposed transactions | 4.2 | 2.3.3 | ASI02 |
| **CTRL-0060** Implement escape filtering before incorporating web content into prompts | 4.1 | 2.3.1 | ASI01 |
| **CTRL-0061** Use structured retrieval APIs for web searches rather than web scraping | 2.1 | 2.1.2 | ASI01 |
| **CTRL-0062** Implement input guardrails to detect prompt injection and adversarial attacks | 4.1 | 2.3.1 | ASI01 |
| **CTRL-0063** Prioritise search results from verified, high-quality domains | 2.1 | 2.3.1 | ASI06 |
| **CTRL-0064** Limit computer use to accessing only safe and trusted resources | 2.7 | 2.1.2 | ASI02 |
| **CTRL-0065** Ensure every agent can be immediately paused or terminated by its operators | 4.4 | 2.3.3 | ASI10 |
| **CTRL-0066** Ensure "take over" mode is activated when entering sensitive data | — | 2.3.1 | ASI02 |
| **CTRL-0067** Ensure proper documentation of programmatic interfaces for agent use | 2.4 | 2.3.1 | ASI02 |
| **CTRL-0068** Use code linters to screen generated code for bad practices and poor syntax | 4.2 | 2.3.1 | ASI05 |
| **CTRL-0069** Run agent-generated code only in isolated compute environments with network access blocked by default | 2.9, 2.8 | 2.1.2 | ASI05 |
| **CTRL-0070** Review all agent-generated code before execution | 4.2, 4.4 | 2.2.2 | ASI05 |
| **CTRL-0071** Use static code analysers to detect security vulnerabilities and code quality issues | 4.2 | 2.3.1 | ASI05 |
| **CTRL-0072** Monitor runtime and memory consumption of agent-generated code | 3.1 | 2.3.3 | ASI02 |
| **CTRL-0073** Create a denylist of commands that agents are not permitted to execute | 2.7 | 2.1.2 | ASI05 |
| **CTRL-0074** Conduct CVE scanning and block execution of code with High or Critical vulnerabilities | 4.2 | 2.3.1 | ASI04, ASI05 |
| **CTRL-0075** Do not grant write access to agents unless strictly necessary | 2.8 | 2.1.2 | ASI02 |
| **CTRL-0076** Require human approval for any destructive changes to databases, tables, or files | 4.4 | 2.2.2 | ASI02, ASI09 |
| **CTRL-0077** Enable versioning or soft-delete for managed object stores to allow recovery from accidental modifications | 2.5 | 2.1.2 | ASI02 |
| **CTRL-0078** Enforce throttling or rate limits on agent-initiated database operations | 3.1 | 2.1.2 | ASI02 |
| **CTRL-0079** Validate agent-generated database queries for efficiency before execution against production databases | 3.1 | 2.3.3 | ASI02 |
| **CTRL-0080** Implement caching mechanisms to reduce repetitive database queries by agents | 3.1 | — | ASI02 |
| **CTRL-0081** Implement input guardrails to detect personally identifiable information in data accessed by agents | 4.1 | 2.3.1 | — |
| **CTRL-0082** Do not grant agents access to personally identifiable or sensitive data unless strictly required | 2.8, 2.7 | 2.1.2 | ASI03 |
| **CTRL-0083** Disallow unknown or external files unless they have been scanned for threats | 4.1, 2.1 | 2.3.1 | ASI01, ASI04 |
| **CTRL-0084** Set minimum and maximum limits on what agents can modify within system resources | 2.7 | 2.1.2 | ASI02 |
| **CTRL-0085** Log system health metrics and implement automated alerts for abnormal conditions | 4.3 | 2.3.3 | ASI08 |
| **CTRL-0086** Limit the number of concurrent queries to external systems by agents | 3.1 | 2.1.2 | ASI02 |
| **CTRL-0089** Enforce default-deny network egress for agent runtimes, allowing only approved destinations | 2.6, 2.9 | 2.1.2 | ASI02 |
| **CTRL-0090** Enforce data-flow and capability policies at runtime with a deterministic policy layer that separates untrusted content from privileged actions | 2.9, 4.1 | 2.3.1 | ASI01 |
| **CTRL-0091** Require verified provenance for tools, skills, and dependencies, and re-verify them on every update | 2.1, 2.4 | 2.3.1 | ASI04 |
| **CTRL-0092** Contain evaluations and red-team exercises so that agents cannot reach real systems, credentials, or people | 2.9, 3.2 | 2.3.2 | ASI10 |
| **CTRL-0093** Monitor agents for deceptive and collusive behaviour using an independent monitor | 4.3, 3.4 | 2.3.3 | ASI10 |
| **CTRL-0094** Measure the quality of human oversight and redesign approval steps that have become rubber stamps | 4.4 | 2.2.2 | ASI09 |
| **CTRL-0095** Apply due diligence and technical bounds to third-party agents before delegating to them or transacting with them | 2.1, 3.4 | 2.2.1 | ASI04 |
| **CTRL-0096** Harden agent frameworks and runtimes before exposing them, and patch framework vulnerabilities promptly | 2.3, 2.8 | 2.3.1 | ASI05, ASI03 |
