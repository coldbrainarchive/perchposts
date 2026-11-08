#!/usr/bin/env python3
"""Patch v569 -> v570: Video poster generation.
At upload time (both comment and new-post), capture the first frame via Canvas,
upload it as a JPEG to R2, and store poster URL in the attachment JSON.
PostAttachment (Fr) and the compose preview video both use poster= attribute.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v569.js'
dst = '_deploy/assets/index-DUcNPOLc-v570.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# ── Shared canvas helper (reused as a string in both upload patches) ──
# Generates a poster blob from a video File and resolves it (or null on error)
POSTER_HELPER = (
    'let _isVid=!_ff.type.startsWith(`image/`);'
    'let _getPoster=_isVid?new Promise(_res=>{'
      'let _pv=document.createElement(`video`),'
          '_pu=URL.createObjectURL(_ff);'
      '_pv.muted=!0;_pv.playsInline=!0;'
      '_pv.onloadedmetadata=()=>{_pv.currentTime=0.1};'
      '_pv.onseeked=()=>{'
        'let _pc=document.createElement(`canvas`);'
        '_pc.width=_pv.videoWidth||320;'
        '_pc.height=_pv.videoHeight||240;'
        '_pc.getContext(`2d`).drawImage(_pv,0,0);'
        '_pc.toBlob(_b=>{URL.revokeObjectURL(_pu);_res(_b)},`image/jpeg`,0.7)'
      '};'
      '_pv.onerror=()=>{URL.revokeObjectURL(_pu);_res(null)};'
      '_pv.src=_pu'
    '}):Promise.resolve(null);'
)

POSTER_UPLOAD_AND_SET_CA = (
    '_getPoster.then(async _pb=>{'
      'let _pu2=null;'
      'if(_pb){'
        'let _pfd=new FormData;'
        '_pfd.append(`file`,new File([_pb],`poster.jpg`,{type:`image/jpeg`}));'
        'let _pr=await fetch(`${R}/upload`,{method:`POST`,body:_pfd}).then(_r=>_r.json()).catch(()=>null);'
        'if(_pr?.url)_pu2=_pr.url'
      '}'
      'return fetch(`${R}/upload`,{method:`POST`,body:_fd})'
        '.then(_fr=>_fr.json())'
        '.then(_fj=>{'
          'if(!_fj.url)throw Error(_fj.error||`Upload failed`);'
          '_setCA({type:_isVid?`video`:`image`,url:_fj.url,...(_pu2?{poster:_pu2}:{})})'
        '})'
    '}).catch(_fErr=>alert(`Upload failed: `+_fErr.message)).finally(()=>_setCUL(!1))'
)

# ── 1. Comment upload handler: add poster generation ──
patch(
    '_fd.append(`file`,_ff);fetch(`${R}/upload`,{method:`POST`,body:_fd}).then(_fr=>_fr.json()).then(_fj=>{if(!_fj.url)throw Error(_fj.error||`Upload failed`);_setCA({type:_ff.type.startsWith(`image/`)?`image`:`video`,url:_fj.url})}).catch(_fErr=>alert(`Upload failed: `+_fErr.message)).finally(()=>_setCUL(!1))',
    '_fd.append(`file`,_ff);' + POSTER_HELPER + POSTER_UPLOAD_AND_SET_CA,
    'comment upload generates poster'
)

# ── 2. New post upload handler M: add poster generation ──
patch(
    'let n=new FormData;n.append(`file`,e);let r=await fetch(`${R}/upload`,{method:`POST`,body:n}),i=await r.json();if(!r.ok)throw Error(i.error||`Upload failed`);E({type:t,url:i.url}),D(null)',
    (
        'let _vp2=null;'
        'if(t===`video`){'
          'const _pb2=await new Promise(_res=>{'
            'let _pv2=document.createElement(`video`),'
                '_pu3=URL.createObjectURL(e);'
            '_pv2.muted=!0;_pv2.playsInline=!0;'
            '_pv2.onloadedmetadata=()=>{_pv2.currentTime=0.1};'
            '_pv2.onseeked=()=>{'
              'let _pc2=document.createElement(`canvas`);'
              '_pc2.width=_pv2.videoWidth||320;'
              '_pc2.height=_pv2.videoHeight||240;'
              '_pc2.getContext(`2d`).drawImage(_pv2,0,0);'
              '_pc2.toBlob(_b=>{URL.revokeObjectURL(_pu3);_res(_b)},`image/jpeg`,0.7)'
            '};'
            '_pv2.onerror=()=>{URL.revokeObjectURL(_pu3);_res(null)};'
            '_pv2.src=_pu3'
          '});'
          'if(_pb2){'
            'let _pfd2=new FormData;'
            '_pfd2.append(`file`,new File([_pb2],`poster.jpg`,{type:`image/jpeg`}));'
            'const _pr2=await fetch(`${R}/upload`,{method:`POST`,body:_pfd2}).then(_r=>_r.json()).catch(()=>null);'
            'if(_pr2?.url)_vp2=_pr2.url'
          '}'
        '}'
        'let n=new FormData;n.append(`file`,e);'
        'let r=await fetch(`${R}/upload`,{method:`POST`,body:n}),i=await r.json();'
        'if(!r.ok)throw Error(i.error||`Upload failed`);'
        'E({type:t,url:i.url,...(_vp2?{poster:_vp2}:{})}),D(null)'
    ),
    'new post upload generates poster'
)

# ── 3. Fr (PostAttachment): add poster to destructure + video element ──
patch(
    'function Fr({attachment:e,postId:o}){if(!e)return null;let{type:t,url:n,title:r,description:i,image:a}=e;',
    'function Fr({attachment:e,postId:o}){if(!e)return null;let{type:t,url:n,title:r,description:i,image:a,poster:_vpost}=e;',
    'Fr destructures poster'
)

patch(
    'controls:!0,playsInline:!0,preload:`metadata`,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}',
    'controls:!0,playsInline:!0,preload:`metadata`,...(_vpost?{poster:_vpost}:{}),style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}',
    'Fr video uses poster attribute'
)

# ── 4. Compose preview video: add poster from _cA.poster ──
patch(
    'src:_cA.url,style:{maxHeight:72,maxWidth:128,borderRadius:8},muted:!0,preload:`metadata`,onLoadedMetadata:_ve=>{_ve.target.currentTime=0.1}',
    'src:_cA.url,...(_cA.poster?{poster:_cA.poster}:{}),style:{maxHeight:72,maxWidth:128,borderRadius:8},muted:!0,preload:`metadata`,onLoadedMetadata:_ve=>{_ve.target.currentTime=0.1}',
    'compose preview video uses poster'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
