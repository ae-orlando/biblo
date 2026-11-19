# Original fullstack roadmap — historical reference

Archived on 2026-10-20. This preserves the earlier phase/time estimates and workspace rules; they are not the current learning contract. Follow [[master-plan]] and [[learning-system]] instead.

## Current Phase
Phase 0: Browser console fundamentals

## Phases

- [ ] **Phase 0** — JS in the browser console (weeks 1–2)
  - Goal: variables, loops, functions in console, no tools.
  - Exit: 10 exercises as code files in `~/learning/phase-0/`, no Obsidian per-exercise notes.
  - Notes: [[index|Notes Index]], [[00-js-how-to-use|How to Use JS Track]], [[01-js-values-types|Values & Types]], [[02-js-control-flow|Control Flow]], [[03-js-functions-scope|Functions & Scope]], [[12-js-errors-regex|Errors & Regex]]

- [ ] **Phase 1** — HTML + CSS + DOM, no tools (weeks 3–4)
  - Goal: static page + DOM manipulation by hand.
  - Exit: build a page with form + list, no framework.
  - Notes: [[00-web-foundations|Web Foundations]], [[04-js-objects-prototypes|Objects & Prototypes]], [[05-js-arrays-iterables|Arrays]], [[08-js-dom-events|DOM & Events]], [[09-js-fetch-storage|Fetch & Storage]]

- [ ] **Phase 2** — Node.js, plain scripts (weeks 5–6)
  - Goal: run JS outside browser, files + modules.
  - Exit: CLI script that reads/writes a file.
  - Notes: [[10-node-installation|Node Installation]], [[06-js-destructuring-modules|Destructuring & Modules]], [[10-js-node-scripts|Node Scripts]]

- [ ] **Phase 3** — Node `http` server, no framework (weeks 7–8)
  - Goal: understand request/response without magic.
  - Exit: JSON API with 2 routes using only `http`.
  - Notes: [[00-web-foundations|Web Foundations]], [[07-js-async-event-loop|Async & Event Loop]], [[11-js-node-http|Node HTTP]]

- [ ] **Phase 4** — Express (weeks 9–10)
  - Goal: routing, middleware.
  - Exit: same API rebuilt in Express, code in `~/learning/`.

- [ ] **Phase 5** — Vite + React + TS (week 11+)
  - Goal: components, props, state.
  - Exit: `my-app` renders list from mock API.
  - Parked until Phase 5:
    - [[20-vite|Vite]]
    - [[30-tailwind-css-integration-to-vite|Tailwind CSS Integration]]

- [ ] **Phase 6** — SQLite, then Postgres
  - Goal: persistence, queries, indexes.
  - Exit: API backed by SQLite file, then Postgres.
  - Notes: [[00-web-foundations|Web Foundations]] (Databases vs Files), [[00-postgres-introduction|Postgres Intro]], [[01-psql-workflow|psql Workflow]]
  - Project: [[nies-auth-platform|Nies Auth Platform]] — Django + Postgres skill-up guide, 6-week plan

- [ ] **Phase 1.5** — Linux CLI wizard on Arch (parallel track)
  - Goal: fluent terminal, no GUI crutch.
  - Exit: navigate blind, pipes+grep, fix perms, pacman+AUR, systemctl service, 20+ entries in protips.
  - Notes: [[00-linux-introduction|Linux Introduction]], [[90-linux-protips|Linux Protips]]

- [ ] **Phase 1.6** — Bash scripting + Arch automation (parallel track)
  - Goal: robust `install.sh` with dry-run, idempotent pacman/AUR/stow/systemd.
  - Exit: `04-projects/hyprland-installer` spec implemented, VM-tested, 10+ bash protips.
  - Notes: [[00-bash-basics|Bash Basics]], [[20-arch-automation|Arch Automation]], [[90-bash-protips|Bash Protips]]

- [ ] **Phase 1.7** — Bash as a language (course track, no automation yet)
  - Goal: understand bash itself — expansions, `${}`, arrays, conditionals, functions/scope, redirections, traps.
  - Exit: `13-bash-capstone` `report.sh` built clean (`bash -n` + `shellcheck`), exercises in `03-exercises/bash-lang/`.
  - Notes: [[00-how-to-use-track|How to Use This Track]], [[13-bash-capstone|Capstone]]

- [ ] **Phase 7** — Docker, direnv, LSP, the rest
  - Goal: reproducible env.
  - Exit: app + DB running via `docker compose`.
  - Parked until Phase 7:
    - [[00-docker-introduction|Docker Intro]]

## Rules
- Only add a tool when I have felt the pain it removes.
- Code lives outside Obsidian (`~/learning/`). Obsidian holds concepts (`02-notes/`), daily logs (`06-journal/`), and parked resources (`05-resources/`).
- `00-inbox/`, `03-exercises/`, `04-projects/` are code/work folders, no `index.md` needed. Use search.
