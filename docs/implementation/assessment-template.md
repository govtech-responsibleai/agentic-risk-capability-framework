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
| Register version assessed against | e.g. `2.0.0` (see the [changelog](../arc_framework/changelog.md)) |
| Organisation's relevance threshold | e.g. Impact ≥ 3 AND Likelihood ≥ 3, OR Impact ≥ 4 |
| Assessment date; assessor; reviewer | |

## 1. Capability inventory

Capabilities are system-level: if any agent has one, the system has it. Include read-only functions.

For each capability that acts on the world, record how the system uses it (see [Context](../arc_framework/elements.md#context-how-a-capability-is-used)). **Authority** is the highest of: read, propose, act with approval, act alone. Leave a context cell blank only where it is marked n/a. A blank is read as the most cautious answer.

| Capability | Present? | Authority | Irreversible effects? | Effects outside the organisation? | Which agent / tool provides it | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CAP-01 Planning and Goal Management | | n/a | n/a | n/a | | |
| CAP-02 Agent Delegation | | n/a | n/a | n/a | | |
| CAP-03 Tool Use | | n/a | n/a | n/a | | |
| CAP-04 Multimodal Understanding and Generation | | n/a | n/a | n/a | | |
| CAP-05 Official Communication | | | always | always | | |
| CAP-06 Business Transactions | | | | always | | |
| CAP-07 Internet and Search Access | | read | never | always | | |
| CAP-08 Computer Use | | | | | | |
| CAP-09 Other Programmatic Interfaces | | | | | | |
| CAP-10 Code Execution | | | | | | |
| CAP-11 File and Data Management | | | | | | |
| CAP-12 System Management | | | | | | |

**Conditional components.** Most components and design elements are present in every agentic system. Two components are conditional. Record whether the system has each one; its risks apply only if it does. A component left blank is treated as present.

| Component | Present when | Present? (yes / no, with evidence) |
| --- | --- | --- |
| CMP-04 Memory | The system keeps information beyond a single session, or shares it across users or tasks. | |
| CMP-05 Protocols | At least one tool server or agent that another party builds or operates is connected to the system through an agent protocol such as MCP or A2A, in either direction. Another team in the same organisation counts as another party. | |

## 2. Applicable risks

List **every applicable risk**: all baseline risks (those arising only from components and design elements that every agentic system has), the risks of each conditional component marked present, each capability risk for a capability marked present, and each composite risk whose capabilities are *all* present. Score each; a risk is a **priority** when it meets the threshold. A risk below the threshold stays on the list — its Level 0 controls still apply.

| Risk ID | Statement | Element(s) | Contextualised description (how it would materialise here) | Impact (1–5) | Likelihood (1–5) | Priority? |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | | CMP-01 | | | | |
| … | | | | | | |

## 2a. Capability combinations

Some risks arise only when a system holds several capabilities at once (see [Capability combinations](../arc_framework/capability-combinations.md)). Record the check for each combination rule the register defines. Register 2.0.0 defines two: the lethal trifecta, and oversight within reach. Count what persistent memory holds when answering for each leg.

First record the capabilities that the declared ones give the system. Code Execution, Computer Use, System Management and Agent Delegation can each give a system capabilities that were not declared.

| Declared capability | Implied capability | Added to Section 1, or evidence that it does not apply |
| --- | --- | --- |
| | | |

| Combination | Leg | Supplied by (capability, or "none") | Present in this system? (yes / no, with evidence) |
| --- | --- | --- | --- |
| Lethal trifecta | Untrusted content | | |
| | Sensitive data | | |
| | Outbound channel | | |
| Oversight within reach | Its own safeguards | | |

| Field | Entry |
| --- | --- |
| Lethal trifecta: verdict (present / possible / not present) | |
| If every leg is present: which leg is removed or gated for each agent, and how (CTRL-0097) | |
| If a leg is absent: which one, and the evidence (CTRL-0097 is then *Waived — not applicable*) | |
| Oversight within reach: verdict | |
| If present: how the agent is kept from writing to its own instructions, configuration, permissions, logs and monitors (CTRL-0101) | |

## 3. Controls

One row per control per risk, even where the same control addresses several risks. **Every Level 0 control of every applicable risk is listed with status *Implemented as-is*, or *Waived — not applicable* where the capability or component it concerns is not present in the system, with evidence of its absence.** Level 1 and 2 controls are listed for priority risks (and for any other risk where you choose to adopt them); if not adopted, record why.

| Risk ID | Control ID | Level | Status (as-is / adapted / not adopted / waived — not applicable) | Implementation or adaptation (what, where, thresholds) | Evidence (config, test result, log, review record) | Owner | Verified on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | 0 | Implemented as-is | | | | |
| | | 0 | Waived — not applicable | e.g. "The system uses no MCP servers" | e.g. the tool registry listing every tool it can call | | |
| | | 1 | Adapted | | | | |
| | | 2 | Not adopted — *rationale* | | | | |

!!! note "Evidence"

    Each control in the register names the evidence that shows it is in place and a test that shows it works. Start from those, and record what you actually have.

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
