
- **should-answer-to-one-actor**: A module SHOULD be answerable to one and only one actor — one stakeholder, one source of change requests.
- **should-split-modules-two-stakeholders-drive**: SHOULD trace each anticipated change request to a stakeholder — if two stakeholders can drive changes to the same module independently, the module carries two responsibilities and SHOULD split.
- **should-keep-code-that-changes-together-together**: SHOULD keep code that changes together, together; SHOULD separate code that changes for different reasons even if it looks similar today.
- **should-treat-unexpected-merge-conflicts-as-a-signal**: SHOULD treat unexpected merge conflicts between unrelated features as a signal that a module is absorbing responsibilities for more than one actor.
- **should-prefer-narrow-units**: A long function or wide class is usually a sign that multiple actors share it — SHOULD prefer narrow units each answerable to one actor.
