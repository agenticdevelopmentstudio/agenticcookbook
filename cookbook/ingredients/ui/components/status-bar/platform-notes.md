
- **SwiftUI**: Use `.overlay(alignment: .bottom)` with a `Group` that conditionally renders the bar. Transition: `.move(edge: .bottom).combined(with: .opacity)`. Animation: `.easeInOut(duration: 0.3)`. Use `ProgressView()` for spinner.
- **Compose**: `Box(modifier = Modifier.fillMaxSize())` with `AnimatedVisibility(enter = slideInVertically + fadeIn, exit = slideOutVertically + fadeOut)` at bottom. `CircularProgressIndicator(modifier = Modifier.size(16.dp))`.
- **React/Web**: Absolutely positioned `<div>` at `bottom: 0` with CSS transition on `transform: translateY()` and `opacity`. Use CSS `@keyframes spin` for spinner or a library spinner.

