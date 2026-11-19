import { visibleTodos, messageFor } from './ui.mjs';
const search = document.querySelector('#search');
const reload = document.querySelector('#reload');
const status = document.querySelector('#status');
const list = document.querySelector('#todos');
let todos = [], phase = 'loading', latest = 0;
function render() {
  const visible = phase === 'ready' ? visibleTodos(todos, search.value) : [];
  status.textContent = messageFor(phase, visible.length);
  list.replaceChildren();
  const fragment = document.createDocumentFragment();
  for (const todo of visible) {
    const li = document.createElement('li');
    li.textContent = `${todo.done ? 'Done: ' : ''}${todo.text}`;
    fragment.append(li);
  }
  list.append(fragment);
  list.setAttribute('aria-busy', String(phase === 'loading'));
  // Keep retry available: repeated loads are safe because of latest + abort.
}
let current;
async function load() {
  const mine = ++latest;
  current?.abort(); current = new AbortController();
  phase = 'loading'; render();
  try {
    const mode = new URL(location.href).searchParams.get('mode') ?? 'normal';
    const response = await fetch(`/api/todos?mode=${encodeURIComponent(mode)}`, {
      signal: AbortSignal.any([current.signal, AbortSignal.timeout(5000)]),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data) || data.some(todo => !todo || typeof todo.id !== 'string' || typeof todo.text !== 'string' || typeof todo.done !== 'boolean')) throw new TypeError('bad response');
    if (mine !== latest) return;
    todos = data; phase = 'ready';
  } catch {
    if (mine !== latest) return;
    phase = 'error';
  }
  render();
}
search.addEventListener('input', render);
search.addEventListener('keydown', event => {
  if (event.key === 'Escape') { search.value = ''; render(); }
});
reload.addEventListener('click', load);
load();
