#!/usr/bin/env python3
"""Patch v820 -> v821:
A chirp stays visible when the chirp it replied to was deleted. It shows "Original chirp deleted" where
the quote goes, has no Find button, and counts on feed cards (wr) the same as on the post page.
The phone preview gets "Pinned" and "Latest" titles when a post has pinned chirps, and none otherwise.
The list is drawn bottom up (column-reverse), so each title is pushed after the chirps it sits above.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v820.js'
dst = '_deploy/assets/index-DUcNPOLc-v821.js'

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

patch(t('let i=n||[],a=new Set;i.filter(e=>!e.parent_comment_id).forEach(e=>a.add(e.id));let o=!0;for(;o;)o=!1,i.forEach(e=>{!a.has(e.id)&&e.parent_comment_id&&a.has(e.parent_comment_id)&&(a.add(e.id),o=!0)});let s=i.filter(e=>a.has(e.id));d(s),'),
      t('let s=n||[];d(s),'),
      'keep replies to deleted chirps')
patch(t('function wr(e){let t=e||[],n=new Set;t.filter(e=>!e.parent_comment_id).forEach(e=>n.add(e.id));let r=!0;for(;r;)r=!1,t.forEach(e=>{!n.has(e.id)&&e.parent_comment_id&&n.has(e.parent_comment_id)&&(n.add(e.id),r=!0)});let i={};return t.filter(e=>n.has(e.id)).forEach(e=>{i[e.post_id]=(i[e.post_id]||0)+1}),i}'),
      t('function wr(e){let i={};return(e||[]).forEach(e=>{i[e.post_id]=(i[e.post_id]||0)+1}),i}'),
      'count them on feed cards')
patch(t('children:[w&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:[(0,L.jsx)(`span`,{className:`chat-quote-name`,children:T}),'),
      t('children:[e.parent_comment_id&&!w&&(0,L.jsx)(`div`,{className:`chat-quote-bar`,children:(0,L.jsx)(`p`,{className:`chat-quote-text`,style:{fontStyle:`italic`},children:`Original chirp deleted`})}),w&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:[(0,L.jsx)(`span`,{className:`chat-quote-name`,children:T}),'),
      'deleted note')
patch(t('e.parent_comment_id&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(e.parent_comment_id)},children:`Find`})'),
      t('w&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(e.parent_comment_id)},children:`Find`})'),
      'no Find without a parent')

patch(t('if(_pv)_rev=[..._rev.filter(_x=>!_x.pinned).slice(0,5),..._rev.filter(_x=>_x.pinned)];'),
      t('let _nl=0,_np=0,_st=_x=>(0,L.jsx)(`div`,{className:`chat-section-title`,children:_x},`st-`+_x);if(_pv){let _ps=_rev.filter(_x=>_x.pinned),_ls=_rev.filter(_x=>!_x.pinned).slice(0,5);_nl=_ls.length;_np=_ps.length;_rev=[..._ls,..._ps]}'),
      'preview sections')
patch(t('`dsep-`+_i));}});return _out;})()]}),_pv&&'),
      t('`dsep-`+_i));}if(_np){if(_i===_nl-1)_out.push(_st(`Latest`));if(_i===_rev.length-1)_out.push(_st(`Pinned`))}});return _out;})()]}),_pv&&'),
      'preview titles')
old = '.chat-msg-body.chat-pinned{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}'
patch(old, old + '.chat-section-title{font-size:12px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.07em;padding:6px 4px 4px}', 'title style')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
