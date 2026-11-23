# Capability combinations

<!-- The tables marked "arc:" below are filled in from arc-risk-register/*.yaml when the site is built (scripts/build_risk_register.py). Edit the YAML, not the tables. -->

!!! abstract "Page Summary"

    Some risks belong to no single capability. They arise only when a system holds several capabilities at once. This page explains how ARC handles them: composite risks in the register, a check that reads a system's capabilities and reports whether a dangerous combination is present, and a control that breaks the combination. The lethal trifecta is the worked example.

## Why combinations matter

ARC assesses a system one element at a time. Each [capability](elements.md) brings its own risks, and each risk has its own controls. That works when the risks are independent of each other.

Some are not. Consider three agents:

- An agent that only browses the web can be misled by what it reads, but it holds nothing worth stealing.
- An agent that only reads internal files holds sensitive data, but no outsider can give it instructions.
- An agent that does both can be told by a web page to open a file and send its contents to an address the attacker chose.

The third agent has a risk that neither of the first two has. Each of its capabilities can be well controlled on its own terms, so an assessment that looks at one capability at a time can pass a system that is exposed.

Other fields met this problem long before agents did. Auditors use [segregation-of-duties matrices](https://www.isaca.org/resources/isaca-journal/issues/2016/volume-3/implementing-segregation-of-duties-a-practical-experience-based-on-best-practices) to find duties that no one person should hold together. Security researchers wrote [rules for dangerous combinations of app permissions](https://doi.org/10.1145/1653662.1653691) on mobile phones. Cloud security tools flag ["toxic combinations"](https://docs.cloud.google.com/security-command-center/docs/toxic-combinations-overview) of findings that are minor alone. ARC applies the same idea to the capabilities of an agentic system.

## What ARC builds in

**Composite risks.** A risk in the register can list more than one element, and it applies only when the system has all of them. Components and design elements are present in every agentic system, so a composite risk that lists one of them depends on its capabilities alone. The register has these composite risks:

<!-- arc:composite-risks -->

**A combination check.** A composite risk names specific elements, so it cannot say "any capability that can send data out". The check fills that gap. For each combination ARC checks, the register records which capabilities can supply each part of it, and the check reports whether a system's capabilities complete the combination. The data is in [`combinations.yaml`](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/blob/main/arc-risk-register/combinations.yaml), next to the risks and controls.

**A control that breaks the combination.** Each checked combination has a control. The verdict of the check decides whether that control must be implemented or can be waived. The check does not add or remove risks.

Register 1.3 checks one combination, the lethal trifecta.

## The lethal trifecta

An agent holds the lethal trifecta, a term coined by [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), when it has all three of the following:

1. **Untrusted content.** Content that someone outside the organisation's control can write reaches the agent.
2. **Sensitive data.** The agent can read data that would cause harm if it left the organisation.
3. **An outbound channel.** The agent can cause data to reach a destination outside the organisation's control.

LLMs cannot reliably tell instructions from data, so text in a web page, an email, or a document can direct an agent that reads it. With all three legs in place, one injected instruction is enough. The agent reads the sensitive data and sends it out through a channel it is allowed to use. No control is bypassed, because every step is something the agent is permitted to do.

This has happened. In [EchoLeak](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability), a single crafted email led Microsoft 365 Copilot to send internal data to an attacker. In [ForcedLeak](https://www.varonis.com/blog/forcedleak), instructions in a web-form submission led Salesforce Agentforce to send out customer records. The Frontier Model Forum's [brief on agent security](https://www.frontiermodelforum.org/uploads/2026/06/FMF-Issue-Brief-on-Emerging-Security-Practices-for-AI-Agents.pdf) recommends that, in higher-risk uses, no agent hold all three. Meta's [Agents Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/) gives similar advice.

### Which capabilities supply each leg

A capability can supply a leg wherever it is present, or only in some deployments.

<!-- arc:combination-legs lethal-trifecta -->

**Yes** means the capability supplies the leg wherever it is present. **Maybe** means it depends on the deployment, and the notes below say when. Planning and Goal Management and Tool Use supply no leg by themselves.

??? note "When each capability supplies a leg"

    <!-- arc:combination-notes lethal-trifecta -->

Components are not in the table. Persistent [memory](elements.md) can carry untrusted content or sensitive data from one session into a later one, so count what memory holds when you answer for each leg.

### The verdict

| Verdict | When | What to do |
| --- | --- | --- |
| **Present** | Every leg is supplied by a capability marked Yes | Implement the control below |
| **Possible** | Every leg is supplied, but at least one only by capabilities marked Maybe | Answer the note for each of those capabilities from the system's code and configuration. If every leg is confirmed, implement the control. If a leg is absent, waive the control and record the evidence |
| **Not present** | At least one leg is supplied by no capability | Waive the control wherever it is listed, and record which leg is absent |

The control is:

<!-- arc:combination-control lethal-trifecta -->

It is a [Level 0 control](controls.md#control-levels). Scoring does not waive it. It is waived only when a leg is absent, in the same way that any Level 0 control is waived when the capability or component it concerns is not present.

There are three ways to break the combination:

- **Split the agent.** Give the untrusted content to a separate agent that has no access to sensitive data and returns only structured values.
- **Remove the data.** Take away the sensitive data that the task does not need.
- **Gate the channel.** Restrict the outbound channel outside the agent. Limit recipients and destinations to a fixed allowlist, and require human approval for any message or call that carries data to a new recipient.

The verdict describes the system as a whole. The control applies to each agent, so in a multi-agent system, record which agent holds each leg. Splitting the legs across agents satisfies the control only if the agent that reads untrusted content cannot pass free text to the agent that holds the data or the channel.

### Try it

Tick the capabilities your system has. The check runs in your browser, and nothing is sent anywhere.

<div id="arc-combination-check" data-combination="lethal-trifecta">
<noscript>The interactive check needs JavaScript. The table above gives the same information.</noscript>
</div>

### Worked examples

These are the systems from the [guide for AI developers](../implementation/for-ai-developers.md#application-examples), with a simple question-answering bot for comparison.

| System | Capabilities | Verdict | Why |
| --- | --- | --- | --- |
| Question-answering bot | CAP-04 | **Not present** | Nothing supplies sensitive data |
| Agentic fact checker | CAP-01, 02, 03, 04, 07, 11 | **Present** | Internet and Search Access supplies untrusted content and an outbound channel; File and Data Management supplies sensitive data |
| Agentic coding assistant | CAP-01, 02, 03, 04, 10, 11 | **Possible** | File and Data Management supplies sensitive data. Untrusted content depends on whether it reads repositories or packages that others can change. An outbound channel depends on whether its code runs with network access |
| Agentic call assistant | CAP-01, 02, 04, 06, 09, 11 | **Possible** | File and Data Management supplies sensitive data, and Business Transactions supplies an outbound channel. Untrusted content depends on what its callers and the systems it reads can put in front of it |

## Using the check in an assessment

- **In the developer guide:** the check is part of [Step 2](../implementation/for-ai-developers.md#step-2-evaluate-risks), after the applicable risks are listed.
- **In the assessment template:** [Section 2a](../implementation/assessment-template.md#2a-capability-combinations) records the verdict, the answer for each leg, and how the combination is broken.
- **With a coding agent:** the [ARC assessment skill](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/skills) runs the check. `arc.py assess` prints the verdict and the notes to answer for the capabilities given.

## Limits

- **One combination.** Register 1.3 checks the lethal trifecta only. Capabilities combine in other ways too, for example when code execution gives an agent abilities that its tool list does not show. These are being studied for version 2.0.
- **Capabilities are coarse.** Internet and Search Access covers reading pages and posting to them. Many systems will therefore get a verdict of Possible, and the notes turn that verdict into questions that evidence can answer.
- **Composite risks need every element.** RISK-047 covers the trifecta through web access, and RISK-055 covers it through messages and APIs. Other routes, such as Computer Use alone, are caught by the check and not by a composite risk. Rules of the form "any capability that supplies this leg" are planned for version 2.0.
- **Design time only.** The check reads what a system can do, not what it does in a given session. [CTRL-0090](register-full-text.md#CTRL-0090) covers enforcement at run time.
