#!/usr/bin/env python3
"""Patch v85 -> v88: three-word bird username generator for signup."""
import re, sys

src = '_deploy/assets/index-DUcNPOLc-v85.js'
dst = '_deploy/assets/index-DUcNPOLc-v88.js'

content = open(src, encoding='utf-8').read()

BIRD_GEN = (
    '(function(){'
    'var _a=["african","american","asian","ashy","banded","barred","black","blue","brown",'
    '"chestnut","collared","common","crested","dark","dusky","eastern","elegant","eurasian",'
    '"european","golden","greater","green","grey","hooded","indian","lesser","little","long",'
    '"northern","olive","orange","pacific","painted","pale","purple","red","rufous","scarlet",'
    '"short","silvery","slaty","small","sooty","southern","spotted","streaked","tawny",'
    '"tropical","violet","western","white","yellow"],'
    '_b=["backed","banded","bellied","billed","breasted","browed","capped","cheeked","chested",'
    '"chinned","collared","crested","crowned","eared","eyed","faced","flanked","fronted",'
    '"headed","hooded","lored","naped","necked","rumped","shouldered","sided","tailed",'
    '"throated","tipped","winged","striped","speckled"],'
    '_c=["albatross","antbird","babbler","barbet","bittern","blackbird","booby","bulbul",'
    '"bunting","buzzard","canary","cisticola","cormorant","coucal","crane","cuckoo","dove",'
    '"drongo","duck","eagle","egret","falcon","fantail","finch","flycatcher","francolin",'
    '"goshawk","grebe","grosbeak","gull","harrier","hawk","heron","honeyeater","hornbill",'
    '"hummingbird","ibis","jay","kestrel","kingfisher","kite","lark","lorikeet","magpie",'
    '"manakin","martin","mockingbird","monarch","nightjar","nuthatch","oriole","owl","parrot",'
    '"pelican","penguin","petrel","pheasant","pigeon","pipit","plover","rail","raven","robin",'
    '"sandpiper","shrike","snipe","sparrow","starling","stork","sunbird","swallow","swift",'
    '"tanager","teal","tern","thrush","tit","toucan","vireo","vulture","warbler","waxwing",'
    '"weaver","woodpecker","wren"];'
    'return _a[Math.floor(Math.random()*_a.length)]+"-"+'
    '_b[Math.floor(Math.random()*_b.length)]+"-"+'
    '_c[Math.floor(Math.random()*_c.length)];'
    '})()'
)

errors = []

# 1. Replace username state: add _gu/_su alongside y/b
OLD_STATE = '[y,b]=(0,_.useState)(``)'
NEW_STATE = '[_gu,_su]=(0,_.useState)(function(){' + BIRD_GEN[1:-1].replace('(function(){', '').rsplit('return', 1)[0] + 'return ' + BIRD_GEN[1:-1].rsplit('return ', 1)[1] + '),[y,b]=(0,_.useState)(``)'

# Actually let's do it properly: just insert _gu/_su state before [y,b]
OLD_STATE = '[y,b]=(0,_.useState)(``)'
NEW_STATE = '[_gu,_su]=(0,_.useState)(' + BIRD_GEN + '),[y,b]=(0,_.useState)(``)'

if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: inserted _gu/_su state')
else:
    errors.append('FAIL: username state not found')

# 2. Fix handleAuth to skip username validation when signing up (C is true -> only need password)
OLD_AUTH = 'ie=async()=>{if(!(!y.trim()||!x))'
NEW_AUTH = 'ie=async()=>{if(!(C?!x:(!y.trim()||!x)))'
if OLD_AUTH in content:
    content = content.replace(OLD_AUTH, NEW_AUTH, 1)
    print('OK: fixed handleAuth validation guard')
else:
    errors.append('FAIL: handleAuth guard not found')

# 3. Fix register call to use _gu instead of y.trim()
OLD_REG = 'if(E(!0),C){let e=y.trim();'
NEW_REG = 'if(E(!0),C){let e=_gu;'
if OLD_REG in content:
    content = content.replace(OLD_REG, NEW_REG, 1)
    print('OK: fixed register to use _gu')
else:
    errors.append('FAIL: register let e not found')

# 4. Replace the username input with conditional: show bird display when C (isSignUp), else show input
OLD_INPUT = (
    '(0,L.jsx)(`input`,{placeholder:`Username`,value:y,onChange:e=>b(e.target.value),'
    'style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,'
    'color:`#f8fafc`,fontSize:16,width:`100%`,boxSizing:`border-box`}})'
)
NEW_INPUT = (
    'C?'
    # Bird display div (tap to copy, no @)
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},'
    'children:['
    '(0,L.jsx)(`div`,{onClick:function(){try{navigator.clipboard.writeText(_gu)}catch(e){}},style:{flex:1,padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,color:`#c084fc`,fontSize:15,fontFamily:`monospace`,cursor:`pointer`,userSelect:`none`,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:_gu}),'
    '(0,L.jsx)(`button`,{onClick:function(){_su(' + BIRD_GEN + ')},style:{padding:`9px 14px`,borderRadius:10,border:`1px solid #3f4756`,background:`transparent`,color:`#94a3b8`,fontSize:18,cursor:`pointer`},children:"🔀"})'
    ']})'
    # Login: show normal username input
    ':(0,L.jsx)(`input`,{placeholder:`Username`,value:y,onChange:e=>b(e.target.value),'
    'style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,'
    'color:`#f8fafc`,fontSize:16,width:`100%`,boxSizing:`border-box`}})'
)

if OLD_INPUT in content:
    content = content.replace(OLD_INPUT, NEW_INPUT, 1)
    print('OK: replaced username input with conditional bird display')
else:
    errors.append('FAIL: username input not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
