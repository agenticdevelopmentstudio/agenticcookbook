
- The semantic token source (e.g., `color.surface.primary`, `space.md`, `font.body`) **MUST** be platform-neutral and shared — typically a single JSON/DTCG file that platform builds transform.
- Use the W3C Design Tokens Community Group format (DTCG), which reached its first stable version, [2025.10](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/), in October 2025; pin to a dated revision so one source feeds Style Dictionary or an equivalent transform per platform. See <https://www.designtokens.org/>.
- Tokens **MUST** carry semantic names tied to intent, not raw values; map base → semantic → component layers so a single base change cascades.
- Platform-specific overrides **SHOULD** live as transforms or aliases over the shared source, never as a forked copy of it.

