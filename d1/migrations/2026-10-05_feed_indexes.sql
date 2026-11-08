-- Cut D1 row reads: indexes only, no data is modified or deleted.
--
-- idx_posts_deleted has very low selectivity (deleted is 0 for ~40% of rows) but
-- SQLite still prefers it, so every feed / notif-count query walked ~45k rows.
-- Dropping it lets the planner use the indexes below (verified locally:
-- feed 44,800 -> ~1,250 rows, archive day 44,800 -> ~600, notif lookups -> ~0).

DROP INDEX IF EXISTS idx_posts_deleted;

-- Matches /get-posts ORDER BY pinned_global DESC, pinned DESC, <created_at|last_activity> DESC
CREATE INDEX IF NOT EXISTS idx_posts_feed_created  ON posts(pinned_global DESC, pinned DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_feed_activity ON posts(pinned_global DESC, pinned DESC, last_activity DESC);

-- /notif-count lookups
CREATE INDEX IF NOT EXISTS idx_posts_browser_id     ON posts(browser_id);
CREATE INDEX IF NOT EXISTS idx_posts_username       ON posts(username);
CREATE INDEX IF NOT EXISTS idx_posts_mod_user_id    ON posts(mod_user_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at     ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_comments_browser_id  ON comments(browser_id);
CREATE INDEX IF NOT EXISTS idx_comments_username    ON comments(username);
CREATE INDEX IF NOT EXISTS idx_comments_mod_user_id ON comments(mod_user_id);

PRAGMA optimize;
