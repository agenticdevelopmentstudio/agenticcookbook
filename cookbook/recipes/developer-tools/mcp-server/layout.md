
The server is the composition point: the host speaks the protocol to the server over one transport, and the server dispatches each request to the appropriate primitive. Tools are the primary primitive; resources and prompts are optional and chosen by purpose.

```
                         protocol (JSON-RPC 2.0)
                    revision negotiated at initialize
                          default: 2025-11-25
  ┌──────────────┐  ───────────────────────────────▶  ┌────────────────────────────┐
  │  LLM Host    │   initialize / capabilities         │        MCP Server          │
  │ (Claude,     │   tools/list, tools/call            │                            │
  │  ChatGPT,    │   resources/list, resources/read    │  ┌──────────────────────┐  │
  │  IDE agent)  │   prompts/list, prompts/get         │  │ capability negotiation│  │
  │              │  ◀───────────────────────────────  │  │ + protocol revision   │  │
  └──────┬───────┘   results / structuredContent       │  └──────────┬───────────┘  │
         │           JSON-RPC errors                   │             │              │
         │                                             │   ┌─────────▼──────────┐   │
   transport (one of):                                 │   │  request dispatch  │   │
   ┌─────────────────────┐                             │   └──┬─────────┬───────┘   │
   │ stdio (local subproc)│  no network, no auth        │      │         │           │
   │   — or —             │                             │   tools/    resources/    │
   │ Streamable HTTP      │  OAuth 2.1 resource server  │   call      prompts        │
   │   (remote service)   │  validate aud, no passthru  │      │         │           │
   └─────────────────────┘                             │  ┌───▼───┐ ┌───▼────────┐   │
                                                        │  │ MCP   │ │ resources  │   │
   For Streamable HTTP only:                            │  │ tool  │ │ / prompts  │   │
   ┌───────────────────────────────┐                    │  │ #1..N │ │ (optional) │   │
   │ Authorization Server (OAuth)  │◀── token issuance  │  └───┬───┘ └────────────┘   │
   │ issues aud-scoped tokens      │                    │      │ per-call authorize  │
   └───────────────────────────────┘                    │      ▼ + schema validate   │
                                                         │  downstream API (distinct  │
                                                         │  token via exchange, never │
                                                         │  the inbound token)        │
                                                         └────────────────────────────┘
```

