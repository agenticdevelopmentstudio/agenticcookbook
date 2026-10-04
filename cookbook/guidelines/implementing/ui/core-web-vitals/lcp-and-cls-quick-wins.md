
- **LCP**: preload the LCP image/font, serve responsive images, avoid render-blocking CSS/JS, use `fetchpriority="high"` on the hero image, and prefer server-side rendering for above-the-fold content.
- **CLS**: reserve space for media and dynamic content; avoid inserting content above existing content; use `font-display: optional`/`swap` deliberately and preload fonts to reduce reflow.

