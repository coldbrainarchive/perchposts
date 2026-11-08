#!/usr/bin/env python3
"""Patch v348 -> v350: new post form board/country picker → feed-filter style pills."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v348.js'
dst = '_deploy/assets/index-DUcNPOLc-v350.js'

content = open(src, encoding='utf-8').read()

# Find the two-column div start and the actual end of the whole expression including outer closings
start = content.find('(0,L.jsxs)(`div`,{style:{display:`flex`,minHeight:0},children:[!p&&')
end_anchor = ',(0,L.jsx)(`span`,{className:`feed-post-time`'
end = content.find(end_anchor, start)

if start == -1 or end == -1:
    print('FAIL: anchors not found')
    sys.exit(1)

# The outer tail that closes parent elements after the two-column div
outer_tail = ']})]})]})'

new_section = (
    # Outer grid
    '(0,L.jsxs)(`div`,{className:`search-columns`,children:['
        # LEFT: Boards column
        '!p&&(0,L.jsxs)(`div`,{className:`search-column`,children:['
            '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Boards`}),'
            'nr.filter(e=>!e.virtual).map(e=>'
                '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
                'onClick:()=>g(e.slug),'
                'style:{outline:`none`,boxShadow:e.slug===h?`0 0 0 2px #c084fc`:`none`,borderRadius:999},'
                'children:(0,L.jsx)(Ar,{boardName:e.name,small:!0})}'
            ',e.slug))'
        ']})'
        ','
        # RIGHT: Region / Country column
        '(0,L.jsxs)(`div`,{className:`search-column`,children:['
            'S?'
            # Country drilldown
            '(0,L.jsxs)(L.Fragment,{children:['
                '(0,L.jsxs)(`div`,{className:`search-section-label`,style:{display:`flex`,alignItems:`center`,gap:4},children:['
                    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>C(null),'
                    'style:{background:`none`,border:`none`,color:`#c084fc`,fontSize:11,fontWeight:700,cursor:`pointer`,padding:0},'
                    'children:`← Back`}),'
                    '(0,L.jsx)(`span`,{children:S})'
                ']}),'
                'or.filter(e=>ar[e.name]===S).map(e=>'
                    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
                    'onClick:()=>{y(e.name);C(null);},'
                    'style:{outline:`none`,boxShadow:e.name===v?`0 0 0 2px #c084fc`:`none`,borderRadius:999},'
                    'children:(0,L.jsx)(kr,{country:e.name,small:!0})}'
                ',e.name))'
            ']})'
            ':'
            # Region list
            '(0,L.jsxs)(L.Fragment,{children:['
                '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Region`}),'
                'rr.filter(e=>e!==`World`).map(e=>'
                    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
                    'onClick:()=>C(e),'
                    'style:{outline:`none`,borderRadius:999},'
                    'children:(0,L.jsx)(kr,{continent:e,small:!0})}'
                ',e))'
            ']})'
        ']})'
    ']})'
    + outer_tail
)

content = content[:start] + new_section + content[end:]

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

if p_diff != 0 or b_diff != 2:
    print('ERROR: bracket mismatch (expected p=0, b=2 to match baseline)')
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'OK — Wrote {dst}')
