
OT transforms concurrent operations so they can be applied in any order and converge to the same result. Used primarily for collaborative text editing where character position matters.

SHOULD use OT only for text or sequence editing with a central server. For offline-first or peer-to-peer scenarios, prefer RGA CRDTs — OT requires all operations to pass through a central coordinator for ordering.

