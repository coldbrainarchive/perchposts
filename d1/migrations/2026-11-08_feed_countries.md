# 2026-11-08: every bot post has a country

Region tabs go by tags, plus headlines naming the region or one of its countries (regionTerms; Georgia, Jordan, Chad, Turkey are tags only). Country pills use the same whole-word rule for their own name (countryTerms). Each bot feed has a country, its outlet's home,
and a region, what it covers: BBC Africa is United Kingdom + Africa. A post's region is its own tag,
else its country's home region. A country pill keeps to that country's home region (`countryWhere`).

Data changes (no schema change):
- `bot_config`: the 16 feeds with a region but no country got one: BBC desks, FT and Guardian World:
  United Kingdom; NYT World, Al-Monitor, ScienceDaily: United States; SCMP: Hong Kong (new, Asia);
  MercoPress: Uruguay; Africanews: France (Lyon since 2020).
- `posts`: 18,209 old bot posts from those feeds got the same country, matched on their own link and
  updated in rowid chunks. Undo: set country back to NULL where continent is set and the link is one of
  those outlets (or use Time Travel to 2026-11-08 before the change).

Also on 2026-11-08: 14 missed crash-era repeats of one FT link (`ig.ft.com/ai-tokens/`, posted hourly on
2026-10-02, rowids 161117 to 173822, no chirps or wings) were permanently deleted; rowid 160138 was kept.
