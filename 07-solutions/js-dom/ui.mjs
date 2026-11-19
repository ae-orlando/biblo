export function visibleTodos(todos, query) {
  const needle = query.trim().toLowerCase();
  return todos.filter(todo => todo.text.toLowerCase().includes(needle));
}
export function messageFor(status, count) {
  if (status === 'loading') return 'Loading…';
  if (status === 'error') return 'Could not load todos. Retry.';
  return count === 0 ? 'No matching todos.' : `${count} todos.`;
}
