# Reference: model checks are not browser checks

The reference separates search/messages from DOM work. Rendering creates elements with inert text, handles explicit phases and keeps a polite live region. Reloads abort older requests and use a latest-call guard; response data is validated before rendering.

Run model checks with `python3 90-tools/practice.py check js-dom --reference`. Inspect the page with `python3 90-tools/serve-dom.py --reference`. The browser checklist remains required and is not claimed as automatically verified. A full accessibility evaluation goes beyond the checklist.
