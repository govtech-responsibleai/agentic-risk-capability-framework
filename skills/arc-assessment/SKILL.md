---
name: arc-assessment
description: Assess an agentic AI system with GovTech Singapore's Agentic Risk & Capability (ARC) Framework. Identifies the system's capabilities from its code, lists the applicable risks and controls from the ARC risk register, checks which controls are implemented, and drafts the assessment. Use when building, reviewing, or changing an LLM agent or multi-agent system and the user asks for an ARC assessment, a safety or security risk review of the agent, or which ARC risks or controls apply. Works with the official register or an organisation's own contextualised version.
---

# ARC assessment

This skill applies the [ARC Framework](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/) to the agentic system in the current codebase, following the four steps of ARC's [guide for AI developers](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/for-ai-developers/): identify capabilities, evaluate risks, implement controls, and assess residual risks.

All register content comes from `scripts/arc.py`, which reads the register YAML. Do not answer from memory: quote risk and control IDs (e.g. RISK-034, CTRL-0062) exactly as the script prints them, and record the register version it reports.

## Before you start

1. Ask the user whether their organisation has its own contextualised ARC register. ARC is meant to be adapted by each organisation, so if one exists, use it: `--register <directory or base URL>` (same file layout as the official `arc-risk-register/`). Otherwise the script uses the latest official release; `--version X.Y.Z` pins a specific one.
2. Ask for the organisation's relevance threshold for impact and likelihood (set by its governance team). Don't invent one; if there isn't one, ask the user to choose and record that choice.
3. Check the script runs: `python scripts/arc.py --help`. It needs Python 3.9+ and PyYAML (`pip install pyyaml`, or run it with `uv run`), and network access to `raw.githubusercontent.com` unless `--register` points to a local directory. Release files are cached in `~/.cache/arc-assessment/`.

Global options go before the command; `--format json` goes after it:

```bash
python scripts/arc.py [--version X.Y.Z | --register PATH_OR_URL] elements
python scripts/arc.py [...] assess --capabilities CAP-03,CAP-07 [--detail] [--format json]
python scripts/arc.py [...] show RISK-034 CTRL-0062
python scripts/arc.py [...] template
```

## Step 1: Identify capabilities

1. Run `arc.py elements` and read the capability definitions. They are the authority on what each capability covers.
2. Inspect the codebase for what the system can do autonomously: agent and sub-agent definitions, tool and function schemas, MCP server and plugin configuration, system prompts, orchestration code, and the APIs, databases, file systems, shells, browsers, or payment and messaging services it is wired to.
3. Map each function to a capability. Capabilities are system-level: if any agent has one, the system has it. Look at what the system *does*, not just which tools exist, and remember that read-only access can still expose data. If you're unsure whether something qualifies, include it.
4. Record evidence for each capability as file paths and line numbers, and list the capabilities you considered and ruled out, with reasons.
5. Show the user the capability list and evidence, and get their confirmation before Step 2.

## Step 2: Evaluate risks

1. Run `arc.py assess --capabilities <confirmed IDs>`. It lists every applicable risk: baseline risks (from components and design elements, present in every agentic system), risks from each capability, and risks from combinations of elements, which apply only when all of their elements are present.
2. For each applicable risk, describe in one or two sentences how it would arise in this system, naming the components or code paths involved.
3. Score impact and likelihood from 1 to 5, with reasoning, and mark as *priority* the risks that meet the organisation's threshold.
4. Apply the control levels as ARC defines them (see [Controls → Control levels](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/arc_framework/controls/#control-levels)): Level 0 controls apply to every applicable risk, whatever its score; scoring decides where Level 1 and Level 2 effort goes.

## Step 3: Implement controls

1. For each control in scope, read its guidance (`arc.py show CTRL-xxxx`, or `assess --detail`).
2. Search the codebase for an existing implementation and record the evidence (file paths, configuration, tests). Classify each control as **implemented**, **partly implemented**, **not implemented**, or **not applicable**, with a reason.
3. Adapt generic controls to this system: make each one concrete, measurable, and specific to the components involved. ARC's guide shows the progression from framework control to organisation control to system-specific implementation.
4. For gaps, propose specific changes: what to add, where, and how to test it. Make code changes only if the user asks you to.
5. Follow the expectations for each level in the guide: Level 0 is adopted as-is, and blockers go to the governance team; Level 1 is adopted or adapted, with documented rationale; Level 2 is considered according to the system's risk.

## Step 4: Assess residual risks and record the assessment

1. For each implemented control, ask what failure scenarios it does not prevent (attack vectors it misses, conditions where it fails) and record the residual risk.
2. Flag for review by senior stakeholders, as the guide asks, any catastrophic residual risk (impact 5, even if likelihood is low), regulatory exposure, or risk with no mitigation strategy.
3. Run `arc.py template` and fill in the ARC assessment template: system overview (including the register version and source, and the threshold used), capability inventory with evidence, applicable risks with scores, controls with status, implementation, evidence and owner, residual risks with the accepting authority, and sign-off. Leave owner, accepting authority, and sign-off for the humans responsible; don't fill them in yourself.
4. Save it where the user asks, by default `docs/arc-assessment.md` in the repository, and summarise the gaps and proposed changes for the user.

## Re-running

Re-run the assessment when the system gains or loses a capability, when an agent, tool, or integration is added, or when a new register version is released. Each assessment is tied to the register version it used.

## When the register doesn't fit

Don't change risk or control content to fit the system. If a risk seems wrong for this system, keep it, score it, and explain why in the assessment. If the register is missing a risk this system clearly has, record it as an additional risk in the assessment and suggest the user propose it upstream: <https://github.com/govtech-responsibleai/agentic-risk-capability-framework/blob/main/CONTRIBUTING.md>.
