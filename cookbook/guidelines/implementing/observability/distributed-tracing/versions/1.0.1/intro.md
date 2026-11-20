
# Distributed tracing and context propagation

A distributed trace stitches the spans produced by every service that handles one logical request into a single causal tree. Standardize instrumentation on OpenTelemetry (OTel) and propagation on W3C Trace Context so traces work across vendors and language boundaries. The durable payoff: when something is slow or broken, you can follow one `trace_id` from the edge through every hop.

