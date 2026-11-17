-- Worms: given by people to a post's author or a chirp's author. One row per worm (a person can give many).
-- receiver is who got it (the post or chirp author). Worm counts on profiles = worms received.
CREATE TABLE IF NOT EXISTS worms (
  id         TEXT PRIMARY KEY,
  giver      TEXT NOT NULL,
  receiver   TEXT NOT NULL,
  post_id    TEXT,
  comment_id TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_worms_receiver ON worms(receiver);
CREATE INDEX IF NOT EXISTS idx_worms_post     ON worms(post_id) WHERE post_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_worms_comment  ON worms(comment_id) WHERE comment_id IS NOT NULL;

-- A person's flapped posts (the Flaps tab on profiles), newest flap first
CREATE INDEX IF NOT EXISTS idx_post_votes_user ON post_votes(username, created_at);
