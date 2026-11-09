#!/usr/bin/env python3
"""Patch v903 -> v904: 💬 Most chirps filter (Today / This week / All time), next to Most flaps.
?sort=chirps&range=day|week|all, served by the worker's get-posts?sort=chirps (posts now carry a "rank"
count for both flaps and chirps). Picking one replaces the other; the search-bar chip shows which.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v903.js'
dst = '_deploy/assets/index-DUcNPOLc-v904.js'
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

RK = '(_srt===`flaps`||_srt===`chirps`)'

# Feed
patch('if(_srt!==`flaps`){setFR(null);return}', 'if(!' + RK + '){setFR(null);return}', 'feed: fetch for both')
patch('get-posts?sort=flaps&range=${_frg}', 'get-posts?sort=${_srt}&range=${_frg}', 'feed: fetch sort')
patch('_bl0=m&&SR!==null?SR:_srt===`flaps`?(FR||[])', '_bl0=m&&SR!==null?SR:' + RK + '?(FR||[])', 'feed: base')
patch('_old.length&&!(_srt===`flaps`||_bot===`hide`)', '_old.length&&!(' + RK + '||_bot===`hide`)', 'feed: no older pages')
patch('return n===0?_srt===`flaps`?(t.flaps||0)-(e.flaps||0):', 'return n===0?' + RK + '?(t.rank||0)-(e.rank||0):', 'feed: sort by rank')
patch('_srt===`flaps`&&FR!==null&&b.length===0&&(0,L.jsx)(`div`,{style:{padding:`48px 20px`,textAlign:`center`,color:`#64748b`},'
      'children:_frg===`day`?`No flapped posts today yet`:_frg===`all`?`No flapped posts yet`:`No flapped posts this week yet`}),',
      RK + '&&FR!==null&&b.length===0&&(0,L.jsx)(`div`,{style:{padding:`48px 20px`,textAlign:`center`,color:`#64748b`},'
      'children:`No ${_srt===`flaps`?`flapped`:`chirped`} posts ${_frg===`day`?`today `:_frg===`all`?``:`this week `}yet`}),',
      'feed: empty text')
patch('_canMore&&_srt!==`flaps`&&', '_canMore&&!' + RK + '&&', 'feed: no Load older')

# Search box
patch('_setFlaps=k=>{let n=new URLSearchParams(e);if(_srt===`flaps`&&_frg===k){n.delete(`sort`);n.delete(`range`)}else{n.set(`sort`,`flaps`);n.set(`range`,k)}t(n)},',
      '_setRank=(so,k)=>{let n=new URLSearchParams(e);if(_srt===so&&_frg===k){n.delete(`sort`);n.delete(`range`)}else{n.set(`sort`,so);n.set(`range`,k)}t(n)},',
      'search: rank setter')
patch('[[[`day`,`Today`],[`week`,`This week`],[`all`,`All time`]].map(([k,lb])=>_pill(_srt===`flaps`&&_frg===k,lb,()=>_setFlaps(k)))]}),',
      '[[[`day`,`Today`],[`week`,`This week`],[`all`,`All time`]].map(([k,lb])=>_pill(_srt===`flaps`&&_frg===k,lb,()=>_setRank(`flaps`,k)))]}),'
      '(0,L.jsx)(`div`,{className:`search-section-label`,children:`💬 Most chirps`}),'
      '(0,L.jsxs)(`div`,{className:`srch-row`,children:'
      '[[[`day`,`Today`],[`week`,`This week`],[`all`,`All time`]].map(([k,lb])=>_pill(_srt===`chirps`&&_frg===k,lb,()=>_setRank(`chirps`,k)))]}),',
      'filters: chirps row')
patch('_srt===`flaps`&&(0,L.jsx)(`button`,{type:`button`,style:_chipS,',
      RK + '&&(0,L.jsx)(`button`,{type:`button`,style:_chipS,', 'chip: both')
patch('children:_frg===`day`?`🪽 Top today`:_frg===`all`?`🪽 Top all time`:`🪽 Top this week`}),',
      'children:(_srt===`flaps`?`🪽 Top flaps `:`💬 Top chirps `)+(_frg===`day`?`today`:_frg===`all`?`all time`:`this week`)}),',
      'chip: label')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
