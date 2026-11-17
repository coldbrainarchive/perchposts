-- Reactions on posts (one emoji per person per post; picking another replaces it). The bird number on a post counts
-- the people who responded in any way: flapped, reacted or gave worms.
CREATE TABLE IF NOT EXISTS post_reactions (
  id         TEXT PRIMARY KEY,
  post_id    TEXT NOT NULL,
  username   TEXT NOT NULL,
  emoji      TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(post_id, username)
);
CREATE INDEX IF NOT EXISTS idx_post_reactions_post ON post_reactions(post_id);
CREATE INDEX IF NOT EXISTS idx_post_reactions_user ON post_reactions(username, created_at);
-- the Flaps tab lists every post a person responded to, so worms are looked up by giver too
CREATE INDEX IF NOT EXISTS idx_worms_giver ON worms(giver, created_at);
