
# Eval-driven development for agent behavior

Deterministic code is verified with ordinary unit tests. Agent and LLM behavior is probabilistic — the same input can yield different valid (or invalid) outputs across runs — so it requires an **eval harness** that scores behavior over many trials. Treat evals as the test suite for the non-deterministic parts of the system.

