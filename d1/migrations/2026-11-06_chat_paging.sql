-- Chats load in pages, so finding a page's edge and a post's pinned chirps must not read every chirp.
-- Indexes only, no data is modified.
CREATE INDEX IF NOT EXISTS idx_comments_post_created ON comments(post_id, created_at);
CREATE INDEX IF NOT EXISTS idx_comments_pinned ON comments(post_id) WHERE pinned = 1;
