# ARC agent skills

## `arc-assessment`

An [Agent Skill](https://agentskills.io) that lets a coding agent assess the agentic system it is working on with the ARC Framework. It follows the four steps of ARC's [guide for AI developers](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/for-ai-developers/):

1. identify the system's capabilities from its code, with evidence;
2. list the applicable risks and score them;
3. check which controls are implemented and propose changes for the gaps;
4. record residual risks and draft the assessment in ARC's [assessment template](https://govtech-responsibleai.github.io/agentic-risk-capability-framework/implementation/assessment-template/).

Register content comes from `scripts/arc.py`, which fetches the register YAML from this repository at a release tag (the latest release by default, or `--version X.Y.Z`). With `--register` it reads an **organisation's own contextualised register** instead: a local directory or base URL with the same file layout as [`arc-risk-register/`](../arc-risk-register/).

### Install

For Claude Code, copy the folder into your personal skills directory, or into a project's `.claude/skills/` to share it with the team:

```bash
git clone --depth 1 https://github.com/govtech-responsibleai/agentic-risk-capability-framework.git /tmp/arc
cp -r /tmp/arc/skills/arc-assessment ~/.claude/skills/      # or <project>/.claude/skills/
```

Other agents that support Agent Skills load the same folder from their own skills directory. For an agent without skills support, point it at `SKILL.md`.

The script needs only Python 3.9+. It uses PyYAML if installed, and otherwise a built-in parser that CI checks against PyYAML on every register file. It needs network access to `raw.githubusercontent.com` unless `--register` is a local directory; release files are cached in `ARC_CACHE_DIR` (default `~/.cache/arc-assessment/`), so an assessment pinned with `--version` keeps working offline.

### Use

Ask the agent, for example, "assess this agent with ARC" or "which ARC controls does this system still need?". The script can also be run directly:

```bash
python3 skills/arc-assessment/scripts/arc.py elements
python3 skills/arc-assessment/scripts/arc.py assess --capabilities CAP-03,CAP-07,CAP-11
python3 skills/arc-assessment/scripts/arc.py --version 1.5.0 assess --capabilities CAP-03,CAP-07,CAP-11 --priority RISK-034,RISK-047
python3 skills/arc-assessment/scripts/arc.py show RISK-047 CTRL-0089 CAP-07
python3 skills/arc-assessment/scripts/arc.py --register ./our-arc-register assess --capabilities CAP-02,CAP-06
```

### Maintenance

`skills/tests/test_arc_assessment.py` runs in CI against this repository's register. It checks that the script's applicability logic and controls-in-scope still match the register, that its built-in YAML parser reads every register file exactly as PyYAML does, that it runs without PyYAML, that the template comes out as plain Markdown, and that it accepts an organisation register using the older single `element_id` field.
