-- Huddles board: is_huddle had no index, so every load walked all 211k posts to find a few rows.
-- A partial index holds only the huddles. Index only, no data is modified.
-- Column order matches the ORDER BY in /get-posts. The worker names this index with INDEXED BY.
CREATE INDEX IF NOT EXISTS idx_posts_huddles ON posts(pinned_global DESC, pinned DESC, created_at DESC) WHERE is_huddle = 1;
