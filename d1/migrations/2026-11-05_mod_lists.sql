-- Mod panel: the deleted and archived lists scanned every post on each open (211k rows each, to
-- find 5 and 1). Partial indexes hold only those few rows. Indexes only, no data is modified.
-- The WHERE clauses must match the queries in /get-mod-data for SQLite to use them.
CREATE INDEX IF NOT EXISTS idx_posts_deleted_list  ON posts(created_at DESC) WHERE deleted = 1;
CREATE INDEX IF NOT EXISTS idx_posts_archived_list ON posts(created_at DESC) WHERE archived = 1 AND deleted = 0;
