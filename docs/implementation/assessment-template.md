# Assessment Template

!!! abstract "Page Summary"

    A fill-in record for assessing one agentic system under the ARC Framework. It follows the four steps of the [developer guide](for-ai-developers.md) and fixes the fields every assessment should capture — including the evidence behind each control and who accepts residual risk — so that assessments are comparable across systems and auditable later. Copy the Markdown, or reproduce the tables in your own tooling; [ARCvisor](../resources/index.md#arcvisor) exports the same structure.

## 0. System overview

| Field | Entry |
| --- | --- |
| System name and owner | |
| Purpose and users | |
| Deployment context (internal / external; pilot / production; jurisdiction; sector) | |
| Agents and architecture (single agent / multi-agent; orchestration pattern; protocols such as MCP, A2A) | |
| Autonomy: which actions run without a human in the loop | |
| Register version assessed against | e.g. `1.3.0` (see the [changelog](../arc_framework/changelog.md)) |
| Organisation's relevance threshold | e.g. Impact ≥ 3 AND Likelihood ≥ 3, OR Impact ≥ 4 |
| Assessment date; assessor; reviewer | |

## 1. Capability inventory

Capabilities are system-level: if any agent has one, the system has it. Include read-only functions.

| Capability | Present? | Which agent / tool provides it | Human approval required before acting? |
| --- | --- | --- | --- |
| CAP-01 Planning and Goal Management | | | |
| CAP-02 Agent Delegation | | | |
| CAP-03 Tool Use | | | |
| CAP-04 Multimodal Understanding and Generation | | | |
| CAP-05 Official Communication | | | |
| CAP-06 Business Transactions | | | |
| CAP-07 Internet and Search Access | | | |
| CAP-08 Computer Use | | | |
| CAP-09 Other Programmatic Interfaces | | | |
| CAP-10 Code Execution | | | |
| CAP-11 File and Data Management | | | |
| CAP-12 System Management | | | |

## 2. Applicable risks

List **every applicable risk**: all baseline risks (components CMP-01 to CMP-04 and design DSN-01 to DSN-03 — 24 in register 1.3.0), each capability risk for a capability marked present, and each composite risk whose capabilities are *all* present. Score each; a risk is a **priority** when it meets the threshold. A risk below the threshold stays on the list — its Level 0 controls still apply.

| Risk ID | Statement | Element(s) | Contextualised description (how it would materialise here) | Impact (1–5) | Likelihood (1–5) | Priority? |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | | CMP-01 | | | | |
| … | | | | | | |

## 3. Controls

One row per control per risk. **Every Level 0 control of every applicable risk is listed with status *Implemented as-is*.** Level 1 and 2 controls are listed for priority risks (and for any other risk where you choose to adopt them); if not adopted, record why.

| Risk ID | Control ID | Level | Status (as-is / adapted / not adopted) | Implementation or adaptation (what, where, thresholds) | Evidence (config, test result, log, review record) | Owner | Verified on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | 0 | Implemented as-is | | | | |
| | | 1 | Adapted | | | | |
| | | 2 | Not adopted — *rationale* | | | | |

!!! note "Evidence"

    Evidence is what an auditor or a future maintainer can check without asking you: a configuration file or policy in version control, a test report, a screenshot of a guardrail setting, a log query that shows the control firing. "Implemented" without evidence is a claim, not a control.

## 4. Residual risks

For each priority risk, and for any Level 1/2 control not adopted, ask: *what failure scenarios does the implemented set not prevent?*

| Risk ID | Residual failure scenario | Strategy (accept / monitor / mitigate) | Concrete actions and measurable thresholds | Residual Impact / Likelihood | Accepted by (role) |
| --- | --- | --- | --- | --- | --- |
| | | | e.g. "alert if > 10 injection attempts/day; quarterly red team" | | |

Escalate to senior stakeholders any residual risk with Impact 5, any regulatory exposure, and any risk with no strategy.

## 5. Sign-off and review

| Field | Entry |
| --- | --- |
| Assessor (development team) | |
| Reviewer (governance team) | |
| Residual-risk acceptance authority | name and role — this is the person accepting Section 4 |
| Deployment decision | approve / approve with conditions / defer |
| Conditions | |
| Next review date or trigger | e.g. quarterly; any new capability; register MINOR version change |
