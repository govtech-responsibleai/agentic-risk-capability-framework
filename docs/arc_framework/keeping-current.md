# Keeping the register current

!!! abstract "Page Summary"

    Agentic systems change faster than a register can be rewritten. This page explains how ARC is kept in step with what actually goes wrong: an incident file that every proposed change is checked against, a quarterly review, reference systems that guard the tools against regressions, and the validation that has not been done yet.

## The incident file

ARC keeps a [curated file of incidents](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/incidents), vulnerabilities and research findings that involve agentic systems. Each case is mapped to the elements where the failure arose and to the risks in the register that describe it. A case that no risk describes is filed under a gap theme.

The file is not an incident database. It draws on those that exist, and adds two things: a selection made from the point of view of someone building or deploying an agent, and the mapping to this register. It answers two questions.

- **Which cases does the register not describe?** These are candidates for new risks and controls. The twelve risks added in version 2.0 came from this question.
- **Which risks have no case behind them?** These rest on argument or research alone. That can be justified, but it should be a decision.

## The quarterly review

Four steps, described in full in the incident file's own guide:

1. **Harvest.** A script lists new leads from the upstream trackers that publish machine-readable data, and drops anything already seen.
2. **Triage.** Each lead becomes a case or is logged as left out, with a reason. An agent can prepare this from written rules; a maintainer reviews it.
3. **Verify.** A maintainer opens the primary source for every case of harm and every case with a gap.
4. **Review.** The coverage report is read against the previous one.

A change to the register is proposed when:

- a gap theme has **three or more cases, at least one of them harm, from more than one source**. It becomes a proposal for a new risk or control, with the cases as its evidence;
- a risk has **no case** after two reviews. It is checked: is it still credible, and is it worded so that a case could match it?
- a control's **level** no longer matches the evidence, in either direction.

Proposals go through the register's normal change process and appear in the [changelog](changelog.md).

## What the file cannot tell you

- **How often things happen.** The file holds what was published, in English, and found by the trackers it draws on. Security research and coding agents are over-represented. Quiet operational failures inside organisations are under-represented.
- **Whether a control works.** A case shows that something went wrong. It rarely shows which control would have stopped it.

## Reference systems

The repository holds [profiles of four example systems](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/examples/systems): a question-answering bot and the three worked examples in the [guide for AI developers](../implementation/for-ai-developers.md). A profile lists a system's capabilities, how each is used, and its conditional components.

They do two jobs. The numbers quoted in the developer guide are checked against the assessment tool on every change, so the guide cannot drift from the register. And any tool that implements ARC can be run on the same profiles and compared.

## Validation still to do

Neither ARCvisor nor the assessment skill has been validated against expert assessments. The plan:

1. Add reference systems until they cover every capability and both conditional components.
2. Have two people who know ARC assess each one independently, and record where they differ. The differences show where the register is ambiguous.
3. Run each tool on the same systems and compare three things with the agreed assessments: the capabilities identified, the risks marked as priorities, and whether every Level 0 control is addressed.
4. Publish the agreement rates with each release.

Until this is done, treat a tool's output as a draft for a person to review.
