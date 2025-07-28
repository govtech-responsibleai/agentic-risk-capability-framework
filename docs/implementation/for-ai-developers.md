# For AI Developers

For teams building agentic AI systems, the ARC Framework provides a good starting point for thinking through the risks and controls required to manage safety and security risks. Instead of having to brainstorm a laundry list from scratch, teams can use the ARC Framework and adapt it to the specifics of their agentic AI system.

## Applying the framework

In the subsequent sub-sections, we provide a step-by-step approach for how AI developers should apply the ARC Framework to their team's agentic AI system. 

### Step 1: Identify capabilities

Begin by analysing the agentic AI system's capabilities using either [our capability taxonomy](../capability/index.md) or the one provided by your organisation. 

The easiest way to do this is to list the functions that the agentic AI system performs and compare that to the list of capabilities in the taxonomy. For example, if the system sends emails autonomously to other users, that would clearly fall under "Interaction - Official Commmunications", while being able to generate and execute Python code would qualify for "Operational - Code Execution". 

Note that the capabilities are defined on a system-level, so *even if only one agent has that capability*, that means that the system as a whole has that capability. 

### Step 2: Evaluate risks

Next, for each identified capability, map the specific risks that could arise from the system having that capability using [the ARC Framework's risk mapping](../capability/risks.md) or the one provided by your organisation. The [baseline risks](../baseline/risks.md) should also be included here.

Teams might find it helpful to further contextualise the risks to the use case. For example, defining what "undesirable" content means is important as such definitions are typically culturally specific, and focusing on the most critical topics when evaluating the risk of hallucination (e.g. medical advice, financial products) makes the risk more tractable and concrete.

Additionally, there may be other safety or security risks that are not included in our list - these may be unique to the system's operating context or arise only from a combination of specific capabilities. To brainstorm for such risks, consider thinking through failure modes by asking yourself "What is the worst scenario that could happen if this capability malfunctions or is misused?"

### Step 3: Adopt or adapt controls

Now for each risk, review the recommended technical controls which help to mitigate the risk to an acceptable level - in the ARC Framework, we provide both [baseline](../baseline/controls.md) and [capability](../capability/controls.md) controls. 

Similar to the risks in Step 2, these controls will also require some contextualisation. Not all controls are feasible or effective in every case, and teams should exercise judgement in deciding how to implement the control to meaningfully address the risk.[^1] Some organisations may choose to implement an impact level differentiation for technical controls (<font color='red'>see next section</font>). In that case, teams should note the distinction between mandatory and recommended controls and deal with them accordingly.

### Step 4: Assess residual risks

With the controls in place, teams should assess what the residual risks are and whether these are acceptable. As this is highly dependent on the use case, we do not provide a standard template for this assessment.[^2] Some questions that teams may consider include identifying the scenarios where harm can still occur despite the controls and what the limitations of the controls are.

If teams find that the residual risks are still unacceptable, then more controls would be needed to reduce either the likelihood or impact of the risk. 

<!-- Footnotes -->

[^1]: This is aligned to our recommendation to governance teams implementing the ARC Framework to take a comply-or-explain approach to the technical controls (<font color='red'>see next section</font>).
[^2]: Some existing resources on managing residual risk include [Verizon's article](https://www.verizon.com/business/resources/articles/s/what-is-residual-risk-in-cyber-security/) or [Bitsight's article](https://www.bitsight.com/glossary/residual-risk) on residual risk 