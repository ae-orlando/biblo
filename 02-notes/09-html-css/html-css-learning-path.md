# HTML and CSS learning path — the browser platform first

This is a dedicated foundations course, not a Tailwind/Vite setup guide. It is available now, but your immediate focus can remain Python. Study one new major track at a time; use this as the later frontend stage toward fullstack engineering.

## Sequence and practice

| Unit | Read | Evidence |
| --- | --- | --- |
| Document and assets | [[01-html-document]], [[02-html-links-media]] | Explain source versus DOM, semantic structure and asset URLs |
| Forms and access | [[03-html-forms]], [[04-html-accessibility]] | `web-html`: labels, native validation, keyboard entry and actual local POST |
| CSS reasoning | [[05-css-cascade]], [[06-css-box-model]] | Diagnose which rule/value/box actually controls a result |
| Layout and adaptation | [[07-css-layout]], [[08-css-responsive]] | `web-css`: computed one/two/three-column layout, wrapping and text enlargement |
| Diagnose and integrate | [[09-browser-debugging]], [[10-web-foundations-capstone]] | Independent page/change request; later connect behavior through JavaScript/API contracts |

The labs have supplied starters, real Chromium checks, hints and separate references. The checks do not replace manual accessibility, visual/design or assistive-technology evaluation.

```bash
python3 90-tools/practice.py start web-html
python3 90-tools/practice.py check web-html
python3 90-tools/serve-web.py web-html
```

Open the printed loopback URL; Ctrl-C stops the server. It exposes only the selected exercise assets and a fake form-preview endpoint, not the vault. Use fake names/addresses only. Browser checks need the marked browser environment and an existing Chromium executable; Python's beginner labs do not.

## Assessment

Build from a brief instead of matching a screenshot alone. Explain semantic choices, keyboard behavior, validation boundaries, cascade decisions, sizing and responsive failure cases. Change content/requirements, then verify again. A static linter cannot establish responsive geometry; a browser layout check cannot establish all accessibility.

Continue into [[00-js-how-to-use]] for browser state/events and API clients. A framework follows platform understanding, not the other way around. See [[web-app-structure]] for a static site versus integrated frontend/backend layout.

Sources: [MDN web learning](https://developer.mozilla.org/en-US/docs/Learn_web_development), [HTML standard](https://html.spec.whatwg.org/), [WAI tutorials](https://www.w3.org/WAI/tutorials/).
