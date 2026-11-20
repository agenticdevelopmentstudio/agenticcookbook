
# MCP tool input validation

Every argument a Model Context Protocol (MCP) tool handler receives is model-supplied, untrusted input — even when the tool's caller is "your own" agent, the model can be steered by injected content. The model is **not** an authorization boundary. Pairs with `mcp-server-security`, which covers tool poisoning, token passthrough, and confused-deputy.
