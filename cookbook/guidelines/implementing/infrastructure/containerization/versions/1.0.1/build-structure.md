
- **multi-stage**: Dockerfiles MUST use multi-stage builds so the final image contains only the runtime artifact — not compilers, build tools, dev dependencies, or source. Build in an earlier stage; `COPY --from=<stage>` only what runs.
- **base-image**: The final stage MUST use a minimal base — language-specific `slim`, `alpine`, or distroless. Avoid full OS images when a slim variant carries the runtime. A smaller base means fewer packages and a smaller attack surface.
- **one-concern**: Each image SHOULD address a single concern (one app/process). Decouple distinct services into separate images so they scale and deploy independently.
- **workdir**: Use `WORKDIR` with absolute paths rather than chained `cd`. Use `ENTRYPOINT` for the executable and `CMD` for default arguments.

