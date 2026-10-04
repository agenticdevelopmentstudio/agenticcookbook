
# App Interactions

The communication patterns between components reveal how tightly or loosely they are coupled. A component that communicates only through a narrow delegate protocol is loosely coupled and independently testable. A component that reads and writes shared mutable state is tightly coupled to everything that touches that state. This lens maps the in-process communication patterns to understand where the real dependencies lie — which may differ substantially from what the import graph shows.

