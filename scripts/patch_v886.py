#!/usr/bin/env python3
"""Patch v884 -> v886: v885 plus extra recorder hooks (programmatic writes to the search box and URL changes).
(v885 notes follow.)
Patch v884 -> v885: stop the search box's cursor being drawn in the wrong place for a moment while typing.

Filmed on the user's iPhone (screen recording + iPhone Mirroring): about 250ms after a keystroke, when the search
is applied, the cursor is drawn up to ~2 characters too far right (typing) or left (deleting), then snaps back.
The recorder shows the real cursor position is always correct, so it's a drawing glitch.

At that moment the only thing that touches the search box is React rewriting its defaultValue (the value
attribute) to the newly applied search text. That has no visible effect once the user has typed, but makes
Safari recompute the box's text, and iOS draws the cursor from stale layout. Fix: while the box is focused, keep
passing the box's current defaultValue so React doesn't rewrite it. When it isn't focused the old behaviour
stays (the site clears or sets the box through .value anyway). Keeps v884's recorder for testing.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v884.js'
dst = '_deploy/assets/index-DUcNPOLc-v886.js'
content = open(src, encoding='utf-8').read()
old = 'key:`si`,ref:c,className:`search-input`,defaultValue:n,'
new = 'key:`si`,ref:c,className:`search-input`,defaultValue:(c.current&&document.activeElement===c.current)?c.current.defaultValue:n,'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
content = content.replace(old, new)
hook_old = "const ssr=HTMLInputElement.prototype.setSelectionRange;"
if content.count(hook_old) != 1:
    print('FAIL: recorder hook anchor'); sys.exit(1)
hook_new = hook_old + r"""
const vd=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');
Object.defineProperty(HTMLInputElement.prototype,'value',{configurable:true,enumerable:vd.enumerable,get(){return vd.get.call(this)},set(v){if(isS(this))add(T()+' JS SET value='+JSON.stringify(v)+' (was '+JSON.stringify(vd.get.call(this))+' c='+cur(this)+')');return vd.set.call(this,v)}});
const dd=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'defaultValue');
Object.defineProperty(HTMLInputElement.prototype,'defaultValue',{configurable:true,enumerable:dd.enumerable,get(){return dd.get.call(this)},set(v){if(isS(this))add(T()+' JS SET default='+JSON.stringify(v));return dd.set.call(this,v)}});
const sa=Element.prototype.setAttribute;Element.prototype.setAttribute=function(k,v){if(isS(this))add(T()+' ATTR '+k+'='+JSON.stringify(String(v).slice(0,40)));return sa.call(this,k,v)};
for(const m of ['pushState','replaceState']){const o=history[m].bind(history);history[m]=function(st,t,u){add(T()+' URL '+m+' '+String(u||'').replace(location.origin,'').slice(0,50));return o(st,t,u)}}
const ff=HTMLElement.prototype.focus;HTMLElement.prototype.focus=function(o){if(isS(this))add(T()+' JS focus()');return ff.call(this,o)};
const bb=HTMLElement.prototype.blur;HTMLElement.prototype.blur=function(){if(isS(this))add(T()+' JS blur()');return bb.call(this)};
"""
content = content.replace(hook_old, hook_new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
