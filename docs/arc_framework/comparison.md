# Comparison to other frameworks

This page compares the ARC Framework with six major AI governance frameworks and standards: NIST AI RMF 1.0, EU AI Act, Dimensional Governance, OWASP Agentic AI, Google SAIF 2.0, and CSA MAESTRO. The comparison evaluates each framework across multiple criteria including target audience, unit of analysis, prescriptiveness, risk specificity, and practical implementation support.

!!! note "How to use the Comparison Table"

    - **Click anywhere on the row** (with ► arrows) to expand all frameworks for that criterion (multiple rows can be expanded)
    - **Scroll horizontally** to view all frameworks - look for the animated arrow indicator (→) on the right
    - **Colour coding**: 🟢 Green (strong/desirable) | 🟡 Yellow (moderate/conceptual) | 🔴 Red (limited/general) | ⚪ Grey (not addressed)
    - **Click anywhere on the row again** to collapse expanded rows
    - **Mobile users**: Table is optimized for horizontal scrolling on smaller screens

<style>
.comparison-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 2rem 0;
    font-size: 0.68rem;
    table-layout: auto;
}

.comparison-table th {
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 0.875rem 0.625rem;
    text-align: left;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 1;
    border: 1px solid #333;
    min-width: 210px;
    cursor: default;
}

.comparison-table th:first-child {
    position: sticky;
    left: 0;
    z-index: 2;
    min-width: 240px;
    background-color: #1a1a1a;
    cursor: default;
}

.comparison-table th:hover:not(:first-child) {
    opacity: 0.9;
}

.comparison-table td {
    padding: 0.625rem;
    border: 1px solid var(--md-default-fg-color--lightest);
    vertical-align: top;
    min-width: 210px;
}

.comparison-table td:first-child {
    position: sticky;
    left: 0;
    background-color: var(--md-default-bg-color);
    font-weight: 600;
    z-index: 1;
    min-width: 240px;
}

.comparison-table tbody tr {
    cursor: pointer;
}

.cell-content {
    position: relative;
}

.cell-summary {
    font-weight: 400;
    line-height: 1.4;
}

.cell-details {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out, opacity 0.3s ease-out;
    opacity: 0;
    margin-top: 0;
    padding-top: 0;
    font-weight: 400;
    line-height: 1.5;
    font-size: 0.6rem;
    color: #666;
}

.cell-details.expanded {
    max-height: 800px;
    opacity: 1;
    transition: max-height 0.5s ease-in, opacity 0.4s ease-in;
    margin-top: 0.625rem;
    padding-top: 0.625rem;
    border-top: 2px solid var(--md-default-fg-color--lighter);
}

.expand-icon {
    font-size: 0.75rem;
    opacity: 0.5;
    transition: transform 0.3s;
    flex-shrink: 0;
    margin-top: 0.125rem;
}

.expand-icon.expanded {
    transform: rotate(180deg);
}

.header-expand-icon {
    font-size: 0.7rem;
    opacity: 0.7;
    transition: transform 0.3s;
    margin-left: 0.375rem;
    display: inline-block;
}

.header-expand-icon.expanded {
    transform: rotate(90deg);
}

.criterion-description {
    font-size: 0.6rem;
    color: #666;
    font-weight: 400;
    margin-top: 0.25rem;
    line-height: 1.3;
}

.framework-description {
    font-size: 0.6rem;
    color: #bbb;
    font-weight: 400;
    margin-top: 0.25rem;
    line-height: 1.3;
}

/* Colour coding based on performance */
.cell-green {
    background-color: rgba(76, 175, 80, 0.12);
    border-left: 3px solid #4caf50;
}

.cell-yellow {
    background-color: rgba(255, 152, 0, 0.12);
    border-left: 3px solid #ff9800;
}

.cell-red {
    background-color: rgba(244, 67, 54, 0.12);
    border-left: 3px solid #f44336;
}

.cell-grey {
    background-color: rgba(158, 158, 158, 0.08);
    border-left: 3px solid #9e9e9e;
}

.comparison-table tbody td:not(:first-child) {
    max-width: 420px;
}

/* Ensure first column doesn't get colour backgrounds */
.comparison-table td:first-child {
    background-color: var(--md-default-bg-color) !important;
    border-left: 1px solid var(--md-default-fg-color--lightest) !important;
}

/* Horizontal scroll indicators */
.table-wrapper {
    position: relative;
}

/* Right gradient - visible at start */
.table-wrapper::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 60px;
    background: linear-gradient(to left, rgba(255,255,255,0.9), transparent);
    pointer-events: none;
    opacity: 1;
    transition: opacity 0.3s;
}


/* Right scroll indicator - hidden by default */
.scroll-indicator-right {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2rem;
    color: #666;
    opacity: 0;
    pointer-events: none;
    animation: slideRight 1.5s ease-in-out infinite;
    transition: opacity 0.3s;
}

/* Left scroll indicator - hidden by default, same position as right */
.scroll-indicator-left {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2rem;
    color: #666;
    opacity: 0;
    pointer-events: none;
    animation: slideLeft 1.5s ease-in-out infinite;
    transition: opacity 0.3s;
    z-index: 3;
}

@keyframes slideRight {
    0%, 100% { transform: translateY(-50%) translateX(0); opacity: 0.6; }
    50% { transform: translateY(-50%) translateX(10px); opacity: 0.3; }
}

@keyframes slideLeft {
    0%, 100% { transform: translateY(-50%) translateX(0); opacity: 0.6; }
    50% { transform: translateY(-50%) translateX(-10px); opacity: 0.3; }
}

/* When at START: show right indicator and right gradient */
.table-wrapper.scrolled-start .scroll-indicator-right {
    opacity: 0.6 !important;
}

.table-wrapper.scrolled-start .scroll-indicator-left {
    opacity: 0 !important;
}

.table-wrapper.scrolled-start::after {
    opacity: 1 !important;
}


/* When SCROLLED (middle): show left indicator and left gradient, hide right */
.table-wrapper.scrolled .scroll-indicator-right {
    opacity: 0 !important;
}

.table-wrapper.scrolled .scroll-indicator-left {
    opacity: 0.6 !important;
}

.table-wrapper.scrolled::after {
    opacity: 0 !important;
}


/* When at END: show left indicator and left gradient only */
.table-wrapper.scrolled-end .scroll-indicator-right {
    opacity: 0 !important;
}

.table-wrapper.scrolled-end .scroll-indicator-left {
    opacity: 0.6 !important;
}

.table-wrapper.scrolled-end::after {
    opacity: 0 !important;
}

</style>

<div class="table-wrapper" style="overflow-x: auto;" id="tableWrapper">
<div class="scroll-indicator-right">→</div>
<div class="scroll-indicator-left">←</div>
<table class="comparison-table">
<thead>
<tr>
    <th>Criterion</th>
    <th>
        ARC Framework
        <div class="framework-description">Capability-centric governance for agentic AI systems</div>
    </th>
    <th>
        NIST AI RMF 1.0
        <div class="framework-description">Lifecycle risk management for AI systems</div>
    </th>
    <th>
        EU AI Act
        <div class="framework-description">Risk-based legislation for AI in Europe</div>
    </th>
    <th>
        Dimensional Governance
        <div class="framework-description">Adaptive governance via continuous dimensions</div>
    </th>
    <th>
        OWASP Agentic AI
        <div class="framework-description">Threat-modelling for agentic attack surfaces</div>
    </th>
    <th>
        Google SAIF 2.0
        <div class="framework-description">Defence-in-depth principles for enterprise agents</div>
    </th>
    <th>
        CSA MAESTRO
        <div class="framework-description">Layered security architecture for agentic systems</div>
    </th>
</tr>
</thead>
<tbody>

<!-- Primary Audience -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Primary Audience
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">Who is expected to use the framework</div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Org & security teams
        </div>
        <div class="cell-details">
            Organisation governance teams, AI developers, product managers, security engineers, and compliance officers working cross-functionally on agentic systems. Designed for teams managing risks throughout the organisation and product lifecycle who need structured governance without heavy certification overhead.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Broad AI actors
        </div>
        <div class="cell-details">
            AI actors (organisations & individuals) across all sectors voluntarily using the framework. Use-case agnostic and sector-neutral, intended as foundational guidance for anyone designing, developing, or deploying AI systems. Broad applicability but less specialised for agentic contexts.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Regulators & providers/users
        </div>
        <div class="cell-details">
            Providers and users of AI in the EU; regulators and compliance officers enforcing the Act. Mandatory for high-risk AI system providers placing products on EU market and deployers using AI in the EU. Clear regulatory audience with legal obligations.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Multi-stakeholder (policy)
        </div>
        <div class="cell-details">
            Policymakers, oversight bodies, and governance leads designing governance structures. More conceptual than operationally focused, serving those setting governance policy and defining oversight mechanisms. Less useful for frontline implementation teams.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Security engineers & practitioners
        </div>
        <div class="cell-details">
            Security engineers, red teams, and blue teams building and defending agentic applications. Designed for practitioners responsible for securing agentic systems with focus on threat identification, attack surface analysis, and technical mitigations.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            CISOs & enterprise builders
        </div>
        <div class="cell-details">
            CISOs, security architects, and enterprise builders integrating agentic AI into enterprise security architectures. Bridges security principles with practical enterprise deployment considerations, designed for security leadership.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Security engineers, researchers & developers
        </div>
        <div class="cell-details">
            Security engineers, researchers, and developers working on agentic AI systems. Focuses on practitioners who need layered architectural guidance for building and securing agentic systems with defence-in-depth approaches.
        </div>
    </div>
</td>
</tr>

<!-- Unit of Analysis -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Unit of Analysis
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">What is the main governance object or focal point</div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Capability–risk mapping
        </div>
        <div class="cell-details">
            Capabilities with components and system design. Organises governance around what the system can do (capabilities) and maps these to specific risks and controls. Focuses on the powers the system possesses (e.g., internet access, file system access, code execution) as the primary unit for risk analysis.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Lifecycle risk functions
        </div>
        <div class="cell-details">
            AI systems and lifecycle stages organised into four functions: Govern, Map, Measure, and Manage. Categories and subcategories within each function provide structure. Lifecycle-oriented approach addresses systems broadly across development and deployment phases.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Risk categories (tiered)
        </div>
        <div class="cell-details">
            AI systems defined by risk category: unacceptable, high, limited, and minimal risk. High-risk AI triggers compliance obligations. Agentic systems recognised as spanning ecosystems with continuous risk profiles requiring dynamic oversight.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Continuous dimensions
        </div>
        <div class="cell-details">
            Continuous dimensions of decision authority, process autonomy, and accountability. Analyses how control and responsibility shift as systems move along these dimensions towards greater autonomy. Conceptual lens rather than concrete system components.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Threat/attack surfaces
        </div>
        <div class="cell-details">
            Threats and attack surfaces for agent workflows organised by component: reasoning loops, memory systems, tool use, identity/permissions, oversight mechanisms, and multi-agent interactions. Security-first perspective analysing where vulnerabilities exist.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Principles & control families
        </div>
        <div class="cell-details">
            Principles and control families across the agent lifecycle. Organises security around core principles (human controller, limited powers, observability) and associated control families. Strategic rather than granular component analysis.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Layered architecture
        </div>
        <div class="cell-details">
            Layered security architecture analysing threats at each layer of agentic systems. Examines security across model layer, agent layer, and application layer with layer-specific threat models and controls. Defence-in-depth architectural view.
        </div>
    </div>
</td>
</tr>

<!-- Prescriptiveness -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Prescriptiveness
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">Level of detailed requirements vs. high-level principles</div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Medium–High
        </div>
        <div class="cell-details">
            Structured risk→control mapping with implementation checklists and governance workflows. Provides detailed guidance on selecting controls based on capability profiles and risk thresholds. Not legally binding or certifiable but highly structured with clear decision points.
        </div>
    </div>
</td>
<td class="cell-red">
    <div class="cell-content">
        <div class="cell-summary">
            Low
        </div>
        <div class="cell-details">
            Voluntary guidance with tasks and outcomes but not prescriptive in implementation. Provides categories, subcategories, and suggested actions that organisations adapt to their context. Not certifiable or legally binding. High-level principles requiring significant interpretation.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            High
        </div>
        <div class="cell-details">
            Legally binding requirements with strict obligations for high-risk AI. Mandatory policies, documentation, conformity assessments, logging, transparency, and human oversight. Non-compliance results in significant penalties. Most prescriptive framework with clear legal requirements.
        </div>
    </div>
</td>
<td class="cell-red">
    <div class="cell-content">
        <div class="cell-summary">
            Low–Medium
        </div>
        <div class="cell-details">
            Conceptual thresholds with limited concrete controls. Provides framework for thinking about governance dimensions and thresholds but offers few specific implementation requirements or control specifications. Requires significant interpretation and operationalisation.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Medium–High
        </div>
        <div class="cell-details">
            Enumerated threats with specific mitigation strategies. Provides catalogue of concrete threats and corresponding mitigation techniques. More prescriptive than conceptual frameworks with actionable security guidance, though allows implementation flexibility.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Medium
        </div>
        <div class="cell-details">
            Principle-led control families rather than detailed requirements. Provides security principles and control families offering structure for security architects to design implementations, but requires organisational interpretation and adaptation. Not a full specification.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Medium
        </div>
        <div class="cell-details">
            Layer-specific threat models with risk-based control guidance. Provides structured approach to identifying and mitigating threats at each architectural layer. Balances prescriptive threat enumeration with flexibility in control selection and implementation.
        </div>
    </div>
</td>
</tr>

<!-- Coverage of Agentic AI -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Coverage of Agentic AI
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">How explicitly the framework addresses agentic AI capabilities</div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Strong – capability-driven
        </div>
        <div class="cell-details">
            Explicitly designed for agentic AI with capability lens tailored to agentic powers, autonomy, tool use, and planning. Directly addresses agent-specific risks including excessive agency, tool misuse, goal misalignment, and uncontrolled autonomy. Purpose-built for agentic systems.
        </div>
    </div>
</td>
<td class="cell-red">
    <div class="cell-content">
        <div class="cell-summary">
            General autonomy only
        </div>
        <div class="cell-details">
            General AI coverage not agentic-specific. Addresses AI systems broadly but does not explicitly cover agentic autonomy, tool use, planning, or multi-agent systems. Users must interpret lifecycle guidance for agentic contexts without specific tailoring.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Implicit via risk-based approach
        </div>
        <div class="cell-details">
            Emerging agentic guidance being developed. Act adapting to agentic AI with guidance on continuous risk management, dynamic guardrails, and real-time monitoring. Recognises challenges of autonomous systems but standards still under development. Coverage evolving.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Conceptual – governance dynamics
        </div>
        <div class="cell-details">
            Conceptual focus on autonomy and governance dynamics through dimensions of authority, autonomy, and accountability. Addresses governance implications of agent autonomy but lacks specific guidance on agentic capabilities like tool use, planning, or multi-agent systems.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Strong – agent-specific threats
        </div>
        <div class="cell-details">
            Explicitly addresses agent-specific threats across reasoning, memory, tools, identity, oversight, and multi-agent interactions. Strong coverage of agentic components including tool misuse, memory poisoning, multi-agent trust issues, and reasoning loop manipulation. Purpose-built for agentic security.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Strong – agent-explicit principles
        </div>
        <div class="cell-details">
            Agent-explicit principles tailored to agents: human controller requirement, limited powers, and plan/action observability. Directly addresses agent-specific security challenges including autonomous decision-making, tool access, and dynamic behaviour. Strong agentic focus.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Strong – layered agentic threats
        </div>
        <div class="cell-details">
            Layer-specific analysis of agentic threats across model, agent, and application layers. Addresses unique security challenges at each layer of agentic systems including prompt injection, tool abuse, and multi-agent coordination risks. Comprehensive agentic coverage.
        </div>
    </div>
</td>
</tr>

<!-- Evidence/Evaluation -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Evidence/Evaluation
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">Whether the framework cites empirical research or operational data</div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Conceptual & examples
        </div>
        <div class="cell-details">
            Framework development with worked examples. Based on conceptual analysis and practical case studies. Lacks formal empirical evaluation or operational data from deployed systems. Future work includes validation studies to assess framework effectiveness in practice.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Multi-stakeholder development
        </div>
        <div class="cell-details">
            Developed through multi-stakeholder engagement including workshops, public comments, and cross-sector input. Living document intended to evolve with AI practices. Informed by diverse perspectives but lacks formal empirical evaluation of framework effectiveness.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Legislative process
        </div>
        <div class="cell-details">
            Law enacted through EU legislative process; harmonised standards and technical specifications under development collaboratively. No formal evaluation of framework effectiveness yet given recent enactment. Evidence base developing through standardisation and enforcement.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Conceptual with case studies
        </div>
        <div class="cell-details">
            Conceptual framework grounded in governance theory with illustrative case studies. No empirical studies validating the framework's effectiveness or testing its practical application in organisational settings. Primarily theoretical with limited operational validation.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Practitioner-grounded
        </div>
        <div class="cell-details">
            Grounded in security practitioner experience with real-world examples of agentic security issues. Based on community knowledge and observed attack patterns. No formal empirical evaluation or systematic testing of mitigation effectiveness across diverse contexts.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Narrative & internal experience
        </div>
        <div class="cell-details">
            Based on Google's security engineering experience and enterprise AI deployment insights. Policy and engineering narratives drawing on internal operational experience. No formal benchmarks or empirical studies validating effectiveness across diverse organisational contexts.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Practitioner-led
        </div>
        <div class="cell-details">
            Developed by cloud security practitioners and researchers with industry experience in securing AI systems. Combines theoretical security principles with practical implementation insights. Limited formal empirical validation but grounded in operational security practice.
        </div>
    </div>
</td>
</tr>

<!-- Typical Artifacts -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Typical Artifacts
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">Deliverables or tools the framework produces</div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Risk register & capability profile
        </div>
        <div class="cell-details">
            Produces risk registers, capability profiles, control tier checklists, and sign-off workflows. Includes templates for documenting capability assessments, risk evaluations, control implementations, and governance decision points. Designed for organisational accountability and traceability.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Use-case profiles & outcome categories
        </div>
        <div class="cell-details">
            Risk management tasks, outcomes, organisational profiles, and implementation playbook. Organisations create tailored profiles documenting how they address each function. Playbook provides sector-specific implementation guidance. Focus on process documentation.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Registrations & documentation
        </div>
        <div class="cell-details">
            Technical documentation, conformity assessments, risk management plans, comprehensive logs, and living documentation. Extensive records required for high-risk systems including AIMS scope, policies, objectives, control implementations, audit reports, and management reviews.
        </div>
    </div>
</td>
<td class="cell-red">
    <div class="cell-content">
        <div class="cell-summary">
            Dimension definitions & thresholds
        </div>
        <div class="cell-details">
            Dimension definitions, threshold guidance, and oversight role descriptions. Provides conceptual tools for governance analysis rather than operational artifacts. Outputs are primarily analytical frameworks and governance design principles rather than implementation templates.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Threat navigator & mitigation sheets
        </div>
        <div class="cell-details">
            Threat navigator, threat/mitigation sheets, and red-team prompts. Security-focused artifacts including threat catalogues organised by agentic component, detailed mitigation guidance, and practical testing materials for security teams to assess vulnerabilities.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Principles & control families
        </div>
        <div class="cell-details">
            Security principles, control families, CISO guidance, dynamic least-privilege frameworks, and robust logging architectures. Strategic guidance for security leaders and architectural patterns for security engineers. Less focus on detailed implementation specifications.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Layer-specific threat models
        </div>
        <div class="cell-details">
            Layer-specific threat models, security controls mapped to architectural layers, and risk assessment templates. Provides structured artifacts for analysing security at model, agent, and application layers with corresponding control implementations.
        </div>
    </div>
</td>
</tr>

<!-- Control Selection Logic -->
<tr onclick="toggleRow(this)" style="cursor: pointer;">
<td>
    Control Selection Logic
    <span class="header-expand-icon">►</span>
    <div class="criterion-description">How safeguards are selected and prioritised</div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Capability- & risk-based thresholds
        </div>
        <div class="cell-details">
            Controls selected by capability profile and deployment context. Uses impact×likelihood thresholds to determine minimum control sets. Tailored to specific capabilities (e.g., internet access requires different controls than file system access). Tiered control levels scale with risk.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Risk-based & flexible
        </div>
        <div class="cell-details">
            Organisations identify, measure, and prioritise risks contextually. Framework provides process for risk management but not specific risk→control mappings. Organisations define their own risk appetite and select controls accordingly with significant flexibility.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Risk category obligations
        </div>
        <div class="cell-details">
            Based on risk category and continuous assessment. Control requirements vary by risk classification with extensive controls for high-risk AI. Agentic guidance adds continuous risk assessment, dynamic oversight, and shared responsibility for evolving systems.
        </div>
    </div>
</td>
<td class="cell-yellow">
    <div class="cell-content">
        <div class="cell-summary">
            Dimensional thresholds
        </div>
        <div class="cell-details">
            By dimensional thresholds where higher autonomy requires stricter oversight. Suggests that as systems move towards greater autonomy along dimensions, oversight requirements increase. Provides conceptual logic but not specific risk→control mappings or control catalogues.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Threat-driven
        </div>
        <div class="cell-details">
            Controls selected based on threat presence and attack surface. For example, tool misuse threats require sandboxing and least-privilege access; memory threats require input validation and integrity checks. Direct mapping from identified threats to specific mitigations.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Principle-aligned (defence-in-depth)
        </div>
        <div class="cell-details">
            Control selection guided by core principles: limit powers, ensure observability, maintain human controller. Dynamic least-privilege limits agent powers; observability requirements ensure plan/action monitoring; human-in-the-loop for critical decisions. Hybrid defence approach.
        </div>
    </div>
</td>
<td class="cell-green">
    <div class="cell-content">
        <div class="cell-summary">
            Risk-based layered controls
        </div>
        <div class="cell-details">
            Layer-specific risk assessment driving control selection at each architectural layer. Controls chosen based on risk profile at model, agent, and application layers. Defence-in-depth approach with coordinated controls across layers addressing threats at appropriate levels.
        </div>
    </div>
</td>
</tr>

</tbody>
</table>
</div>

<div style="margin: 0; text-align: center;">
    <button id="exportBtn" onclick="exportTableToExcel()" class="export-button">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="margin-right: 8px; vertical-align: middle;">
            <path d="M14 11v3H2v-3H0v3c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-3h-2z" fill="currentColor"/>
            <path d="M7 11.5V1h2v10.5l3.5-3.5L14 9.5 8 15.5 2 9.5l1.5-1.5L7 11.5z" fill="currentColor"/>
        </svg>
        Export to Excel
    </button>
</div>

<style>
.export-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    letter-spacing: 0.3px;
}

.export-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.1);
}

.export-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.export-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .comparison-table {
        font-size: 0.6rem;
    }

    .comparison-table th:first-child,
    .comparison-table td:first-child {
        min-width: 100px;
        font-size: 0.65rem;
    }

    .comparison-table th {
        min-width: 140px;
        padding: 0.625rem 0.375rem;
    }

    .comparison-table td {
        min-width: 140px;
        padding: 0.5rem 0.375rem;
    }

    .comparison-table tbody td:not(:first-child) {
        max-width: 200px;
    }

    .criterion-description {
        display: none;
    }

    .framework-description {
        font-size: 0.55rem;
    }

    .header-expand-icon {
        font-size: 0.65rem;
    }

    .cell-details {
        font-size: 0.55rem;
    }

    .scroll-indicator-right,
    .scroll-indicator-left {
        font-size: 1.5rem;
    }

    .export-button {
        padding: 10px 20px;
        font-size: 12px;
    }
}

@media (max-width: 480px) {
    .comparison-table {
        font-size: 0.55rem;
    }

    .comparison-table th:first-child,
    .comparison-table td:first-child {
        min-width: 80px;
        font-size: 0.6rem;
    }

    .comparison-table th {
        min-width: 120px;
        padding: 0.5rem 0.25rem;
    }

    .comparison-table td {
        min-width: 120px;
        padding: 0.375rem 0.25rem;
    }

    .comparison-table tbody td:not(:first-child) {
        max-width: 160px;
    }

    .framework-description {
        display: none;
    }

    .export-button {
        padding: 8px 16px;
        font-size: 11px;
    }

    .export-button svg {
        width: 12px;
        height: 12px;
    }
}
</style>

<!-- Load SheetJS library -->
<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>

<script>
function exportTableToExcel() {
    const table = document.querySelector('.comparison-table');
    if (!table) return;

    const exportBtn = document.getElementById('exportBtn');
    exportBtn.disabled = true;
    exportBtn.textContent = 'Exporting...';

    try {
        // Create workbook
        const wb = XLSX.utils.book_new();

        // Create worksheet data
        const wsData = [];

        // Get headers
        const headers = ['Criterion'];
        const headerCells = table.querySelectorAll('thead th');
        headerCells.forEach((th, index) => {
            if (index > 0) {
                // Get framework name (first line of text, excluding description)
                const text = th.textContent.trim().split('\n')[0].trim();
                headers.push(text);
            }
        });
        wsData.push(headers);

        // Get all criteria rows
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const criterionCell = row.querySelector('td:first-child');
            if (!criterionCell) return;

            // Get criterion name (first line, excluding description)
            const criterionText = criterionCell.childNodes[0].textContent.trim();

            // Get all cell values for this criterion
            const cells = row.querySelectorAll('td:not(:first-child)');
            const rowData = [criterionText];

            cells.forEach(cell => {
                const summary = cell.querySelector('.cell-summary');
                const details = cell.querySelector('.cell-details');

                let cellValue = '';
                if (summary) {
                    cellValue = summary.textContent.trim();
                }
                if (details) {
                    const detailText = details.textContent.trim();
                    if (detailText && detailText !== cellValue) {
                        cellValue += '\n\n' + detailText;
                    }
                }
                rowData.push(cellValue);
            });

            wsData.push(rowData);
        });

        // Create worksheet
        const ws = XLSX.utils.aoa_to_sheet(wsData);

        // Set column widths
        const colWidths = [
            { wch: 25 },  // Criterion column
            { wch: 35 },  // ARC Framework
            { wch: 35 },  // NIST AI RMF 1.0
            { wch: 35 },  // EU AI Act
            { wch: 35 },  // Dimensional Governance
            { wch: 35 },  // OWASP Agentic AI
            { wch: 35 },  // Google SAIF 2.0
            { wch: 35 }   // CSA MAESTRO
        ];
        ws['!cols'] = colWidths;

        // Set row heights for wrapped text
        const rowHeights = wsData.map(() => ({ hpt: 15 }));
        ws['!rows'] = rowHeights;

        // Apply text wrapping to all cells
        const range = XLSX.utils.decode_range(ws['!ref']);
        for (let row = range.s.r; row <= range.e.r; row++) {
            for (let col = range.s.c; col <= range.e.c; col++) {
                const cellAddress = XLSX.utils.encode_cell({ r: row, c: col });
                if (!ws[cellAddress]) continue;

                if (!ws[cellAddress].s) ws[cellAddress].s = {};
                ws[cellAddress].s.alignment = {
                    wrapText: true,
                    vertical: 'top'
                };
            }
        }

        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, 'Framework Comparison');

        // Generate and download file
        XLSX.writeFile(wb, 'arc-framework-comparison.xlsx');

        exportBtn.disabled = false;
        exportBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="margin-right: 8px; vertical-align: middle;"><path d="M14 11v3H2v-3H0v3c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-3h-2z" fill="currentColor"/><path d="M7 11.5V1h2v10.5l3.5-3.5L14 9.5 8 15.5 2 9.5l1.5-1.5L7 11.5z" fill="currentColor"/></svg>Export to Excel';
    } catch (error) {
        console.error('Export failed:', error);
        alert('Failed to export table. Please try again.');
        exportBtn.disabled = false;
        exportBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="margin-right: 8px; vertical-align: middle;"><path d="M14 11v3H2v-3H0v3c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-3h-2z" fill="currentColor"/><path d="M7 11.5V1h2v10.5l3.5-3.5L14 9.5 8 15.5 2 9.5l1.5-1.5L7 11.5z" fill="currentColor"/></svg>Export to Excel';
    }
}

function toggleRow(element) {
    // Find the row - element could be the tr, td, or first-child td
    let row;
    if (element.tagName === 'TR') {
        row = element;
    } else if (element.tagName === 'TD') {
        row = element.parentElement;
    } else {
        row = element.closest('tr');
    }

    if (!row) return;

    const firstCell = row.querySelector('td:first-child');
    const icon = firstCell.querySelector('.header-expand-icon');
    const cells = row.querySelectorAll('td:not(:first-child) .cell-details');

    // Check if this row is already expanded
    const isExpanded = icon && icon.classList.contains('expanded');

    if (isExpanded) {
        // Collapse this row
        cells.forEach(cell => {
            cell.classList.remove('expanded');
        });
        if (icon) icon.classList.remove('expanded');
    } else {
        // Expand this row
        cells.forEach(cell => {
            cell.classList.add('expanded');
        });
        if (icon) icon.classList.add('expanded');
    }
}

// Horizontal scroll indicator
document.addEventListener('DOMContentLoaded', function() {
    const tableWrapper = document.getElementById('tableWrapper');
    if (!tableWrapper) return;

    function updateScrollIndicators() {
        const scrollLeft = tableWrapper.scrollLeft;
        const scrollWidth = tableWrapper.scrollWidth;
        const clientWidth = tableWrapper.clientWidth;

        // Remove all classes first
        tableWrapper.classList.remove('scrolled', 'scrolled-start', 'scrolled-end');

        // Check if table even needs scrolling
        if (scrollWidth <= clientWidth) {
            // Table fits entirely, no scrolling needed - hide all indicators
            return;
        }

        // Determine scroll position
        const isAtStart = scrollLeft <= 10;
        const isAtEnd = (scrollLeft + clientWidth) >= (scrollWidth - 10);

        if (isAtStart) {
            // At the start - show RIGHT indicator
            tableWrapper.classList.add('scrolled-start');
        } else if (isAtEnd) {
            // At the end - show LEFT indicator only
            tableWrapper.classList.add('scrolled-end');
        } else {
            // In the middle - show LEFT indicator
            tableWrapper.classList.add('scrolled');
        }
    }

    tableWrapper.addEventListener('scroll', updateScrollIndicators);

    // Set initial state after page load
    setTimeout(updateScrollIndicators, 200);

    // Also update on window resize
    window.addEventListener('resize', updateScrollIndicators);
});
</script>

## Key Takeaways

### When to use each framework

Each framework serves distinct governance needs depending on your context and objectives. 

For organisations seeking structured, capability-aware governance across diverse agentic systems without heavy certification overhead, the **ARC Framework** offers a practical starting point. Those establishing broader AI risk management processes should consider **NIST AI RMF** for foundational guidance, particularly for general AI systems, while the **EU AI Act** becomes mandatory for any AI providers or users operating in Europe, especially when deploying high-risk or agentic AI. 

At a more conceptual level, **Dimensional Governance** supports policy development and oversight structure design through its focus on high-level governance architecture. Security-focused teams will find complementary value in **OWASP Agentic AI** for technical hardening and threat-based testing, **Google SAIF 2.0** for enterprise security integration and CISO-level strategy, and **CSA MAESTRO** for layer-specific security analysis with defence-in-depth implementation.

### Complementary use

Many frameworks can be used together to create a more comprehensive governance approach. 

The **ARC Framework** pairs particularly well with other standards: combine it with **OWASP** to leverage ARC Framework's governance and control selection alongside OWASP's detailed security threat analysis and red-teaming capabilities, or integrate it with **NIST AI RMF** to apply NIST's lifecycle functions while implementing ARC Framework's capability-specific controls. For organisations operating in Europe, **ARC Framework** provides a practical way to operationalise **EU AI Act** requirements for high-risk agentic systems. 

Security-focused teams can achieve comprehensive coverage by combining **SAIF**'s enterprise principles with **OWASP**'s threat catalogues and **MAESTRO**'s layered architecture for defence-in-depth. 

At the governance level, **Dimensional Governance** and **ARC Framework** complement each other well — use Dimensional for policy-level governance structure and strategic framing, then apply ARC Framework for operational implementation and day-to-day risk management.
