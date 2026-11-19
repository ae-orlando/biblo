# CSS lab: resilient layout measured in a real browser

**ID:** web-css. Read [[05-css-cascade]] through [[09-browser-debugging]]. The complete static HTML is supplied so you can focus on work/styles.css; do not remove cards/content to pass geometry checks.

Requirements: six cards arranged in one column at viewport 360px, two at 768px, three at 1200px; gaps at least 12px where columns exist. Center .page with maximum width 1120px and at least 16px narrow-screen side space. Long unbroken headings and text enlargement must not produce horizontal document overflow.

Search button: at least 44px high, useful keyboard focus with an outline at least 2px, and normal-size text contrast at least 4.5:1. Use opaque text/background pairs on body/button for the deliberately limited automated contrast calculation. This is a product exercise, not a universal layout rule or full WCAG audit.

```bash
python3 90-tools/practice.py start web-css
python3 90-tools/practice.py check web-css
python3 90-tools/serve-web.py web-css
```

Checks inspect actual Chromium boxes, focus/computed styles, selected contrast pairs and a 200% root-text-size change—not CSS-source keywords. The native search submission is a static demonstration, not a working search backend.

Manual completion: inspect intermediate widths, real zoom, readability/design and keyboard/accessibility behavior. Explain cascade/box/grid/flex choices and catch a long-content overflow defect. Extend with a sidebar/control without hiding essential content.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/web-css/explanation.md)
