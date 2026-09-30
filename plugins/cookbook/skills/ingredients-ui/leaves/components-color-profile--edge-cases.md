<!-- leaf: ingredients-ui/components-color-profile--edge-cases · source: ingredients/ui/components/color-profile.md -->

# Color Profile

**Rules** (cite as `ingredients-ui/components-color-profile--edge-cases#<slug>`):

- `many-custom-profiles` SHOULD — List SHOULD scroll; performance SHOULD remain smooth with 50+ profiles.
- `hex-color-parsing` MUST — #rrggbb and rrggbb formats MUST both be accepted. Invalid hex returns nil/default.

## Edge Cases

- **Many custom profiles**: List SHOULD scroll; performance SHOULD remain smooth with 50+ profiles.
- **Profile storage corruption**: Fall back to built-in defaults.
- **Hex color parsing**: `#rrggbb` and `rrggbb` formats MUST both be accepted. Invalid hex returns nil/default.
