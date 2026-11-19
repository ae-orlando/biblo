# HTML, CSS and browser workflow bridge

> Expanded foundations now live in [[html-css-learning-path]]. This compact bridge remains a reference; it is not a substitute for the new semantic/forms/cascade/layout lessons and real-browser exercises.

## Outcome and prerequisites

Before [[08-js-dom-events]], create a small semantic document and inspect how scripts, styles and network requests affect it. You need functions/objects and [[00-web-foundations]], not React, Vite or Tailwind.

## Structure before behavior

HTML defines document semantics and native controls. A label identifies a form input; a button has keyboard behavior that a clickable div does not supply automatically. CSS controls presentation, layout and responsive behavior; JavaScript coordinates state and effects. Use native controls before rebuilding their behavior with event handlers.

```html
<form id="add">
  <label for="todo">Todo text</label>
  <input id="todo" name="text" required minlength="2">
  <button type="submit">Add</button>
</form>
<p id="status" role="status" aria-live="polite"></p>
<ul id="todos"></ul>
<script type="module" src="./app.mjs"></script>
```

This is a fragment, not a complete page or application. Use the js-dom starter for a complete served document. Client validation improves feedback; the server still validates untrusted requests.

## Layout and inspection

Understand the box model, cascade/specificity, inherited properties, normal flow, flex/grid and viewport constraints. Start with a readable single column, visible focus and controls that remain usable without a pointer. Do not infer accessibility from a Lighthouse score alone.

Serve only the selected lab with `python3 90-tools/serve-dom.py`; open its printed loopback URL. Inspect Elements for the actual DOM, Console for errors, Network for asset/API status and request/response headers. A missing module asset is not fixed by changing a CSS selector.

## Concrete practice

In `js-dom/work/`, implement the lab's model and browser contract. Add a stylesheet that keeps a clear label/control relationship, readable widths and visible keyboard focus. Check narrow/wide viewports, keyboard navigation, literal injection payload and loading/error/empty modes. Record which behaviors were observed and which assistive-technology checks remain unperformed.

Transfer: add a form to the HTTP capstone, define its server error display and preserve typed input after validation failure. Explain document loading, module fetching, event handling and response rendering without a framework.

Sources: [MDN HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content), [CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics), [forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms), [WAI forms](https://www.w3.org/WAI/tutorials/forms/).
