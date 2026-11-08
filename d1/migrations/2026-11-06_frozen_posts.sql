-- Archiving now freezes a post: no new chirps, wings or reactions, and its author can't delete it.
-- archived keeps its old meaning of hidden from members, which every feed query already respects.
-- Posts archived before today were hidden, so they carry over as frozen and hidden.
ALTER TABLE posts ADD COLUMN frozen INTEGER NOT NULL DEFAULT 0;
UPDATE posts SET frozen = 1 WHERE archived = 1;
CREATE INDEX IF NOT EXISTS idx_posts_frozen_list ON posts(created_at DESC) WHERE frozen = 1 AND deleted = 0;
