#!/usr/bin/env python3
"""Patch v993 -> v994: huddle inbox fixes.
- Admin/mod birds get their real colour (white / purple) on huddle cards and in the members sheet even when the
  huddle's member list doesn't carry their role (or they aren't a member), using the same admin/mod lists as
  notifications.
- Opening a huddle always tells the server how far this device has already read, so badges for huddles you'd
  read before the update clear as soon as you open them.
- A card clears its badge when this device has read past the newest unread chirp (not the last line, which can be
  a system line like "back in the huddle")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v993.js'
dst = '_deploy/assets/index-DUcNPOLc-v994.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('function _hxCol(m){return m.role===`admin`?',
      'function _hxRole(m){const l=String(m&&m.username||``).toLowerCase();return _adminUsers.has(l)?`admin`:_modUsers.has(l)?`mod`:m&&m.role||null}\n'
      'function _hxCol(m){m={...m,role:_hxRole(m)};return m.role===`admin`?', 'role from admin/mod lists')
patch('function _hxFace(m,sz){const b=', 'function _hxFace(m,sz){m={...m,role:_hxRole(m)};const b=', 'face uses role')
patch('const loc=_rdGet(e.id),caught=!!(hx&&hx.last&&loc&&loc>=hx.last.t&&unread);',
      'const loc=_rdGet(e.id),caught=!!(hx&&unread&&loc&&loc>=(hx.nt||hx.last&&hx.last.t||`~`));', 'caught vs newest unread')
patch('if(t&&t.is_huddle)_hxIds.add(r);', 'if(t&&t.is_huddle){_hxIds.add(r);const _l=_rdGet(r);_l&&_hxPost(r,_l)}', 'send local read on open')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
