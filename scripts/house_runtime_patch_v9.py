#!/usr/bin/env python3
"""Fail-closed additive lantern patch for original V9 canvas renderer (no new engine)."""
from pathlib import Path
import sys

OLD = "  if(o.type==='house_3d')smoke(sx+fw*.64,dy+3,x,y);\n}"
NEW = """  if(o.type==='house_3d'){houseLantern(sx+55,dy+39,x,y);smoke(sx+fw*.21,dy+9,x,y);}
}
// Shared animation clock; no per-house timers or image requests.
function houseLantern(x,y,tx,ty){
  const flicker=enhanced.reduced?0:Math.sin(state.time*4+noise(tx,ty,37)*6.283)*.10;
  ctx.fillStyle=`rgba(255,184,75,${(.30+flicker).toFixed(3)})`;
  ctx.fillRect(Math.round(x)-2,Math.round(y)-3,7,8);
  ctx.fillStyle='#fff1ad';ctx.fillRect(Math.round(x),Math.round(y),1,2);
}"""

def patch(path: Path) -> None:
    source = path.read_text(encoding='utf-8')
    if source.count(OLD) != 1 or 'function houseLantern(' in source:
        raise ValueError('Unexpected V9 renderer callsite; refusing to modify')
    target = source.replace(OLD, NEW)
    if target.count('function houseLantern(') != 1 or target.count("if(o.type==='house_3d')") != 1:
        raise ValueError('Unexpected patch output; refusing to write')
    if len(target.splitlines()) > 400:
        raise ValueError('Renderer architecture limit >400 lines')
    path.write_text(target, encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python house_runtime_patch_v9.py original-graphics-enhancement.js')
    patch(Path(sys.argv[1]))
