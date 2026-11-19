CREATE TABLE events(id bigint PRIMARY KEY,user_id integer NOT NULL,kind text NOT NULL,created_at timestamptz NOT NULL);
INSERT INTO events
SELECT n, n % 1000, CASE WHEN n % 3 = 0 THEN 'login' ELSE 'view' END,
       timestamptz '2026-01-01T00:00:00Z' + n * interval '1 second'
FROM generate_series(1,30000) n;
ANALYZE events;
