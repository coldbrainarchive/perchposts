#!/usr/bin/env python3
"""Patch v892 -> v893: stop the iPhone search cursor jumping on keyword (non-tag) searches.
Filmed on the user's iPhone with v892 (feed no longer changes while typing): typing "ethan" still drew the
cursor a letter too far right for ~0.3s. The suggestions box (#_urd, a scrollable overlay) hides itself as soon
as the text stops matching any board/region/country/user, and hiding or showing that layer is what makes iOS
misdraw the cursor (tag words keep it open, which is why they were fine).
Fix: while there's text in the box, the suggestions box stays open; when nothing matches it shows a single
"Search posts for ..." row (tapping it, or the keyboard's Search key, runs the keyword search).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v892.js'
dst = '_deploy/assets/index-DUcNPOLc-v893.js'
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

# 1. Keep the box visible whenever there's text.
patch("id:`_urd`,style:(S||C||P||w||T||UR.length>0)?void 0:",
      "id:`_urd`,style:(S||C||P||w||T||UR.length>0||n.trim())?void 0:",
      'stay open with text')

# 2. "Search posts for ..." row when nothing else matches.
ROW = ("n.trim()&&!(C||P||w||T||UR.length>0)&&(0,L.jsxs)(`button`,{type:`button`,onClick:()=>{a(!1);c.current&&c.current.blur()},"
       "style:{display:`flex`,alignItems:`center`,gap:8,width:`100%`,minHeight:38,padding:`8px 44px 8px 38px`,background:`none`,border:`none`,"
       "color:`#cbd5e1`,fontSize:13,textAlign:`left`,cursor:`pointer`,boxSizing:`border-box`,overflow:`hidden`},"
       "children:[(0,L.jsx)(`span`,{children:`🔍`}),(0,L.jsx)(`span`,{style:{whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`},"
       "children:`Search posts for “`+n.trim()+`”`})]}),")
patch("_u.username))})]}),]})]})]})})}function Rr(",
      "_u.username))})]})," + ROW + "]})]})]})})}function Rr(",
      'search posts row')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
