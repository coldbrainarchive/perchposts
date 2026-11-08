-- A deleted account keeps a marker row, which retires its username and blocks its login.
-- Names on old content with no account behind them are retired the same way, so nobody can claim them.
ALTER TABLE mod_users ADD COLUMN deleted_at TEXT;
CREATE INDEX IF NOT EXISTS idx_mod_users_deleted ON mod_users(username) WHERE deleted_at IS NOT NULL;
INSERT INTO mod_users (id, email, password_hash, username, role, created_at, deleted_at)
SELECT lower(hex(randomblob(16))), 'retired-' || lower(hex(randomblob(8))) || '@users.local', '', name, 'user',
       strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
FROM (
  SELECT username AS name FROM comments WHERE username IS NOT NULL
  UNION SELECT username FROM post_votes WHERE username IS NOT NULL
  UNION SELECT username FROM comment_reactions WHERE username IS NOT NULL
  UNION SELECT username FROM posts INDEXED BY idx_posts_human_activity WHERE username NOT IN ('NewsBot','ScienceBot','NatureBot','SportsBot')
)
WHERE name != '__system__' AND name NOT IN ('NewsBot','ScienceBot','NatureBot','SportsBot') AND name NOT IN (SELECT username FROM mod_users);
