-- 2026-11-27: passport stamps. One row per stamp a bird has earned (k), with when (at) and any detail (d, JSON).
-- k = '_chk' marks that the bird's past has been filled in (and when it was last checked).
CREATE TABLE IF NOT EXISTS stamps (username TEXT NOT NULL, k TEXT NOT NULL, at TEXT NOT NULL, d TEXT, PRIMARY KEY (username, k));
