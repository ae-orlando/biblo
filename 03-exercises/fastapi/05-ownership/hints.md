# Ownership — progressive hints

1. A valid request schema does not establish who may change which object.
2. The same trusted principal/policy must apply to reads and writes; do not trust owner/admin claims from body/header fields.
3. Keep the dependency denied by default, override it only in isolated tests, filter public fields and verify that rejected writes preserve data. Real authentication is a separate implementation/test boundary.
