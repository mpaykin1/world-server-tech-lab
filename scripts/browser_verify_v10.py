#!/usr/bin/env python3
"""Real Chromium game proof for original V9 vs bounded V10 art, with same camera.
No production deploy or invented iPhone evidence. Python 3 / Pillow / playwright.
"""
import argparse, base64, hashlib, json, re, statistics
from pathlib import Path
from playwright.sync_api import sync_playwright

MAP_SHA='183302c32964f5a43ca7fe7ab4d00c1a8d1d4fe861c8688fbe41c2c9369dec8e'

def html_embedded(root):
    src=(root/'demo.html').read_text(encoding='utf-8')
    def embed(match):
        rel=match.group(0)
        path=(root/rel).resolve()
        if not path.is_relative_to(root.resolve()):raise ValueError('escaping asset path')
        return 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
    src=re.sub(r'assets/[\w./-]+\.png',embed,src)
    def script(m):return '<script>\n'+(root/m.group(1)).read_text('utf-8')+'\n</script>'
    return re.sub(r'<script src="([\w.-]+\.js)"></script>',script,src)

def sample(browser,root,folder,mobile,width,height,out):
    p=browser.new_context(viewport={'width':width,'height':height},is_mobile=mobile,has_touch=mobile,device_scale_factor=1)
    page=p.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m:errors.append('console:'+m.text) if m.type=='error' else None)
    page.set_content(html_embedded(root),wait_until='domcontentloaded')
    page.wait_for_function('window.__graphicsDemoMetrics?.loaded===window.__graphicsDemoMetrics?.total && window.__graphicsDemoMetrics?.total>=44',timeout=25000)
    page.wait_for_timeout(250)
    first=page.evaluate('({x:player.x,y:player.y, blocked: mapData.blockedTiles.slice(),world:mapData.width+"x"+mapData.height})')
    page.keyboard.down('ArrowRight');page.wait_for_timeout(400);page.keyboard.up('ArrowRight')
    moved=page.evaluate('player.x')-first['x']
    assert moved>5,(folder,moved)
    touch=None
    if mobile:
        session=p.new_cdp_session(page)
        x=page.evaluate('player.x')
        session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'id':55,'x':80,'y':260}]})
        session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'id':55,'x':120,'y':260}]})
        page.wait_for_timeout(340)
        session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        touch=round(page.evaluate('player.x')-x,2)
        assert touch>0,(folder,touch)
    tests=[]
    for _ in range(3):
        ms=page.evaluate('''() => {const t=performance.now();for(let i=0;i<70;i++)drawWorld();return (performance.now()-t)/70;}''')
        tests.append(round(ms,3))
    scenes=[]
    for scene,x,y in [('village',5,6),('cliff_route',27,14),('holdout_mine',40,6)]:
        page.evaluate('''([x,y]) => {player.x=x*TILE+8;player.y=y*TILE+8;state.time=11.5;drawWorld();}''',[x,y])
        page.wait_for_timeout(85)
        met=page.evaluate('window.__graphicsDemoMetrics')
        path=out/f'{folder}_{scene}_{width}x{height}.png';page.screenshot(path=str(path),animations='disabled')
        scenes.append({'scene':scene,'screenshot':path.name,'landscapeV10':met.get('landscapeV10'), 'fps_observed':met.get('fps'),'water_tiles':met.get('waterTilesV9')})
    rep={'build':folder,'viewport':[width,height],'mobile_emulated':mobile,'loaded':met['loaded'],'total':met['total'],
         'js_errors':errors,'original_map':first['world'],'blockedTiles':first['blocked'],
         'keyboard_dx':round(moved,2),'touch_dx':touch,'draw_cpu_samples_ms':tests,
         'draw_cpu_median_ms':round(statistics.median(tests),3),'scenes':scenes}
    assert not errors and met['loaded']==met['total'] and met['loaded']>=44
    p.close();return rep

def verify(original,candidate,out):
    out.mkdir(parents=True,exist_ok=True)
    for root in (original,candidate):
        assert hashlib.sha256((root/'map.json').read_bytes()).hexdigest()==MAP_SHA
        assert len((root/'graphics-enhancement.js').read_text().splitlines())<=400
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        reps=[]
        for name,root in [('v9_original',original),('v10_landscape',candidate)]:
            for width,height,mobile in [(1200,780,False),(390,844,True)]:
                reps.append(sample(browser,root,name,mobile,width,height,out))
        browser.close()
    target=[r for r in reps if r['build']=='v10_landscape']
    for r in target:
        assert any((s.get('landscapeV10') or {}).get('cliffEdges',0)>0 for s in r['scenes'])
        assert any((s.get('landscapeV10') or {}).get('grassTufts',0)>0 for s in r['scenes'])
    report={'baseline': 'original V9 owner playable snapshot','candidate':'V10 offline graphical slice same engine',
            'browser':'Chromium headless Linux','runs':reps,
            'art_quality_independent_score':None,'actual_iPhone11':False,
            'public_live_deployment':False,'owner_pass_fail':None}
    (out/'v10_browser_evidence.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('original',type=Path);ap.add_argument('candidate',type=Path);ap.add_argument('out',type=Path)
    args=ap.parse_args()
    result=verify(args.original,args.candidate,args.out)
    for run in result['runs']:
        print(run['build'],run['viewport'],'cpu_ms',run['draw_cpu_median_ms'],'keyboard',run['keyboard_dx'],'touch',run['touch_dx'],
              'scene_art',[v['landscapeV10'] for v in run['scenes']])
    print('BROWSER_VERIFIED_V10')