CREATE INDEX events_recent_login
ON events(user_id,created_at DESC,id DESC) WHERE kind = 'login';
