import { test } from 'node:test';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const { summarizeOrders } = await import(pathToFileURL(path.join(process.env.PRACTICE_TARGET, 'main.mjs')));
const order = (id, user, cents, status = 'paid') => ({ id, user, cents, status });

test('groups paid orders, sorts users, preserves input and ignores cancelled totals', () => {
  const input = [order('1', 'Ben', 200), order('2', 'Ana', 90), order('3', 'Ben', 25), order('4', 'Z', 99, 'cancelled')];
  const before = structuredClone(input);
  input.forEach(Object.freeze); Object.freeze(input);
  assert.deepEqual(summarizeOrders(input), [{ user: 'Ana', count: 1, cents: 90 }, { user: 'Ben', count: 2, cents: 225 }]);
  assert.deepEqual(input, before);
  assert.deepEqual(summarizeOrders([]), []);
});
test('handles dictionary-like keys and independent calls', () => {
  assert.deepEqual(summarizeOrders([order('x', '__proto__', 0)]), [{ user: '__proto__', count: 1, cents: 0 }]);
  assert.deepEqual(summarizeOrders([order('y', 'other', 5)]), [{ user: 'other', count: 1, cents: 5 }]);
});
test('rejects malformed records, duplicate IDs and overflow', () => {
  for (const input of [null, {}, [null], [order('', 'A', 1)], [order('a', '', 1)], [order('a', 'A', -1)], [order('a', 'A', 1.1)], [order('a', 'A', '1')], [order('a', 'A', Infinity)], [order('a', 'A', 1, 'other')], [order('a', 'A', 1), order('a', 'B', 2, 'cancelled')], [order('a', 'A', Number.MAX_SAFE_INTEGER), order('b', 'A', 1)]]) {
    assert.throws(() => summarizeOrders(input));
  }
});
