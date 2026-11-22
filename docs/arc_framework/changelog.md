# Changelog

!!! abstract "Page Summary"

    What changed in each version of the ARC risk register, and the versioning policy that lets you cite or pin a specific version. The current version is shown at the top of the [Interactive Risk Register](risk-register.md) and recorded in the register's machine-readable YAML (`arc-risk-register/register.yaml`).

## Versioning policy

The register version lives in `arc-risk-register/register.yaml` and follows `MAJOR.MINOR.PATCH`:

| Change | Bump | Examples |
| --- | --- | --- |
| The model changes — elements, failure modes, hazard categories, or what the control levels mean | **MAJOR** | adding a failure mode; redefining Level 0 |
| Entries are added, retired, merged, re-tiered, or re-mapped | **MINOR** | new risks; a control moved between levels; a control attached to a different risk |
| Wording, references, or crosswalks change without altering meaning | **PATCH** | clarifying a recommendation; adding a source |

Rules that hold across versions:

- **IDs are never reused.** A retired or merged entry keeps its ID and gains a `superseded_by` pointer, so assessments and citations written against an older version remain resolvable.
- Each release to the `main` branch is tagged `v<version>` on GitHub; the register YAML for any version can be retrieved from the tag.
- To cite a specific version: *GovTech Singapore (2026). Agentic Risk & Capability Framework, risk register v1.5.0.* followed by the site URL.

## 2.0.0 — in preparation { #v2-0-0 }

Version 2.0 changes the model, so an assessment or a contextualised register written against 1.x needs migrating. This section is a draft and grows as the changes are agreed.

- **Protocols is a component.** CMP-05 covers the standard interfaces, such as MCP and A2A, through which a system connects to tools, services and agents that another party builds or operates, in either direction. This follows the Cyber Security Agency of Singapore's addendum and IMDA's framework, which both list protocols as a component, with a narrower definition: a function or API wrapper that the system's own team writes is a tool, not a protocol connection. RISK-006 (tool poisoning) now arises from Protocols, and its description covers hidden instructions in tool descriptions and agent cards, shadowing, and definitions that change after approval. RISK-053 (third-party agents) now requires both Protocols and Agent Delegation.
- **Conditional components.** A component can state when a system has it (`present_when`). Memory is present when the system keeps information beyond a single session or shares it across users or tasks; Protocols when another party's tool server or agent is connected through an agent protocol. The risks of a conditional component apply only to systems that have it. This replaces the 1.4.0 practice of listing those risks for every system and waiving their Level 0 controls one by one. A system without persistent memory or outside connections now has 17 baseline risks, down from 20.
- **Twelve new risks, written from the incident file.** A [curated list of 366 cases](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/incidents) was mapped to the register, and each gap that had three or more cases, at least one of them harm, from more than one source, became a risk:
    - RISK-056 Actions beyond the agent's tools through code execution and reachable credentials (Code Execution)
    - RISK-057 Pursuit of a goal by means the principal did not sanction (Planning and Goal Management)
    - RISK-058 Instruction and configuration files as a way in (Instructions)
    - RISK-059 Prompt injection through inbound messages (Other Programmatic Interfaces)
    - RISK-060 Agent credentials that are over-broad, long-lived, or outlive their use (Roles and Access Controls)
    - RISK-061 Dependence on a model provider (LLM)
    - RISK-062 Agent alters or disables the oversight placed on it (the new rule "oversight within reach")
    - RISK-063 Authority passing between agents without a check (Agent Delegation)
    - RISK-064 Harm from a connected tool server or agent to the system that connects to it (Protocols)
    - RISK-065 Instructions or approvals forged in the principal's name (Roles and Access Controls)
    - RISK-066 Personal data collected, kept, or passed on beyond what the task needs (File and Data Management)
    - RISK-067 Use of the agent by its own principal against others (Instructions; the first risk under Misuse by the Principal)
- **Ten new controls.** Three are Level 0: CTRL-0098 (keep credentials and backups out of reach of agent-run code), CTRL-0100 (load instruction and configuration files only from locations the operator controls) and CTRL-0101 (no write access for agents to their own instructions, configuration, permissions, logs or monitors). Seven are Level 1: CTRL-0099, CTRL-0102, CTRL-0103, CTRL-0104, CTRL-0105, CTRL-0106 and CTRL-0107.
- **A second combination rule.** "Oversight within reach" is present when a capability lets the agent change what governs it. It brings RISK-062 into scope and requires CTRL-0101.
- **MCP-specific controls apply only with Protocols.** CTRL-0010, CTRL-0012, CTRL-0013 and CTRL-0031 now mitigate RISK-064, which arises from the Protocols component, and are removed from RISK-004, RISK-005, RISK-048 and RISK-015. A system with no outside tool servers or agents no longer carries them.
- **Controls say where they are enforced and how to check them.** Every control records its enforcement point (prompt, model, harness, infrastructure or organisation), its usual owner, the lifecycle phases it applies in, the evidence that shows it is in place, and a test that shows it works. Of the 93 controls, 45 are enforced mainly in the harness, 23 in infrastructure, 11 by the organisation, 8 in the model and 6 in the prompt.
- **Every control has references.** The 68 controls that had none now cite one to three sources each, drawn mainly from the CSA addendum, OWASP's Securing Agentic Applications Guide, IMDA's framework, the Five Eyes guidance, and NIST publications.
- **Two controls merged.** CTRL-0006 (human approval before high-impact actions) is retired in favour of CTRL-0042 (human confirmation before high-impact or irreversible tool actions), which now also mitigates RISK-001, 002, 003, 019 and 020. CTRL-0014 (MCP servers from verified and trusted developers) is retired in favour of CTRL-0091 (verified provenance for tools, skills and dependencies), whose guidance now includes assessing the publisher.
- **Stronger sources for 13 risks.** Opinion pieces, secondary news and sources that did not support the risk as described are replaced with papers, advisories, standards and a tribunal decision. The risks are RISK-006, 015, 016, 020, 025, 030, 031, 032, 035, 042, 043, 044 and 054; RISK-018 and RISK-047 each have one source updated.
- **Overlays.** An organisation's version of the register can be kept as an overlay: one file that adds its own entries (with a namespaced ID such as `EXA-RISK-001`), changes fields of existing ones, removes what it does not use, and marks controls that a shared platform provides. `scripts/apply_overlay.py` writes the effective register, and the assessment skill takes `--overlay` directly. See [For governance teams](../implementation/for-governance-teams.md#keeping-your-version-as-an-overlay).
- **Two new crosswalks.** Risks are mapped to [MITRE ATLAS](https://atlas.mitre.org/) (release 2026.10): 23 risks that involve an adversary, a security weakness, or goal-directed agent behaviour that ATLAS catalogues are mapped, and the rest are left unmapped. Controls are mapped to the practice areas of the Five Eyes guidance [Careful adoption of agentic AI services](https://www.cyber.gov.au/publication/careful-adoption-of-agentic-ai-services) (May 2026): 88 of 95 controls are mapped. The guidance does not number its practice areas, so the IDs are ARC's own.
- **Combination rules.** `combinations.yaml` now holds *roles* (what a capability can contribute, such as untrusted content or an outbound channel) and *rules* that name the roles that must all be supplied. Any capability that supplies a role will do, so a rule covers every pairing. A rule that is present or possible brings its risks into scope. Some marks apply only from a certain authority upwards: Official Communication and Business Transactions are an outbound channel only when the agent itself sends or transacts.
- **One exfiltration risk.** RISK-047 now arises from the lethal trifecta rule instead of from Internet and Search Access plus File and Data Management, and its description covers every route in and out. RISK-055, added in 1.5.0 for the message route, is retired and points to RISK-047. The 256 capability sets that completed the trifecta in 1.5.0 without any risk carrying CTRL-0097 are now covered.
- **Capabilities that give a system others.** Code Execution, Computer Use, System Management and Agent Delegation can give a system capabilities that were not declared. The register lists these (`implies`), and an assessment either adds each implied capability or records why it does not apply.
- **Retired entries.** A risk or control that is merged or withdrawn keeps its ID and gains `superseded_by`. It no longer applies to any system, and the full-text register lists it under "Retired" so that older citations resolve.
- **Context: authority, reversibility and reach.** Each capability that acts on the world (CAP-05 to CAP-12) lists the authority levels it can be used at (read, propose, act with approval, act alone) and says whether its effects are irreversible and external: always, never, or a question for the assessor. An assessment records these for the system. Where they are not stated, the most cautious case is assumed, so a 1.x assessment carries over unchanged.
- **Official Communication and Business Transactions no longer assume autonomy.** Their definitions drop "autonomously", "without prior human review or approval" and "within predefined authorisation limits". A system that drafts official messages for a person to send now has CAP-05, at the authority *propose*.
- **Risks can need a minimum authority** (`min_authority`). RISK-032 (unauthorised transactions), RISK-041 (unintended overwriting or deletion), RISK-045 (misconfiguration of system resources) and RISK-049 (sandbox escape) apply only when the agent itself carries out the action, that is, at *act with approval* or above.
- **Control levels can depend on context** (`level_when`). CTRL-0042 (human confirmation before high-impact or irreversible tool actions) is Level 0 when a capability acts alone with irreversible and external effects. CTRL-0043 (log all tool invocations) is Level 0 when a capability acts alone. Both remain Level 1 otherwise.
- **Six failure modes.** "Agent Failure", which held 37 of 55 risks, is split into *Agent Error* (the agent makes a mistake; 26 risks) and *Agent Misbehaviour* (the agent pursues an objective by means its principal did not sanction; RISK-002, 022, 049, 050 and 051). *Safeguard Failure* is new and holds the risks that describe a missing or weak safeguard, not a trigger: RISK-015, 016, 017, 018 and 052. *Misuse by the Principal* is new and covers harm that the agent's own user or operator directs. RISK-011 (leakage across memory contexts) moves to Tool or Resource Malfunction. External Manipulation is unchanged.
- **Two new hazards.** HZ-10 Financial or contractual loss, on RISK-031, RISK-032 and RISK-033, and HZ-11 Harm to third parties, on RISK-049. RISK-032 and RISK-033 become Safety and Security risks as a result.
- **No thirteenth capability.** Agent-to-agent interaction is not added as a capability. Agent Delegation (CAP-02) remains the capability, and Protocols covers the channel to other parties' agents, including requests they send in.

## 1.5.0 — November 2026 { #v1-5-0 }

Level 0 is re-tiered and matched to its subject. Human approval of the highest-risk actions becomes a floor, controls that rely only on a probabilistic detector or on code quality leave it, and each Level 0 control now names the capability or component it concerns, so the waiver rule introduced in 1.4.0 applies cleanly. The register also gains a check for capability combinations, starting with the lethal trifecta.

- **Capability combinations and the lethal trifecta.** A new page, [Capability combinations](capability-combinations.md), explains risks that arise only when capabilities are held together. The register now records, in `combinations.yaml`, which capabilities supply each leg of the lethal trifecta: untrusted content, sensitive data, and an outbound channel. A check reads a system's capabilities and reports the combination as present, possible, or not present. The check is on the page, in the [assessment template](../implementation/assessment-template.md#2a-capability-combinations), and in the ARC assessment skill. The verdict decides whether the new control is implemented or waived; it does not change which risks apply.
- **A control that breaks the trifecta.** CTRL-0097 (Level 0) requires that no one agent hold untrusted content, sensitive data, and an unrestricted outbound channel at once: remove one, or gate the outbound channel outside the agent. It is attached to RISK-037, RISK-044, RISK-047 and RISK-055, and is waived, with evidence, when one of the three is absent.
- **Exfiltration through messages.** RISK-047 applied only to systems with both Internet and Search Access and File and Data Management, so an email or ticketing agent was missed. RISK-055 (data exfiltration through message and API channels) covers the same combination for systems with Other Programmatic Interfaces (CAP-09) and File and Data Management (CAP-11). CAP-09's definition now states that it includes sending and receiving email, chat, and other messages through an API or mail protocol.

- **Human approval for transactions, official communications and deletion is Level 0.** CTRL-0056 now requires explicit human confirmation for any business transaction outside limits that an accountable human has pre-authorised, and for every transaction where no limits are set; it was narrowed from "any business transaction" to agree with Business Transactions (CAP-06), which transacts autonomously within limits. CTRL-0058 (agents propose transactions; a separate controller executes them) is Level 0, giving RISK-033 (leakage of transaction credentials) its first Level 0 control. CTRL-0053 (human approval for communications on sensitive matters) is Level 0, and its guidance now requires the approval to be enforced in the sending path. CTRL-0076 now requires human approval for destructive changes that cannot be readily undone; changes recoverable through version control or soft-delete (CTRL-0077) may proceed without it.
- **Approvals must stay real decisions.** CTRL-0094 (measure the quality of human oversight) is Level 0 and is now attached to RISK-031, RISK-032 and RISK-041 as well as RISK-052. A system with no human approval steps records it as waived.
- **Least privilege is Level 0.** CTRL-0029 now applies to every system, giving RISK-015 (overly permissive roles) its first Level 0 control.
- **Detector-only and code-quality controls leave Level 0.** CTRL-0051 (copyright input guardrails) and CTRL-0068 (code linters) move to Level 1. RISK-039 keeps code sandboxing and static analysis at Level 0; RISK-029 (copyrighted content) is now left to scoring.
- **Untrusted input kept out of system instructions.** CTRL-0019 stays Level 0 but now requires keeping untrusted inputs out of system instructions, with delimiters as a second measure, instead of relying on delimiters and the model's compliance alone.
- **CVE scanning stays with code execution.** CTRL-0074 (CVE-scan agent-generated code and block High or Critical vulnerabilities) is now attached only to RISK-040 (vulnerable or malicious code). It is removed from RISK-048 (supply-chain compromise) and RISK-054 (insecure framework defaults), which are already covered by CTRL-0091 (verified provenance, including vulnerability scanning of new packages) and CTRL-0096 (runtime hardening and timely patching).
- **Tool authentication covers every remote tool.** CTRL-0009 now requires robust authentication on all tool servers and APIs, including MCP servers, so RISK-004 (weak tool authentication) keeps an authentication control in systems that use no MCP servers. Its MCP-specific requirements are unchanged. CTRL-0010 and CTRL-0013 remain specific to MCP servers.
- **Working and persistent memory.** The Memory component (CMP-04) now distinguishes working memory, which every agent has, from persistent memory, which keeps information beyond a single session or shares it across users or tasks. The memory-write controls CTRL-0021, CTRL-0022 and CTRL-0023 now concern persistent memory, so a system that keeps nothing beyond a session records CTRL-0021 as waived, with evidence. RISK-010 (poisoned memory) and RISK-011 (leakage across memory contexts) are unchanged.
- Register: 54 → 55 risks and 94 → 95 controls; Level 0 controls 39 → 44; risks with no Level 0 control 12 → 9. Level 0 controls per system, before waivers, compared with 1.4.0: a single-agent Q&A system stays at 21 (it gains least privilege and oversight quality, the latter waived where there are no approval steps, and loses CVE scanning and copyright guardrails); the developer guide's fact checker goes from 29 to 31, its coding assistant from 34 to 36, and its call assistant from 29 to 34, with one more applicable risk (RISK-055).

## 1.4.0 — November 2026 { #v1-4-0 }

Applicability: a risk should apply only to systems that have the elements it arises from.

- **Multi-agent risks need Agent Delegation.** RISK-012 (cascading errors), RISK-013 (man-in-the-middle attacks between agents) and RISK-051 (unsanctioned coordination) now arise from the agentic architecture (DSN-01) *together with* Agent Delegation (CAP-02), so a single-agent system no longer carries them or their multi-agent controls. Agent Delegation now states that it covers workflows with fixed hand-offs and agents operated by other parties, including counterparties, so these risks apply across organisational boundaries too.
- **Runaway behaviour covers single agents.** RISK-014 stays a baseline risk, rewritten to include an agent acting on its own outputs without bound. It now carries CTRL-0040 (action thresholds) instead of CTRL-0028 (multi-agent cascade monitoring), which stays on RISK-012 and RISK-051, so every system keeps the kill switch (CTRL-0065) and action limits. The agentic architecture element (DSN-01) now includes a single agent's plan–act–observe loop.
- **Sandbox escape needs Code Execution.** RISK-049 (escape from evaluation or sandbox containment) now arises from roles and access controls (DSN-02) *together with* Code Execution (CAP-10), the path in every incident it cites, so systems that cannot run code no longer carry code sandboxing (CTRL-0069) or contained evaluations (CTRL-0092) through it. Default-deny egress (CTRL-0089) is now also attached to RISK-037 (exposure of sensitive data through computer use), so computer-use agents keep it.
- **Level 0 waived when its subject is absent.** A Level 0 control still applies to every applicable risk whatever its score, but is waived when the capability or component it concerns is not present in the system (for example, MCP-server controls in a system that uses no MCP servers). The assessment records the waiver with evidence; the [Assessment Template](../implementation/assessment-template.md) gains a *Waived — not applicable* status and keeps one row per control per risk.
- **Site and tools.** A [full-text register](register-full-text.md) with a link for every risk and control, and an `llms.txt` index, make the site readable by AI agents; the site's register JSON and generated pages are now built from the YAML at build time rather than committed. The [ARC assessment skill](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/skills) lets a coding agent assess the system it is building against the register.
- Register: 54 risks and 94 controls (unchanged); baseline risks 24 → 20. Systems with Agent Delegation and Code Execution carry the same risks and Level 0 controls as before; a single-agent Q&A system goes from 26 Level 0 controls to 21.

## 1.3.0 — November 2026 { #v1-3-0 }

Consolidation release: no change to the framework's model. Published to the site together with 1.2.0.

- **Data integrity.** Crosswalk IDs are quoted strings; an unquoted `2.10` had been read as `2.1`, mis-mapping three controls to the wrong CSA Addendum section. The validator now rejects non-string IDs.
- **Mappings corrected.** Twelve controls were attached to the wrong risk or missing from an obvious one (circuit breakers not on cascading errors; least privilege not on overly permissive roles; fraud detection on credential leakage instead of unauthorised transactions; and others). 23 links added, 4 moved.
- **Hazards recorded.** Every risk lists the hazards it results in (`hazards.yaml`, nine categories); a risk's Safety/Security type must agree with its hazards. The register page can be filtered by hazard.
- **Level 0 applicability stated once.** A Level 0 control attaches to every risk whose elements are present, regardless of impact/likelihood score; scoring governs Levels 1 and 2. The developer guide's worked examples were corrected to follow this.
- **ARCvisor follows the Level 0 rule.** It lists every Level 0 control for every applicable risk, not only for risks above the scoring thresholds, and Level 0 entries start blank instead of defaulting to "I accept all residual risk"; the export flags any left undescribed. The model for each step is now one setting (`ARCVISOR_MODEL`).
- **Site.** The December-2025 comparison page was retired in favour of the generated Crosswalks; an [Assessment Template](../implementation/assessment-template.md) and a contributing guide were added; the register now carries a version.

## 1.2.0 — August 2026 { #v1-2-0 }

- **Eight new risks** (RISK-047 to RISK-054) from the 2026 evidence base: data exfiltration through untrusted content + sensitive data + an outbound channel (the first *composite* risk), tool/skill supply-chain compromise, sandbox escape, deceptive behaviour toward overseers, unsanctioned inter-agent coordination, automation bias, dependence on third-party agents, insecure runtime defaults.
- **Eight new controls** (CTRL-0089 to CTRL-0096): default-deny egress, deterministic data-flow policy layer, verified provenance for tools and skills, contained evaluations, an independent monitor for deception and collusion, measured oversight quality, third-party agent due diligence, runtime hardening.
- **Nine controls updated** for the 2026 landscape: MCP specification 2026-07-28, agent identity mechanisms, a generalised kill switch (CTRL-0065), approval-fatigue caveats on human-approval controls, continuous safety testing (CTRL-0038).
- Register: 54 risks, 94 controls (39 Level 0).

## 1.1.0 — August 2026 { #v1-1-0 }

- **Mapping realignment.** Risk-to-control mappings had been offset by one position from CTRL-0044 onward in the YAML, the site, and the paper appendix; corrected, and two duplicate controls merged. A validator now runs before every build.
- **Level 0 redefined as strictly unwaivable**, and ten controls that could not meet that bar re-tiered (Level 0 from 45 to 35 of 86).
- **Risks may arise from a combination of elements** (`element_ids` list); a multi-element risk applies only when all its elements are present.
- **Crosswalks** to the OWASP Top 10 for Agentic Applications, OWASP's agentic threat taxonomy, the CSA Securing Agentic AI Addendum (final, 17 June 2026), and IMDA's Model AI Governance Framework for Agentic AI, on every entry and on a generated [Crosswalks](crosswalks.md) page.
- **ARCvisor** reads this register directly instead of a stale private copy; continuous integration validates the register, builds the site, and runs the app's tests on every change.
- Register: 46 risks, 86 controls.

## December 2025 site update

Introduction with design rationale and literature review; unified Elements page; interactive risk register; ARCvisor tool and preprint; the framework paper accepted at IASEAI 2026. Register content unchanged (46 risks, 88 controls).

## 1.0.0 — August 2025 { #v1-0-0 }

Initial public release of the framework and register: three elements (components, design, twelve capabilities), three failure modes, two hazard families, 46 risks and 88 controls at three levels.
