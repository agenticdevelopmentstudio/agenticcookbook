
# SRP

A module should be answerable to one and only one actor — one stakeholder, one source of change requests. "Reason to change" is a person or role, not an abstract concern. When two actors can each independently demand a change to the same module, the module is serving two masters and its history will show conflicting edits that each broke the other actor's expectations. Where separation-of-concerns partitions by *kind of work* (UI, logic, data), SRP partitions by *who requests the change*.

- Trace each anticipated change request to a stakeholder — if two stakeholders can drive changes to the same module independently, the module carries two responsibilities and should split
- Keep code that changes together, together; separate code that changes for different reasons even if it looks similar today
- Treat unexpected merge conflicts between unrelated features as a signal that a module is absorbing responsibilities for more than one actor
- A long function or wide class is usually a sign that multiple actors share it — prefer narrow units each answerable to one actor

