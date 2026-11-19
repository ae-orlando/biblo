import http from 'node:http';
import { randomUUID } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

function readBody(req) {
  return new Promise((resolve, reject) => {
    let bytes = 0, failed = false;
    const chunks = [];
    req.on('data', chunk => {
      bytes += chunk.length;
      if (bytes > 1024) {
        if (!failed) { failed = true; chunks.length = 0; reject(Object.assign(new Error('body too large'), { status: 413 })); }
      } else if (!failed) chunks.push(chunk);
    });
    req.on('end', () => {
      if (failed) return;
      try { resolve(JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(Buffer.concat(chunks)))); }
      catch { reject(Object.assign(new Error('invalid JSON'), { status: 400 })); }
    });
    req.on('error', reject);
    req.on('aborted', () => reject(new Error('request aborted')));
  });
}

export function createServer() {
  const todos = new Map();
  return http.createServer(async (req, res) => {
    const send = (status, value) => {
      if (res.destroyed || res.writableEnded) return;
      res.writeHead(status, { 'content-type': 'application/json; charset=utf-8', 'x-content-type-options': 'nosniff' });
      res.end(status === 204 ? undefined : JSON.stringify(value));
    };
    try {
      const url = new URL(req.url, 'http://localhost');
      const collection = url.pathname === '/api/todos';
      const match = /^\/api\/todos\/([^/]+)$/.exec(url.pathname);
      if (!collection && !match) return send(404, { error: 'not found' });
      if (collection && req.method === 'GET') return send(200, [...todos.values()]);
      const allowed = collection ? ['GET', 'POST'] : ['PATCH', 'DELETE'];
      if (!allowed.includes(req.method)) { res.setHeader('Allow', allowed.join(', ')); return send(405, { error: 'method not allowed' }); }
      if (match && !todos.has(match[1])) return send(404, { error: 'not found' });
      if (match && req.method === 'DELETE') { todos.delete(match[1]); return send(204); }
      if ((req.headers['content-type'] ?? '').split(';')[0].trim().toLowerCase() !== 'application/json') return send(415, { error: 'expected application/json' });
      const data = await readBody(req);
      if (!data || typeof data !== 'object' || Array.isArray(data)) return send(400, { error: 'expected object' });
      if (collection) {
        if (typeof data.text !== 'string' || !data.text.trim()) return send(400, { error: 'text required' });
        const todo = { id: randomUUID(), text: data.text.trim(), done: false };
        todos.set(todo.id, todo); return send(201, todo);
      }
      if (typeof data.done !== 'boolean') return send(400, { error: 'done must be boolean' });
      const todo = { ...todos.get(match[1]), done: data.done };
      todos.set(todo.id, todo); return send(200, todo);
    } catch (error) {
      send(error.status ?? 500, { error: error.status ? error.message : 'internal error' });
    }
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  createServer().listen(3000, '127.0.0.1', () => console.log('Local learning API: http://127.0.0.1:3000/api/todos'));
}
