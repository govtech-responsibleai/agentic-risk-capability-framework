# Elements of agentic systems

Across all agentic systems, there are three indispensable elements to examine:
**(1)** the components of an agent,
**(2)** the design of the agentic system, and
**(3)** the capabilities of the agentic system.

---

## Components

Components are essential parts of a single, standalone agent.
Here, we synthesize prevailing agreement on the key components of an agent from various sources, such as **OpenAI** [^1].

* **LLM**: The LLM is the central reasoning engine that processes instructions, interprets user inputs, and generates contextually appropriate responses by leveraging its trained language understanding and generation capabilities.
* **Tools**: Tools enable LLMs to interact with the external environment — editing files, querying databases, controlling devices, or accessing APIs. This is facilitated by **MCP servers**, which provide LLMs a consistent interface to discover and utilize a variety of tools.
* **Instructions**: Instructions are the blueprint that defines an agent’s role, capabilities, and behavioral constraints, ensuring it operates within intended parameters and maintains consistent performance across different scenarios.
* **Memory**: The memory or knowledge base component provides the agent with contextual awareness and information persistence, enabling it to maintain coherent conversations, learn from past interactions, and access relevant facts without requiring constant re-instruction.

---

## Design

We now broaden our perspective to examine how agentic AI systems are assembled from individual agents from a system design perspective.

* **Agentic Architecture**: The agentic architecture defines how multiple agents are interconnected, coordinated, and orchestrated to collectively solve complex tasks that exceed individual agent capabilities. This includes patterns like hierarchical delegation, parallel processing, or sequential handoffs between specialized agents.
  Different architectures result in varying levels of system-wide risk, and these need to be considered carefully. Similarly, the **protocols** [^2] by which agents communicate may also give rise to security risks.

* **Roles and Access Controls**: Roles and access controls establish differentiated responsibilities and permissions across agents within the system, ensuring that each agent operates within appropriate boundaries while being able to fulfill its designated function. This is critical because it limits unauthorized actions, contains the blast radius of potential failures or security breaches, and enables the system to maintain reliability even when individual agents may be compromised or behave unexpectedly.

* **Monitoring and Traceability**: Monitoring and traceability enable visibility into agentic system behavior, interactions, and decision-making pathways. They allow developers and operators to understand what agents are doing, why they made particular choices, and how outcomes were produced. This is essential for post-hoc debugging, real-time anomaly detection, and establishing accountability — particularly when agents operate with autonomy or interact with sensitive systems and data.

---

## Capabilities

We see three broad categories of capabilities — **cognitive**, **interaction**, and **operational** — which can be further broken down into more granular abilities.

### Cognitive Capabilities

*Cognitive capabilities* encompass the agentic AI system’s internal “thinking” skills — how it analyses information, forms plans, learns from experience, and monitors its own performance.

* **Planning & Goal Management**: The capability to develop detailed, step-by-step, and executable plans with specific tasks in response to broad instructions. This includes prioritizing activities, managing dependencies between tasks, monitoring progress, and adapting to changes or obstacles.
* **Agent Delegation**: The capability to assign subtasks to other agents and coordinate their activities to achieve broader goals. This includes identifying suitable components for specific tasks, issuing clear instructions, managing inter-agent dependencies, and monitoring performance or failures.
* **Tool Use**: The capability to evaluate available options and choose the best tool for specific subtasks. This requires understanding the capabilities and limitations of different tools and matching them appropriately to the tasks.

### Interaction Capabilities

*Interaction capabilities* describe how the agentic AI system exchanges information with users, other agents, and external systems. These are differentiated based on how and what they interact with.

* **Natural Language Communication**: The capability to fluently and meaningfully converse with human users, handling a wide range of situations such as explaining complex topics, generating documents or prose, or discussing issues interactively.
* **Multimodal Understanding & Generation**: The capability to take in image, audio, or video inputs and/or generate image, audio, or video outputs — including analyzing visual information, transcribing speech, or creating multimedia content.
* **Official Communication**: The capability to compose and directly publish communications that formally represent an organization to external parties (e.g., customers, partners, regulators, courts, media) via approved channels and formats, without human oversight.
* **Business Transactions**: The capability to execute transactions involving money, services, or commitments with external parties. It can process payments, make reservations, or perform authorized business actions.
* **Internet & Search Access**: The capability to access and search the Internet for knowledge resources, particularly for up-to-date information to provide accurate answers.
* **Computer Use**: The capability to directly control a computer interface by moving the mouse, clicking buttons, and typing on behalf of the user. It can navigate applications and perform GUI-based tasks.
* **Other Programmatic Interfaces**: The capability to interact with external systems through APIs, SDKs, or backend services — for instance, sending and receiving data via RESTful APIs, pushing code to repositories, or invoking cloud services to retrieve or manipulate information.

### Operational Capabilities

*Operational capabilities* focus on the agentic AI system’s ability to execute actions safely and efficiently within its operating environment.

* **Code Execution**: The capability to write, execute, and debug code in various programming languages to automate tasks or solve computational problems.
* **File & Data Management**: The capability to create, read, modify, organize, convert, query, and update information across both unstructured files (e.g., PDFs, Word docs, spreadsheets) and structured data stores (e.g., SQL/NoSQL databases, data warehouses, vector stores).
* **System Management**: The capability to adjust system configurations, manage computing resources, and handle technical infrastructure tasks. This includes monitoring system performance, securely handling authentication and access controls, and performing optimizations while maintaining security best practices.


[^1]: OpenAI (2025). *A Practical Guide to Building Agents.* [https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^2]: Google (2025). *Agent2Agent (A2A) Protocol – Latest.* [https://a2a-protocol.org/latest/](https://a2a-protocol.org/latest/)
