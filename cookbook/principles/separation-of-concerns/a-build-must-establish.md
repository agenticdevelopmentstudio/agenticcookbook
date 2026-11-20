
- `should-have-one-reason-to-change`: each function, module, and service has one reason to change, or the work says why not
- `should-split-when-description-needs-and`: each module's responsibility is described in one sentence without "and", or the module was split, or the work says why not
- `should-separate-ui-logic-and-data`: UI rendering, business logic, and data access sit in separate layers that can change independently, or the work says why not
- `should-treat-cross-feature-edits-as-coupling`: no change to one feature forces edits in an unrelated feature, or the coupling is named as a defect
- `should-co-locate-by-reason-to-read`: code is separated by reason to change and co-located by reason to read, with no feature's behavior scattered across files to follow it, or the work says why
- `should-separate-workflow-steps-into-distinct-agents`: each step of a workflow runs in its own agent, with no one agent doing everything, or the work says why not
