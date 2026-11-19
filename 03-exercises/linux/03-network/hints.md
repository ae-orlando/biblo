# Layered diagnosis — progressive hints

1. Validate scheme/host/port before opening a connection. Redirects can move a request outside your allowed scope.
2. An HTTP error status is still an HTTP response. A high-level client may throw for that status, so choose an API whose behavior you understand.
3. A direct HTTPConnection with a timeout exposes the status without automatic redirects. Close it in finally; do not read unlimited bodies merely to inspect status.
