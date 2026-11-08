#!/usr/bin/env python3
"""Patch v835 -> v836: deleted accounts move from a separate Trash card into the Flock list, greyed out at
the bottom, with a Deleted sort that brings them to the top. The self delete message now warns the profile
could be gone forever, rather than promising it can come back.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v835.js'
dst = '_deploy/assets/index-DUcNPOLc-v836.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('`Your posts and chirps stay on the site, shown as Extinct Bird, and you won\'t be able to sign in. An admin can bring your account back if you ask. Delete anything you want gone first.`'),
      t('`Your profile could be gone forever. Your posts and chirps stay on the site, shown as Extinct Bird, and you won\'t be able to sign in. Delete anything you want gone first.`'), 'self delete wording')

# the old card goes
a = content.index(t('_tr.length>0&&(0,L.jsxs)(`div`,{className:`content-card account-trash`'))
end = t(']},_a.id))]}),')
b = content.index(end, a) + len(end)
content = content[:a] + content[b:]
print('OK: remove trash card')

ROW = ('let _dr=_tr.filter(_a=>!se.trim()||(_a.username||``).toLowerCase().includes(se.toLowerCase())).map(_a=>(0,L.jsxs)(`div`,{className:`flock-deleted`,style:{display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`,padding:`12px 20px`,borderBottom:`1px solid #2e303a`,background:`rgba(148,163,184,0.04)`},children:['
       '(0,L.jsxs)(`div`,{style:{flex:1,minWidth:170,opacity:.55,pointerEvents:`none`},children:[(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6,flexWrap:`wrap`},children:[(0,L.jsx)(Xn,{record:{username:`Extinct Bird`},name:_a.username,color:`#9ca3af`}),(0,L.jsx)(`span`,{style:{fontSize:10,fontWeight:700,color:`#94a3b8`,background:`rgba(100,116,139,0.18)`,padding:`1px 6px`,borderRadius:999},children:`DELETED`})]}),(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:11,marginTop:4},children:(_a.deleted_by===`self`?`Deleted their account`:`Deleted by a mod`)+` · `+Un(_a.deleted_at)})]}),'
       '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6},children:[(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Bring ${_a.username} back?`))return;let _r=await fetch(`${R}/restore-member`,{method:`POST`,headers:{"Content-Type":`application/json`,...$n()},body:JSON.stringify({user_id:_a.id})});if(!_r.ok)alert(`Could not bring them back`);_e()},style:{padding:`4px 10px`,borderRadius:6,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:11,cursor:`pointer`,whiteSpace:`nowrap`},children:`Bring back`}),'
       '(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Delete ${_a.username} forever? They can never come back. Their posts stay as Extinct Bird and the name stays retired.`))return;let _r=await fetch(`${R}/purge-member`,{method:`POST`,headers:{"Content-Type":`application/json`,...$n()},body:JSON.stringify({user_id:_a.id})});if(!_r.ok)alert(`Could not delete them`);_e()},style:{padding:`4px 10px`,borderRadius:6,border:`1px solid #374151`,background:`transparent`,color:`#f87171`,fontWeight:600,fontSize:11,cursor:`pointer`,whiteSpace:`nowrap`},children:`Delete forever`})]})]},_a.id));')

patch(t('return n(t.user_metadata?.role)-n(e.user_metadata?.role)}return 0});return(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16},children:[(0,L.jsxs)(`div`,{style:{padding:`14px 20px`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`},children:[(0,L.jsxs)(`h3`,{style:{margin:0,color:`#f8fafc`,fontSize:16,fontWeight:700,marginRight:`auto`},children:[`Flock `,'),
      t('return n(t.user_metadata?.role)-n(e.user_metadata?.role)}return 0});' + ROW + 'return(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16},children:[(0,L.jsxs)(`div`,{style:{padding:`14px 20px`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`},children:[(0,L.jsxs)(`h3`,{style:{margin:0,color:`#f8fafc`,fontSize:16,fontWeight:700,marginRight:`auto`},children:[`Flock `,'),
      'deleted rows')
patch(t('(0,L.jsx)(`option`,{value:`mod`,children:`Mods first`})]})]}),(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,maxHeight:480,overflowY:`auto`},children:[t.length===0&&'),
      t('(0,L.jsx)(`option`,{value:`mod`,children:`Mods first`}),_tr.length>0&&(0,L.jsx)(`option`,{value:`deleted`,children:`Deleted`})]})]}),(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,maxHeight:480,overflowY:`auto`},children:[F===`deleted`&&_dr,t.length===0&&'),
      'deleted sort')
patch(t('`Delete ${i||`this flock member`}? They\'ll go to the Trash, where an admin can bring them back.`'),
      t('`Delete ${i||`this flock member`}? They\'ll stay greyed out in the Flock, where an admin can bring them back.`'), 'mod delete wording')

# rows go at the end of the list unless sorting by Deleted
a = content.index(t('[F===`deleted`&&_dr,t.length===0&&'))
end = t('children:`Delete`})]})]},n.id)})]})]})})(),')
if content.count(end) != 1:
    errors.append('FAIL (end of list)')
else:
    content = content.replace(end, t('children:`Delete`})]})]},n.id)}),F!==`deleted`&&_dr]})]})})(),'))
    print('OK: rows at the end')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
