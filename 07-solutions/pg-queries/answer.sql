CREATE VIEW user_summary AS
SELECT u.id AS user_id, count(l.id) AS login_count, max(l.occurred_at) AS last_login
FROM users u LEFT JOIN logins l ON l.user_id = u.id
GROUP BY u.id;

CREATE VIEW never_logged_in AS
SELECT u.id AS user_id FROM users u
WHERE NOT EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id);

CREATE VIEW latest_logins AS
SELECT user_id, id AS login_id, occurred_at
FROM (
  SELECT l.*, row_number() OVER (
    PARTITION BY user_id ORDER BY occurred_at DESC, id DESC
  ) AS position
  FROM logins l WHERE user_id IS NOT NULL
) ranked WHERE position = 1;
