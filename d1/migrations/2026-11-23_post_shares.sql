-- Shares (user's request, 2026-11-23): one row per bird per post (huddle send, Copy link or the phone's share menu).
-- posts.share_count is the number shown beside Share; a counted share also bumps the post's last_activity (Flock).
ALTER TABLE posts ADD COLUMN share_count INTEGER NOT NULL DEFAULT 0;
CREATE TABLE IF NOT EXISTS post_shares (
  post_id TEXT NOT NULL,
  username TEXT NOT NULL,
  via TEXT,
  created_at TEXT NOT NULL,
  PRIMARY KEY (post_id, username)
);
