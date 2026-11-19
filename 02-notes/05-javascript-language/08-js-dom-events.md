---
created: 2026-10-08
updated: 2026-10-21
---

# 08 — DOM & Events (select, manipulate, forms)

> Prerequisites: [[17-html-css-and-browser-workflow]], objects/functions, basic async. Practice: `js-dom` in [[practice-catalog]]; Node model checks do not verify browser rendering or accessibility. Use a dedicated local practice page, not an arbitrary real site with private data.

## Outcomes

After this note you can: build a list + form with no framework; use one parent click listener for all current and future items (delegation); show loading/empty/error states; insert user text safely so injected HTML can't run as code.

Serve everything here over `http://localhost` (see [[00-js-how-to-use]] workflow) — never `file://`.

## Mental model
What the DOM is: the browser turns your HTML into a live tree of objects (elements). JS can find elements, change them, and listen for user actions. `querySelector('#id')` finds the first element matching a CSS selector. You change safe text with `textContent` and `createElement` — never build HTML with `innerHTML` from user input, because injected `<script>` or `onerror` code would run (XSS attack). Events (clicks, keys) bubble up from the child to parents, so one parent listener can handle all current and future children — that is called delegation.

Run in Chrome console (`Ctrl+Shift+J`) or a local folder served over `http://` (modules + fetch need it; plain `<script>` works on `file://`).

```html
<!-- index.html -->
<ul id="list"><li>one</li></ul>
<input id="in" placeholder="type + Enter">
<script type="module" src="./app.js"></script>
```

```js
// app.js
const list = document.querySelector('#list');
const li = document.createElement('li');
li.textContent = 'two'; // safe — not innerHTML
list.append(li);
console.log(list.children.length); // 2
```

## Select + modify
What each does: `querySelector` returns the first match (`querySelectorAll` returns all). `.value` / `.checked` are the live current form values (always read these, not `getAttribute('value')` which is only the initial HTML). `classList` adds/removes CSS classes. `dataset` reads `data-*` attributes.

```js
const el = document.querySelector('#in'); // first match; querySelectorAll for all
el.value = 'hi'; // property (live) — not getAttribute('value') (initial HTML)
el.classList.add('hot'); el.classList.toggle('hot', true);
el.setAttribute('data-id', '7'); console.log(el.dataset.id); // 7 — data-* API
el.style.color = 'red'; // inline style (prefer classes)
console.log(el.matches('#in'), el.closest('body') !== null); // true true
console.log(document.querySelectorAll('li').length); // static NodeList — [...nodes].map(...) to use array methods
```

## Events (bubble + delegate + options)
What happens: `addEventListener('click', fn)` runs `fn` when the event occurs. In the callback, `e.target` is where the event started, `e.currentTarget` is the element with the listener. `preventDefault()` blocks the built-in action (form reload, link navigation). `input` fires every keystroke (use for live search), `change` fires when the value is committed (use for settings).

```js
document.querySelector('#list').addEventListener('click', (e) => {
  if (e.target.matches('li')) console.log('clicked', e.target.textContent);
  // one listener handles present AND future <li>s — delegation
});
document.querySelector('#in').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') console.log('enter:', e.currentTarget.value);
  // e.target = where it happened, e.currentTarget = where listener sits
});
// e.preventDefault() stops default (form reload, link nav); stopPropagation() stops bubbling (rare).
// Options: { once: true } auto-removes; { passive: true } for scroll/touch perf; { capture: true } flips to capture phase.
// Cleanup: const fn = (e) => {}; el.addEventListener('click', fn); el.removeEventListener('click', fn);
// Events: input (every keystroke) vs change (committed on blur/Enter) — search uses input, settings use change.
// focus/blur don't bubble — use focusin/focusout for delegation.
```

```js
// Custom events — child → app communication without frameworks:
list.addEventListener('todo:toggle', (e) => console.log('toggled', e.detail.id));
list.dispatchEvent(new CustomEvent('todo:toggle', { bubbles: true, detail: { id: 7 } }));
```

## Forms (the Phase 1 exit) + validation API
What each does: `submit` fires when the form is sent. `e.preventDefault()` keeps the page from reloading. `form.checkValidity()` returns true/false for `required` / `minlength` rules, `form.reportValidity()` shows the built-in error bubbles. `new FormData(form)` collects values keyed by `name=`. `form.reset()` clears it.

```js
const form = document.createElement('form');
form.innerHTML = `<input name="todo" required minlength="2"><button>Add</button>`; // static template only — never user data
const input = form.querySelector('input');
form.addEventListener('submit', (e) => {
  e.preventDefault(); // stay on page
  if (!form.checkValidity()) { form.reportValidity(); return; } // native bubbles + :invalid styling
  const data = new FormData(form); // keyed by name=
  console.log(data.get('todo'));
  form.reset();
});
document.body.append(form);
// Custom rule: input.setCustomValidity('Already exists'); input.reportValidity(); — clear with setCustomValidity('')
// CSS: input:invalid { border-color: red } — free visual feedback.
```

Labels + a11y (non-negotiable for ship): every input gets `<label for="id">`, error text lives in `aria-live="polite"` region, Escape clears, focus returns to input after add.

## Render loop pattern (no framework) + efficient batching
The pattern redraws a list from state: clear the ul, construct nodes with textContent in a DocumentFragment, then append them together. A fragment groups DOM operations but does not guarantee exactly one paint/reflow or a performance win; browsers already batch work. Measure before claiming a speedup and preserve focus when replacing interactive nodes.

```js
const state = ['a', 'b'];
const render = () => {
  const ul = document.querySelector('#list');
  ul.textContent = ''; // clear
   const frag = document.createDocumentFragment(); // group construction; no paint-count guarantee
  for (const t of state) {
    const li = document.createElement('li');
    li.textContent = t; frag.append(li);
  }
  ul.append(frag);
};
// Alternative for static shells: const tpl = document.querySelector('#row-template'); tpl.content.cloneNode(true);
// Helpers: el.scrollIntoView({ block: 'nearest' }), matchMedia('(prefers-color-scheme: dark)').matches,
// getComputedStyle(el).color — read computed CSS; IntersectionObserver for lazy-load (see 09 patterns).
```

Always render three states: `loading` (skeleton/disable), `empty` ("No todos yet"), `error` (message + retry button). A list that only handles success is unfinished.

## Pitfalls
- `el.innerHTML += userInput` inserts user text as HTML, so `<img onerror=...>` runs as code (XSS attack) — use `textContent` + `createElement` for user strings.
- `querySelector` returns `null` when nothing matches, and `null.textContent` crashes — guard the result or use `?.`.
- `querySelectorAll` returns a `NodeList` (has `forEach`, no `map`) — convert with `[...nodes]` to use array methods.
- Forgetting `preventDefault()` on `submit` reloads the page and wipes state.
- `el.onclick = fn` replaces the old handler; `addEventListener` adds without replacing — always use the latter.
- `getAttribute('value')` reads only the initial HTML; `.value` reads the live current input — read `.value` / `.checked`.
- `change` fires late (on blur/commit) — use `input` for live search as the user types.

## Try it (only on your dedicated local practice page)
```js
document.body.style.outline = '2px solid red';
console.log(document.querySelectorAll('a').length);
const b = document.createElement('button'); b.textContent = 'hi'; document.body.append(b);
b.addEventListener('click', (e) => console.log('target:', e.target.tagName));
```

Node check (DOM-free logic only):
```bash
node -e 'const s=["a","b"]; console.log(s.map(t=>`<li>${t}</li>`).join(""))'
```

## Optional scratch drills (inside js-dom/work, served locally)
1. `list/` (`index.html`+`app.js`): `<ul>` + `<input>` + `<button>`; Enter/button appends `textContent` item, clears input, ignores empty. No `innerHTML` with input. Render empty-state text when list is empty.
2. `delegate/` : 3 initial `<li>` + click-delegation logging text; add items dynamically, prove new ones also log (delegation). Add `dblclick` to remove item via `.remove()`. Use `DocumentFragment` in render.
3. `ship/` — **validated todo page**: form with `required minlength=2` + `submit` handler (`preventDefault` + `checkValidity/reportValidity` + `FormData` + `reset`), `<label>`, `aria-live` error region, `CustomEvent('todo:add')` on success, loading/error/empty states. Show reload bug by commenting `preventDefault`.

## Break it
In `ship/`, replace one `li.textContent = value` with `li.innerHTML = value`, type `<img src=x onerror=alert(1)>` as a todo, observe execution. Revert to `textContent`, keep the payload as inert text. Log `innerHTML-user-input → XSS → textContent+createElement` in [[90-js-protips]].

## Check
1. `target` vs `currentTarget` in a delegated list?
2. Property vs attribute for `input.value` — which is live?
3. `input` vs `change`, and which validates with `reportValidity`?
Gate: kill `preventDefault`, submit, confirm reload bug; restore, confirm no reload + `:invalid` styling works.

## Related

- [[04-js-objects-prototypes|Objects]] (elements are objects)
- [[09-js-fetch-storage|Fetch & Storage]]
- [[14-js-strings-numbers-dates|Strings, Numbers, Dates]] (escape helper)

Sources: [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model), [events](https://developer.mozilla.org/en-US/docs/Web/API/Event), [constraint validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation). Browser/manual verification is recorded separately; see [[implementation-status]].
