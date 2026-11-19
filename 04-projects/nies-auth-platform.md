---
created: 2026-10-19
updated: 2026-10-21
---

# Nies Technologies — Auth Platform (skill-up guide)

> **Learning-system alignment:** this remains a project specification, not evidence of completed work. Preserve its Django/templates/session decisions. Use [[baseline-diagnostic]], [[postgres-learning-path]], [[20-python-backend-bridge]], [[30-django-auth-bridge]] and [[25-http-security-boundaries]] for prerequisite bridges. Hour/week estimates and performance targets are planning assumptions, not guarantees or certification thresholds. The rebuild did not deploy anything, create accounts or modify an external business project.

Backend partner role for Nies Technologies: fast, secure registration + login + dashboard. Ad asks for one of PHP/Laravel, Node, Python/Django/Flask, plus a database, auth, APIs, security, deployment. Frontend already exists in plain HTML/CSS/JS.

**Recorded starting assumption (2026-10-19; recheck with diagnostics):** can create databases/tables, insert data, basic querying. Comfortable in Linux shell + shell scripting. Strong HTML/CSS/JS.

**Target:** integration-ready backend in 2 weeks, deployable in 4, portfolio-grade in 6. ~40 h/week.

Bundled learning labs/attempts now live inside the vault under [[learning-system]]. An isolated learner project may live under `04-projects/django-auth-training/`. Existing external/business repositories remain untouched and need an explicit location/scope decision before modification. This note holds requirements and acceptance criteria.

---

## 1. Locked decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Backend | **Django + PostgreSQL** | Python known, ad accepts it, secure defaults |
| Frontend integration | **Django templates + progressive JS** | Their HTML becomes templates; no API needed for v1 |
| Auth | **Server-side sessions in `HttpOnly` cookies** | Safest for a browser app; no JWT in `localStorage` |
| API layer | **Skip DRF for v1** | Add small JSON endpoints only where JS truly needs them |
| Email | **Transactional email API** (Resend/Postmark/SES) | Delivery latency/failure vary; use local fake email during learning and explicitly design the request/delivery boundary before choosing a provider |
| Deployment | **VPS + nginx + Gunicorn + systemd + Certbot** | Linux edge; no PaaS hiding details |
| OAuth | **Not in v1** | Email/password first; `django-allauth` adds Google later |

Do not let anyone talk this into React, JWT, microservices, or Docker for v1.

**Reframe the ad's absolutes.** "100% smooth / no errors / eliminate hacking" is not achievable. Offer measurable targets instead:

- p95 auth-page response < 300 ms
- Lighthouse mobile ≥ 90
- OWASP ZAP baseline: no medium/high findings
- Tested auth flows, coverage ≥ 85%
- 99.9% uptime target
- Predictable session lifetimes, not "no timeout"

Saying this in the first call reads as senior, not negative.

---

## 2. Module map

| # | Module | Hours | Priority |
| --- | --- | --- | --- |
| 1 | Linux & environment (production) | 6 | Medium |
| 2 | HTTP, cookies, sessions | 6 | **Critical** |
| 3 | Python backend essentials | 10 | High |
| 4 | PostgreSQL: design → performance → integrity | 40 | **Critical** |
| 5 | Django fundamentals | 30 | **Critical** |
| 6 | Auth deep dive | 20 | **Critical** |
| 7 | Security | 20 | **Critical** |
| 8 | Testing | 12 | High |
| 9 | Performance | 10 | Medium |
| 10 | Deployment & ops | 20 | High |
| 11 | Git & collaboration | 5 | Medium |
| 12 | Frontend integration | 10 | High |
| 13 | Documentation & communication | 5 | Medium |

**Learning rules**

- 30% docs, 70% typing. 90 minutes reading → stop and build.
- Every module ends with an artifact: schema file, working page, test suite, deployed URL, script.
- Keep an error journal: date, symptom, root cause, fix, prevention rule. Review Fridays.
- Teach-back: 300 words or 3-minute video without notes at module end.
- Spaced repetition Mondays: one exercise from 1 week ago, one from 3 weeks ago.
- Timebox debugging: 30 minutes → read the error, check docs, then ask.
- Never learn two hard things at once. Official docs over random blogs.

---

## 3. Module 1 — Linux & environment (6 h)

Production Linux, not beginner commands.

**Learn:** processes/signals, permissions, systemd units + `journalctl`, SSH keys, `ufw`, env vars, cron vs systemd timers, `ss`/`lsof`/`curl`/`dig`, log locations.

- [ ] Create a non-root sudo user on a VM/VPS, add SSH key, disable root login and password auth. Verify from a second terminal before closing the first.
- [ ] Write a systemd service running a trivial Python HTTP server. Start, check status, `journalctl -u`, kill, confirm auto-restart.
- [ ] `ss -tulpn` to find a listener; `curl -v` and `dig` to trace a request.
- [ ] Script with `set -euo pipefail` that fails loudly on a missing env var. `shellcheck` clean.
- [ ] systemd timer running a "hello" script every minute; verify in `journalctl`.

**Done when:** you can explain what happens between a browser request and your app process, and debug "it's not reachable" without guessing.

Related: [[00-linux-introduction]], [[40-linux-processes]], [[60-linux-networking]], [[70-linux-shell-workflow]], [[90-linux-protips]], [[10-robust-bash-scripts]].

---

## 4. Module 2 — HTTP, cookies, sessions (6 h)

The mental model behind every auth bug in the brief.

**Learn:** request/response, methods, status codes, headers, redirects, cookies (`HttpOnly`, `Secure`, `SameSite`), sessions vs tokens, same-origin policy, CORS, TLS basics, DNS.

- [ ] `curl -v` a real login form. Identify `Set-Cookie`; send it back with `-b` and prove you are authenticated.
- [ ] 30-line Python `http.server` that sets and reads a cookie. Inspect in devtools → Application → Cookies.
- [ ] Status-code drill: write the correct code for 12 scenarios (created, bad input, unauthenticated, forbidden, not found, duplicate email conflict, too many requests, redirect after POST, server error…).
- [ ] Redirect-after-POST: form that re-submits on refresh (bad) vs one that redirects (good).
- [ ] Same-origin demo: two ports, `fetch` across them, read the CORS error, then fix it deliberately.

**Done when:** you can explain session vs cookie vs token, and why `HttpOnly` + `Secure` + `SameSite=Lax` matters, without notes.

Related: [[00-web-foundations]], [[09-js-fetch-storage]].

---

## 5. Module 3 — Python backend essentials (10 h)

**Learn:** virtualenv/`uv`, modules/imports, exceptions, context managers, timezone-aware `datetime`, `secrets`, `os.environ`, `json`, `logging`, type hints, `pytest` basics.

- [ ] CLI password generator using `secrets`, with length and character-set flags.
- [ ] Config loader reading env vars that **fails loudly** if `SECRET_KEY` or `DATABASE_URL` is missing. No silent defaults for secrets.
- [ ] `logging` with levels, formatter, rotating file handler. Log a fake request lifecycle.
- [ ] Timezone exercise: store UTC, display Africa/Nairobi. Never naive datetimes.
- [ ] 8 `pytest` tests for pure functions: valid, boundary, invalid, exception path.

**Done when:** you can split code into modules and test pure logic without a database.

---

## 6. Module 4 — PostgreSQL (40 h) — biggest gap

Current level: `INSERT` + basic `SELECT`. Missing: schema design, constraints, indexes, transactions, operations.

### Level 1 — Schema design (8 h)

**Learn:** `text` vs `varchar`, `timestamptz`, `boolean`, `uuid` vs `bigint`, `jsonb` sparingly; `NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY`, `ON DELETE`; 1:1, 1:N, M:N; enough normalization to avoid duplication.

- [ ] **Design the auth schema on paper.** Tables: `users`, `profiles`, `email_verification_tokens`, `password_reset_tokens`, `login_attempts`, `audit_log`. Every column: type, nullability, default, constraint. Every relationship: cardinality and delete behavior.
- [ ] **Write `schema.sql`** with every constraint. Then break each one and record the exact error: duplicate email, null required field, invalid email via `CHECK`, orphan token, delete user with tokens under `RESTRICT` vs `CASCADE`.

**Done when:** you can defend every column and constraint out loud.

Related: [[02-sql-datatypes]], [[04-primary-foreign-keys]], [[05-relationships]], [[09-altering-tables]].

### Level 2 — Querying (10 h)

**Learn:** `INNER` vs `LEFT JOIN`, `GROUP BY`/`HAVING`, aggregates, subqueries, one CTE, `RETURNING`, basic window function.

- [ ] **pgexercises.com — every section.** Not just the easy ones.
- [ ] **Seed 100,000 users** with `generate_series`, plus profiles, logins, tokens. Write these 14 queries:
  1. Users in Nairobi with a completed profile
  2. Registrations per day, last 30 days
  3. Users with zero logins
  4. Top 10 users by login count
  5. Registered but never verified
  6. Duplicate emails (prove the constraint holds)
  7. Average sessions per active user
  8. Users with >3 failed logins in 24 h
  9. Monthly registration cohorts
  10. Latest login per user (window function or `LATERAL`)
  11. Users on `gmail.com`
  12. Delete unverified users older than 30 days, `RETURNING`
  13. Dashboard query: one user + profile + last 5 audit events
  14. Count users per verification status (`GROUP BY` + `HAVING`)

**Done when:** all 14 run correctly and you can explain each join choice.

Related: [[06-table-joining-methods]], [[08-filtering-sorting-aggregates]], [[12-subqueries-ctes-views]].

### Level 3 — Indexes & performance (8 h)

**Learn:** B-tree, composite index **column order**, unique/partial indexes, write cost, `EXPLAIN ANALYZE`, seq vs index scan, estimated vs actual rows.

- [ ] **Benchmark.** Inspect existing indexes first: UNIQUE email already has a supporting index. Compare no-index/index behavior on a separate disposable benchmark table; never drop a real integrity constraint to produce a slow baseline. Save representative plans, data shape and measurements without a promised speedup.
- [ ] **Composite order.** `WHERE status = 'active' AND created_at > ...`. Try `(status, created_at)` and `(created_at, status)`. Explain which the planner uses and why.
- [ ] **Write cost.** 10,000 inserts with 1 index vs 6 indexes. Record the difference.

**Done when:** you can look at a plan and say "seq scan, why, and what I'd change."

Related: [[11-indexes-and-performance]].

### Level 4 — Transactions & integrity (6 h)

**Learn:** `BEGIN`/`COMMIT`/`ROLLBACK`, atomicity, why registration (user + token) is one transaction, isolation levels at a high level.

- [ ] **Atomicity proof.** Insert user + token, force an error before commit, roll back, verify zero rows. Then do it correctly and verify both rows.
- [ ] **Constraint race.** Two `psql` sessions, insert the same email concurrently. Observe who wins and what the loser sees.

**Done when:** you can explain why "check then insert" in app code is not enough without a unique constraint.

Related: [[10-transactions]].

### Level 5 — Roles & backups (4 h)

- [ ] **Least privilege.** Create `app_user` with `CONNECT`, `USAGE`, DML only. Prove `DROP TABLE` and `CREATE TABLE` fail. Use this role for Django.
- [ ] **Backup drill.** Dump and restore into a separate newly created scratch database; verify data, schema, constraints and generated-ID behavior. Do not drop the original to test the backup. A real systemd backup timer is a later VM/deployment task.

Related: [[13-admin-and-ops]].

### Level 6 — ORM bridge (4 h)

- [ ] Rebuild the schema as Django models, then reproduce 3 SQL queries in the ORM. Print generated SQL and compare. Understand `select_related` vs `prefetch_related`.

**Module done when:** you can design the auth schema from scratch in 20 minutes and justify each index and constraint.

---

## 7. Module 5 — Django fundamentals (30 h)

**Learn:** project vs app, settings/env vars, models, migrations, ORM, URLs, views (FBV/CBV), templates, forms, admin, static/media, custom user model, messages, redirects.

- [ ] Official tutorial parts 1–7, typed by hand.
- [ ] **Start with a custom user model using email login.** Retrofitting this later is painful.
- [ ] "Notes" app: create, list, detail, edit, delete — with ownership (user A cannot edit user B's note).
- [ ] Forms: validation, custom `clean_email`, duplicate handling, errors rendered next to fields.
- [ ] Template inheritance: `base.html`, auth-aware nav, static CSS/JS.
- [ ] Customize admin: list display, search, filters.
- [ ] 15 ORM queries including `select_related` and `prefetch_related`; print the SQL.
- [ ] `django-environ` (or `python-dotenv`), `DEBUG=False` in prod, `ALLOWED_HOSTS`.

**Done when:** you can build a CRUD app with auth and tests without following a tutorial.

---

## 8. Module 6 — Auth deep dive (20 h)

**Learn:** Django auth views, sessions, password hashers, Argon2, validators, session expiry/rotation, `django-allauth`.

- [ ] Register / login / logout / dashboard from scratch with Django forms and auth functions.
- [ ] **Argon2** as primary hasher. Inspect a hash in the DB. Raise the cost factor and verify rehash-on-login.
- [ ] Inspect session cookie in devtools; confirm `HttpOnly`, `Secure`, `SameSite`. Verify the session key **changes on login** (session fixation test).
- [ ] "Remember me": 2-week session vs browser-close session. Test both.
- [ ] `django-allauth`: email verification, resend, expired link, already-verified link.
- [ ] Password reset: request, email, token, new password, reuse attempt, expired token. Generic responses for unknown emails.
- [ ] `django-axes`: lockout after N failures, success resets counter, unlock procedure.
- [ ] Inactive user cannot log in. Unverified user gets a clear, non-leaky message.

**Done when:** every flow works and every failure case has a test.

---

## 9. Module 7 — Security (20 h)

**Learn:** OWASP Top 10, cheat sheets (Password Storage, Session Management, Authentication, SQLi, XSS), security headers, CSP, user enumeration, open redirect, secrets management.

- [ ] **PortSwigger Web Security Academy:** SQLi (5 labs), XSS (5), authentication (5), session management (3). Do the labs.
- [ ] Deliberately `mark_safe` user input in a scratch view. Exploit your own XSS. Fix it, add a CSP. Note what changed.
- [ ] Deliberately vulnerable raw SQL with string concatenation. Exploit with `' OR 1=1 --`. Fix with parameters. **Local only.**
- [ ] Open redirect: `?next=//evil.com`. Fix with `url_has_allowed_host_and_scheme`.
- [ ] Enumeration audit: compare register/login/reset responses for known vs unknown emails. Make them indistinguishable.
- [ ] Remove `{% csrf_token %}` from a form, observe the 403, explain why it is correct.
- [ ] Run `python manage.py check --deploy` against the intended production settings; fix or explicitly justify findings for that environment, not blindly silence warnings in local development.
- [ ] OWASP ZAP baseline against staging; fix medium/high; rerun.
- [ ] `pip-audit` and `bandit`; triage findings in a short note.

**Done when:** ZAP baseline has no medium/high findings and you can explain each fix in one sentence.

---

## 10. Module 8 — Testing (12 h)

**Learn:** `pytest-django`, fixtures, factories, `Client`, test DB isolation, coverage, `freezegun`, email backend in tests.

Build this matrix (~25 tests):

| Area | Cases |
| --- | --- |
| Register | valid, duplicate email, weak password, mismatched confirm, invalid email |
| Verification | valid token, expired, reused, wrong user |
| Login | valid, wrong password, unknown email, inactive, locked out, rate limited |
| Logout | session invalidated |
| Reset | known email, unknown email, valid token, expired, reused, password change invalidates sessions |
| Access | dashboard requires login; user A cannot access user B |
| CSRF | POST without token rejected with CSRF enforcement explicitly enabled in the test client |

- [ ] Coverage ≥ 85%; inspect uncovered lines.
- [ ] `freezegun` for expiry tests instead of sleeping.
- [ ] Assert an email was sent; extract token from it (`locmem` backend).
- [ ] **Break code on purpose** (remove a permission check, skip expiry). Confirm a test fails. If not, the suite is decorative.

**Done when:** suite runs under 60 seconds and catches your deliberate bugs.

---

## 11. Module 9 — Performance (10 h)

**Learn:** `django-debug-toolbar`, N+1 queries, indexes in practice, caching, static serving, compression, Lighthouse, load testing.

- [ ] Dashboard: count queries with the toolbar. Reduce to a constant with `select_related`/`prefetch_related`. Record before/after.
- [ ] Inspect the email uniqueness index before adding anything; measure the actual login query and avoid a duplicate index with no justified workload benefit.
- [ ] Cache one dashboard aggregate for 60 s; measure the hit path.
- [ ] Lighthouse mobile ≥ 90. Fix top 3 issues (usually images, render-blocking CSS, missing dimensions).
- [ ] `hey` or `k6`: 50 concurrent users on `/login` for 30 s. Record p95.
- [ ] nginx: gzip/brotli, cache headers for static assets. Measure again.

**Done when:** p95 auth-page response < 300 ms locally and Lighthouse mobile ≥ 90.

---

## 12. Module 10 — Deployment & ops (20 h)

**Learn:** VPS provisioning, SSH hardening, `ufw`, `fail2ban`, nginx reverse proxy, Gunicorn, systemd, Certbot, backups, logging, monitoring.

- [ ] VPS: non-root sudo user, SSH keys, no root login, no password auth, `ufw` (22/80/443), `fail2ban`.
- [ ] Manual deploy: PostgreSQL, venv, Gunicorn, systemd unit, nginx reverse proxy, static files via nginx.
- [ ] TLS with Certbot, HTTP→HTTPS redirect, HSTS. Target SSL Labs grade A.
- [ ] `deploy.sh`: `set -euo pipefail`, pull, install, migrate, collectstatic, restart, health check, rollback. `shellcheck` clean.
- [ ] `backup.sh`: `pg_dump -Fc`, timestamp, retention (7 daily / 4 weekly), optional encryption, offsite copy. **Restore drill documented.**
- [ ] `healthcheck.sh`: HTTP check + `pg_isready` + disk space; non-zero exit on failure. Wire to timer or Uptime Kuma.
- [ ] Simulate a 500; find it in `journalctl`, nginx error log, Sentry.
- [ ] Reboot the server. Confirm everything returns automatically.
- [ ] **Recovery test:** reproduce deployment on a separate disposable environment using only the README; record actual duration and missing dependencies. Do not destroy an existing production/business server for a learning drill.

**Done when:** the redeploy test passes. This is the skill most applicants lack.

Related: [[30-linux-permissions]], [[60-linux-networking]], [[13-admin-and-ops]], [[10-robust-bash-scripts]], [[30-script-workflow]].

---

## 13. Module 11 — Git & collaboration (5 h)

- [ ] Feature branch → commits → PR to yourself → review → merge. Five times.
- [ ] `.gitignore` excluding `.env`, `*.sqlite3`, `__pycache__`, `staticfiles/`.
- [ ] `gitleaks` on history; rotate anything leaked.
- [ ] Resolve a merge conflict deliberately.
- [ ] Conventional commits (`feat:`, `fix:`, `chore:`) for one week.
- [ ] Practice `git revert`; explain when to use it vs `reset`.

**Done when:** clean history, no secrets, and you can review someone else's PR with useful comments.

---

## 14. Module 12 — Frontend integration (10 h)

- [ ] Convert 4 of Nies' pages into Django templates: `base.html`, register, login, dashboard. Keep their CSS classes intact.
- [ ] Auth-aware nav: Dashboard/Logout vs Login/Register.
- [ ] Render form errors next to fields; preserve entered values on validation failure.
- [ ] One progressive-JS feature with loading/error states. Prefer a non-sensitive validation or owned-data operation; a public email-availability endpoint conflicts with the account-enumeration policy unless explicitly justified and mitigated. Keep CSRF/auth rules appropriate to the operation.
- [ ] Responsive check at 360/768/1440 px. No horizontal scroll.
- [ ] Lighthouse mobile ≥ 90 on the real pages; no console errors.

**Done when:** their design runs on your backend and every form failure is understandable to a user.

**Integration contract to agree before coding:** field names, validation rules, error message format, redirect target per form, who owns assets.

---

## 15. Module 13 — Documentation & communication (5 h)

- [ ] README a stranger can follow: setup, env vars, run, test, deploy.
- [ ] One architecture diagram: browser → nginx → Gunicorn → Django → PostgreSQL, plus email API.
- [ ] Three short ADRs: "sessions over JWT", "Django templates over SPA", "VPS over PaaS" — with tradeoffs.
- [ ] 2-minute demo video: register → verify → login → dashboard → reset.
- [ ] Weekly status template: done, next, blockers, risks.

**Done when:** someone else can run the project from the README without asking you.

---

## 16. Six-week schedule

| Week | Modules | Artifact |
| --- | --- | --- |
| 1 | 1, 2, 3, SQL levels 1–2 | `schema.sql`, 14 queries, pgexercises complete |
| 2 | SQL levels 3–6, Django | Benchmarks, auth core locally, 10 tests |
| 3 | Auth, Security, Testing | Full auth suite, ZAP clean, coverage ≥ 85% |
| 4 | Performance, Deployment | Live HTTPS URL, scripts, restore drill, redeploy test |
| 5 | Integration, Git | Nies' frontend on staging, Lighthouse ≥ 90 |
| 6 | Docs, buffer | README, ADRs, demo video, final security pass |

**Daily rhythm (8 h):** 1 h docs → 5 h building → 1 h tests → 1 h notes/docs. Friday: error journal review, spaced repetition, demo.

**Milestone gates**

- **End of week 2 — integration-ready.** Register/login/logout with Argon2 + sessions; schema defended; one index proven with `EXPLAIN ANALYZE`; 10 passing tests. This is when you can honestly start on the real project.
- **End of week 4 — deployable.** Live URL, clean ZAP baseline, backups restored, redeploy from README.
- **End of week 6 — portfolio-grade.** Demo video, docs, measured performance.

**Do not disappear for six weeks.** Progress update to Nies on day 7 and day 14; 30-minute scope call in week 1.

---

## 17. First five days

- [ ] **Day 1:** Django tutorial parts 1–4; PostgreSQL connection; custom user model; `.env`.
- [ ] **Day 2:** Auth schema on paper; `schema.sql`; break every constraint deliberately.
- [ ] **Day 3:** pgexercises joins/aggregates; migrate schema as Django models.
- [ ] **Day 4:** Seed 100k users; benchmark email lookup; transaction exercise.
- [ ] **Day 5:** Register/login/logout/dashboard; inspect cookies; first 5 tests.

Friday outcome: working auth core + a schema you can defend — the evidence Nies asked for.

---

## 18. Self-assessment (tick only if no Googling)

- [ ] Explain why Argon2/bcrypt beats SHA-256 for passwords
- [ ] Explain `HttpOnly`, `Secure`, `SameSite` and when each matters
- [ ] Explain session vs JWT and when each is appropriate
- [ ] Design users/tokens/attempts schema with constraints
- [ ] Explain why a unique constraint beats an application-level duplicate check
- [ ] Write a query with `LEFT JOIN` + `GROUP BY` + `HAVING`
- [ ] Read an `EXPLAIN ANALYZE` plan and spot a seq scan
- [ ] Explain composite index column order
- [ ] Prove a transaction rolls back cleanly
- [ ] Create a least-privilege database role
- [ ] Explain how parameterized queries stop SQLi
- [ ] Explain where `mark_safe`/`|safe` is dangerous
- [ ] Prevent an open redirect with `next`
- [ ] Prevent user enumeration in login and reset
- [ ] Write tests for expiry and reuse of tokens
- [ ] Deploy nginx + Gunicorn + systemd + TLS
- [ ] Restore a database from backup
- [ ] Run ZAP and triage findings
- [ ] Refuse "100% secure" and offer measurable targets

Checkbox count is not a readiness certificate. Demonstrate every critical correctness/authorization/recovery requirement with actual artifacts, negative tests and independent change requests; record unresolved risks. Use [[study-and-review]] instead of averaging away a critical security gap with unrelated ticks.

---

## 19. Resources (finish, don't collect)

**SQL/PostgreSQL:** pgexercises.com · PostgreSQL docs (constraints, indexes, transactions) · *Use The Index, Luke* · SQLBolt warm-up.

**Django:** official tutorial · docs topics: auth, sessions, security, testing, deployment checklist · `django-allauth`, `django-axes`.

**Security:** OWASP Top 10 · OWASP Cheat Sheets (Password Storage, Session Management, Authentication, SQLi, XSS) · PortSwigger Web Security Academy.

**HTTP:** MDN HTTP docs · web.dev Learn Performance.

**Testing:** pytest-django docs · coverage.py docs.

**Ops:** nginx docs · Gunicorn docs · systemd manual · Certbot docs · DigitalOcean Ubuntu + nginx + Gunicorn tutorials.

**Tools:** `shellcheck` · Google Shell Style Guide · OWASP ZAP · Lighthouse · `hey`/`k6` · SSL Labs · `pip-audit` · `bandit` · Sentry · Uptime Kuma.

---

## 20. Skip until v1 ships

Docker/Kubernetes, microservices, Redis beyond one cache experiment, Celery (unless email volume demands it), GraphQL, React/Next, MongoDB, JWT from scratch, OAuth providers, CI/CD beyond a simple GitHub Actions test job, 40-hour video courses.

None are on the critical path.

---

## 21. Terms before committing (not yet agreed)

40 h/week for undocumented equity is a full-time commitment. Before week 5:

- [ ] Written collaboration agreement: equity %, vesting, IP ownership, decision rights, exit terms, time commitment.
- [ ] Keep the auth-starter as your own reusable repo; license project-specific work.
- [ ] Agree measurable targets, not "100% smooth" (section 1).
- [ ] Clarify who pays for VPS, domain, email service — and who owns those accounts.
- [ ] Kenya Data Protection Act 2019: privacy policy, lawful basis, breach handling, possible ODPC registration.
- [ ] Portfolio rights: nothing that prevents showing the work.
- [ ] Private repo until terms are agreed.

If terms are still not in writing by the time you have a live URL, that is information worth having before investing 240 hours.

---

## 22. Message to Nies (send after week 2)

Unsent draft only. Use it after the described artifacts actually exist, replacing proficiency/completion claims and placeholders with accurate evidence. No message is sent by this rebuild.

> Hi Nies — following up on my application. I'm strongest in Python/Django, PostgreSQL, and Linux deployment. Rather than just tell you, I built the auth core: **[live URL]** / **[repo]**. It covers registration, email verification, login, password reset, rate limiting, dashboard, tests, and a hardened deployment. I can own backend and deployment and integrate with your existing frontend.
>
> Can we do a 30-minute call to align on v1 scope, the frontend stack, and a short written collaboration agreement? I can start with a 2-week auth-core milestone.

Attach live URL, repo, 2-minute walkthrough, test/security results.

---

## Related Notes

- [[master-plan]] — roadmap and vault rules
- [[11-indexes-and-performance]] — indexes, EXPLAIN, N+1
- [[10-transactions]] — atomicity
- [[06-table-joining-methods]] — joins
- [[08-filtering-sorting-aggregates]] — GROUP BY / HAVING
- [[12-subqueries-ctes-views]] — CTEs
- [[13-admin-and-ops]] — roles, backups
- [[60-linux-networking]] — ports, DNS, debugging
- [[09-js-fetch-storage]] — cookies and storage
- [[00-web-foundations]] — HTTP status codes
- [[10-robust-bash-scripts]] — deploy/backup scripts
