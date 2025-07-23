# What is a Baseline? 

There are common aspects across all agentic AI systems - the agents themselves have similar components (LLM, tools, instructions, memory), while the system itself has some architectural requirements for the "agentic" part to work effectively. In this section, we describe each of these aspects and explain how they may give rise to certain risks (but we defer the full treatment of the risks to the next section).

## Components of an Agent

<img src="../assets/agent-components.png" alt="Components of an agent" style="width: min(600px, 50%); display: block; margin: 0 auto;">
<font style="font-style: italic; text-align: center;">Figure 1: Components of a typical agent in an agentic AI system</font>

Based on our literature review of agents, we observe that individual agents are typically composed of four key components as shown in Figure 1 above. We go through them in turn below.

### LLM

The LLM is the **central reasoning engine that processes instructions, interprets user inputs, and generates contextually appropriate responses** by leveraging its trained language understanding and generation capabilities. As the cognitive core of the agent, it orchestrates all other components, such as determining when to access memory, which tools to invoke, and how to synthesize information into coherent outputs that align with the given instructions.

Teams today have a wide range of LLMs to pick from - from large closed-source LLMs such as OpenAI's GPT o3, Anthropic's Claude 4 Opus, or Gemini 2.5 Pro, to smaller open-weights models like Llama 3.3 8B, Qwen3 8B, and Mistral Small 3.1. Moreover, some teams may choose to finetune models to achieve greater performance for their specific use case or domain.

The choice of LLM has significant implications for the safety and security of the agent - some LLMs are more prone to being jailbroken than others, while others are less aligned and thus more likely to generate malicious or harmful outputs. In addition, using LLMs which are hosted by external model providers versus hosting it internally on your own infrastructure carries different risks.

### Tools

What sets agents apart from standard LLM applications is the ability to autonomously execute actions, and the most critical enabler of that is tool use. Tools transform the agent from a passive conversational system into **an active problem-solver that can manipulate files, query databases, control devices, or access APIs based on the LLM's reasoning and user needs.** Underlying the ecosystem of tools for agents is the Model Context Protocol ("MCP"), which provides a consistent interface for LLMs to discover and interact with a variety of external tools and services, thereby enabling simpler actions from executing code on the local `bash` terminal as well as more complex ones like merging pull requests on GitHub automatically. 

Tools are closely related to capabilities because tools enable capabilities - executing code or reading databases would not be possible without a MCP server to bridge between the LLM and the external tool (i.e. the `bash` terminal or the Postgres database). However, tools are distinct from capabilities (see the previous section [Why the ARC Framework?](../intro/why_arc.md#why-focus-on-capabilities) for the full discussion), and we analyse them as a distinct component of an agent.

While the risks relating to tools tend to be linked to their capabilities (e.g. code execution risks arise from having access to the `bash` terminal), there are some common risks which are shared by all tools, such as weak authentication protocols, rogue MCP tools, or vulnerability to prompt injections. Basic hygiene standards for the use of tools in agentic AI systems may be needed to manage these risks.

### Instructions

Instructions are **the blueprint which defines an agent's role, capabilities, and behavioural constraints**, ensuring it operates within intended parameters and maintains its performance across different scenarios. Without clear instructions, even sophisticated LLMs with powerful tools and extensive knowledge bases would  produce inconsistent or misaligned outputs that fail to meet user expectations or safety requirements.

Due to the importance of instructions in guiding the agent's behaviour, poor instructions can give rise to serious safety and security risks in an agentic AI system. For example, incorrectly defined objectives can result in agents optimising for the wrong metric, which either renders it ineffective or leads to unforeseen safety and security consequences for the organisation. Furthermore, a lack of instructions on the proper ethical or safety guidelines may cause the LLM to take actions which are contradictory to the organisation's or user's well-being.

### Memory

The memory or knowledge base component **provides the agent with contextual awareness and information persistence**, enabling it to maintain coherent conversations, learn from past interactions, and access relevant facts without requiring constant re-instruction. For more complex multi-agent systems, the memory component is critical for the agent to operate collaboratively with other agents in the system and to retain the contextual understanding necessary for complex, multi-step tasks.

Memory components are vulnerable to data poisoning where malicious actors inject false or misleading information that gets stored and later influences the agent's decisions. Privacy and data leakage risks may also occur if agents inadvertently stores and shares sensitive information from previous interactions. There may also be persistence risks where temporary errors, biases, or inappropriate responses become permanently encoded in the knowledge base, reinforcing problematic behaviors over time and making the agent increasingly unreliable.

## Design of an agentic system

We now broaden our perspective to examine how agentic AI systems are assembled from individual agents, focusing specifically on two aspects - the agentic architecture (i.e. how agents are connected) and their roles and access controls (i.e. how the task is split across agents).

### Agentic Architecture

The agentic architecture defines **how multiple agents are interconnected, coordinated, and orchestrated to collectively solve complex tasks that exceed individual agent capabilities**, including patterns like hierarchical delegation, parallel processing, or sequential handoffs between specialised agents. One key aspect of any agentic architecture is the level of agentic autonomy, or the range of decisions that agents are permitted to make.[^3] 

<img src="../assets/agent-workflows.png" alt="Agentic architectures" style="width: min(600px, 50%); display: block; margin: 0 auto;">
<font style="font-style: italic; text-align: center;">Figure 2: Illustration of two different agentic architectures</font>

Some agentic AI systems may use a linear workflow for greater control and predictability, while others may use a centralised orchestration approach with specialised agentic roles to speed up the processing of many data sources. For example, a customer support system may use a linear agentic workflow where queries pass sequentially through classification, research, solution generation, and quality assurance agents, while an internal analytics system may spin up multiple agents simultaneously to access different data sources, perform specialised analytical functions (e.g. statistics, visualization, anomaly detection), and converge their outputs through a central agent which produces the final analytics report.

Different architectures result in varying levels of system-wide risk, and these need to be considered carefully. Linear systems are vulnerable because tainted inputs spread from one agent to the next like a chain reaction, while centrally orchestrated systems can isolate failures to specific agents but risk having problems at the top level affect all subordinate agents.

### Roles and Access Controls

Roles and access controls **establish differentiated responsibilities and permissions across agents within the system**, ensuring that each agent operates within appropriate boundaries while being able to fulfill its designated function. This is critical because it limits unauthorised actions, contains the blast radius of potential failures or security breaches, and enables the system to maintain reliability even when individual agents may be compromised or behave unexpectedly.

There are various possible roles depending on the level of specialisation required, such as orchestrator agents that manage workflows, specialist agents that perform pre-defined technical functions, or interface agents that handle external communications. Returning to our earlier example, some types of agents in a customer support system may include intake agents that receive and classify queries, knowledge agents that search documentation for answers, and response agents that craft and send customer communications. In contrast, an internal analytics system would employ different roles, such as data ingestion agents to collect information from various sources, analysis agents to generate insights, and reporting agents to create visualizations and reports.

Defining roles and access controls poorly may result in agents having unauthorised access to data or systems, allowing compromised agents to delete files, steal information, or break critical systems. Additionally, agents may inherit too many privileges from shared accounts, meaning a simple data processing agent could accidentally cause major damage because it has access to powerful system controls it was never meant to use.

<!---- footnotes --->

[^1]: While this is not always the case
[^3]: <https://developer.nvidia.com/blog/agentic-autonomy-levels-and-security/> or <https://huggingface.co/blog/ethics-soc-7>
