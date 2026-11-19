# FastAPI lab: deny by default and enforce object ownership

**ID:** api-ownership. Prerequisites: dependencies, HTTP/security and [[07-fastapi-security]]. This tests **authorization**, not a real credential-issuing service.

Export Principal(user_id,roles=frozenset()), get_principal and create_app(). The default dependency rejects requests with 401—even a spoofed X-User-ID must not establish identity. Tests override the actual dependency with a trusted Principal; do not ship that override as authentication.

Factory-owned fake documents: one belongs to A with content 'A draft'; two belongs to B with 'B draft'. GET /documents/ID and PUT /documents/ID permit only its owner or role admin. Absent/inaccessible → the chosen 404 policy. Public output is {id,content}, not owner internals. PUT accepts exactly content, a trimmed strict nonblank string up to 1000 characters; extra owner_id attempts → 422. Denied writes change nothing.

```bash
python3 90-tools/practice.py start api-ownership
python3 90-tools/practice.py check api-ownership
```

Completion: catch a skipped ownership check, explain 401 versus the chosen 404 policy, then design organization scoping and the unimplemented real identity/session/provider integration gate. Do not deploy this as a finished authentication system.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/api-ownership/explanation.md)
