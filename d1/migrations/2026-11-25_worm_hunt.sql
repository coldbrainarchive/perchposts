-- Globe worm hunt (shared): each bird's current flight, and the worms that pop up near hunting birds.
CREATE TABLE IF NOT EXISTS hunt_birds (username TEXT PRIMARY KEY, from_lat REAL NOT NULL, from_lng REAL NOT NULL, to_lat REAL NOT NULL, to_lng REAL NOT NULL, depart_at INTEGER NOT NULL, arrive_at INTEGER NOT NULL, seen_at INTEGER NOT NULL, spawn_at INTEGER, brg0 REAL, brg1 REAL, v0 REAL);
CREATE INDEX IF NOT EXISTS idx_hunt_birds_seen ON hunt_birds(seen_at);
CREATE TABLE IF NOT EXISTS hunt_worms (id TEXT PRIMARY KEY, lat REAL NOT NULL, lng REAL NOT NULL, value INTEGER NOT NULL DEFAULT 1, born_at INTEGER NOT NULL, gone_at INTEGER NOT NULL, caught_by TEXT, caught_at INTEGER);
CREATE INDEX IF NOT EXISTS idx_hunt_worms_live ON hunt_worms(gone_at) WHERE caught_by IS NULL;
-- added 2026-11-25 (bird turns): ALTER TABLE hunt_birds ADD COLUMN brg0 REAL; ALTER TABLE hunt_birds ADD COLUMN brg1 REAL;
-- added 2026-11-25 (tap to flap): ALTER TABLE hunt_birds ADD COLUMN v0 REAL;

-- 2026-11-26: each bird's colour for the public dots on the globe (set by the owner's page; roles override it)
ALTER TABLE hunt_birds ADD COLUMN col TEXT;

-- 2026-11-26: the game's bars: total distance flown (km) and each bird's home spot
ALTER TABLE hunt_birds ADD COLUMN flown REAL DEFAULT 0;
ALTER TABLE hunt_birds ADD COLUMN home_lat REAL;
ALTER TABLE hunt_birds ADD COLUMN home_lng REAL;

-- 2026-11-26: dinner: when the bird last ate its daily worm, and how many days it went without one (for starving, later)
ALTER TABLE hunt_birds ADD COLUMN fed_at INTEGER;
ALTER TABLE hunt_birds ADD COLUMN missed INTEGER DEFAULT 0;

-- 2026-11-26: left in the water: when its stamina runs out (then it drowns, washes up at home, loses its worms),
-- when the player was last told, and the drowning news for their next visit
ALTER TABLE hunt_birds ADD COLUMN wet_until INTEGER;
ALTER TABLE hunt_birds ADD COLUMN wet_note_at INTEGER;
ALTER TABLE hunt_birds ADD COLUMN drowned_at INTEGER;
ALTER TABLE hunt_birds ADD COLUMN drowned_lost INTEGER;
