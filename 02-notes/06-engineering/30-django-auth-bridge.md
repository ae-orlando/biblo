# Django auth bridge — framework mechanisms before deployment

> Optional older project-specific reference. Your chosen main backend path is [[python-learning-path]] → [[fastapi-learning-path]], independent of the Nies project. This worksheet is preserved, not assigned as a prerequisite or substituted for the new course.

## Prerequisites and scope

Complete [[20-python-backend-bridge]], `python-config`, PostgreSQL modeling/query/transaction labs, [[25-http-security-boundaries]] and [[10-testing-and-debugging]]. This bridge supports [[nies-auth-platform]] without changing its Django + templates + server-side sessions direction.

This is an assessed project worksheet, **not an installed or executed Django course**. Select a supported Django release, use its matching official documentation, and create an explicitly chosen learner project under `04-projects/django-auth-training/` when ready. Do not alter an external business project or deploy a server automatically.

## Mechanisms to understand

A URL pattern selects a view; the view validates input and coordinates model/form/service behavior; templates render escaped output. Models describe persistence and migrations record schema changes. The ORM is not permission enforcement and does not eliminate transaction/concurrency issues. Inspect generated SQL and query count when behavior or performance matters.

Use Django's auth/session/password facilities. Decide a custom user model at project start when needed, before initial migrations. Do not recreate the course's illustrative token tables beside framework/allauth internals without a defined ownership and integration plan. An email uniqueness policy belongs in actual database constraints as well as form validation.

## Incremental builds and acceptance

1. **CRUD foundation:** owned notes with list/create/update/delete, forms and template errors. Prove user A cannot inspect/change B's objects through altered URLs or submitted IDs. Include anonymous cases.
2. **Auth flow:** registration/login/logout using documented framework functions, session cookies and generic failure responses. Inspect session rotation on login and invalidation on logout; do not assume a decorator covers object ownership.
3. **Email/token flow:** use a local in-memory email backend with fake addresses. Test verification/reset token expiry, reuse, wrong user and unknown-account response policy before choosing a real email provider.
4. **Database boundary:** use the intended runtime role, explicit migrations and transaction boundaries. Reproduce an important SQL query with the ORM; compare SQL/results and show an N+1 regression test or query-count observation.
5. **Security tests:** enforce CSRF in the test client when testing it—test clients may otherwise relax checks. Exercise validation, ownership, rate-limit policy and failure paths; use deterministic time controls rather than waiting for real expiry.

## Completion and change request

Save runnable setup/test instructions, dependency versions, actual results, a request-flow diagram and an unresolved-risk list. Add a requirement: an account can join multiple organizations but may access only its organization's records. Update the model, authorization and negative tests together.

Deployment is a later, separately scoped gate: HTTPS, cookies, secrets, logging, migrations, rollback, backups/restores and health checks. A local toy server, clean security scan or “16 checkboxes” does not certify a real authentication platform as ready.

Sources: [Django supported versions](https://www.djangoproject.com/download/), [official docs](https://docs.djangoproject.com/), [auth topics](https://docs.djangoproject.com/en/stable/topics/auth/), [testing](https://docs.djangoproject.com/en/stable/topics/testing/), [deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/). Follow version-matched pages once a release is chosen.
