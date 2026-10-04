
# MCP tool input validation

Every argument a Model Context Protocol (MCP) tool handler receives is model-supplied, untrusted input — even when the tool's caller is "your own" agent, the model can be steered by injected content. The model is **not** an authorization boundary. Pin guidance to the MCP spec revision dated **2025-06-18** (tool `inputSchema` is JSON Schema **2020-12**). Pairs with `mcp-server-security`, which covers tool poisoning, token passthrough, and confused-deputy.

