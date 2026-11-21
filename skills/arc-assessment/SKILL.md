---
name: arc-assessment
description: Assess an agentic AI system with GovTech Singapore's Agentic Risk & Capability (ARC) Framework. Identifies the system's capabilities from its code, lists the applicable risks and controls from the ARC risk register, checks which controls are implemented, and drafts the assessment. Use when building, reviewing, or changing an LLM agent or multi-agent system and the user asks for an ARC assessment, a safety or security risk review of the agent, or which ARC risks or controls apply. Works with the official register or an organisation's own contextualised version.
---

# ARC assessment

This skill applies the [ARC Framework](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/) to the agentic system in the current codebase, following the four steps of ARC's [guide for AI developers](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/for-ai-developers/): identify capabilities, evaluate risks, implement controls, and assess residual risks. The output is a filled-in ARC [assessment template](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/assessment-template/).

All register content comes from `scripts/arc.py`. Do not answer from memory: quote risk, control, and element IDs (e.g. RISK-034, CTRL-0062, CAP-07) exactly as the script prints them.

## Running the script

The script needs only Python 3.9+ (it uses PyYAML if present, and a built-in parser otherwise). Below, `ARC` stands for `python3 <skill directory>/scripts/arc.py`, where the skill directory is the folder containing this file (for example `.claude/skills/arc-assessment` or `~/.claude/skills/arc-assessment`). Run it from the repository root.

```bash
ARC elements                                          # definitions of components, design elements, capabilities
ARC assess --capabilities CAP-03,CAP-07               # applicable risks and their controls
ARC assess --capabilities ... --priority RISK-...     # ...plus every control in scope, once each
ARC show RISK-034 CTRL-0062 CAP-07                    # full text of any entry
ARC template                                          # the assessment template as plain Markdown
```

- Global options go before the command: `--version X.Y.Z`, `--register PATH_OR_URL`, `--refresh`. `--format json` goes after it; use JSON for large systems.
- By default the script reads the latest official release from `raw.githubusercontent.com`. The first output line names the version. **Pass that `--version` on every later command**, so the whole assessment uses one register version (and works offline from the cache).
- Release files are cached in `ARC_CACHE_DIR` (default `~/.cache/arc-assessment/`). If that isn't writable, set `ARC_CACHE_DIR` to a directory inside the repository's working area.

## Before you start

Ask the user these questions. If you can't reach them, choose a sensible default and record the assumption in the assessment's overview.

1. **Does the organisation have its own contextualised ARC register?** ARC is meant to be adapted by each organisation. If one exists, use it with `--register <directory or base URL>` (same file layout as the official `arc-risk-register/`). If it has its own assessment template, use `ARC template --file <path>`.
2. **What are the organisation's relevance threshold and scoring scales?** These are set by its governance team. If there are none, use ARC's [five-point impact and likelihood scales](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/for-governance-teams/#step-4-define-relevance-criteria), and ask the user to choose a threshold.
3. **Where should the assessment be saved?** The default is `docs/arc-assessment.md`.

## Step 1: Identify capabilities

1. Run `ARC elements` and read the capability definitions. **Go by each definition, not the name.** For example, the capability called "Multimodal Understanding and Generation" also covers text-only conversation.
2. Inspect the codebase for what the system can do autonomously, including:
   - agent and sub-agent definitions;
   - tool and function schemas, and MCP server and plugin configuration;
   - system prompts and orchestration code;
   - the APIs, databases, file systems, shells, browsers, and messaging or payment services it is connected to.
3. Map each function to every capability whose definition it fits. One function can map to several capabilities. For example, an email-sending tool can be both Official Communication and Other Programmatic Interfaces.
4. Follow these rules when mapping:
   - Capabilities are system-level: if any agent has one, the system has it.
   - Look at what the system *does*, not just which tools exist. Read-only access can still expose data.
   - If you are unsure, include the capability and mark it as borderline so the reviewer can decide.
   - Count what the system is built to do. If a defect lets it do more (for example, an injection flaw that runs arbitrary queries), record the defect as a finding, not as a capability.
5. For each capability, record:
   - the evidence, as file paths and line numbers;
   - which agent or tool provides it;
   - whether a human approves before it acts. If only some actions are approved, say which.

   Also list the capabilities you ruled out, with reasons.
6. Show the user the capability list and evidence. Get their confirmation before Step 2.

## Step 2: Evaluate risks

1. Run `ARC --version X.Y.Z assess --capabilities <confirmed IDs>`. It lists every applicable risk:
   - baseline risks, which come from components and design elements and are present in every agentic system;
   - risks from each capability;
   - risks from combinations of elements, which apply only when all of their elements are present.
2. For each applicable risk, describe in one or two sentences how it would arise in this system, naming the components or code paths involved.
3. Score impact and likelihood on the scales from "Before you start", with a reason for each score. Mark as *priority* the risks that meet the threshold.
4. Run `assess` again with `--priority <priority risk IDs>`. Its "Controls in scope" section lists each control once, with the risks it addresses:
   - the Level 0 controls of every applicable risk;
   - the Level 1 and 2 controls of the priority risks.

   This follows ARC's [control levels](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/controls/#control-levels): scoring decides where Level 1 and 2 effort goes, and does not remove Level 0 controls.

## Step 3: Implement controls

For each control in scope, follow these steps.

1. Read its guidance with `ARC show CTRL-xxxx`, or use `assess --detail --format json`.
2. Search the codebase for an existing implementation, and record the evidence: file paths, configuration, or tests.
3. Fill in the template's Controls table:
   - **Status:** as-is, adapted, not adopted, or waived — not applicable.
   - **Implementation:** what is done, where, and with what thresholds. For a control that isn't in place yet, write "Not implemented", followed by the specific change you propose and how to test it.
   - **Evidence:** what you found.

   Write one row per control per risk, as the template requires, even where the same control addresses several risks: `--priority` lists each control once with its risks, so expand it into one row for each.
4. Make each control concrete and specific to the components involved. ARC's guide shows the progression from framework control to organisation control to system-specific implementation; with no organisation register, go straight from framework control to system.
5. Apply the expectations for each level from the guide's table:
   - **Level 0:** adopted as-is. The template expects every Level 0 control to be implemented before sign-off.
     - A Level 0 control is waived only when the capability or component it concerns is not present in the system, for example a control on MCP servers in a system that uses none, or on persistent memory in a system that keeps nothing beyond a session. Record it as *Waived — not applicable*, with the evidence that the capability or component is absent.
     - Any other Level 0 control that isn't implemented is a blocker for the governance team. List these blockers at the top of your summary.
   - **Level 1:** adopted or adapted, or not adopted with a documented rationale.
   - **Level 2:** considered according to the system's risk.
6. Make code changes only if the user asks you to.

## Step 4: Assess residual risks and record the assessment

1. For each priority risk, and for any Level 1 or 2 control not adopted, ask what failure scenarios the implemented controls do not prevent: attack vectors they miss, and conditions where they fail. Record each scenario with a strategy: accept, monitor, or mitigate.
2. Flag for senior stakeholders, as the guide asks:
   - any residual risk with impact 5;
   - any regulatory exposure;
   - any risk with no strategy.
3. Run `ARC --version X.Y.Z template` and fill in every section, recording:
   - the register version and source;
   - the threshold and scales used, and any assumptions you made.

   Leave these for the responsible humans: owners, "Verified on" dates, the accepting authority, the deployment decision, and sign-off.
4. Add an **Other findings** section for defects you found that aren't covered by a control, such as bugs that make a control ineffective.
5. Save the assessment and summarise for the user, in this order:
   - Level 0 blockers;
   - high-impact gaps, with proposed changes;
   - what needs a decision from the governance team.

## When the register doesn't fit

Don't change risk or control content to fit the system.

- **If a risk seems wrong for this system:** keep it, score it, and explain why in the assessment.
- **If the register is missing a risk this system clearly has:** add it to the assessment as an additional risk (A1, A2, …) with the same fields. Suggest the user propose it upstream: <https://github.com/govtech-responsibleai/agentic-risk-capability-framework/blob/main/CONTRIBUTING.md>.

## Re-running

Re-run the assessment when the system gains or loses a capability, when an agent, tool, or integration is added, or when a new register version is released. Each assessment is tied to the register version it used.
