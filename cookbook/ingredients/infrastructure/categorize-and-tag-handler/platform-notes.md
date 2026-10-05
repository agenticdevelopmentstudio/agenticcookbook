
SwiftUI, Compose, and React/Web do not apply: the handler has no view layer. The handler logic is identical in the Swift macOS development node and the TypeScript production node; only the LLM backend wiring differs (see the `llm-backend` ingredient). In Swift, log through `os.Logger` with a category per handler; in TypeScript, log structured JSON to stdout.

