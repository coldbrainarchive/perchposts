-- Site-wide switches set by admins in the mod panel (Flock tab). signup_limit: off | day | week
CREATE TABLE IF NOT EXISTS site_settings (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
INSERT OR IGNORE INTO site_settings (key, value) VALUES ('signup_limit', 'off');
-- One row per new account: which network (keyed ip hash) it was made from, for the sign-up limit
CREATE TABLE IF NOT EXISTS signups (
  net        TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_signups_net ON signups(net, created_at);
