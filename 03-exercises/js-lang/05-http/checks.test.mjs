import { test } from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const { createServer } = await import(pathToFileURL(path.join(process.env.PRACTICE_TARGET, 'server.mjs')));

test('API validates bodies, implements CRUD, and survives malformed requests', async () => {
  const server = createServer(); server.listen(0, '127.0.0.1'); await once(server, 'listening');
  const base = `http://127.0.0.1:${server.address().port}`;
  const request = (url, options) => fetch(base + url, { ...options, signal: AbortSignal.timeout(3000) });
  const post = body => request('/api/todos', { method: 'POST', headers: { 'content-type': 'application/json' }, body });
  try {
    assert.deepEqual(await (await request('/api/todos')).json(), []);
    const response = await post('{"text":"  learn  "}');
    assert.equal(response.status, 201); assert.match(response.headers.get('content-type'), /application\/json/);
    const first = await response.json(); assert.equal(first.text, 'learn'); assert.equal(first.done, false); assert.equal(typeof first.id, 'string');
    const second = await (await post('{"text":"next"}')).json(); assert.notEqual(first.id, second.id);
    for (const body of ['{bad', '{}', 'null', '[]', '{"text":" "}', '{"text":5}']) assert.equal((await post(body)).status, 400, body);
    assert.equal((await post(JSON.stringify({ text: '😀'.repeat(400) }))).status, 413);
    assert.equal((await request('/api/todos', { method: 'POST', body: '{"text":"x"}', headers: { 'content-type': 'text/plain' } })).status, 415);
    const updated = await request(`/api/todos/${first.id}`, { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: '{"done":true}' });
    assert.equal(updated.status, 200); assert.equal((await updated.json()).done, true);
    assert.equal((await request(`/api/todos/${first.id}`, { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: '{"done":"yes"}' })).status, 400);
    assert.equal((await request(`/api/todos/${first.id}`, { method: 'DELETE' })).status, 204);
    assert.equal((await request(`/api/todos/${first.id}`, { method: 'DELETE' })).status, 404);
    assert.equal((await request('/unknown')).status, 404);
    assert.equal((await request('/api/todos', { method: 'PUT' })).status, 405);
    const remaining = await (await request('/api/todos')).json(); assert.equal(remaining.length, 1); assert.equal(remaining[0].id, second.id);
  } finally {
    const closed = once(server, 'close'); server.close(); server.closeAllConnections(); await closed;
  }
});
