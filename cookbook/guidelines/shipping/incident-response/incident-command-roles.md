
Separate *coordinating* the response from *doing* the work so neither starves the other. The roles below follow the established Incident Management At Google (IMAG) model; adapt names to your org but keep the separation.

- **incident-commander**: One person **MUST** hold overall coordination of a declared incident. The IC decides, delegates, and owns the response — they do not also debug.
- **communications-lead**: For higher-severity incidents a CL **SHOULD** own stakeholder and customer updates so the IC and responders are not interrupted.
- **operations-lead**: One or more responders **SHOULD** own mitigation and investigation, reporting to the IC.
- For small incidents one person **MAY** hold all roles; as severity rises, roles **MUST** be split across people.
- The IC role **MUST** be explicitly handed off (not implicitly dropped) at shift boundaries or when the holder steps away.

