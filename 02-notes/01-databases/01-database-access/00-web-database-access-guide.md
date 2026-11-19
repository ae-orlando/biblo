Start the database first (it's currently stopped), then pick whichever entry point you prefer.

## Option A: `psql` inside the container (nothing to install)

```bash
docker compose up -d db
docker compose exec db psql -U easyearn -d easyearn
```

You're now at a SQL prompt connected to the `easyearn` database. Useful meta-commands:

```sql
\dt                  -- list tables
\d users             -- describe the users table
\d+ task_completions -- columns, indexes, constraints
\du                  -- list roles
\q                   -- quit
```

## Option B: `psql` from your host

Only works if `psql` is installed locally. The Compose DB is published on **5433**, not 5432 (that port belongs to your unrelated local Postgres):

```bash
psql "postgresql://easyearn:easyearn_dev_password@localhost:5433/easyearn"
```

## Option C: a GUI (DBeaver, pgAdmin, TablePlus, DataGrip)

Connection settings:

| Field | Value |
|---|---|
| Host | `localhost` |
| Port | `5433` |
| Database | `easyearn` |
| User | `easyearn` |
| Password | `easyearn_dev_password` (the Compose default from `compose.yaml`) |

If you ever set `POSTGRES_PASSWORD` in the environment or a root `.env`, use that instead.

## Handy first queries

```sql
SELECT * FROM alembic_version;                    -- which migration is applied
SELECT id, email, username, email_verified, is_admin, created_at FROM users;
SELECT id, user_id, expires_at FROM user_sessions;
SELECT id, email, status, attempts FROM email_jobs;  -- outbox queue
```

## Rules of thumb

- Prefer the app's own flows for creating users — manual `INSERT`s will produce bcrypt-incompatible password hashes and miss referral codes/wallets.
- Don't change schema by hand. Add a migration and run `cd backend && uv run alembic upgrade head`; `alembic current` and `alembic history` show state.
- Data lives in the `earn-easy_postgres_data` volume. `docker compose stop`/`down` keeps it; `docker compose down -v` deletes it.
- If you want app-level access instead of raw SQL, this works from `backend/`:

```bash
uv run python -c "
from app.core.config import get_settings
from app.db.session import create_database_engine, create_session_factory
from sqlalchemy import text
engine = create_database_engine(get_settings())
with create_session_factory(engine)() as db:
    print(db.execute(text('select count(*) from users')).scalar())
engine.dispose()
"
```
