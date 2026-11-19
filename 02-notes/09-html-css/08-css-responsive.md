# CSS 08 — responsive behavior from content constraints

## Outcome

Adapt a page to available space and user text settings rather than one device screenshot. Prerequisites: flex/grid and units. Practice: web-css.

Start from a usable narrow layout, then add space when content benefits. Breakpoints should reflect when a layout stops serving its content, not a permanent list of phone brands. The lab's 360/768/1200 pixel observations and one/two/three columns are explicit exercise acceptance points, not universal product defaults.

```css
.cards { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1rem; }
@media (min-width: 42rem) {
  .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
```

Viewport metadata allows the intended mobile viewport, but still needs fluid layout. Use max-width/min()/clamp() when they express a clear constraint. Check text wrapping, images, controls, gaps and navigation across intermediate widths, not just the three measured points.

## User preferences and change

Test text enlargement and actual browser zoom, long/translated strings, keyboard focus and absent/slow assets. Root-font-size changes in an automated test exercise some text-scaling behavior; they are not a complete substitute for browser zoom or assistive-technology evaluation. Respect reduced-motion preferences if you add animation; the static lab needs no animation.

Never force a tiny fixed viewport or hide content to make a screenshot fit. Overflow can indicate min-content sizing, a fixed width, an unbreakable token or a transformed/positioned box; diagnose the cause.

## Completion

Pass computed geometry checks, inspect the reference/workspace visually and document which manual conditions were actually tried. Change request: support a long card title and an additional control without new horizontal overflow or unreachable buttons. Explain where the layout transitions and why.

Sources: [responsive design](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design), [media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries).
