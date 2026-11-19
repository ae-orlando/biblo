# Migration lab — progressive hints

1. “The commands run successfully individually” does not establish atomicity.
2. Backfill before enforcing canonical format. Enforcing uniqueness may reveal a business-data conflict; that should abort the transaction.
3. Put the update and every schema change inside the same `BEGIN`/`COMMIT`. The checker closes a failed psql connection, rolling back its open transaction. Do not catch and ignore the error.
