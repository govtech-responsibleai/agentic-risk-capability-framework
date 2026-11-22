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

## 1.5.0 — November 2026 { #v1-5-0 }

Level 0 is re-tiered and matched to its subject. Human approval of the highest-risk actions becomes a floor, controls that rely only on a probabilistic detector or on code quality leave it, and each Level 0 control now names the capability or component it concerns, so the waiver rule introduced in 1.4.0 applies cleanly.

- **Human approval for transactions, official communications and deletion is Level 0.** CTRL-0056 now requires explicit human confirmation for any business transaction outside limits that an accountable human has pre-authorised, and for every transaction where no limits are set; it was narrowed from "any business transaction" to agree with Business Transactions (CAP-06), which transacts autonomously within limits. CTRL-0058 (agents propose transactions; a separate controller executes them) is Level 0, giving RISK-033 (leakage of transaction credentials) its first Level 0 control. CTRL-0053 (human approval for communications on sensitive matters) is Level 0, and its guidance now requires the approval to be enforced in the sending path. CTRL-0076 now requires human approval for destructive changes that cannot be readily undone; changes recoverable through version control or soft-delete (CTRL-0077) may proceed without it.
- **Approvals must stay real decisions.** CTRL-0094 (measure the quality of human oversight) is Level 0 and is now attached to RISK-031, RISK-032 and RISK-041 as well as RISK-052. A system with no human approval steps records it as waived.
- **Least privilege is Level 0.** CTRL-0029 now applies to every system, giving RISK-015 (overly permissive roles) its first Level 0 control.
- **Detector-only and code-quality controls leave Level 0.** CTRL-0051 (copyright input guardrails) and CTRL-0068 (code linters) move to Level 1. RISK-039 keeps code sandboxing and static analysis at Level 0; RISK-029 (copyrighted content) is now left to scoring.
- **Untrusted input kept out of system instructions.** CTRL-0019 stays Level 0 but now requires keeping untrusted inputs out of system instructions, with delimiters as a second measure, instead of relying on delimiters and the model's compliance alone.
- **CVE scanning stays with code execution.** CTRL-0074 (CVE-scan agent-generated code and block High or Critical vulnerabilities) is now attached only to RISK-040 (vulnerable or malicious code). It is removed from RISK-048 (supply-chain compromise) and RISK-054 (insecure framework defaults), which are already covered by CTRL-0091 (verified provenance, including vulnerability scanning of new packages) and CTRL-0096 (runtime hardening and timely patching).
- **Tool authentication covers every remote tool.** CTRL-0009 now requires robust authentication on all tool servers and APIs, including MCP servers, so RISK-004 (weak tool authentication) keeps an authentication control in systems that use no MCP servers. Its MCP-specific requirements are unchanged. CTRL-0010 and CTRL-0013 remain specific to MCP servers.
- **Working and persistent memory.** The Memory component (CMP-04) now distinguishes working memory, which every agent has, from persistent memory, which keeps information beyond a single session or shares it across users or tasks. The memory-write controls CTRL-0021, CTRL-0022 and CTRL-0023 now concern persistent memory, so a system that keeps nothing beyond a session records CTRL-0021 as waived, with evidence. RISK-010 (poisoned memory) and RISK-011 (leakage across memory contexts) are unchanged.
- Register: 54 risks and 94 controls (unchanged); Level 0 controls 39 → 43; risks with no Level 0 control 12 → 9. Level 0 controls per system, before waivers, compared with 1.4.0: a single-agent Q&A system stays at 21 (it gains least privilege and oversight quality, the latter waived where there are no approval steps, and loses CVE scanning and copyright guardrails); the developer guide's fact checker goes from 29 to 30, its coding assistant from 34 to 35, and its call assistant from 29 to 32.

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
