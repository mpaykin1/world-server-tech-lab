/* World Server Animation Tech Lab: isolated original-canvas adapter.
 * Tween easing concepts: tweenjs/tween.js MIT @ 84a27a74febbda783eebb7ee3e7d7c7abfd25009
 * Skeletal transforms inspired by DragonBonesJS MIT @ 64b6c69ae35777c2404be68c9192e2c56906079e
 * Bounded particles inspired by pixijs-userland/particle-emitter MIT @ 0fffdd9d18cabd99e5ee1d5dc94136613d5fcb04
 * All methods are original small Canvas adapters; full runtimes NOT installed or executed.
 * No new engine, background loop, timers, dependency, network or production changes.
 */
(() => {
  'use strict';
  const VERSION = 'animation-tech-lab-v1';
  const WAVE = 2 * Math.PI;
  const easing = {
    quadraticInOut(t) { t = Math.max(0, Math.min(1, t)); return t < .5 ? 2*t*t : 1-((-2*t+2)**2)/2; },
    cubicOut(t) { t = Math.max(0, Math.min(1, t)); return 1 - (1-t)**3; }
  };
  const oldKnight = drawKnight;
  const oldAtmosphere = drawAtmosphere;
  const oldRender = drawWorld;
  let lastHeroMotion = 0, lastSkeletalAngle = 0, particleDrawn = 0;
  const maxParticles = 48;
  const supportsReduced = () => Boolean(enhanced.reduced || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches));
  function clip(t) { return Math.max(0,Math.min(1,t)); }
  function hash(i, salt=0) { let n = Math.imul(i + salt + 1337, 0x45d9f3b); n ^= n >>> 16; return (n >>> 0) / 4294967296; }
  function smoothLoop(t) { const p = (t % 1 + 1) % 1; return p < .5 ? easing.quadraticInOut(p*2) : easing.quadraticInOut((1-p)*2); }
  function heroWalking() { return Boolean(enhanced.touch.x||enhanced.touch.y||['w','a','s','d','W','A','S','D','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].some(k=>keys[k])); }
  function riggedCapeAndArm(camX,camY, amplitude) {
    const px=Math.round(player.x-camX-4), py=Math.round(player.y-camY-16);
    const dir=player.dir < 0 ? -1 : 1;
    const shoulderX=px+12+3*dir, shoulderY=py+13;
    const t=state.time*4.2;
    const angle=Math.sin(t)*amplitude + (player.attackT>0 ? -.6 : 0);
    const upper=5, lower=5;
    const elbowX=Math.round(shoulderX+dir*upper*Math.cos(angle));
    const elbowY=Math.round(shoulderY+upper*Math.sin(angle));
    const wristX=Math.round(elbowX+dir*lower*Math.cos(angle*.65));
    const wristY=Math.round(elbowY+lower*Math.sin(angle*.65));
    lastSkeletalAngle=angle;
    ctx.lineCap='square';
    ctx.strokeStyle='#354752';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(shoulderX,shoulderY);ctx.lineTo(elbowX,elbowY);ctx.lineTo(wristX,wristY);ctx.stroke();
    ctx.fillStyle='#c7a476';ctx.fillRect(wristX-1,wristY-1,2,2);
    ctx.strokeStyle='#beab76';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(shoulderX,shoulderY-1);ctx.lineTo(elbowX,elbowY-1);ctx.stroke();
  }
  drawKnight = function animatedKnight(camX,camY) {
    const reduce=supportsReduced();
    const walk=heroWalking();
    const bounce=reduce?0:(walk ? smoothLoop(state.time*4)*1.6 : smoothLoop(state.time*.43)*.6);
    lastHeroMotion=bounce;
    // Character image, collision, camera and input are still drawn by original code.
    ctx.save();ctx.translate(0,-bounce);
    oldKnight(camX,camY);
    if(!reduce) riggedCapeAndArm(camX,camY, walk?.23:.10);
    ctx.restore();
  };
  const emitters=[];
  // Keep deterministic limited emitters tied to existing map coordinates, not per-frame spawns.
  for(const o of mapData.objects){
    if(o.type==='house_3d')emitters.push({kind:'smoke',x:o.x*16+13,y:o.y*16-9,rate:10});
    else if(o.type==='torch')emitters.push({kind:'ember',x:o.x*16+8,y:o.y*16-7,rate:8});
    else if(o.type.startsWith('tree_'))emitters.push({kind:'leaf',x:o.x*16+8,y:o.y*16-10,rate:5});
    else if(o.type==='fish')emitters.push({kind:'glint',x:o.x*16+8,y:o.y*16+6,rate:8});
  }
  // Exact cap; deterministic preselection avoids unbounded particle pools.
  const samples=[];
  for(let i=0;i<maxParticles;i++){
    const e=emitters[i % Math.max(1,emitters.length)];
    if(e)samples.push({emitter:e, seed:hash(i,89), seed2:hash(i,197), speed:.22+hash(i,413)*.34});
  }
  function drawAmbientParticles(){
    particleDrawn=0;
    if(supportsReduced())return;
    const camX=player.x-cvs.width/(2*zoom),camY=player.y-cvs.height/(2*zoom);
    for(const s of samples){
      const e=s.emitter;
      const x0=e.x-camX, y0=e.y-camY;
      if(x0 < -32 || x0 > cvs.width/zoom+32 || y0 < -40 || y0 > cvs.height/zoom+40)continue;
      // Emitter tracks particle age, velocity and alpha, without Pixi dependency.
      const age=(state.time*s.speed + s.seed)%1;
      const alpha=(1-age)*easing.cubicOut(clip(age*7));
      let dx=0,dy=0,size=1,color='#ffffff';
      if(e.kind==='smoke') {dx=Math.sin(age*6+s.seed2*8)*4;dy=-age*21;size=2+Math.floor(age*3);color='#d6d5c2';}
      if(e.kind==='ember') {dx=Math.sin(age*13+s.seed*8)*3;dy=-age*17;size=1;color='#ffd27b';}
      if(e.kind==='leaf')  {dx=Math.sin(age*9+s.seed2*5)*9;dy=age*23-4;size=2;color=s.seed>.5?'#c0a15b':'#8fa75a';}
      if(e.kind==='glint') {dx=Math.sin(age*7+s.seed*7)*6;dy=Math.cos(age*5)*2;size=1;color='#d2f0d9';}
      ctx.globalAlpha=alpha*.72;ctx.fillStyle=color;
      ctx.fillRect(Math.round(x0+dx),Math.round(y0+dy),size,size);
      particleDrawn++;
    }
    ctx.globalAlpha=1;
  }
  drawAtmosphere = function animatedAtmosphere(){
    oldAtmosphere();drawAmbientParticles();
  };
  drawWorld = function animationLabWorld(){
    oldRender();
    const m=window.__graphicsDemoMetrics;
    if(m){
      m.animationLab=VERSION;
      m.animationTweenEasing=Number(lastHeroMotion.toFixed(4));
      m.animationSkeletonAngle=Number(lastSkeletalAngle.toFixed(4));
      m.animationParticles=particleDrawn;
      m.animationParticleCap=maxParticles;
      m.animationEmitterCount=emitters.length;
      m.animationReducedMotion=supportsReduced();
    }
  };
  window.__animationLab={version:VERSION,easing,emitterCount:emitters.length,particleCap:maxParticles,samples:samples.length,getMetrics:()=>({motion:lastHeroMotion,angle:lastSkeletalAngle,particles:particleDrawn})};
})();