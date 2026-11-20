
React Server Components (RSC) are the default for new high-performance **React** apps — but they are not a universal web requirement and apply only when you have already chosen React.

- RSC is only usable **through a framework**. As of 2026: the **Next.js App Router is the mature, production-proven** RSC implementation. **React Router v7 RSC support is newer and less stable** — treat it as evolving, and pin to a tested release before relying on it.
- RSC moves component work to the server so component code and its dependencies do **not** ship to the client; you **SHOULD** keep `"use client"` boundaries small and push interactivity to leaf components.
- RSC adds **real complexity**: a server/client boundary you must reason about, serialization constraints on props, and **framework lock-in**. Adopt it deliberately, not reflexively.
- You **MUST NOT** introduce RSC to a non-React stack or to a React app where the server/client split adds no measurable benefit — that violates simplicity.

