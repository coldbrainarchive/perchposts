-- Globe page (2026-11-23): the hourly trending build is saved here (k = 'trending'), so /globe answers instantly.
CREATE TABLE IF NOT EXISTS globe_cache (k TEXT PRIMARY KEY, v TEXT NOT NULL, at TEXT NOT NULL);
