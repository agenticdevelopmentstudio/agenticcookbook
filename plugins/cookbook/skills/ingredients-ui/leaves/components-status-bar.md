<!-- leaf: ingredients-ui/components-status-bar · source: ingredients/ui/components/status-bar.md -->

**Rules** (cite as `ingredients-ui/components-status-bar#<slug>`):

- `slide-in-animation` MUST
- `slide-out-animation` MUST
- `indeterminate-spinner` MUST
- `status-text-display` MUST
- `overlay-not-push` MUST
- `ease-in-out-timing` MUST
- `update-text-while-visible` SHOULD
- `non-blocking-interaction` MUST
- `announce-appearance` MUST
- `polite-live-region` SHOULD

# Status Bar

## Overview

A slim, animated bar that slides in at the bottom of a view to indicate a background operation is in progress. Shows an indeterminate spinner and a status text message. Appears during sync, loading, or processing operations and disappears when complete.

## Behavioral Requirements

- **slide-in-animation**: The bar MUST slide in from the bottom edge with an animated transition when an operation begins.
- **slide-out-animation**: The bar MUST slide out with an animated transition when the operation completes.
- **indeterminate-spinner**: The bar MUST display an indeterminate progress spinner (platform-native).
- **status-text-display**: The bar MUST display a status text message describing the current operation.
- **overlay-not-push**: The bar MUST be overlaid on existing content (not push content up).
- **ease-in-out-timing**: The animation MUST use an ease-in-out curve with ~0.3s duration.
- **update-text-while-visible**: The bar SHOULD support updating the status text while visible (e.g., "Scanning..." -> "Scanning 42 files...").
- **non-blocking-interaction**: The bar MUST NOT block interaction with the content beneath it.

## Appearance

- **Height**: 28–32pt
- **Background**: System material / translucent with subtle blur (or opaque secondary background)
- **Spinner**: Platform-native indeterminate `ProgressView` / `CircularProgressIndicator` / CSS spinner, 16pt
- **Text**: Caption, secondary color
- **Spacing**: 8pt between spinner and text
- **Padding**: 8pt horizontal, 4pt vertical
- **Corner radius**: 0 (full-width bar) or 8pt if floating
- **Position**: Bottom edge of container, full width

## Accessibility

- **announce-appearance**: The bar MUST announce its appearance to screen readers with the status text.
- **polite-live-region**: Status text updates SHOULD be announced as polite live region updates (not interrupting).

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI**: Use `.overlay(alignment: .bottom)` with a `Group` that conditionally renders the bar. Transition: `.move(edge: .bottom).combined(with: .opacity)`. Animation: `.easeInOut(duration: 0.3)`. Use `ProgressView()` for spinner.
- **Compose**: `Box(modifier = Modifier.fillMaxSize())` with `AnimatedVisibility(enter = slideInVertically + fadeIn, exit = slideOutVertically + fadeOut)` at bottom. `CircularProgressIndicator(modifier = Modifier.size(16.dp))`.
- **React/Web**: Absolutely positioned `<div>` at `bottom: 0` with CSS transition on `transform: translateY()` and `opacity`. Use CSS `@keyframes spin` for spinner or a library spinner.
