import { test } from 'node:test';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const { latestOnly, mapLimit } = await import(pathToFileURL(path.join(process.env.PRACTICE_TARGET, 'main.mjs')));
const deferred = () => Promise.withResolvers();

test('latest result wins without relying on elapsed-time comparisons', async () => {
  const first = deferred(), second = deferred();
  const search = latestOnly(q => q === 'a' ? first.promise : second.promise);
  const a = search('a'), ab = search('ab');
  second.resolve('AB'); assert.deepEqual(await ab, { applied: true, value: 'AB' });
  first.resolve('A'); assert.deepEqual(await a, { applied: false });
  const independent = latestOnly(async q => q);
  assert.deepEqual(await independent('x'), { applied: true, value: 'x' });
});
test('stale failures do not overwrite current state; current failures propagate', async () => {
  const old = deferred(); const search = latestOnly(q => q === 'old' ? old.promise : Promise.resolve(q));
  const pending = search('old'); await search('new'); old.reject(new Error('old failure'));
  assert.deepEqual(await pending, { applied: false });
  await assert.rejects(latestOnly(async () => { throw new Error('current failure'); })(), /current failure/);
});
test('bounds in-flight work and preserves input order', async () => {
  const gates = [deferred(), deferred(), deferred(), deferred()];
  const reachedTwo = deferred(), reachedThree = deferred();
  let active = 0, peak = 0, started = 0;
  const result = mapLimit([0, 1, 2, 3], 2, async i => {
    active++; peak = Math.max(peak, active); started++;
    if (started === 2) reachedTwo.resolve();
    if (started === 3) reachedThree.resolve();
    await gates[i].promise; active--; return i * 10;
  });
  await reachedTwo.promise; assert.equal(started, 2);
  gates[1].resolve(); await reachedThree.promise; assert.equal(started, 3);
  gates.forEach(g => g.resolve());
  assert.deepEqual(await result, [0, 10, 20, 30]); assert.equal(peak, 2);
});
test('empty input, invalid limits and failures are handled', async () => {
  assert.deepEqual(await mapLimit([], 3, x => x), []);
  for (const limit of [0, -1, 1.5, '2']) await assert.rejects(mapLimit([1], limit, x => x));
  await assert.rejects(mapLimit([1, 2, 3], 1, async () => { throw new Error('worker failed'); }), /worker failed/);
});
