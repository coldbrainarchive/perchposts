#!/usr/bin/env python3
"""Patch v900 -> v901: Flock goes back to the Boards tab (first, where it was); Most flaps gets
Today / This week / All time (?sort=flaps&range=day|week|all, week when range is missing).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v900.js'
dst = '_deploy/assets/index-DUcNPOLc-v901.js'
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

# Feed: fetch the chosen range
patch('_srt=l.get(`sort`)||``,', '_srt=l.get(`sort`)||``,_frg=l.get(`range`)||`week`,', 'feed: range param')
patch('fetch(`${R}/get-posts?sort=flaps`)', 'fetch(`${R}/get-posts?sort=flaps&range=${_frg}`)', 'feed: fetch range')
patch('return()=>{_c=!0}},[_srt]),', 'return()=>{_c=!0}},[_srt,_frg]),', 'feed: refetch on range change')
patch('children:`No flapped posts this week yet`',
      'children:_frg===`day`?`No flapped posts today yet`:_frg===`all`?`No flapped posts yet`:`No flapped posts this week yet`',
      'feed: empty text per range')

# Search: Flock back in Boards
patch('children:g.filter(x=>x.slug!==`activity`).map(', 'children:g.map(', 'boards: Flock back')

# Search: Sort row becomes Most flaps with three ranges
old_sort = ("(0,L.jsx)(`div`,{className:`search-section-label`,children:`Sort`}),"
            "(0,L.jsxs)(`div`,{className:`srch-row`,children:["
            "_pill(d===`activity`,`🪶 Flock`,()=>{if(d===`activity`)A();else ee(`activity`)}),"
            "_pill(_srt===`flaps`,`🪽 Most flaps · this week`,()=>_setParam(`sort`,_srt===`flaps`?``:`flaps`))]}),")
new_sort = ("(0,L.jsx)(`div`,{className:`search-section-label`,children:`🪽 Most flaps`}),"
            "(0,L.jsxs)(`div`,{className:`srch-row`,children:["
            "[[`day`,`Today`],[`week`,`This week`],[`all`,`All time`]].map(([k,lb])=>_pill(_srt===`flaps`&&_frg===k,lb,()=>_setFlaps(k)))]}),")
patch(old_sort, new_sort, 'filters: flaps ranges')
patch('_srt=e.get(`sort`)||``,',
      '_srt=e.get(`sort`)||``,_frg=e.get(`range`)||`week`,'
      '_setFlaps=k=>{let n=new URLSearchParams(e);if(_srt===`flaps`&&_frg===k){n.delete(`sort`);n.delete(`range`)}else{n.set(`sort`,`flaps`);n.set(`range`,k)}t(n)},',
      'search: range + setter')
# Chip shows the range; clearing removes both params
patch("onClick:ev=>{ev.stopPropagation(),_setParam(`sort`,``)},children:`🪽 Most flaps`}),",
      "onClick:ev=>{ev.stopPropagation();let n=new URLSearchParams(e);n.delete(`sort`);n.delete(`range`);t(n)},"
      "children:_frg===`day`?`🪽 Top today`:_frg===`all`?`🪽 Top all time`:`🪽 Top this week`}),",
      'chip: range label')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
