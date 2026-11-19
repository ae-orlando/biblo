# Neovim Diagnostics Workflow (Yoru)

Inline text is off: no `virtual_text`, no `underline`, no `virtual_lines`.
Errors and warnings show as gutter signs only. Hint/info tips are hidden
(severity floor = WARN).

## Find
| Key | Action |
| --- | ------ |
| `]e` / `[e` | next / previous **error** |
| `]w` / `[w` | next / previous **warning** |
| `]d` / `[d` | next / previous any diagnostic |
| `<leader>cd` | read full message for current line (float) |
| `<leader>ud` | toggle gutter signs on/off |

## Review
- `<leader>xx` — Trouble, all diagnostics (workspace)
- `<leader>xX` — Trouble, current buffer only
- `:lua vim.diagnostic.setloclist()` — location list (`:lnext` / `:lprev`)
- `K` — LSP hover on a symbol

## Fix
1. `]e` to jump to the next error
2. `<leader>cd` to read it
3. fix the code
4. `<leader>fl` — run linter manually (it no longer auto-runs)
5. `:w` — save so the LSP re-checks

## Notes
- Linting is manual-only now; automatic lint autocmds are disabled.
- Hint/info diagnostics are hidden by the `WARN` severity floor in
  `lua/plugins/lsp.lua`.
- `gi.repository` errors in Python are Pyright false positives (PyGObject
  is dynamic). Fix with `pip install pygobject-stubs` or `# type: ignore`.

## Quickfix vs Location list
Two similar-looking lists in Neovim — they are **not** interchangeable.

| List | Open with | Scope | Filled by |
| --- | --- | --- | --- |
| **Quickfix** | `:copen` | project / workspace | `:grep`, `:make`, `:vim`, some test runs |
| **Location** | `:lopen` | current window/buffer | `vim.diagnostic.setloclist()`, LSP |

- Diagnostics go to the **location list** (`:lopen`), not the quickfix list.
- `:copen` will look empty if nothing wrote to the quickfix list.
- Navigate quickfix: `:cnext` / `:cprev` / `:cfirst` / `:clast`
- Navigate location list: `:lnext` / `:lprev` / `:lfirst` / `:llast`

## Debugging (DAP)
Your DAP keymaps (all `<leader>d…`):

| Key | Action |
| --- | --- |
| `<leader>db` | toggle breakpoint |
| `<leader>dB` | conditional breakpoint |
| `<leader>dc` | continue / start |
| `<leader>dO` | step over |
| `<leader>di` | step into |
| `<leader>do` | step out |
| `<leader>du` | toggle Debug UI |
| `<leader>dr` | REPL |
| `<leader>dw` | hover (inspect variable) |
| `<leader>dt` | terminate |
| `<leader>td` | debug the nearest test |

Typical loop: `<leader>db` on a line → `<leader>dc` → `<leader>du` for the
UI → `<leader>dw` to inspect variables → `<leader>dt` when done.

### Does it work on all languages?
No. The keymaps are universal, but each language needs an adapter installed.
In this setup only **Python** (debugpy) and **JavaScript/TypeScript/Node/browser**
(js-debug-adapter) are wired up. Other languages need the corresponding
LazyVim `lang.*` extra added to `lazyvim.json` (which pulls the Mason adapter).

Testing (neotest) also reuses DAP via `<leader>td`.
