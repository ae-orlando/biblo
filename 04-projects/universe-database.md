# Universe database — independent modeling and reporting

## Prerequisites and goal

After `pg-schema` and `pg-queries` in [[practice-catalog]], design a small related dataset without copying a complete schema first. Use [[postgres-learning-path]] and the private course cluster; never use a real application database for a resettable exercise.

The original learner design remains in `02-notes/01-databases/00-postgres/99-practice-projects/universe databas.md`. The full worked script is preserved in [[2026-10-universe-worked-example]]. These are distinct earlier designs (including different fifth-table choices), not one schema to merge blindly.

## Brief and deliverables

Model galaxies, stars, planets, moons and a justified fifth entity. Define cardinalities and optionality; document simplifications such as whether a planet can have more than one host star. Choose keys, constraints, units and sensible numeric ranges. Do not mistake a course's “five tables and N rows” rule for professional data-model quality.

Create your own `04-projects/universe-training/` files when attempting:
- `design.md`: entities, rules, assumptions, units and delete/retention decisions.
- `schema.sql` and fake `seed.sql`, with enough data to exercise missing relationships and ties.
- `queries.sql`: joins, zero-related-row reports, aggregate filters, an absence query and a deterministic latest/ranked result.
- `checks.sql` or a script: valid inserts first, intended constraint failures, row/result verification and changed-data cases.
- `evidence.md`: actual execution, one caught defect, design tradeoffs and remaining limits.

Avoid assuming generated IDs start at 1 in a reused database. Use returned IDs or explicit fixture identities chosen for an empty isolated dataset. Specify output ordering rather than relying on insertion order.

## Acceptance and change request

Prove referential integrity, required values, domain checks and deterministic reports. Then change a requirement: a planet can be associated with multiple stars. Evolve the model and queries without losing associations; explain which previous assumptions and constraints must change.

Consult the worked example only after an attempt, record assistance and rebuild a variant independently. The project is not marked completed by the curriculum rebuild. Use [[study-and-review]].
