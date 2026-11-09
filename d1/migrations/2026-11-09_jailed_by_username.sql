-- Caging an account by username alone was silently ignored: jailed.browser_id was NOT NULL, and
-- accounts-only posts often have no browser_id. Recreate the table with browser_id optional;
-- one row per username, and per browser_id when there is one. (Table was empty when this ran.)
CREATE TABLE jailed_new (
  id         TEXT PRIMARY KEY,
  browser_id TEXT,
  username   TEXT,
  ip_hash    TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
INSERT INTO jailed_new (id, browser_id, username, ip_hash, created_at) SELECT id, browser_id, username, ip_hash, created_at FROM jailed;
DROP TABLE jailed;
ALTER TABLE jailed_new RENAME TO jailed;
CREATE UNIQUE INDEX IF NOT EXISTS idx_jailed_username ON jailed(username) WHERE username IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_jailed_browser_id ON jailed(browser_id) WHERE browser_id IS NOT NULL;
