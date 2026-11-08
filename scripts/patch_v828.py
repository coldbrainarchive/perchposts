#!/usr/bin/env python3
"""Patch v827 -> v828: on the phone preview, tapping a chirp opens the full chat centred on that chirp,
and tapping a photo or video in a chirp opens it in place instead of opening the chat.
Centring repeats for the first second because the chat resizes as it opens and photos load in, and it
stops at the first touch or wheel so it can't fight the person scrolling.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v827.js'
dst = '_deploy/assets/index-DUcNPOLc-v828.js'

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

patch(t('onClickCapture:_pv?_ev=>{_ev.stopPropagation();_ev.preventDefault();_openC()}:void 0'),
      t('onClickCapture:_pv?_ev=>{let _tg=_ev.target;if(_tg.closest(`.chat-bubble`)&&(_tg.tagName===`VIDEO`||_tg.tagName===`IMG`&&_tg.style.cursor===`zoom-in`))return;_ev.stopPropagation();_ev.preventDefault();_fid.current=_tg.closest(`.chat-msg`)?.dataset.commentId||null;_openC()}:void 0'),
      'preview taps')
patch(t('_ckR=(0,_.useRef)(null);'), t('_ckR=(0,_.useRef)(null),_fid=(0,_.useRef)(null);'), 'target ref')
patch(t('(0,_.useEffect)(()=>{if(!_cf)return;let _y=_cyR.current,'),
      t('(0,_.useEffect)(()=>{if(!_cf||!_fid.current)return;let _id=_fid.current,_w=D.current;_fid.current=null;if(!_w)return;let _go=()=>{let _n=_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n)return;let _a=_n.getBoundingClientRect(),_b=_w.getBoundingClientRect();_w.scrollTop+=_a.top-_b.top-Math.max(0,(_w.clientHeight-_a.height)/2)},_tm=[0,150,500,1000].map(_x=>setTimeout(_go,_x)),_st=()=>_tm.forEach(clearTimeout);_w.addEventListener(`touchstart`,_st,{passive:!0});_w.addEventListener(`wheel`,_st,{passive:!0});return()=>{_st();_w.removeEventListener(`touchstart`,_st);_w.removeEventListener(`wheel`,_st)}},[_cf]),(0,_.useEffect)(()=>{if(!_cf)return;let _y=_cyR.current,'),
      'centre on open')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
