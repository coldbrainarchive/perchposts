-- Globe worm hunt (shared): each bird's current flight, and the worms that pop up near hunting birds.
CREATE TABLE IF NOT EXISTS hunt_birds (username TEXT PRIMARY KEY, from_lat REAL NOT NULL, from_lng REAL NOT NULL, to_lat REAL NOT NULL, to_lng REAL NOT NULL, depart_at INTEGER NOT NULL, arrive_at INTEGER NOT NULL, seen_at INTEGER NOT NULL, spawn_at INTEGER);
CREATE INDEX IF NOT EXISTS idx_hunt_birds_seen ON hunt_birds(seen_at);
CREATE TABLE IF NOT EXISTS hunt_worms (id TEXT PRIMARY KEY, lat REAL NOT NULL, lng REAL NOT NULL, value INTEGER NOT NULL DEFAULT 1, born_at INTEGER NOT NULL, gone_at INTEGER NOT NULL, caught_by TEXT, caught_at INTEGER);
CREATE INDEX IF NOT EXISTS idx_hunt_worms_live ON hunt_worms(gone_at) WHERE caught_by IS NULL;
