# Reference: permission evidence and recovery evidence

`answer.sql` grants only the privileges needed by the exercise reader. The creating owner runs `ALTER DEFAULT PRIVILEGES`, so its subsequently created table is readable too. Negative tests establish that DML, schema creation and dropping an owned-by-someone-else table are denied.

The checker restores a plain dump into a new local database and exercises rows, constraints and the identity sequence. This is stronger than checking backup size, but it does not establish production recovery time, offsite durability, application compatibility or restoration of cluster-wide roles.

Verification: `python3 90-tools/practice.py check pg-restore --reference`.
