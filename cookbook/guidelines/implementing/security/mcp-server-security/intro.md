
# MCP server security

A Model Context Protocol (MCP) server exposes tools, resources, and prompts to an AI agent over an untrusted boundary: tool descriptions and tool outputs flow straight into the model's context, and remote servers participate in OAuth flows. Treat every string the server emits as model-influencing input and every token it receives as untrusted. Pin guidance to the MCP spec revision dated **2025-06-18** (Security Best Practices + Authorization), which carries the normative MUST/MUST NOT statements below.

