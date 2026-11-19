# Reference: policy separated from identity verification

The reference denies by default, lets tests inject a trusted principal, scopes object access to owner/admin and filters responses through a public schema. Ordinary update input cannot set owner_id. Existence is hidden through a chosen shared 404 response policy.

No password/session/bearer verification or credential issuance is implemented. A test override is not a secure identity provider. Verification: `python3 90-tools/practice.py check api-ownership --reference`; actual authentication/deployment remain separate gates.
