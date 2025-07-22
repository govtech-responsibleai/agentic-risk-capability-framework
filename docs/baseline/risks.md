# Baseline Risks

In this section, we describe the baseline risks using the logical structure we described in the previous section. 

## Tools

For example, some MCP servers (especially newer or poorly created ones) do not correctly implement authentication and authorisation, resulting in the confused deputy problem where the LLM confuses the user's request with another user's (or even an admin's) request.[^9] Additionally, there may be rogue MCP servers or tools which appear similar to the original one (and perhaps with special features), but actually contain malicious code which are executed upon loading the MCP server in your internal environment.[^10] Enforcing basic hygiene checks for MCP servers is important to help mitigate these risks.