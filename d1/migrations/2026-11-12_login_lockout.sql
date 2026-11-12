-- Login lockout: 10 wrong passwords in a row lock an account for 15 minutes (mods/admins can unlock).
ALTER TABLE mod_users ADD COLUMN failed_logins INTEGER NOT NULL DEFAULT 0;
ALTER TABLE mod_users ADD COLUMN locked_until TEXT;
