#!/usr/bin/env python3
"""Patch v1024 -> v1025: videos up to 100 MB.
- Uploads now send the file itself as the request body (?name=...), not wrapped in a form, so the server can stream
  videos straight into storage (cleaning them on the way) without holding them in memory. Progress rings still work.
- Size is checked on the phone before uploading: videos up to 100 MB, photos up to 50 MB after shrinking.
  Too big → the tile says "Too big · max 100 MB" (no Retry) with a message, instead of failing part way."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1024.js'
dst = '_deploy/assets/index-DUcNPOLc-v1025.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('x.open(`POST`,`${R}/upload`);const h=er()||{};for(const k in h)x.setRequestHeader(k,h[k]);',
      'x.open(`POST`,`${R}/upload?name=`+encodeURIComponent(file.name||`file`));const h=er()||{};for(const k in h)x.setRequestHeader(k,h[k]);x.setRequestHeader(`Content-Type`,file.type||`application/octet-stream`);',
      'send the bare file')
patch('const fd=new FormData;fd.append(`file`,file);x.send(fd)', 'x.send(file)', 'no form wrapper')
patch('async function _mtUpload(S,it){const g=S.gen;it.err=null;it.p=0;_mtEmit(S);',
      'async function _mtUpload(S,it){const g=S.gen;it.err=null;it.p=0;_mtEmit(S);if(it.type===`video`&&it.file.size>_MT_MAXV){_mtTooBig(S,it);return}',
      'videos checked before uploading')
patch('if(g!==S.gen||it.gone)return;if(it.type===`image`&&up===it.file&&',
      'if(g!==S.gen||it.gone)return;if(it.type===`image`&&up.size>_MT_MAXI){_mtTooBig(S,it);return}if(it.type===`image`&&up===it.file&&',
      'photos checked after shrinking')
patch('x.err===`heic`?', 'x.err===`big`?(0,L.jsxs)(`div`,{className:`mt-err mt-heic`,children:[`Too big`,(0,L.jsx)(`small`,{children:x.type===`video`?`max 100 MB`:`max 50 MB`})]}):x.err===`heic`?', 'too-big tile')
c += r'''
const _MT_MAXV=1e8,_MT_MAXI=5e7;
function _mtTooBig(S,it){it.err=`big`;it.xhr=null;_mtSync(S);const mb=Math.round(it.file.size/1e6);
 _hxToast(it.type===`video`?`That video is ${mb} MB — videos can be up to 100 MB (about 30 seconds of 4K, or 2 minutes of 1080p). Trim it or record in 1080p.`:`That photo is too big to upload (max 50 MB).`)}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
