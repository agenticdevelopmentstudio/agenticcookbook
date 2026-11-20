
Treat the following as roadmap/proposed behavior. Do **not** write configs or guidance that assume it as current.

- The **native Go compiler ("tsgo", "Project Corsa")** and the **TypeScript 7.0** line are a proposed reimplementation targeting large build speedups. As of this writing, confirm actual release state against the official [TypeScript blog](https://devblogs.microsoft.com/typescript/) and [microsoft/typescript-go](https://github.com/microsoft/typescript-go) before depending on it.
- "**strict by default**" and the **removal of legacy module/target modes** (e.g. dropping `node10` resolution, raising the minimum target) are PLANNED breaking changes discussed for the 6.0/7.0 line. Until you have verified them in shipped release notes, **MUST** keep setting `"strict": true` explicitly rather than relying on an implicit default.

