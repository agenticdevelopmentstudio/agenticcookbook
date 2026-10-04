
# Snapshot testing discipline

A snapshot (or approval) test is only as strong as the human review of its diff. A snapshot captures a serialized value once, then fails when future output diverges. That makes the *review* — not the assertion — the actual test. Use snapshots for stable, structured output; lean on explicit assertions everywhere logic matters.

