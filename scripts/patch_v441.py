#!/usr/bin/env python3
"""Patch v440 -> v441:
Replace floating invite dropdown with an inline invite picker in the post body,
mirroring the new-post-form Add Birds mechanic.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v440.js'
dst = '_deploy/assets/index-DUcNPOLc-v441.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Simplify the Invite span in actions → plain button, no dropdown ────────
# Remove the span wrapper + floating dropdown, keep just the toggle button
OLD_INV_SPAN = ('c?.is_huddle&&(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`},'
                'children:[(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
                'onClick:()=>{_setWpInvOpen(v=>!v);_setWpInvQ(``);_setWpInvR([]);},children:`Invite`}),'
                '_wpInvOpen&&(0,L.jsxs)(`div`,{style:{position:`absolute`,bottom:`calc(100% + 6px)`,left:0,'
                'background:`#1a1d27`,border:`1px solid #374151`,borderRadius:10,padding:10,zIndex:100,'
                'minWidth:240,boxShadow:`0 4px 20px rgba(0,0,0,0.4)`},onClick:t=>{t.stopPropagation();},')
NEW_INV_SPAN = ('c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
                'onClick:()=>{_setWpInvOpen(v=>!v);_setWpInvQ(``);_setWpInvR([]);_setWpInvP(null);},children:_wpInvOpen?`✕ Cancel`:`Invite`}),!c?.is_huddle&&(0,L.jsx)(`div`,{style:{display:`none`},')
if OLD_INV_SPAN in content:
    content = content.replace(OLD_INV_SPAN, NEW_INV_SPAN, 1)
    print('OK: Invite span → plain toggle button')
else:
    errors.append('FAIL: Invite span not found')

# ── 2. Remove the rest of the old dropdown (its closing brackets) ─────────────
# The dropdown's closing was: `)})]})]}),c?.is_huddle&&(Leave button)`
# After removing the span opening in step 1, the dropdown body + closing brackets remain.
# Find and remove the dropdown body up to its closing point.
# The dropdown closing before Leave: `)})]})]}),c?.is_huddle`
# Now with the bad prefix replaced we need to close the fake div we used as placeholder.
# Actually let's find what remains from the old dropdown body after step 1.
# The old dropdown children were: [label, input, results_list]
# These now appear orphaned. Find the closing of the old dropdown.
OLD_DROP_CLOSE = 'children:[(0,L.jsx)(`div`,{style:{fontSize:11,color:`#94a3b8`,marginBottom:6},children:`Add to huddle:`})'
DROP_END       = ')})]})]}),c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{const _un3='
drop_s = content.find(OLD_DROP_CLOSE)
drop_e = content.find(DROP_END, drop_s) + len('),')  # keep the comma
if drop_s != -1 and drop_e > len('),'):
    # Remove from OLD_DROP_CLOSE through the closing brackets, replace the placeholder div with nothing
    # Also need to remove the fake div we injected: !c?.is_huddle&&(0,L.jsx)(`div`,{style:{display:`none`},...)
    # The placeholder div goes until DROP_END too
    old_placeholder = content[drop_s:drop_e]
    content = content[:drop_s] + content[drop_e-len(','):]
    print('OK: old dropdown body removed')
else:
    errors.append('FAIL: old dropdown body not found')

# ── 3. Insert inline invite picker just before the actions div ─────────────────
# Insertion point: the IIFE body close + attachment + actions start
BEFORE_ACTIONS = ']})})(),'
ACTIONS_START  = '(0,L.jsxs)(`div`,{className:`feed-post-actions`'
insert_pt      = content.find(BEFORE_ACTIONS + ACTIONS_START, 355000)
if insert_pt == -1:
    errors.append('FAIL: insertion point before actions not found')
else:
    # Build the inline invite picker UI
    # Reuses _wpInvQ, _wpInvR, _wpInvP states
    # Fetch logic mirrors the old dropdown
    INVITE_UI = (
        # Outer conditional: only show when huddle + invite open
        'c?.is_huddle&&_wpInvOpen&&(0,L.jsxs)(`div`,{style:{marginTop:8,padding:`10px 14px`,'
        'background:`#1a1d27`,borderRadius:12,border:`1px solid #374151`},'
        'children:['
          # Search bar row with tagged pill + input
          '(0,L.jsxs)(`div`,{className:`search-bar`,style:{marginBottom:_wpInvR.length>0||_wpInvP?6:0},'
          'children:['
            # Show pending user as a removable pill
            '_wpInvP&&(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
            'onClick:()=>{_setWpInvP(null);},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},'
            'children:[(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,'
            'padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
            'background:_wpInvP.role===`admin`?`#ffffff`:Hn(_wpInvP.browser_id||null,_wpInvP.username),'
            'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1},'
            'children:[(()=>{const _jd=Jn({username:_wpInvP.username,browser_id:_wpInvP.browser_id||null,is_admin:_wpInvP.role===`admin`})||{};'
            'return _jd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}}):'
            '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`🐦`});})()'
            ',(0,L.jsx)(`span`,{children:_wpInvP.username})]})]}),'
            # Search input
            '(0,L.jsx)(`input`,{className:`search-input`,value:_wpInvQ,'
            'onChange:t=>{_setWpInvQ(t.target.value);clearTimeout(_wpInvTimer.current);'
            '_wpInvTimer.current=setTimeout(()=>{if(t.target.value.trim()){'
            'fetch(`${R}/search-users?q=${encodeURIComponent(t.target.value.trim())}`)'
            '.then(_r=>_r.ok?_r.json():{users:[]}).then(_d=>_setWpInvR(_d.users||[])).catch(()=>_setWpInvR([]));}else{_setWpInvR([]);}},300);},'
            'placeholder:`Add Birds`})'
          ']})'
          # Search results
          ',_wpInvR.length>0&&!_wpInvP&&(0,L.jsx)(`div`,{style:{maxHeight:120,overflowY:`auto`,marginBottom:4},'
          'children:_wpInvR.filter(_u=>{const _em=[c.username,...JSON.parse(c.huddle_members||`[]`)'
          '.map(_m=>{const _ci=(_m||``).lastIndexOf(`:`);if(_ci>0){const _r=_m.slice(_ci+1);if(_r===`admin`||_r===`mod`)return _m.slice(0,_ci);}return _m||``;})];'
          'return!_em.some(_e=>(_e||``).toLowerCase()===(_u.username||``).toLowerCase());}).slice(0,6)'
          '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
          'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
          'onClick:()=>{_setWpInvP(_u);_setWpInvQ(``);_setWpInvR([]);},'
          'children:(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,padding:`0 7px`,'
          'borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
          'background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username),'
          'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1},'
          'children:[(()=>{const _jd=Jn({username:_u.username,browser_id:_u.browser_id||null,is_admin:_u.role===`admin`})||{};'
          'return _jd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}}):'
          '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`🐦`});})()'
          ',(0,L.jsx)(`span`,{children:_u.username})]})},'
          '_u.username))})'
          # Invite confirm button
          ',_wpInvP&&(0,L.jsx)(`button`,{type:`button`,'
          'style:{width:`100%`,marginTop:8,padding:`8px`,borderRadius:8,border:`none`,'
          'background:`#c084fc`,color:`#fff`,fontWeight:700,fontSize:13,cursor:`pointer`},'
          'onClick:()=>{fetch(`${R}/invite-to-huddle`,{method:`POST`,'
          'headers:{"Content-Type":`application/json`,...er()},'
          'body:JSON.stringify({post_id:c.id,'
          'invite_username:(_wpInvP.role===`admin`||_wpInvP.role===`mod`)?`${_wpInvP.username}:${_wpInvP.role}`:_wpInvP.username,'
          'browser_id:Gn()})}).then(async _r=>{if(_r.ok){'
          'const _ij=await _r.json().catch(()=>({}));if(_ij.post)l(Cr(_ij.post));'
          'const _sc=_ij.systemComment||{id:`__sys_${Date.now()}`,content:`👥 ${_wpInvP.username} was added to the huddle`,'
          'username:`__system__`,created_at:new Date().toISOString(),browser_id:null,parent_comment_id:null,is_mod:0};'
          'd(e=>[...e,_sc]);_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);_setWpInvP(null);}});},'
          'children:`Invite `+_wpInvP.username})'
        ']})'
        ','
    )
    insert_at = insert_pt + len(BEFORE_ACTIONS)
    content = content[:insert_at] + INVITE_UI + content[insert_at:]
    print('OK: inline invite picker inserted before actions div')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
