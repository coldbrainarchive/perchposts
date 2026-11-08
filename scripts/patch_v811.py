#!/usr/bin/env python3
"""Patch v810 -> v811:
The post page's comment pill moves out of the row under the post and into the chat header.
Phone preview: the header comes back as a slim row with just the pill (Oldest/Newest stay hidden).
Desktop: the pill replaces the post title and the "N Chirps" text.
Phone full chat: back arrow, title and Oldest/Newest, with no count.
Feed cards keep their own pill.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v810.js'
dst = '_deploy/assets/index-DUcNPOLc-v811.js'

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

patch(t('(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{if(window.innerWidth<768){_openC();return}let e=document.querySelector(`.comments-shell`);e&&e.scrollIntoView({behavior:`smooth`}),setTimeout(()=>{let e=D.current;e&&(e.scrollTop=e.scrollHeight)},350)},children:[(0,L.jsx)(`span`,{children:`💬`}),(0,L.jsx)(`span`,{children:u.filter(_c=>_c.username!==`__system__`).length})]}),'),
      '', 'remove pill under post')

patch(t('(0,L.jsxs)(`span`,{className:`comments-panel-title`,onClick:_cf?_closeC:void 0,children:[_ct]}),(0,L.jsx)(`span`,{className:`chat-count`,children:`${_cn} Chirp${_cn===1?``:`s`}`})'),
      t('_cf?(0,L.jsxs)(`span`,{className:`comments-panel-title`,onClick:_closeC,children:[_ct]}):(0,L.jsxs)(`span`,{className:`feed-post-action-pill`,style:{cursor:`default`},"aria-label":`${_cn} chirp${_cn===1?``:`s`}`,children:[(0,L.jsx)(`span`,{children:`💬`}),(0,L.jsx)(`span`,{children:_cn})]})'),
      'pill in chat header')

patch('.chat-preview .chat-panel-header{display:none!important}',
      '.comments-shell.chat-preview .chat-panel-header{padding:12px 14px 2px;border-bottom:none;background:none}',
      'slim header in preview')
patch('.chat-count{flex:none;color:#94a3b8;font-size:13px;font-weight:600;white-space:nowrap;margin-right:10px}',
      '', 'remove count style')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
