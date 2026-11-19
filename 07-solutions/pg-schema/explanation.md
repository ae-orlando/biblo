# Reference: schema invariants

`answer.sql` uses identity keys for entities, a profile's shared primary/foreign key for optional one-to-one cardinality, and explicit cascading child deletion. `NOT NULL`, `UNIQUE` and the canonicalization check enforce different invariants; none substitutes for the others.

The lowercase policy is an exercise decision, not universal email semantics. A real system must decide address normalization, verification and retention with its requirements. Generated keys can have gaps. Counterexample to test: removing the profile PK allows multiple profiles for one user.

Verification: `python3 90-tools/practice.py check pg-schema --reference`.
