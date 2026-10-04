
Cover, at minimum, these attack classes:

| Attack class | OWASP ref | What you are probing |
|---|---|---|
| Direct prompt injection | LLM01 | User input overrides system instructions |
| Indirect prompt injection | LLM01 | Hidden instructions in retrieved docs, web pages, or tool output |
| Jailbreaks | LLM01 | Role-play, encoding, and refusal-bypass to elicit blocked behavior |
| Sensitive info disclosure | LLM02 | Training-data, secret, or PII exfiltration |
| Improper output handling | LLM05 | Model output that triggers XSS, SQLi, or command injection downstream |
| Excessive agency / tool abuse | LLM06 | Unintended tool calls, privilege escalation, destructive actions |
| System-prompt leakage | LLM07 | Extraction of the system prompt or embedded policy/secrets |

- Indirect prompt injection (poisoned RAG content, tool results, file contents) is the highest-leverage agent attack and **MUST** be tested explicitly, not just direct user-input injection.
- Excessive agency tests **MUST** verify that the agent cannot exceed its least-privilege tool and permission scope, even when instructed to.

