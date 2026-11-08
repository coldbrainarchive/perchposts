-- Keep every post but never scan the posts table: indexes only, no data is modified or deleted.
--
-- Filtered feeds (board / country / continent / Flock) used to scan all ~211k posts per click
-- (200k-420k rows read each). /get-posts now pages newest-first by rowid with a ?before cursor:
--   board, username  -> existing idx_posts_board / idx_posts_username, one page of rows
--   country/continent -> bounded 4,000-row window (no index: building one writes ~211k rows,
--                        double the free tier's 100k/day write limit)
--   Flock (activity)  -> commented posts + the partial index below (only ~10 rows)
--
-- Each CREATE INDEX reads the whole table once (~420k rows read). The worker cron builds
-- missing indexes in the 00:05 UTC run, right after the daily limits reset.

-- Posts written by people (Flock view). The WHERE must match HUMAN_POSTS in worker.js exactly.
CREATE INDEX IF NOT EXISTS idx_posts_human_activity ON posts(last_activity DESC)
  WHERE username NOT IN ('NewsBot','ScienceBot','NatureBot','SportsBot');

-- Bot run expiry: UPDATE bot_logs ... WHERE status = 'running' AND started_at < ? (was ~100k rows/day)
CREATE INDEX IF NOT EXISTS idx_bot_logs_status ON bot_logs(status, started_at);
