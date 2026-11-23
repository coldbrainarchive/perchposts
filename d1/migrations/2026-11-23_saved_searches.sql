-- Saved searches (user's request, 2026-11-23): up to 5 per account, JSON [{qs, def}] — qs is the search bar's
-- filters as a query string (flock, board, continent, country, utag, user, bot, q); def marks the default one.
ALTER TABLE mod_users ADD COLUMN saved_searches TEXT;
