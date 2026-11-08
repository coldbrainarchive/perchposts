# Removed bot duplicates (2026-11-05)

120,275 repeat bot posts were permanently deleted, nearly all reposted during the crashes of 16 Sept
to 5 Oct. One post was kept per article: a copy with chirps or wings if there was one, otherwise the
oldest. None of the deleted posts had any activity. The database went from 272MB to 157MB.

To get them back, D1 Time Travel can restore the whole database until about 2026-12-05, which also
undoes everything since then:
`wrangler d1 time-travel restore daboysforum-db --bookmark=00002c6c-000012ac-0000511a-f0aaaa816faadfb5a265cbcd4bb8edd9`

Repeats are now refused by `/create-post` using the bot_links table, whose keys are `l:` plus a cleaned
link (kept forever) and `t:` plus a cleaned headline (blocks for 6 days).
