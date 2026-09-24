## non-UI component

This component comes from a `logic` root: shared code with no visual surface —
a model, client, engine, store or protocol. Write the recipe as a
specification of that code's contract, in the same template, so a port to
another platform is translation work.

- **Behavioral Requirements** carry the contract: the public operations and
  their inputs and outputs, the data shapes and their invariants, the errors
  each operation can raise or return and when, ordering and concurrency rules
  (which thread or actor, what may run in parallel, what is serialised),
  persistence and caching, and every side effect (files, network, processes,
  notifications). Name each type and field as the source names it.
- **Appearance**, **States** (the visual-state table) and **Accessibility**
  are one line each: `Not applicable — this is <what it is>, not a visual
  component.` Put runtime state machines (idle, loading, connected, failed)
  under Behavioral Requirements, not in the visual-state table.
- **Conformance Test Vectors** are input → expected output or effect pairs a
  port's unit tests can assert, traced to the source (and to its tests when
  they are given).
- **Edge Cases** are the boundary inputs and failure paths: empty and missing
  data, malformed input, cancellation, timeouts, concurrent calls, a missing
  file or an unreachable server.
- **Configuration** lists what the caller or environment supplies: parameters,
  defaults, environment variables, settings keys, injected dependencies.
- A genuine gap here is a contract the code's purpose calls for that the
  source leaves undefined — an error that is swallowed, a race with no
  ordering rule, input that is never validated. Mark it with the usual
  `NEEDS REVIEW: Not implemented in source.` marker; UI-only concerns
  (contrast, labels, focus, motion) never apply.
- **Platform Notes** name each platform's standard library or framework
  equivalent — the collection, concurrency, networking, persistence or
  serialisation API a port starts from. The **WinUI 3** bullet names the
  .NET / Windows App SDK APIs (`HttpClient`, `System.Text.Json`,
  `Windows.Storage`, `Task`/`async`, `ObservableCollection`,
  `INotifyPropertyChanged`) and what differs from the source.
