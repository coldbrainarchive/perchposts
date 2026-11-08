#!/usr/bin/env python3
"""Patch v435 -> v436:
Huddles only:
- Postcard: remove Leave and Invite buttons (keep only comment counter)
- Post page: reorder to comment counter, Invite, Leave, Delete
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v435.js'
dst = '_deploy/assets/index-DUcNPOLc-v436.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── POSTCARD ──────────────────────────────────────────────────────────────────
# Remove Leave button (postcard)
LEAVE_PC_START = '(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:t=>{t.preventDefault();t.stopPropagation();const _bid=Gn()'
LEAVE_PC_END   = 'children:`Leave`}),'

leave_s = content.find(LEAVE_PC_START)
if leave_s == -1:
    errors.append('FAIL: postcard Leave start not found');
else:
    leave_e = content.find(LEAVE_PC_END, leave_s) + len(LEAVE_PC_END)
    invite_s = leave_e  # Invite starts right after Leave

    # Remove Invite span (postcard) — ends just before comment counter link
    INV_PC_END_MARKER = '(0,L.jsxs)(I,{to:`/post/${e.id}`,state:{scrollToComments'
    invite_e = content.find(INV_PC_END_MARKER, invite_s)
    if invite_e == -1:
        errors.append('FAIL: postcard Invite end not found')
    else:
        # Remove both Leave and Invite from postcard
        content = content[:leave_s] + content[invite_e:]
        print('OK: postcard Leave + Invite removed')

# ── POST PAGE ─────────────────────────────────────────────────────────────────
# Extract Leave block, Invite block, then comment counter
# Then reassemble: comment_counter + Invite + Leave

PP_ACTIONS_MARKER = 'feed-post-actions`,children:['
pp_a = content.find(PP_ACTIONS_MARKER)
children_start = pp_a + len(PP_ACTIONS_MARKER)

LEAVE_PP_MARKER = 'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{const _un3='
LEAVE_PP_END    = 'children:`Leave`}),'
INV_PP_START_MARKER = 'c?.is_huddle&&(0,L.jsxs)(`span`,{style:{position:`relative`'
LIKE_PP_MARKER  = '!c?.is_huddle&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,style:re'
CC_PP_MARKER    = '(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{let e=document.querySelector(`.comments-shell`)'
CC_PP_END       = ']}),'   # ends before share/like button

leave_s2 = content.find(LEAVE_PP_MARKER, children_start)
leave_e2 = content.find(LEAVE_PP_END, leave_s2) + len(LEAVE_PP_END)
inv_s2   = content.find(INV_PP_START_MARKER, leave_e2)
like_s2  = content.find(LIKE_PP_MARKER, inv_s2)
cc_s2    = content.find(CC_PP_MARKER, like_s2)
cc_e2    = content.find(CC_PP_END, cc_s2) + len(CC_PP_END)

if any(x == -1 or x == len(CC_PP_END)-1 for x in [leave_s2, leave_e2, inv_s2, like_s2, cc_s2]):
    errors.append('FAIL: post page blocks not found')
else:
    leave_block  = content[leave_s2:leave_e2]
    invite_block = content[inv_s2:like_s2]
    cc_block     = content[cc_s2:cc_e2]

    # New order: [like (unchanged)] + cc_block + invite_block + leave_block + [rest unchanged]
    # Current: leave_block + invite_block + [like unchanged] + cc_block + [rest]
    # We splice: remove leave+invite from start, remove cc from middle, reinsert as cc+invite+leave
    pre       = content[children_start:leave_s2]         # anything before leave (empty)
    like_area = content[like_s2:cc_s2]                   # like button
    rest      = content[cc_e2:]                          # share, delete, etc.

    new_children = pre + like_area + cc_block + invite_block + leave_block + rest
    content = content[:children_start] + new_children
    print('OK: post page reordered to: comment counter, Invite, Leave, [Delete unchanged]')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
