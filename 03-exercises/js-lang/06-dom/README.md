# Lab: accessible client with explicit UI states

**ID:** `js-dom` · Modern browser + Node 24 for model tests · Outcome: show usable failure/empty/loading states and render untrusted text safely.

Prerequisites: [[08-js-dom-events]], [[09-js-fetch-storage]], [[17-html-css-and-browser-workflow]]. This is a read-only client lab; CRUD integration belongs in the capstone.

## Contract

Implement `work/ui.mjs`:
- `visibleTodos(todos,query)`: case-insensitive literal search after trimming query; return matching records without mutation.
- `messageFor(status,count)`: `loading` → `Loading…`; `error` → `Could not load todos. Retry.`; `ready` with zero → `No matching todos.`; otherwise `${count} todos.`

Implement `work/app.mjs`: fetch `/api/todos`, validate the response, bound waiting, show status, render through textContent/createElement, support search, Escape-to-clear and retry. Keep labels and a polite status region. Stale requests must not overwrite current state.

```bash
python3 90-tools/practice.py start js-dom
python3 90-tools/practice.py check js-dom
python3 90-tools/serve-dom.py
```

Open `http://127.0.0.1:8000/`. The server exposes only selected exercise assets and fake API data, not your vault. Ctrl-C stops it.

## Required browser checklist — not covered by Node tests

- Normal list renders; the `<img ...>` fixture appears as literal text and executes nothing.
- Search `sql`, `[`, and an absent value; clear with Escape.
- Open `/?mode=slow`: observe loading. `/?mode=empty`: observe empty state. `/?mode=error`: observe failure and retry affordance.
- Use keyboard only; labels identify inputs, focus remains usable, status changes are announced by an assistive-technology check where available.
- Rapid retries cannot restore stale results; Network/Console show no unexplained errors.

Record actual results in `work/browser-evidence.md`. Green model tests alone do **not** complete this lab. Extend with a validated add form and API integration after the HTTP lab.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/js-dom/explanation.md) · [DOM introduction](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
