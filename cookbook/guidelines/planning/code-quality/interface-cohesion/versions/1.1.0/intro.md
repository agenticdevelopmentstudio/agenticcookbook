
# Interface Cohesion

A well-factored module exposes a coherent public surface. When multiple files jointly define, implement, or serve a single public API contract — a protocol and its default implementation, a set of co-exported types, or a shared base class and its required overrides — those files belong in the same scope group. This lens identifies clusters of files united by a shared public interface rather than by directory proximity alone.

