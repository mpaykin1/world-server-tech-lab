/* World Server Tech Lab / animation v2 — original Canvas extension, not a new engine.
 * Uses existing map/collision, draw pass, RAF, reduced-motion controls and assets.
 * Source concepts: Tween.js easing, DragonBones two-bone rigs, Pixi bounded emitters.
 * Zero imported dependencies and zero new timers. Applied AFTER v9 scene + animation A1.
 */
(() => {
  'use strict';
  const formerWorld = drawWorld;
  const formerKnight = drawKnight;
  const formerObject = objectRender;
  const formerTerrain = drawTerrain;
  const MAX_SHIMMERS = 28, MAX_SMOKE = 8, MAX_SWAY = 18;
  let shimmers = 0, smokeWisps = 0, swayTrees = 0, stride = 0, cape = 0;
  let oldX = player.x, oldY = player.y;
  const reduced = () => enhanced.reduced || Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches);
  const wave = (t) => Math.sin(t * Math.PI * 2);
  const ease = (t) => t*t*(3-2*t); // original smoothstep / tween, clamped phase below
  // Cap excess winding from a slow tab, then use actual displacement rather than key state.
  drawKnight = function v2Knight(camX, camY) {
    const moved = Math.hypot(player.x-oldX,player.y-oldY)>0.015;
    oldX=player.x;oldY=player.y;
    stride = moved ? wave(player.walkT/4) : 0;
    cape = reduced() ? 0 : (moved ? wave(player.walkT/4-.22)*2 : wave(state.time*.39)*.45);
    const px=Math.round(player.x-camX-4),py=Math.round(player.y-camY-16);
    // Three lapped folds are BEHIND the original 24x32 pixel hero, retaining its identity.
    ctx.save();
    if (!reduced()) {
      const flip=player.dir<0?-1:1, cx=px+(flip<0?16:8), cy=py+11;
      ctx.fillStyle='#513a49';
      ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx-flip*(4+cape),cy+15);
      ctx.lineTo(cx+flip*2,cy+18);ctx.lineTo(cx+flip*4,cy+4);ctx.fill();
      ctx.strokeStyle='#ac6e68';ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(cx+flip*1,cy+3);ctx.lineTo(cx-flip*(2+cape*.65),cy+15);ctx.stroke();
    }
    formerKnight(camX,camY);
    // Boot glints show alternating planted vs lifted foot without changing collision anchors.
    if (!reduced() && moved) {
      ctx.fillStyle='#d4b586';
      const shift=Math.round(3*stride),footY=py+27;
      ctx.fillRect(px+7+shift, footY-Math.max(0,Math.round(stride*2)),3,1);
      ctx.fillRect(px+15-shift,footY-Math.max(0,Math.round(-stride*2)),3,1);
    }
    ctx.restore();
  };
  function crownWobble(o,x,y,camX,camY) {
    // Independent tree phases, base anchored to the SAME tile, no map mutations.
    const sx=Math.round(x*TILE-camX), sy=Math.round(y*TILE-camY);
    const gust = (wave(state.time*.21 + noise(x,y,713)) *
      (0.003+0.007*ease((wave(state.time*.08+noise(x,y,717))+1)/2)));
    return {sx,sy,gust};
  }
  objectRender = function v2Object(item,camX,camY) {
    const {o,x,y}=item;
    if (reduced() || !inView(x*TILE-camX,y*TILE-camY,105)) return formerObject(item,camX,camY);
    if (o.type.startsWith('tree_') && swayTrees<MAX_SWAY) {
      const {sx,sy,gust}=crownWobble(o,x,y,camX,camY);
      ctx.save();ctx.translate(sx+8,sy+16);ctx.rotate(gust);ctx.translate(-sx-8,-sy-16);
      formerObject(item,camX,camY);ctx.restore();
      // Wind-borne dots beneath crown move at a different tempo from the trunk.
      ctx.fillStyle='#a6b673';
      const drift=Math.round(3*wave(state.time*.35+noise(x,y,719)));
      ctx.fillRect(sx+5+drift,sy-11,2,1);
      swayTrees++;
    } else {
      formerObject(item,camX,camY);
    }
    if(o.type==='house_3d' && smokeWisps<MAX_SMOKE){
      const s=state.time*.24+noise(x,y,729);
      const img=imgs['obj_house_3d'];if(!img)return;
      const dx=Math.round(x*TILE-camX+img.width*.21),dy=Math.round(y*TILE-camY-(img.height-TILE)+9);
      for(let k=0;k<2 && smokeWisps<MAX_SMOKE;k++){
        const p=(s+k*.52)%1,alpha=(1-ease(p))*.32;
        ctx.fillStyle=`rgba(220,218,198,${alpha.toFixed(3)})`;
        ctx.fillRect(dx+Math.round(wave(p*.85+k*.27)*6),dy-Math.round(p*25),2+(p*3|0),2);
        smokeWisps++;
      }
    }
  };
  drawTerrain = function v2Terrain(camX,camY,bounds) {
    formerTerrain(camX,camY,bounds);
    if(reduced())return;
    // Highlights are limited and allocated only to wet visible tiles; shadow/physics untouched.
    for(let y=bounds.y0;y<=bounds.y1 && shimmers<MAX_SHIMMERS;y++){
      for(let x=bounds.x0;x<=bounds.x1 && shimmers<MAX_SHIMMERS;x++){
        if(noise(x,y,733)>.27)continue;
        const t=tileAt(x,y);if(t!=='water'&&t!=='shallow')continue;
        const sx=Math.round(x*TILE-camX),sy=Math.round(y*TILE-camY);
        if(!inView(sx,sy,TILE))continue;
        const phase=(state.time*.37+noise(x,y,739))%1;
        ctx.fillStyle=`rgba(197,228,213,${(.07 + .22*ease(1-Math.abs(phase*2-1))).toFixed(3)})`;
        ctx.fillRect(sx+2+Math.round(phase*6),sy+5,3,1);shimmers++;
      }
    }
  };
  drawWorld = function v2World(){
    shimmers=0;smokeWisps=0;swayTrees=0;
    formerWorld();
    if(window.__graphicsDemoMetrics){Object.assign(window.__graphicsDemoMetrics,{
      animationV2:'v2-gait-cape-wind-water-smoke',v2Stride:stride,v2Cape:cape,
      v2Trees:swayTrees,v2Shimmers:shimmers,v2SmokeWisps:smokeWisps,
      v2Limits:[MAX_SWAY,MAX_SHIMMERS,MAX_SMOKE]
    });}
  };
  window.__animationLabV2={version:'v2',caps:{sway:MAX_SWAY,shimmer:MAX_SHIMMERS,smoke:MAX_SMOKE}};
})();