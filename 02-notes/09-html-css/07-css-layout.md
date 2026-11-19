# CSS 07 — normal flow, flexbox and grid

## Outcome

Choose a layout mechanism based on relationships, not copy-pasted positioning. Prerequisites: box model and selectors. Practice: web-css.

Start with normal document flow. A simple readable single column often needs no layout framework. Use flexbox for an adaptable row/column relationship and grid for explicit two-dimensional tracks. Absolute positioning is useful for deliberate overlays, not the default for every content element.

```css
.filters { display: flex; flex-wrap: wrap; align-items: end; gap: 1rem; }
.cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
```

Flex has main/cross axes determined by direction; alignment terms follow those axes, not permanently “horizontal”/“vertical.” Allow wrapping and understand flex-basis/grow/shrink when controls should adapt. Do not reorder visual items to mask a misleading DOM/keyboard sequence.

Grid defines tracks, placement and gaps. An fr distributes available space; intrinsic minimum sizes can still create overflow. minmax(0, 1fr) can deliberately allow tracks to shrink below min-content, paired with appropriate item wrapping/min-width. It does not mean every grid needs that pattern or that overflow should be hidden.

## Practice and debugging

Build web-css's six-card layout and filter controls. Use DevTools layout overlays and actual bounding boxes. At a chosen width, predict column widths/gaps before inspecting them. Remove min-width/wrapping in a private copy and introduce a long token to find the overflow cause.

Transfer: add an optional sidebar without making the main content unreadably narrow. Compare a flex and grid solution; explain the constraint that made one clearer. Preserve logical reading and keyboard order.

Sources: [flexbox](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox), [grid](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids).
