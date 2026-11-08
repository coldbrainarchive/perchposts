-- Deleted accounts wait in the admin's Trash until brought back or deleted forever.
-- Names with no real account behind them have nothing to restore, so they count as already deleted forever.
ALTER TABLE mod_users ADD COLUMN deleted_by TEXT;
ALTER TABLE mod_users ADD COLUMN left_huddles TEXT;
ALTER TABLE mod_users ADD COLUMN purged_at TEXT;
UPDATE mod_users SET purged_at = deleted_at WHERE deleted_at IS NOT NULL AND password_hash = '';
