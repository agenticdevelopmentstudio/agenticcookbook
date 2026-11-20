
- **non-root**: The image MUST run as a non-root user. Create an unprivileged user/group and set `USER` before `ENTRYPOINT`. Do not install or rely on `sudo`.
- **no-baked-secrets**: The image MUST NOT bake secrets (API keys, tokens, certs, passwords) into layers, `ENV`, or build args — they persist in image history even if later removed. Inject runtime config via environment/mounted secrets (see twelve-factor-config). For build-time credentials, use BuildKit secret mounts (`RUN --mount=type=secret,...`), which do not persist in the final image.
- **least-files**: Use a `.dockerignore` to exclude `.git`, secrets, local env files, build output, and `node_modules` from the build context — this shrinks context, speeds builds, and prevents accidental secret leakage.
- **drop-extras**: Do not install packages "just in case." Fewer packages means fewer CVEs to patch.

