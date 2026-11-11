#!/usr/bin/env python3
"""Patch v1009 -> v1010: no AutoFill bar (passwords / contacts) on the New Post text boxes, Post and Huddle side.
Every input / textarea in the New Post card is marked autocomplete="off" (plus the password-manager opt-outs);
the Add Birds and link boxes also skip auto-capitalise / auto-correct (they're names and URLs)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1009.js'
dst = '_deploy/assets/index-DUcNPOLc-v1010.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{
 const mark=()=>{document.querySelectorAll(`.nh-card input:not([data-naf]),.nh-card textarea:not([data-naf])`).forEach(el=>{if(el.type===`file`)return;el.dataset.naf=`1`;
  el.setAttribute(`autocomplete`,`off`);el.setAttribute(`aria-autocomplete`,`none`);el.setAttribute(`data-1p-ignore`,`true`);el.setAttribute(`data-lpignore`,`true`);el.setAttribute(`data-form-type`,`other`);
  if(!el.name)el.setAttribute(`name`,`pp-`+Math.random().toString(36).slice(2,8));
  const ph=el.placeholder||``;if(/Add Birds|URL/i.test(ph)){el.setAttribute(`autocapitalize`,`off`);el.setAttribute(`autocorrect`,`off`);el.spellcheck=!1}})};
 new MutationObserver(mark).observe(document.body,{childList:!0,subtree:!0});mark();
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
