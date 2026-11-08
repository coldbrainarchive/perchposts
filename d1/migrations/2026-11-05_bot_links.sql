-- What the bots have posted, so an article can't be posted again. The seen list in bot_seen only lasts
-- about 3 days, and updated live blogs were being reposted for months. Despite the column name, url holds
-- keys: l: plus a cleaned link (permanent) or t: plus a cleaned headline (blocks for 6 days). See worker.js.
CREATE TABLE IF NOT EXISTS bot_links (
  url        TEXT PRIMARY KEY,
  created_at TEXT NOT NULL
) WITHOUT ROWID;
