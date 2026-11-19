# Transfer lab — progressive hints

1. Treat the balance sum and nonnegative balances as invariants; inspect them after each rejected transfer.
2. Two callers locking the same pair in opposite orders can deadlock. Order row locks by account ID independently of transfer direction.
3. PL/pgSQL `PERFORM ... ORDER BY ... FOR UPDATE`, `FOUND`, `GET DIAGNOSTICS ... ROW_COUNT` and `RAISE EXCEPTION` are useful. An exception rolls back changes from the failed statement unless deliberately caught in a subtransaction.
