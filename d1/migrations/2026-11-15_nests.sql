-- Sign-up nests: every device gets 5 usernames (eggs) at a time, and a fresh set only every 15 minutes.
-- Sign-up only accepts a name from the device's own nest. net is the keyed IP hash, used for a looser cap per network
-- so clearing the browser doesn't hand out endless eggs. Rows are deleted on sign-up and after 2 days.
CREATE TABLE IF NOT EXISTS nests (
  device    TEXT PRIMARY KEY,
  net       TEXT,
  names     TEXT NOT NULL,
  prev      TEXT,
  issued_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_nests_net    ON nests(net, issued_at);
CREATE INDEX IF NOT EXISTS idx_nests_issued ON nests(issued_at);
