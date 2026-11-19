import { test } from 'node:test';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const { visibleTodos, messageFor } = await import(pathToFileURL(path.join(process.env.PRACTICE_TARGET, 'ui.mjs')));
test('search matches literal text case-insensitively without mutating data', () => {
  const todos = Object.freeze([Object.freeze({ id: '1', text: 'Read SQL', done: false }), Object.freeze({ id: '2', text: '[literal]', done: true })]);
  assert.deepEqual(visibleTodos(todos, ' sql '), [todos[0]]);
  assert.deepEqual(visibleTodos(todos, '['), [todos[1]]);
  assert.deepEqual(visibleTodos(todos, ''), todos);
  assert.deepEqual(visibleTodos(todos, 'missing'), []);
});
test('status messages distinguish failure, loading, empty and results', () => {
  assert.equal(messageFor('loading', 0), 'Loading…');
  assert.equal(messageFor('error', 0), 'Could not load todos. Retry.');
  assert.equal(messageFor('ready', 0), 'No matching todos.');
  assert.equal(messageFor('ready', 2), '2 todos.');
});
// These tests deliberately do not claim to verify DOM rendering or accessibility.
