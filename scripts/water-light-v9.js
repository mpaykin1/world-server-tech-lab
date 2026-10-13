/* ART V9 water enhancement; existing terrain, camera and collisions preserved.
 * Shared game clock, deterministic shoreline, no new engine/timers/dependencies.
 */
(() => {
  'use strict';
  const TILE_COUNT_BUDGET=900;
  const previousTerrain=drawTerrain;
  let lastWaterTiles=0, lastRipples=0;
  const isWet=t=>t==='water'||t==='shallow';
  const isBank=(x,y)=>!isWet(tileAt(x-1,y))||!isWet(tileAt(x+1,y))||
                      !isWet(tileAt(x,y-1))||!isWet(tileAt(x,y+1));
  function ripple(x,y,tx,ty,bank){
    const cycle=(state.time*.68+noise(tx,ty,92))%1;
    const phase=cycle<.5?cycle*2:(1-cycle)*2;
    const width=bank?2+phase*2:2+phase*3;
    ctx.globalAlpha=(bank?.40:.28)*(1-cycle);
    ctx.strokeStyle=bank?'#e1ead6':'#a7d5d6';
    ctx.lineWidth=1;
    ctx.beginPath();
    ctx.moveTo(Math.round(x+6-width),Math.round(y+8));
    ctx.lineTo(Math.round(x+6+width),Math.round(y+8));
    ctx.stroke();
    ctx.globalAlpha=1;
  }
  drawTerrain=function v9WaterTerrain(camX,camY,bounds){
    previousTerrain(camX,camY,bounds);
    lastWaterTiles=0;lastRipples=0;
    if(enhanced.reduced)return;
    for(let ty=bounds.y0;ty<=bounds.y1&&lastWaterTiles<TILE_COUNT_BUDGET;ty++){
      for(let tx=bounds.x0;tx<=bounds.x1&&lastWaterTiles<TILE_COUNT_BUDGET;tx++){
        if(!isWet(tileAt(tx,ty)))continue;
        const x=Math.round(tx*TILE-camX),y=Math.round(ty*TILE-camY);
        if(!inView(x,y,16))continue;
        lastWaterTiles++;
        if(noise(tx,ty,71)<.77)continue;
        ripple(x,y,tx,ty,isBank(tx,ty));lastRipples++;
      }
    }
  };
  const prevWorld=drawWorld;
  drawWorld=function v9WaterWorld(){
    prevWorld();
    if(window.__graphicsDemoMetrics){
      window.__graphicsDemoMetrics.waterTilesV9=lastWaterTiles;
      window.__graphicsDemoMetrics.animatedRipplesV9=lastRipples;
    }
  };
  window.__waterLightV9={version:'v9-shoreline-ripples',maxWaterTiles:TILE_COUNT_BUDGET};
})();
