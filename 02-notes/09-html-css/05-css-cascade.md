# CSS 05 — selectors, cascade, inheritance and computed values

## Outcome

Explain why a declaration wins instead of adding increasingly strong selectors until a page changes. Prerequisite: basic HTML/DOM. Practice: web-css, with deliberate rule conflicts in a private copy.

CSS matches selectors to elements and resolves competing declarations. “Last rule wins” applies only after relevant cascade factors tie; origin, importance/layers, specificity and ordering all matter. Inheritance is different: some properties can inherit from an ancestor when not otherwise specified. Margin does not inherit merely because color does.

```css
.card { color: #0f172a; }
.card h2 { font-size: 1.25rem; }
.card:focus-within { border-color: #155e75; }
```

An element selector matches a tag, .class a class and #id an ID. Combinators express relationships. Pseudo-classes select states/conditions; pseudo-elements address generated/particular content. Keep selectors as local and understandable as the responsibility requires; an ID and !important everywhere is not a sustainable component strategy.

## Inspect what the browser did

DevTools Styles shows matched/overridden rules; Computed shows resolved values. A crossed-out declaration may lose the cascade; an unknown/invalid property can be ignored; a missing stylesheet may never have loaded. Distinguish these causes before editing specificity.

Custom properties can name repeated design decisions such as spacing/colors. They participate in the cascade; they are not a separate universal global configuration system. Avoid building a token framework before the page actually has repeated decisions worth naming.

## Practice and retrieval

In web-css, set a body text color, then override a card heading with a local rule. Predict inheritance and the winning value; inspect it. Introduce an equally specific later rule, then a more specific rule and explain the result without resorting immediately to !important.

Transfer: extract a repeated component style and preserve its focus/error states. Explain why changing DOM structure can change a descendant selector's match and why a computed value may differ from the literal unit/value written in source.

Sources: [cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Cascade), [specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity), [inheritance](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Inheritance).
