# Reference: migration failure is a result, not an inconvenience

`answer.sql` performs the backfill and constraint changes in one transaction. A uniqueness failure aborts it; closing the session rolls it back. No arbitrary duplicate is chosen as the surviving contact.

This is a deliberately small-table exercise. Large migrations need lock planning, compatibility across deployments, validation and operational review. Versioned migration tools normally record applied migrations; `IF NOT EXISTS` can conceal drift rather than make migrations safe.

Verification: `python3 90-tools/practice.py check pg-migration --reference`.
