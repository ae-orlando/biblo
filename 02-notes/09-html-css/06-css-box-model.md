# CSS 06 — boxes, units and readable content

## Outcome

Predict total occupied space, choose units deliberately and prevent content from being clipped when it grows. Prerequisite: cascade/computed values. Practice: web-css.

The box model separates content, padding, border and margin. With content-box, a declared width applies to content; padding/border add to the outer size. border-box includes them in the declared width. Margin remains outside either box model. A common deliberate baseline includes pseudo-elements:

```css
*, *::before, *::after { box-sizing: border-box; }
```

That reset does not choose a layout or prevent all overflow. Normal block/inline flow, margin behavior and a container's constraints still matter.

## Units express relationships

px is a CSS reference pixel, not necessarily one physical display pixel. rem relates to root font size; em and percentages depend on their context/property. Viewport units relate to the viewport, with mobile browser UI behavior worth checking. Use unitless line-height for text scaling and sensible maximum reading widths rather than a fixed-height text box.

```css
.page { width: min(calc(100% - 2rem), 70rem); margin-inline: auto; }
p { line-height: 1.6; overflow-wrap: anywhere; }
```

This is one layout choice, not a universal page width. Content can change through translation, user text size, missing images or long identifiers/URLs. A clipped box that matches one screenshot is not robust design. Avoid hiding overflow as the default “fix” for inaccessible content.

## Practice

In web-css, inspect content/padding/border dimensions, then change box-sizing in a private copy and explain the difference. Add a long unbroken heading, enlarge text and verify no horizontal page overflow. Explain where wrapping is appropriate and where data/code might instead need deliberate scrolling.

Transfer: add a long translated label and keep controls operable without fixed heights. Document the intended reading width, spacing scale and minimum control size as requirements, not magic constants.

Sources: [box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model), [values/units](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units).
