/* WORLD SERVER Tech Lab: authored micro-composition over original medieval terrain.
 * Keeps exact map/collisions and draw order; no new engine, timers or asset requests.
 */
(() => {
  'use strict';
  const originalCliff=drawV9CliffMaterial;
  drawV9CliffMaterial=function v10CliffMaterial(tx,ty,sx,sy,type){
    const img=imgs.cliff_macro_v10;
    if(type!=='cliff'||!img?.naturalWidth)return originalCliff(tx,ty,sx,sy,type);
    const wx=mod(tx,mapData.width),wy=mod(ty,mapData.height);
    const mx=Math.floor(wx/4),my=Math.floor(wy/4),variant=v9CliffVariant(mx,my);
    ctx.drawImage(img,variant*64+(wx%4)*TILE,(wy%4)*TILE,TILE,TILE,sx,sy,TILE,TILE);
    return true;
  };
  const PREVIOUS=drawTerrain, TILE_BUDGET=900;
  let flowers=0, cliffEdges=0, shoreSparkles=0, grassTufts=0;
  const wet=t=>t==='water'||t==='shallow';
  function dot(x,y,color,w=1,h=1){ctx.fillStyle=color;ctx.fillRect(x|0,y|0,w,h);}
  function flower(x,y,seed){
    const white=seed>.5,petal=white?'#fff6d1':'#fee167';
    dot(x-1,y,petal,3,1);dot(x,y-1,petal,1,3);
    dot(x,y,'#c78e31');dot(x,y+2,'#347142');flowers++;
  }
  function grass(tx,ty,x,y){
    const patch=noise(Math.floor(tx/3),Math.floor(ty/3),691);
    const n=noise(tx,ty,697);
    if(patch>.66 && n>.21){
      const ox=3+(noise(tx,ty,701)*9|0), oy=3+(noise(tx,ty,709)*9|0);
      dot(x+ox,y+oy,'#315a34',1,3);dot(x+ox+1,y+oy-1,'#a9c85c',1,2);
      if(n>.65)dot(x+ox-3,y+oy+1,'#4e8540',1,2);
      grassTufts++;
    }
    const bloom=noise(Math.floor(tx/4),Math.floor(ty/4),719);
    if(bloom>.68 && noise(tx,ty,727)>.66){
      const fx=x+4+(noise(tx,ty,733)*7|0);
      const fy=y+5+(noise(tx,ty,739)*7|0);
      flower(fx,fy,noise(tx,ty,743));
    }
  }
  function cliffLip(tx,ty,x,y){
    // Only real cliff/non-cliff contacts receive a stepped moss crown.
    const above=tileAt(tx,ty-1),below=tileAt(tx,ty+1);
    const left=tileAt(tx-1,ty),right=tileAt(tx+1,ty);
    if(above!=='cliff'){
      for(let k=0;k<16;k+=2){
        const h=1+(noise(tx*17+k,ty,751)*3|0);
        dot(x+k,y,'#284e35',2,h+1);
        dot(x+k,y,'#6caa57',2,1);
        if(k%6===0)dot(x+k,y-1,'#b4c977',2,1);
      }
      cliffEdges++;
    }
    if(below!=='cliff'){
      for(let k=0;k<16;k+=3){
        const h=2+(noise(tx*21+k,ty,757)*3|0);
        dot(x+k,y+16-h,'#34484d',3,h);
      }
      cliffEdges++;
    }
    if(left!=='cliff'||right!=='cliff'){
      const side=left!=='cliff'?0:14;
      for(let k=2;k<15;k+=4){
        const spread=noise(tx,ty*9+k,761)>.5?3:2;
        dot(x+side,y+k,'#506f64',spread,2);
      }
      cliffEdges++;
    }
  }
  function water(tx,ty,x,y){
    if(!wet(tileAt(tx,ty)))return;
    const nearby=['grass','sand','path','stone_path'];
    const near=nearby.includes(tileAt(tx,ty-1))||nearby.includes(tileAt(tx,ty+1))||
               nearby.includes(tileAt(tx-1,ty))||nearby.includes(tileAt(tx+1,ty));
    if(!near||noise(tx,ty,773)<.55)return;
    const t=enhanced.reduced?0:Math.sin(state.time*3+noise(tx,ty,779)*6.28);
    const px=x+3+(noise(tx,ty,787)*8|0),py=y+3+(noise(tx,ty,797)*9|0);
    dot(px,py,t>.3?'#e7fbeb':'#9bd5d4',3,1);
    dot(px+1,py+1,'#75b7ca',2,1);
    shoreSparkles++;
  }
  drawTerrain=function v10LandscapedTerrain(camX,camY,bounds){
    PREVIOUS(camX,camY,bounds);
    flowers=0;cliffEdges=0;shoreSparkles=0;grassTufts=0;
    let sampled=0;
    for(let ty=bounds.y0;ty<=bounds.y1&&sampled<TILE_BUDGET;ty++){
      for(let tx=bounds.x0;tx<=bounds.x1&&sampled<TILE_BUDGET;tx++){
        const sx=Math.round(tx*TILE-camX),sy=Math.round(ty*TILE-camY);
        if(!inView(sx,sy,16))continue;
        sampled++;
        const type=tileAt(tx,ty);
        // Preserve all gameplay and never decorate the safe mine switchback.
        if(type==='grass')grass(tx,ty,sx,sy);
        else if(type==='cliff')cliffLip(tx,ty,sx,sy);
        else if(wet(type))water(tx,ty,sx,sy);
      }
    }
  };
  const previousWorld=drawWorld;
  drawWorld=function v10WorldWithMetrics(){
    previousWorld();
    if(window.__graphicsDemoMetrics){
      window.__graphicsDemoMetrics.landscapeV10={flowers,cliffEdges,shoreSparkles,grassTufts};
    }
  };
  window.__landscapeArtV10={version:'v10-cliff-meadow-shore',tileBudget:TILE_BUDGET};
})();