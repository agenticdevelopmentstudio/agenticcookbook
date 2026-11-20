
# MCP server design

Guidance for authoring a Model Context Protocol (MCP) server — the side that exposes context and capabilities to an LLM host. (Consuming MCP servers is covered elsewhere.) The model routes on the names, descriptions, and schemas you publish, so treat them as the public contract.

**Pin to a dated spec revision.** Default to the stable **2025-11-25** revision unless the host requires an older one. Negotiate the revision during initialization rather than hard-coding it. Treat any release-candidate or draft revision as a forecast and gate it behind explicit opt-in.

