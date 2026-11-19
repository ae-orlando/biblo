# FastAPI learning path — Python first, explicit contracts next

## Entry gate

Complete [[python-learning-path]]'s synchronous checkpoint first. Understand functions, imports, exceptions, dictionaries, classes, basic annotations and tests. Then study [[00-web-foundations]]. SQL prerequisites apply before the persistence unit, not before your first Python program.

This is framework learning independent of any current project. Django remains an optional old reference, not your main backend path. FastAPI does not supply every security, persistence or operational decision automatically.

## Sequence

| Unit | Read | Demonstration |
| --- | --- | --- |
| Application and HTTP | [[01-fastapi-application]], [[02-fastapi-contracts]] | `api-contract`: strict validated input, response and OpenAPI contract |
| Boundaries and tests | [[03-fastapi-dependencies]], [[04-fastapi-testing]] | `api-dependencies`: isolated factories and a substituted dependency |
| Async, when understood | [[11-python-async]], [[05-fastapi-async]] | `api-async`: bounded work, deadline and task cleanup |
| Persistence | Relevant [[postgres-learning-path]] units, [[06-fastapi-persistence]] | `api-postgres`: real transactions and no overselling under concurrent requests |
| Security policy | [[25-http-security-boundaries]], [[07-fastapi-security]] | `api-ownership`: default denial and object-level policy, not a real login system |
| Operation and integration | [[08-fastapi-operation]], [[09-fastapi-capstone]], [[web-app-structure]] | Independent change request, deployment/recovery worksheet, then frontend integration |

Find specifications in [[practice-catalog]]. Later units have explicit prerequisites; do not start them simultaneously.

## Local tooling

```bash
python3 90-tools/install-learning-runtime.py fastapi
python3 90-tools/practice.py start api-contract
python3 90-tools/practice.py check api-contract
```

The installer is only needed if the marked local environment is absent/incomplete. It installs under .tools/, not globally. The author already installed and tested a runtime; beginner Python does not need it. Matching versions and transitive pins are documented in [[python-fastapi-expansion-status]].

TestClient sends requests to the ASGI app in-process; this does not prove a reverse proxy, TLS or deployment works. The apps retain /openapi.json but disable CDN-backed docs pages for offline/privacy-friendly tests. A default FastAPI app normally has interactive docs; self-host assets before requiring an offline UI.

## Scope and exit

The authorization lab injects a trusted identity only in tests; actual identity verification/session/token lifecycle is a separate security gate. The persistence app is a local teaching app with bootstrap DDL, not production migrations/roles. No hosting account, remote deployment or credentials are created by the curriculum.

Exit with a tested API, a documented contract, deliberate failure evidence and a changed requirement. Then move to [[html-css-learning-path]] and existing JavaScript as a focused frontend stage toward fullstack engineering.

Sources: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/), [deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/).
