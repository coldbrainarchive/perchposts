-- posts
CREATE TABLE IF NOT EXISTS posts (
  id            TEXT PRIMARY KEY,
  title         TEXT,
  content       TEXT,
  board         TEXT,
  username      TEXT,
  browser_id    TEXT,
  ip_hash       TEXT,
  continent     TEXT,
  country       TEXT,
  community_id  TEXT,
  is_mod        INTEGER NOT NULL DEFAULT 0,
  moderator     INTEGER NOT NULL DEFAULT 0,
  author_role   TEXT,
  mod_user_id   TEXT,
  created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  last_activity TEXT,
  is_huddle     INTEGER NOT NULL DEFAULT 0,
  huddle_members TEXT,
  deleted       INTEGER NOT NULL DEFAULT 0,
  archived      INTEGER NOT NULL DEFAULT 0,
  votes         INTEGER NOT NULL DEFAULT 0,
  pinned        INTEGER NOT NULL DEFAULT 0,
  pinned_global INTEGER NOT NULL DEFAULT 0,
  locked        INTEGER NOT NULL DEFAULT 0,
  frozen        INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_posts_board         ON posts(board);
CREATE INDEX IF NOT EXISTS idx_posts_browser_id    ON posts(browser_id);
CREATE INDEX IF NOT EXISTS idx_posts_last_activity ON posts(last_activity DESC);
CREATE INDEX IF NOT EXISTS idx_posts_mod_user_id   ON posts(mod_user_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at    ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_username      ON posts(username);
-- Feed sort order; see migrations/2026-10-05_feed_indexes.sql (no index on deleted: it misleads the planner)
CREATE INDEX IF NOT EXISTS idx_posts_feed_created  ON posts(pinned_global DESC, pinned DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_feed_activity ON posts(pinned_global DESC, pinned DESC, last_activity DESC);
-- Flock view; see migrations/2026-11-05_paged_feeds.sql (WHERE must match HUMAN_POSTS in worker.js)
CREATE INDEX IF NOT EXISTS idx_posts_human_activity ON posts(last_activity DESC)
  WHERE username NOT IN ('NewsBot','ScienceBot','NatureBot','SportsBot');
-- Mod panel lists; see migrations/2026-11-05_mod_lists.sql
CREATE INDEX IF NOT EXISTS idx_posts_deleted_list  ON posts(created_at DESC) WHERE deleted = 1;
CREATE INDEX IF NOT EXISTS idx_posts_archived_list ON posts(created_at DESC) WHERE archived = 1 AND deleted = 0;
CREATE INDEX IF NOT EXISTS idx_posts_frozen_list   ON posts(created_at DESC) WHERE frozen = 1 AND deleted = 0;
CREATE INDEX IF NOT EXISTS idx_posts_huddles ON posts(pinned_global DESC, pinned DESC, created_at DESC) WHERE is_huddle = 1;

-- comments
CREATE TABLE IF NOT EXISTS comments (
  id                TEXT PRIMARY KEY,
  post_id           TEXT NOT NULL REFERENCES posts(id),
  parent_comment_id TEXT,
  content           TEXT,
  username          TEXT,
  browser_id        TEXT,
  ip_hash           TEXT,
  is_mod            INTEGER NOT NULL DEFAULT 0,
  moderator         INTEGER NOT NULL DEFAULT 0,
  author_role       TEXT,
  mod_user_id       TEXT,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  deleted           INTEGER NOT NULL DEFAULT 0,
  pinned            INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_comments_post_id            ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_post_created      ON comments(post_id, created_at);
CREATE INDEX IF NOT EXISTS idx_comments_pinned            ON comments(post_id) WHERE pinned = 1;
CREATE INDEX IF NOT EXISTS idx_comments_parent_comment_id  ON comments(parent_comment_id);
CREATE INDEX IF NOT EXISTS idx_comments_browser_id         ON comments(browser_id);
CREATE INDEX IF NOT EXISTS idx_comments_username           ON comments(username);
CREATE INDEX IF NOT EXISTS idx_comments_mod_user_id        ON comments(mod_user_id);

-- post_votes
CREATE TABLE IF NOT EXISTS post_votes (
  id          TEXT PRIMARY KEY,
  post_id     TEXT NOT NULL REFERENCES posts(id),
  browser_id  TEXT NOT NULL,
  value       INTEGER NOT NULL,
  username    TEXT,
  ip_hash     TEXT,
  is_mod      INTEGER NOT NULL DEFAULT 0,
  mod_user_id TEXT,
  created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  UNIQUE(post_id, browser_id)
);

CREATE INDEX IF NOT EXISTS idx_post_votes_post_id ON post_votes(post_id);

-- comment_reactions
CREATE TABLE IF NOT EXISTS comment_reactions (
  id         TEXT PRIMARY KEY,
  comment_id TEXT NOT NULL REFERENCES comments(id),
  browser_id TEXT NOT NULL,
  emoji      TEXT NOT NULL,
  username   TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  UNIQUE(comment_id, browser_id, emoji)
);

CREATE INDEX IF NOT EXISTS idx_comment_reactions_comment_id ON comment_reactions(comment_id);

-- bans
CREATE TABLE IF NOT EXISTS bans (
  id         TEXT PRIMARY KEY,
  browser_id TEXT,
  ip_hash    TEXT,
  username   TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- jailed
-- browser_id optional: accounts are caged by username (see migrations/2026-11-09_jailed_by_username.sql)
CREATE TABLE IF NOT EXISTS jailed (
  id         TEXT PRIMARY KEY,
  browser_id TEXT,
  username   TEXT,
  ip_hash    TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_jailed_username ON jailed(username) WHERE username IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_jailed_browser_id ON jailed(browser_id) WHERE browser_id IS NOT NULL;

-- bot_seen
CREATE TABLE IF NOT EXISTS bot_seen (
  id         INTEGER PRIMARY KEY,
  urls       TEXT NOT NULL DEFAULT '[]',
  last_run   TEXT,
  updated_at TEXT
);
INSERT OR IGNORE INTO bot_seen (id, urls, last_run) VALUES (1, '[]', NULL);

-- bot_config
CREATE TABLE IF NOT EXISTS bot_links (
  url        TEXT PRIMARY KEY,
  created_at TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS bot_config (
  id         INTEGER PRIMARY KEY,
  config     TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT
);
INSERT OR IGNORE INTO bot_config (id, config) VALUES (1, '{}');

-- bot_logs
CREATE TABLE IF NOT EXISTS bot_logs (
  id                TEXT PRIMARY KEY,
  started_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  finished_at       TEXT,
  status            TEXT NOT NULL DEFAULT 'running',
  run_type          TEXT,
  posted            INTEGER NOT NULL DEFAULT 0,
  posted_articles   TEXT NOT NULL DEFAULT '[]',
  skipped_seen      INTEGER NOT NULL DEFAULT 0,
  skipped_bad_title INTEGER NOT NULL DEFAULT 0,
  feed_errors       TEXT NOT NULL DEFAULT '[]',
  post_failed       INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_bot_logs_status ON bot_logs(status, started_at);

-- mod_users (replaces Supabase Auth)
CREATE TABLE IF NOT EXISTS mod_users (
  id            TEXT PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  username      TEXT NOT NULL,
  role          TEXT NOT NULL DEFAULT 'mod',
  created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  deleted_at    TEXT,
  deleted_by    TEXT,
  left_huddles  TEXT,
  purged_at     TEXT
);
CREATE INDEX IF NOT EXISTS idx_mod_users_deleted ON mod_users(username) WHERE deleted_at IS NOT NULL;
-- Notification read state per account, so "read" syncs across devices.
-- notif_state.seen_at: everything up to here is read (Mark all read / Clear all).
-- notif_reads: individual notifications tapped after seen_at (notif_time = the notification's own time).
CREATE TABLE IF NOT EXISTS notif_state (
  user_key TEXT PRIMARY KEY,
  seen_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS notif_reads (
  user_key   TEXT NOT NULL,
  notif_id   TEXT NOT NULL,
  notif_time TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  PRIMARY KEY (user_key, notif_id)
);
