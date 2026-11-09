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
