# FastAPI checkpoint — independent backend, then fullstack integration

## Goal and prerequisites

Complete the five FastAPI labs and their Python/HTTP/SQL prerequisites. Build a new small application from a written brief rather than copying the supplied reference. Possible domains: equipment booking, reading groups, maintenance tickets or inventory. This is not tied to a current business project.

## Required artifacts

- A short problem statement, user roles, invariants, API contract and explicit non-goals.
- An app factory and the smallest module/package structure that makes responsibilities testable; see [[web-app-structure]].
- Validated request/response schemas, meaningful errors and object-level policy.
- A durable relational model, recorded migrations and correctly parameterized/transactional access.
- Domain, request and database integration tests, including competing writes and unauthorized access.
- Configuration without real secrets, a local setup/run/test README and actual failure/recovery evidence.
- A runbook and unresolved-risk list; do not invent deployment success or identity verification.

## Changed requirements

Choose a new requirement after the first version: retry-safe reservations, organization-scoped visibility, an import with invalid rows, or a filtered/paginated report. Specify the policy, add discriminating tests, change the implementation and explain the tradeoff. Preserve existing behavior unless the requirement intentionally changes it.

Use documentation, but show you can diagnose a defect and make the change without a step-by-step completed solution. A green reference audit is not your capstone evidence.

## Next focused stage

Study [[html-css-learning-path]], then the existing JavaScript track for browser behavior and API integration. Start with accessible HTML/native controls and an explicit loading/error/empty-state client. A frontend framework or TypeScript can follow when its benefit is understood; learning every framework is not a prerequisite to fullstack competence.

Then integrate the independent frontend/backend with real authorization, end-to-end tests and an executed delivery/recovery plan. The goal is maintaining a changing system, not collecting one more demo screenshot.
