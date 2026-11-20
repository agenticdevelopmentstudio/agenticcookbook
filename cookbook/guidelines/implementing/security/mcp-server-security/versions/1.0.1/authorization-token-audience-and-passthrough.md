
Treat a remote MCP server as an OAuth 2.1 **resource server**.

- The server **MUST NOT** accept any token that was not explicitly issued for it (validate the `aud`/audience per RFC 8707 resource indicators).
- The server **MUST NOT** pass a received token through to a downstream API ("token passthrough" is explicitly forbidden). To call a downstream service, use a token-exchange flow to obtain a distinct token, or act as its own client.
- The server **MUST** validate every inbound token before processing the request and reject ones lacking it in the audience.

