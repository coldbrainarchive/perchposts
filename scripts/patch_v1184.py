#!/usr/bin/env python3
"""Patch v1183 -> v1184: a "🤖 Bot News" space (next to Flock) that shows only the bots' posts, newest first,
with load-older paging (worker ?bots=1). The Filters tab's Bots filter (All / Hide bots / Only bots) is removed:
Flock is the people-only view, Bot News the bots-only view."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1183.js'
dst = '_deploy/assets/index-DUcNPOLc-v1184.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("var nr=[{name:`Flock`,slug:`activity`,icon:`🪶`,virtual:!0},",
      "var nr=[{name:`Flock`,slug:`activity`,icon:`🪶`,virtual:!0},{name:`Bot News`,slug:`botnews`,icon:`🤖`,virtual:!0},", 'space in the list')
patch("const _SPACES=[`activity`,`feedback`,`cage`];", "const _SPACES=[`activity`,`botnews`,`feedback`,`cage`];", 'shown with the spaces')
patch("{activity:`#22d3ee`,general:", "{activity:`#22d3ee`,botnews:`#a5b4fc`,general:", 'colour')
patch("turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity&limit=50`:`${R}/get-posts?limit=50`;if(u&&u!==`activity`)turl+=",
      "turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity&limit=50`:u===`botnews`?`${R}/get-posts?bots=1&limit=50`:`${R}/get-posts?limit=50`;if(u&&u!==`activity`&&u!==`botnews`)turl+=", 'fetch bot posts')
patch("_url=_act?`${R}/get-posts?activity=1&sort=activity&limit=50`:`${R}/get-posts?limit=50`;if(u&&!_act)_url+=",
      "_url=_act?`${R}/get-posts?activity=1&sort=activity&limit=50`:u===`botnews`?`${R}/get-posts?bots=1&limit=50`:`${R}/get-posts?limit=50`;if(u&&!_act&&u!==`botnews`)_url+=", 'load older bot posts')
patch("b=_bl.filter(e=>u?y?fr.includes(e.username)?(e.comment_count??n[e.id]??0)>0||(i[e.id]?.voteCount??0)>0:!0:cr(e)===(sr(u)?.name||u):!0)",
      "b=_bl.filter(e=>u?y?fr.includes(e.username)?(e.comment_count??n[e.id]??0)>0||(i[e.id]?.voteCount??0)>0:!0:u===`botnews`?fr.includes(e.username)||!!(e.browser_id&&String(e.browser_id).startsWith(`bot-`)):cr(e)===(sr(u)?.name||u):!0)", 'keep only bot posts')
patch("(0,L.jsx)(`div`,{className:`search-section-label`,children:`🤖 Bots`}),(0,L.jsxs)(`div`,{className:`srch-row`,children:[_pill(!_botF,`All`,()=>_setParam(`bot`,``)),_pill(_botF===`hide`,`Hide bots`,()=>_setParam(`bot`,`hide`)),_pill(!!_botF&&_botF!==`hide`,`Only bots`,()=>_setParam(`bot`,`only`))]}),",
      "", 'no Bots filter')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
