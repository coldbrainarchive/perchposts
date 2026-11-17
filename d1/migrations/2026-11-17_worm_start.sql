-- Worm trading: everyone keeps the worms they had before worms became gifts (flaps on their posts + reactions on their
-- chirps, counted now, on 2026-11-17). Your worms = worm_start + worms received - worms given.
ALTER TABLE mod_users ADD COLUMN worm_start INTEGER NOT NULL DEFAULT 0;
UPDATE mod_users SET worm_start =
  COALESCE((SELECT COUNT(*) FROM post_votes pv JOIN posts p ON pv.post_id = p.id WHERE p.username = mod_users.username AND pv.value > 0 AND p.deleted = 0 AND (p.archived = 0 OR p.archived IS NULL)), 0)
  + COALESCE((SELECT COUNT(*) FROM comment_reactions cr JOIN comments c ON cr.comment_id = c.id WHERE c.username = mod_users.username AND c.deleted = 0), 0);
