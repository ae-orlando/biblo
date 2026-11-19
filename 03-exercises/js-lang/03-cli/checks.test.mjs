import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
const script = path.join(process.env.PRACTICE_TARGET, 'main.mjs');
const run = (...args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8', timeout: 3000 });

test('help and usage have distinct exit/output contracts', () => {
  const help = run('--help'); assert.equal(help.status, 0); assert.match(help.stdout, /usage/i); assert.equal(help.stderr, '');
  for (const args of [[], ['one', 'two'], ['--unknown']]) {
    const result = run(...args); assert.equal(result.status, 2); assert.equal(result.stdout, ''); assert.match(result.stderr, /usage/i);
  }
});
test('reads a spaced path, validates records and handles I/O/JSON errors', async () => {
  const dir = await mkdtemp(path.join(process.env.TMPDIR, 'js-cli-'));
  try {
    const file = path.join(dir, 'some data.json');
    await writeFile(file, JSON.stringify([{ label: 'a', value: 2 }, { label: 'b', value: -0.5 }]));
    let result = run(file); assert.equal(result.status, 0); assert.equal(result.stderr, ''); assert.deepEqual(JSON.parse(result.stdout), { count: 2, total: 1.5 });
    for (const text of ['[]', '{}', '{bad', '[{"label":"x","value":null}]', '[{"label":"","value":1}]']) {
      await writeFile(file, text); result = run(file);
      if (text === '[]') { assert.equal(result.status, 0); assert.deepEqual(JSON.parse(result.stdout), { count: 0, total: 0 }); }
      else { assert.equal(result.status, 1); assert.equal(result.stdout, ''); assert.ok(result.stderr.length); }
    }
    result = run(path.join(dir, 'missing')); assert.equal(result.status, 1); assert.equal(result.stdout, ''); assert.match(result.stderr, /ENOENT|not found|missing/i);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
