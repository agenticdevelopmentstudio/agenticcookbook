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
- **Deep Linking**, **Localization**, **Accessibility Options**, **Feature
  Flags**, **Analytics**, **Privacy** and **Logging** each get one sentence,
  `Not applicable: …`, traced to the source — unless the code does that
  thing: a user-facing error string is localization, a token or credential is
  privacy, a log call is logging.
- A genuine gap here is a contract the code's purpose calls for that the
  source leaves undefined. Only four things qualify for the usual
  `NEEDS REVIEW: Not implemented in source.` marker: an error that vanishes
  with no signal, a race with no ordering rule, input the purpose needs
  validated that is never validated, and a contract the code declares (a doc
  comment, a protocol) but does not meet. UI-only concerns (contrast, labels,
  focus, motion) never apply.
- Everything else is a fact, stated as a requirement or an edge case, never a
  marker:
  - an absent feature — no timeout, no cancellation, no retry, no logging;
  - a hardcoded English string or missing localization (under Localization);
  - a lossy but deliberate projection, or an error that is lossy but still
    surfaced (logged, returned, shown) — a logged failure is not swallowed;
  - behavior the source's own doc comment declares (`[:]` on undecodable
    input) — that is the contract;
  - a caller precondition that a doc comment, type signature or schema (a
    UNIQUE column) documents or enforces;
  - ordering in code that cannot interleave: single-threaded JavaScript, or a
    non-`Sendable` class used synchronously. Swift isolation is answered by
    the declaration — `Sendable`, `actor`, `@MainActor`, or a `public` type
    with no `Sendable` conformance that the compiler keeps in its domain;
  - what a server, backend route or other code outside the given sources
    does. State what this code does ("each call sends one POST with no
    idempotency key; the backend's response surfaces unchanged") and name the
    owner of the rest.
- **Platform Notes** name each platform's standard library or framework
  equivalent — the collection, concurrency, networking, persistence or
  serialisation API a port starts from. The **WinUI 3** bullet names the
  .NET / Windows App SDK APIs (`HttpClient`, `System.Text.Json`,
  `Windows.Storage`, `Task`/`async`, `ObservableCollection`,
  `INotifyPropertyChanged`) and what differs from the source. For server
  code, name the ASP.NET Core equivalent (minimal API route, middleware,
  `IHostedService`); it is never "not applicable".
