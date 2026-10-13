/* V11 original pixel-art atlas: independent style layer, no game logic changes.
 * Frame-limited authored decals; input, collisions, animation, and RAF unchanged.
 */
(() => {
  'use strict';
  const previousObject = objectRender;
  const previousTerrain = drawTerrain;
  const previousWorld = drawWorld;
  const DECAL_BUDGET = 90;
  let treeSelection = 0, decalCount = 0;
  function treeVariant(item) {
    const {o,x,y} = item;
    if (!o?.type?.startsWith('tree_')) return null;
    return {type: 'obj_' + o.type, variant: Math.floor(noise(x,y,110011)*3)};
  }
  objectRender = function v11Object(item,camX,camY) {
    const hit = treeVariant(item);
    if (!hit) return previousObject(item,camX,camY);
    const original = imgs[hit.type];
    const alternate = imgs['v11_' + item.o.type + '_' + hit.variant];
    if (!alternate?.naturalWidth) return previousObject(item,camX,camY);
    try {
      imgs[hit.type] = alternate;
      treeSelection++;
      return previousObject(item,camX,camY);
    } finally { imgs[hit.type] = original; }
  };
  function decalType(tx,ty,type) {
    const n=noise(tx,ty,110019),near=tileAt(tx+1,ty);
    if (type==='grass') {
      if(n<.82) return -1;
      if(near==='cliff')return 5;
      return n>.95 ? 6 : n>.9 ? 0 : 1;
    }
    if(type==='cliff')return n>.77 ? (tileAt(tx,ty-1)==='grass' ? 5 : 2) : -1;
    if(type==='water'||type==='shallow') {
      const land=tileAt(tx,ty+1);
      if(n>.67 && land!=='water' && land!=='shallow')return 3;
      return n>.94 ? 7 : -1;
    }
    if(type==='sand')return n>.81 ? 4 : -1;
    return -1;
  }
  drawTerrain = function v11Terrain(camX,camY,bounds) {
    previousTerrain(camX,camY,bounds);
    decalCount=0;
    const sheet=imgs.art_v11_decals;
    if(!sheet?.naturalWidth)return;
    for(let y=bounds.y0;y<=bounds.y1&&decalCount<DECAL_BUDGET;y++) {
      for(let x=bounds.x0;x<=bounds.x1&&decalCount<DECAL_BUDGET;x++) {
        const sx=Math.round(x*TILE-camX),sy=Math.round(y*TILE-camY);
        if(!inView(sx,sy,16))continue;
        const n=decalType(x,y,tileAt(x,y));if(n<0)continue;
        ctx.drawImage(sheet,n*16,0,16,16,sx,sy,16,16);
        decalCount++;
      }
    }
  };
  drawWorld = function v11World() {
    treeSelection = 0;
    previousWorld();
    if (window.__graphicsDemoMetrics) {
      window.__graphicsDemoMetrics.revision = 'graphics-demo-001-v11-experimental';
      window.__graphicsDemoMetrics.artV11 = {enabled: true,
        selected:treeSelection,decals:decalCount,authoredSprites:13,
        decalBudget:DECAL_BUDGET,extraTimers:0};
    }
  };
  window.__artV11 = {version:'v11-pixel-art-atlas',engineChanged:false};
})();