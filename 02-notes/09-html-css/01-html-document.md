# HTML 01 — document structure and semantic meaning

## Outcome

Create a complete document, identify its parsed DOM and choose elements by meaning rather than visual appearance. No JavaScript framework is needed. Practice: the structure portion of web-html.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Local training page</title>
</head>
<body>
  <main><h1>Local training page</h1><p>Meaningful content goes here.</p></main>
</body>
</html>
```

The doctype requests standards mode; lang identifies the document language. Head metadata is not the main visible page; title identifies a browser tab/history entry. Body contains document content. The viewport declaration matters for mobile layout, but does not itself make a page responsive.

The browser parses markup into a DOM tree and can repair malformed markup. “It looks okay” does not prove the source expressed what you intended. Inspect both source and Elements; a malformed option tag can disappear from the actual select's options.

## Semantic structure

Use main for the primary content, nav for a meaningful navigation region, header/footer in their appropriate context, headings for an understandable hierarchy, lists for list relationships and tables for tabular data—not arbitrary layout. A section normally needs a meaningful theme/heading; div is a generic grouping element when no stronger meaning is appropriate.

One clear page-level h1 is this course's convention, not a theorem that every other heading pattern is syntactically impossible. Do not choose h4 solely because its default font is small; CSS controls appearance.

Attributes belong in valid syntax, IDs should be unique, and void elements such as input/img do not have ordinary closing tags. Escape text that would otherwise be interpreted as markup. Semantic elements/native controls provide useful behavior and accessibility information; random nested divs do not automatically supply it.

## Practice and retrieval

Create the web-html page's main content, heading structure and data table with caption/scoped headers. Predict its tree before inspecting Elements. Introduce a malformed tag in a private copy, compare source/DOM, then repair the cause. Explain which structure remains understandable without CSS.

Source: [MDN document structure](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents), [HTML semantics](https://html.spec.whatwg.org/multipage/semantics.html).
