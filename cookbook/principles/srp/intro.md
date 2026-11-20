
# SRP

A module should be answerable to one and only one actor — one stakeholder, one source of change requests. "Reason to change" is a person or role, not an abstract concern. When two actors can each independently demand a change to the same module, the module is serving two masters and its history will show conflicting edits that each broke the other actor's expectations. Where separation-of-concerns partitions by *kind of work* (UI, logic, data), SRP partitions by *who requests the change*.
