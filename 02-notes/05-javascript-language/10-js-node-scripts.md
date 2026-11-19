---
created: 2026-10-08
updated: 2026-10-21
---

# 10 — Node Scripts (`fs`, `argv`, `npm`)

> Prerequisites: [[06-js-destructuring-modules]], [[12-js-errors-regex]]. Practice: `js-cli` in [[practice-catalog]]. Starter, fixture, test and learner paths are all vault-local; no npm dependency is needed for the bundled labs.

## Outcomes

After this note you can: write a command-line tool that reads `--flags`, prints `--help`, and exits `0` on success / `1` on misuse; read/write files and stream huge files without loading them fully; send/listen to named events; run a test file with `node --test`.

## Mental model
What Node is: JS running outside the browser, with OS access. `node:fs` reads/writes files, `node:path` builds file paths, `process` gives arguments (`process.argv`), current folder (`process.cwd`), and environment variables (`process.env`). Browser-only names (`window`, `document`, `localStorage`) do not exist here. Always `import` from `'node:...'` — the `node:` prefix guarantees the built-in version.

```js
// info.mjs
console.log(process.argv); // [node, file, ...args]
console.log(process.cwd()); // where launched
console.log(import.meta.url); // file://... — ESM file URL
```

```bash
node info.mjs hello --out=x
```

## Files (`node:fs/promises` + `node:path`)
What each does: `writeFile(path, text)` creates/overwrites a file. `readFile(path, 'utf8')` reads it as text (without `'utf8'` you get a raw `Buffer`). `mkdir(name, { recursive: true })` creates folders. For huge files, stream chunk-by-chunk instead of `readFile` so you don't run out of memory.

```js
import fs from 'node:fs/promises';
import path from 'node:path';
const file = path.join(process.cwd(), 'data.json');
await fs.writeFile(file, JSON.stringify({ n: 1 }, null, 2) + '\n');
console.log(await fs.readFile(file, 'utf8'));
await fs.mkdir('out', { recursive: true }); // no error if exists
console.log(path.basename(file), path.extname(file)); // data.json .json
// Big files: stream, don't readFile (RAM):
// import { createReadStream } from 'node:fs'; for await (const chunk of createReadStream(file, 'utf8')) process.stdout.write(chunk);
```

## Args (no lib needed for small CLIs)
What it is: `process.argv` is an array `[nodePath, filePath, ...yourArgs]`. `.slice(2)` drops the first two so you keep only your args. Below, `get('--name', 'anon')` finds the flag and returns the next item, or the default. `--help` prints usage and exits `0`; missing args print usage to `stderr` and set `exitCode 1`.

```js
// args.mjs: node args.mjs --name orl --count 3
const args = process.argv.slice(2);
const get = (flag, dflt) => {
  const i = args.indexOf(flag);
  return i === -1 ? dflt : (args[i + 1] ?? dflt);
};
console.log(get('--name', 'anon'), Number(get('--count', '1')));
if (args.includes('--help')) { console.log('usage: node args.mjs --name <n> --count <k>'); process.exitCode = 0; }
else if (!args.length) { console.error('usage: node args.mjs --name <n>'); process.exitCode = 1; }
```

`process.exitCode = 1` over `process.exit(1)` — lets pending IO flush. Listen for `process.on('SIGINT', cleanup)` in long-runners.

## Events (the DOM analogy on the server)
What it does: `EventEmitter` is a message bus. `.on('name', fn)` subscribes a listener, `.emit('name', data)` calls all listeners with `data`. Same idea as `addEventListener` / `dispatchEvent` in the browser, but for server code.

```js
import { EventEmitter } from 'node:events';
const bus = new EventEmitter();
bus.on('todo:add', (t) => console.log('added', t));
bus.emit('todo:add', { id: 1 });
// Same shape as addEventListener/dispatchEvent — one listener fans out to many subscribers.
```

## `npm` minimal (only what Phase 2 needs)

```bash
npm init -y
npm i zod          # dep
npm i -D vitest    # dev-dep (Phase 4+) — or zero-dep: node --test (built-in runner, Node 20+)
npx --no-install tsc --init  # only if TypeScript is already a chosen local dependency
node --run test    # Node's own script runner (Node 22+), not an npm-version feature
node --watch server.mjs  # rerun on save
node --env-file=.env server.mjs  # load .env without dotenv (Node 20.6+)
```

`package.json` `{ "type": "module" }` makes `.js` ESM; without it use `.mjs` (this track uses `.mjs` always, no config needed).

Zero-dep test:
```js
// sum.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
test('adds', () => assert.equal(1 + 1, 2));
```
```bash
node --test sum.test.mjs
```

## Env + stdin/out
What they are: `process.env.NAME` reads an environment variable (set with `NAME=value node file.mjs` or a `.env` file with `--env-file`). `process.stdin` is piped input, `process.stdout` is normal output — `echo hi | node echo.mjs` feeds `hi` into the script.

```js
console.log(process.env.HOME ?? 'no-home'); // env
// HOME=x node env.mjs — or .env + --env-file
for await (const line of process.stdin) { process.stdout.write(`echo:${line}`); break; }
// echo hi | node echo.mjs
```

## Pitfalls
- `readFile(path)` without `'utf8'` returns a raw `Buffer` (bytes), not text — pass `'utf8'` or call `buf.toString()`.
- In ESM, use Node's supported import.meta path properties or fileURLToPath from node:url. A URL's .pathname is not a general filesystem conversion: encoded spaces and platform-specific paths need proper conversion.
- `readFileSync` inside a server blocks all requests while it reads — use `await` with `node:fs/promises`, except one-shot CLI startup.
- `require(...)` in `.mjs` throws — use `import` (this track is ESM-only).
- Forgetting `await` on `writeFile` then exiting truncates the file — top-level `await` works in `.mjs`, so await it.
- `readFile` on a 1GB log loads it all into RAM and crashes — stream huge files chunk by chunk.

## Try it
```bash
mkdir -p .practice-runtime/scratch
node --input-type=module -e 'import fs from "node:fs/promises"; const p=".practice-runtime/scratch/t.txt"; await fs.writeFile(p,"hi\n"); console.log(await fs.readFile(p,"utf8"));'
node -e 'console.log(process.argv.slice(1))' hello --out=x
HOME=x node -e 'console.log(process.env.HOME)'
python3 90-tools/practice.py check js-cli
```

## Optional scratch drills (inside js-cli/work)
1. `cat.mjs`: `readFile(argv[2], 'utf8')` → stdout; missing arg → `stderr` usage + `exitCode 1`; missing file → catch `ENOENT`, friendly message, `exitCode 1`. Add `--help`.
2. `upper.mjs`: read file, write `out.txt` uppercased + `\n`; use `path.join(cwd, ...)`, `mkdir --recursive`. Prove `await` ordering (read before write finishes). Bonus: streaming variant with `createReadStream` for a 100MB file.
3. `ship.mjs` — **args + events CLI**: `--name --count` parser + `--help`; emits `run:start/run:done` on an `EventEmitter`; `HOME` override demo; `npm init -y` in folder + `node --run` script entry + one `node:test` assertion file.

## Break it
Compare console.log(buffer) with process.stdout.write(buffer): the former displays a Buffer representation; the latter writes raw bytes. Omitting utf8 does not necessarily corrupt a cat-like tool, because byte-preserving output can be appropriate. State whether your tool's contract is bytes or decoded text, then test it.

## Check
1. `exitCode` vs `exit()` — which flushes IO?
2. `readFile` vs stream — where's the cutoff?
3. `EventEmitter.on/emit` maps to which DOM pair?
Gate: `cat.mjs` missing-file prints friendly `ENOENT` line and exits `1`.

## Related

- [[06-js-destructuring-modules|Destructuring & Modules]]
- [[11-js-node-http|Node HTTP]]

Sources: [Node fs](https://nodejs.org/docs/latest-v24.x/api/fs.html), [ESM](https://nodejs.org/docs/latest-v24.x/api/esm.html), [test runner](https://nodejs.org/docs/latest-v24.x/api/test.html), [CLI](https://nodejs.org/docs/latest-v24.x/api/cli.html). npx may otherwise download packages; do not treat it as automatically local-only. Lab verification: [[implementation-status]].
