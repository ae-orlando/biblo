# HTML 02 — URLs, links and media

## Outcome

Resolve asset/navigation URLs correctly and provide useful link/media semantics. Prerequisite: document structure. Practice: web-html and the later independent page.

A URL is not a filesystem path. /styles.css refers to the current origin's root; styles.css is relative to the document/base URL; #main targets an element in the document. A route deeper in an application can therefore change a relative asset URL. Inspect Network rather than guessing that a missing stylesheet is a CSS selector problem.

```html
<a href="#main">Skip to content</a>
<img src="/schedule.svg" width="320" height="80" alt="">
```

In the lab the graphic is decorative because the schedule is already conveyed by a real table. Empty alt deliberately omits redundant decoration from the text alternative; an informative image needs a useful alternative conveying its purpose/content. A filename or “image of” repeated mechanically is not adequate judgment.

## Native navigation and resource behavior

Use an anchor with href for navigation and a button for an action. Link text should make its purpose understandable. Opening a new tab is a deliberate choice, not a requirement for every external link; if chosen, consider explicit rel="noopener" and communicate surprising behavior.

Supply dimensions/aspect ratio to reduce layout shifts. Responsive image sizing needs CSS and sometimes srcset/sizes/picture; do not download a giant image simply to shrink it visually. Video/audio need appropriate captions/transcripts and usable controls. The first lab avoids accounts, copyrighted external assets and remote media entirely.

## Practice and transfer

Explain why a root-relative lab asset works at its served origin but may need adjustment behind a path-prefixed deployment. Observe a missing asset's actual 404. Add an informative image to your own page with a justified alternative, then test narrow layout and image loading.

Do not serve the whole vault to make an asset URL work. Copy only deliberate public assets into the dedicated site's public/served boundary.

Sources: [links](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Creating_links), [images](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_images), [WAI images](https://www.w3.org/WAI/tutorials/images/).
