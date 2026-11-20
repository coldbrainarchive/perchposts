#!/usr/bin/env python3
"""Patch v1273 -> v1274: Time filter + Flaps / Chirps ranking work together.
With a day (or "N h ago") picked, the ranking window ends there: That day / That week (7 days ending there) / All time
(everything before it). Sends rank_until to /get-posts; the buttons and the search-bar chip say "That day / That week"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1273.js'
dst = '_deploy/assets/index-DUcNPOLc-v1274.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# end of the picked window (ISO) from the time param: a date -> next midnight UTC; ago_N -> now - N h
c = c.replace("function _ppIco(k){", "function _ppRU(q){try{if(!q)return``;if(q.includes(`-`))return new Date(new Date(q).getTime()+86400000).toISOString();if(q.startsWith(`ago_`))return new Date(Date.now()-parseInt(q.slice(4))*3600000).toISOString()}catch(e){}return``}function _ppIco(k){", 1)
assert '_ppRU' in c
patch("fetch(`${R}/get-posts?sort=${_srt}&range=${_frg}`)",
      "fetch(`${R}/get-posts?sort=${_srt}&range=${_frg}${_ppRU(qT)?`&rank_until=${encodeURIComponent(_ppRU(qT))}`:``}`)", 'ranked fetch with window')
patch("},[_srt,_frg]),", "},[_srt,_frg,qT]),", 'refetch when time changes')
# the window already applies the time; don't also cut the ranked list to posts created that day
patch("filter(e=>{if(!qT||m||(TR!==null&&_bl0===TR))return!0;",
      "filter(e=>{if(!qT||m||(TR!==null&&_bl0===TR)||_srt===`flaps`||_srt===`chirps`)return!0;", 'no double time filter')
# dropdown buttons: That day / That week when a time is picked
for w in ['flaps', 'chirps']:
    patch("[[[`day`,`Today`],[`week`,`This week`],[`all`,`All time`]].map(([k,lb])=>_pill(_srt===`%s`" % w,
          "[[[`day`,q2?`That day`:`Today`],[`week`,q2?`That week`:`This week`],[`all`,`All time`]].map(([k,lb])=>_pill(_srt===`%s`" % w, 'buttons ' + w)
patch("(_frg===`day`?`today`:_frg===`all`?`all time`:`this week`)]}",
      "(_frg===`day`?(q2?`that day`:`today`):_frg===`all`?`all time`:(q2?`that week`:`this week`))]}", 'chip wording')
patch("posts ${_frg===`day`?`today `:_frg===`all`?``:`this week `}yet`}",
      "posts ${_frg===`day`?(qT?`that day `:`today `):_frg===`all`?(qT?`before then `:``):(qT?`that week `:`this week `)}${qT?``:`yet`}`}", 'empty message')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
