CREATE TABLE users(id integer PRIMARY KEY, name text NOT NULL);
CREATE TABLE logins(id integer PRIMARY KEY, user_id integer REFERENCES users(id), occurred_at timestamptz NOT NULL);
INSERT INTO users VALUES (1,'Ana'),(2,'Ben'),(3,'Cara'),(4,'Dana');
INSERT INTO logins VALUES
  (10,1,'2026-01-01T10:00:00Z'),
  (11,1,'2026-01-02T10:00:00Z'),
  (12,2,'2026-01-03T10:00:00Z'),
  (13,NULL,'2026-01-04T10:00:00Z'),
  (14,1,'2026-01-02T10:00:00Z');
