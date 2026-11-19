# Browser 09 — inspect evidence instead of guessing

## Outcome

Use source, DOM, computed styles, layout, validation and network observations to narrow a browser problem. Apply to both web labs and later JavaScript/API integration.

## A diagnostic sequence

1. Reproduce the exact viewport, input and action. Preserve the actual symptom.
2. Network: did the document/stylesheet/image/API request use the intended URL, succeed and have a suitable content type? A 404 asset is not fixed with more specificity.
3. Elements: does the parsed DOM contain the element/option/relationship you intended? Browsers repair malformed HTML; source text and DOM can differ.
4. Styles/Computed: did the selector match, did the declaration lose/parse incorrectly, or did a different sizing constraint dominate?
5. Layout: identify the overflowing box and its content/padding/track/minimum sizes.
6. Interaction: inspect native validity, submitted names, current focus and keyboard operation.
7. For later scripts, inspect Console and request/response/state transitions instead of treating every fetch failure as CORS.

Make one discriminating observation before changing several unrelated things. Confirm the repair and a nearby regression case at another size/input.

## Practice

Deliberately break one option tag, one asset URL, one label association and one layout constraint in separate private copies. Predict which observation exposes each defect. The lab reference itself had a malformed option caught by real Chromium testing during authoring; preserving that lesson is more useful than assuming generated source is correct.

Automated browser checks verify selected interactions and computed properties, not every aesthetic or accessibility judgment. Run the actual page through the local restricted server, use fake data and record manual evidence. No browser-extension collection or cloud audit is required.

Transfer: diagnose a page that looks correct but submits no email, and another that looks broken because the CSS request returned HTML. Explain the failed layer without random fixes.

Sources: [Chrome DevTools](https://developer.chrome.com/docs/devtools/), [Firefox DevTools](https://firefox-source-docs.mozilla.org/devtools-user/).
