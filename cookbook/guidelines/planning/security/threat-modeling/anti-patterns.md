
- **One-time gate**: a single pre-launch review that is never revisited. Architecture drifts and the model goes stale.
- **Controls without threats**: adding TLS or input validation because a checklist says so, with no recorded threat they address. The control cannot be reasoned about or removed safely.
- **Boundary blindness**: enumerating threats on internal flows while ignoring the actual trust boundary (the network edge, the untrusted client, the multi-tenant split).
- **Tool worship**: assuming a diagramming or scanning tool *is* the threat model. The four questions and recorded decisions are the artifact; tools only assist.

