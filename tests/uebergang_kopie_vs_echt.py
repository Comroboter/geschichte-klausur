import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,sys,json
from playwright.async_api import async_playwright
JS="""window.__s=[];(function f(){const k=document.querySelector('.station.on > .hero > .kicker');
const ov=document.querySelector('.peek.on .peek-in');const pk=[...document.querySelectorAll(ov?'.peek.on .peek-in > .content > *':'.station.on > .content > .runway > .rw-sheet > .rw-in > .content > *')];  // Overlay, sonst nur die direkte Vorschau (nicht die verschachtelte)
const real=[...document.querySelectorAll('.station.on > .content > *')];
function pos(list){if(!list.length)return null;const base=list[0].closest('.peek-in,.rw-in')||list[0].closest('.station');const kk=base.querySelector('.kicker');const kt=kk?kk.getBoundingClientRect().top:0;return list.map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.top-kt),Math.round(r.height)]})}
window.__s.push([Math.round(performance.now()),document.querySelector('.peek.on')?'ov':'', JSON.stringify(pos(pk)),JSON.stringify(pos(real)),location.hash]);requestAnimationFrame(f)})()"""
async def main(w,h):
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={'width':w,'height':h},color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page(); await pg.goto(URL+''); await pg.wait_for_timeout(1500)
        for k in range(11):  # 12 Schritte, ohne Rücksprung zur Übersicht
            await pg.evaluate(JS); await pg.click('#next'); await pg.wait_for_timeout(1600)
            s=await pg.evaluate('window.__s'); await pg.evaluate('window.__s=[]')
            # last clone positions before hash change, real positions right after and at end
            hs=[x[4] for x in s]; target=hs[-1]
            before=[x for x in s if x[4]!=target]; after=[x for x in s if x[4]==target]
            clone=before[-1][2] if before else None
            r0=after[0][3] if after else None; r1=after[-1][3]
            import json as J
            cl=J.loads(clone) if clone and clone!='null' else []; re0=J.loads(r0) if r0 and r0!='null' else []; reE=J.loads(r1) if r1 and r1!='null' else []
            n=min(len(re0),len(cl)); bad=[(i,cl[i],re0[i]) for i in range(n) if cl[i]!=re0[i] and not (cl[i][1]==0 and re0[i][1]==0)]  # zugeklappte Abschnitte (Höhe 0) zählen nicht
            drift=[(i,re0[i],reE[i]) for i in range(min(len(re0),len(reE))) if re0[i]!=reE[i]]
            print(target,'OK' if not bad and not drift else ('KOPIE≠ECHT '+str(bad[:3]) if bad else '')+(' DRIFT '+str(drift[:3]) if drift else ''))
        await b.close()
asyncio.run(main(int(sys.argv[1]),int(sys.argv[2])))
