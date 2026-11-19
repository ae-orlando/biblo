---
created: 2026-10-08
updated: 2026-10-21
---

# Practical JavaScript session workflow

Choose your level through [[baseline-diagnostic]], not an assumed biography. Your editor is optional; the same loop works in Neovim, VS Code or another tool. Follow [[00-js-how-to-use]] for prerequisites and real lab locations.

## Setup (once, 15 min)

```bash
node -v   # want v24.x
python3 90-tools/practice.py doctor
python3 90-tools/practice.py start js-values
```

An optional Neovim mapping for your own configuration (not installed by the rebuild) must quote filenames safely. A terminal invocation is enough; there is no requirement to modify editor configuration:

```lua
-- Optional personal setup, not a course prerequisite.
-- Prefer the lab check command in a terminal; node --check is syntax-only.
```

That is 90% of your tooling. No extensions, no debugger, no bundler.

## Where things live

- Concepts: `02-notes/05-javascript-language/` (what you read).
- Your code: the `work/` directory created by the launcher for a lab in [[practice-catalog]]. Lesson numbers and lab numbers need not match.
- Gotcha log: `90-js-protips.md` (one line per bug you hit).

Keep attempts separate from supplied starter/reference code. Improve concept notes when you discover and verify a correction; preserve actual learning history rather than treating notes as untouchable.

## Session loop (30-60 min blocks, one block = one section)

1. **Read (10 min):** open the note, read the `Outcomes` box first, then the code. Don't copy-paste yet.
2. **Try (5 min):** type one `Try it` line into the terminal yourself:
   ```bash
   node -e 'console.log(typeof null)'
   ```
   Typing matters. Copy-paste doesn't stick.
3. **Build:** edit the created lab implementation, for example `03-exercises/js-lang/01-values/work/main.mjs`, in your chosen editor. Run `python3 90-tools/practice.py check js-values` from the vault root.
4. **Break:** introduce one representative bug and show the test catches it, then repair it.
5. **Stop rule:** record the actual check result and a concrete next action. node --check alone is not “running green”; honest unfinished work is better than a fabricated success.

## How you view outputs

- **Node scripts:** the terminal is the screen. `console.log` prints to stdout.
  ```bash
  node ship.mjs hello   # normal output
  echo $?               # exit code: 0 = ok, 1 = misuse/error
  node bad.mjs; echo $? # always check the code on errors
  ```
  Inside nvim: `:terminal` opens a shell split, or `<leader>r` runs the current file and shows output below.
- **Browser pages (notes 08-09):** the page is the screen, `F12` is the terminal.
  ```bash
   python3 90-tools/serve-dom.py
   # open the printed loopback URL; use the lab's browser checklist
  ```
  `console.log` in `app.js` appears in the Console tab. Network tab shows each `fetch` + its status.
- **Servers (notes 11, 13):** two terminals. T1 runs, T2 asks:
  ```bash
   python3 90-tools/practice.py check js-http
  ```
  `-i` shows status + headers (without it you can't tell 200 from 404).

## How to read an error (message plus relevant stack/context)

```
SyntaxError: Unexpected token '}'      <- line 1: WHAT broke
    at file:///home/.../ship.mjs:7:3  <- last line: WHERE (file:line:col)
```

- `SyntaxError` = never ran → run `node --check file.mjs`, fix the line:col.
- `ReferenceError/TypeError` = ran, died mid-way → open that line in nvim.
- Nothing printed + `echo $?` = `1` → your `exitCode` path fired; check your usage message.
- Red in Chrome Console = same: first line what, stack link where (click it).

## Deliberate bugs (the Break it habit, with example)

Point: cause each classic bug once on purpose so you recognize it later in 5 seconds instead of 50 minutes.

Worked example (note 05, `sort` mutates):

```bash
cd 03-exercises/js-lang/02-data/work
nvim dedupe.mjs   # confirm it uses toSorted and prints source unchanged
node dedupe.mjs   # GREEN baseline: source after: [10,9,2]
```

Break it (one line in nvim):

```js
// const fixed = [...arr].toSorted((a, b) => a - b);
const fixed = arr.sort((a, b) => a - b); // BUG on purpose
```

```bash
node dedupe.mjs   # RED: source after: [2,9,10] — original mutated
```

Fix it: undo the line, re-run green. Log one line in `90-js-protips.md`:

```
2026-10-08 — sort mutated state → in-place → toSorted for UI
```

Same shape every time: green → one-line bug → run → read output → undo → green → log. Never break two things at once.

## When stuck (15-min rule)

1. Re-read the error's first + last line (above).
2. Shrink the file to 5 lines that still break. Most bugs vanish here.
3. Compare the actual contract, inputs and failing assertion; do not blindly imitate a snippet with a different environment or purpose.
4. Record the minimal reproducer, exact error and attempted hypothesis. Ask a focused question or review a missing prerequisite; do not skip a dependency merely to tick off another Build. Timeboxes are optional aids, not advancement gates.

## Glossary (words notes assume)

- `stdout/stderr`: normal output vs error output. Usage help goes to `stderr`.
- `exit code`: number a program returns; `0` ok, `1` misuse.
- `REPL`: `node` with no file — type a line, see the answer, `Ctrl+D` exits.
- `lint/check`: `node --check file.mjs` = syntax only, doesn't run.
- `server/client`: server waits (your `node server.mjs`), client asks (`curl`, browser, `fetch`).

## Related


- [[00-js-how-to-use|How to Use]] (track order + rules)
- [[90-js-protips|JS Protips]] (your bug log)

For current commands, use [[practice-catalog]] and [[study-and-review]]. Old illustrative scratch filenames in this note are self-authored examples, not already-created files. Serve only a dedicated lab directory, never the vault root.
