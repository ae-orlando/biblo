import { test } from 'node:test';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const { parseCount } = await import(pathToFileURL(path.join(process.env.PRACTICE_TARGET, 'main.mjs')));

test('accepts complete decimal counts, whitespace and zero', () => {
  for (const [input, expected] of [['0', 0], [' 42\n', 42], ['007', 7], ['9007199254740991', Number.MAX_SAFE_INTEGER]]) {
    assert.equal(parseCount(input), expected);
  }
});
test('does not coerce objects, booleans, null or numbers', () => {
  for (const input of [null, undefined, 7, true, [], { toString: () => '7' }]) assert.throws(() => parseCount(input), TypeError);
});
test('rejects incomplete, negative, nonfinite and unsafe counts', () => {
  for (const input of ['', ' ', '42px', '-1', '+1', '1.2', '1e3', '0x10', 'Infinity', '9007199254740992', '１２']) {
    assert.throws(() => parseCount(input), RangeError, input);
  }
});
