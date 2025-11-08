# :material-shield-search: About the ARC Framework

In this section, we provide a detailed overview of the ARC Framework.

## Objective

The objective of the ARC Framework is to **help organisations systematise how they identify and manage the risks of agentic AI systems**. This is vital as companies begin to develop products and systems which provide LLMs with some agency to act autonomously on behalf of the organisation (which has a larger blast radius than with simpler LLM chatbots). 

## Baseline vs Capability Risks

One key aspect of the ARC Framework is in distinguishing between baseline and capability risks, where baseline risks apply to *all agentic AI systems* and capability risks apply to *agentic AI systems with a given capability set*[^1]. In our framework, capability risks will vary depending on the actual capability set of the agentic AI system - systems with more (or riskier) capabilities will incur more capability risks.

Note that each organisation has its own operating context - be it national (or state) regulations, industry-specific applications, or company-level considerations. As such, while we provide an initial list of both baseline and capability risks, these are meant only for reference and not as prescriptive guidance. Organisations should adapt these risks to their specific context, as we previously recommended for LLM safety testing.[^2]

### Baseline Risks

All agents have **common components**, such as the LLM, tools, instructions, and memory,[^3] and have **similar design considerations**, especially how agents are networked together and granted different roles within the system. Baseline risks capture the risks which arise from these two sources.

For example, choosing a LLM which is less aligned to societal values results in greater risk of the agentic AI system misunderstanding instructions or performing unintended actions, while allowing a single "super-user" agent to access all private data incurs greater privacy risks. 

In the ARC Framework, we identify the baseline risks arising from the four components and two design considerations and provide two lists of baseline controls: one with fewer controls and another with more controls. Having two lists provides policy options for organisations - the shorter list may be enforced for all systems, while the longer list can be used either as best practices or mandated for more mission-critical systems. 

Find out more in [our dedicated section on baseline risks](../baseline/index.md).

### Capability Risks

Beyond the common components and design patterns, **agentic AI systems often differ in the capabilities that they have to perform their intended tasks**. For example, an agentic coding assistant would have capabilities in searching the Internet (for documentation), executing code in your computer, and generating answers to your questions, while a travel planning assistant may need to be able to book flights on your behalf or to email clarifying questions to hotels or tourist attractions. 

In the ARC Framework, we start with a taxonomy of capabilities which agentic AI systems may have. From each capability, we describe the specific risks that may arise due to that capability and suggest the corresponding technical controls that would help to mitigate those risks. The nexus between capabilities, risks, and controls is crucial because this provides adaptable guidance to system owners - agentic AI systems with more capabilities incur more risks and thus controls. 

Find out more in [our dedicated section on capability risks](../capability/index.md).

## Implementation

Frameworks are only as useful when they are applied to real-world use. In designing this framework, we took much care to consider the practical constraints that organisations face as well as the competing concerns of governance teams and AI developers.

To make the ARC Framework easier to implement, we provide detailed step-by-step approaches for **how governance teams can implement the ARC Framework at an organisational level** as well as **how AI developers can apply the ARC Framework to manage the safety and security risks at a system level**. We also go through detailed examples to illustrate how this would work in specific situations. 

Find out more in [our dedicated section on implementation](../implementation/index.md).

<!-- to ensure that the framework strikes an appropriate balance between:
* Thoroughly mapping out the risk landscape, and not being too inflexible to changes
* Being applicable and adaptable to all agentic AI systems, and not being too generic or watered down
* Providing meaningful guidance on the risks and controls, and not being too prescriptive
* Making it scalable at an organisation-level, and not simply being a paper exercise -->

 <!--- Footnotes below --->

[^1]: Goh et al. Measuring What Matters: A Framework for Evaluating Safety Risks in Real-World LLM Applications. <https://arxiv.org/abs/2507.09820>, 2025. Accessed: 2025-07-21.
[^2]: We deliberately borrow this phrase from Amartya Sen's Capability Approach, which this framework is partially inspired by. For more background, see <https://iep.utm.edu/sen-cap/>.
[^3]: This is adapted from OpenAI's guide to building agents ([article](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)), though we include the extra component of the memory or knowledge base.