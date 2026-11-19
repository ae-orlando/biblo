# FastAPI 07 — identity, ownership and explicit security boundaries

## Outcome

After [[25-http-security-boundaries]] and dependencies/testing, enforce object-level authorization and identify what is still missing from authentication. Practice: api-ownership.

Authentication establishes a trustworthy principal. Authorization decides what that principal may do to a specific object. A request field, query parameter or X-User-ID header is not automatically trustworthy identity. Pydantic validates shape, not ownership or permission.

## The lab deliberately does not issue credentials

The default dependency denies access with 401. Tests override that dependency with a trusted Principal to isolate policy. That override is **test-only**; it is not real password, bearer-token, session or OIDC verification. Do not deploy the exercise by replacing it with a user-controlled header.

For a real application, choose a reviewed identity/session approach and document issuer/audience/signature/expiry verification or server-side session lifecycle as appropriate. Include logout/revocation, rotation, recovery, enumeration/rate-limit policy, cookie/CSRF rules where relevant, secret management and negative tests. A copied JWT example does not establish all of these.

## Enforce policy at each operation

The exercise permits owners and explicitly authorized admins, denies others and filters response fields. It uses 404 for absent **or inaccessible** documents as a chosen existence-disclosure policy; another product may deliberately choose 403. Apply the same policy to reads and writes. Reject attempts to set owner/admin fields through an ordinary content-update body.

List/search/bulk operations also need scoping; checking a detail route alone does not secure them. A UI that hides a button does not protect a backend endpoint. Log security-relevant outcomes without credentials, tokens or unnecessarily sensitive content.

## Completion and transfer

Prove unauthenticated rejection, user A/user B isolation, admin policy and mass-assignment rejection. Introduce a skipped ownership check in a private copy and confirm the test fails. Then add organization membership and update both query scoping and negative tests.

Record the unimplemented identity-provider gate clearly. The supplied toy data and policy tests are not a deployment-ready authentication service or a complete security audit.

Sources: [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/), [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
