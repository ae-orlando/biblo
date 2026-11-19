# HTTP and browser security boundaries

## Outcome

After [[00-web-foundations]], trace a browser request, explain cookies/sessions and identify the component responsible for validation, authentication and authorization. Apply this to the selected [[fastapi-learning-path]] and later fullstack integration; js-http is an optional runtime teaching API and existing project notes are not the curriculum's goal.

## Different mechanisms solve different problems

- **Authentication:** establish who a requester is.
- **Authorization:** decide whether that requester may perform this operation on this object. Hiding a button is not enforcement.
- **Session:** server-recognized state across requests, often referenced by an opaque cookie. A cookie and a session are not synonyms.
- **TLS:** protects a connection in transit under its trust model; it does not fix an unsafe query or authorization defect.
- **CORS:** browser policy for eligible cross-origin reads. It is not authentication or a firewall against nonbrowser clients.
- **CSRF protection:** mitigates unwanted authenticated state-changing browser requests in the relevant credential model. A same-origin deployment does not make every CSRF concern disappear.
- **XSS defense:** keep untrusted data out of executable contexts. DOM textContent and template autoescaping help in their intended contexts, not as universal sanitizers.

HttpOnly prevents JavaScript access to a cookie, not every effect an XSS can cause. Secure limits cookie sending to secure transport contexts; SameSite influences cross-site sending. Choose cookie lifetime, rotation, logout/revocation and response behavior explicitly. Do not put a browser application's session token in localStorage merely because JSON storage is convenient.

## Exercise and checkpoint

For a login form and dashboard:
1. Draw request, response, Set-Cookie and subsequent Cookie flow.
2. Identify where passwords are hashed, sessions are rotated, authorization is checked and CSRF is enforced.
3. Specify unknown-user versus wrong-password responses without leaking account existence unnecessarily.
4. Write a user-A/user-B ownership test, an unauthenticated test and a CSRF-enforced test.
5. Explain why a passing scanner or a particular coverage percentage is not proof of security.

Only test deliberate vulnerabilities in your own isolated fake-data environment. No real account, credential, email API or remote scan is required by the vault rebuild. Continue through framework documentation rather than inventing a password/session system from scratch.

Sources: [OWASP authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html), [session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [MDN cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies).
