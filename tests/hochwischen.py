"""Hochwischen am Seitenende (Touch): Nach dem Loslassen hinter der Schwelle muss das Blatt sofort weiterfahren,
ohne Stillstand. Prüft je Station: Wechsel passiert, Blatt bewegt sich spätestens 200 ms nach dem Loslassen (vorher standen es 255 bis 300 ms still)
(im Headless-Browser sind Frames 30 bis 60 ms lang), Endposition ohne Korrektur, Scroll-Sperre wieder weg.
Aufruf: python3 tests/hochwischen.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SKIP_INTRO
import asyncio
from playwright.async_api import async_playwright

REC = """window.__R=[];(function f(){const on=document.querySelector('.station.on'),rs=on&&on.querySelector(':scope > .content > .runway .rw-sheet');
__R.push([performance.now(),rs?rs.getBoundingClientRect().top:null,location.hash]);if(__R.length<300)requestAnimationFrame(f)})()"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for W, H in [(820, 1180), (390, 844)]:
            c = await b.new_context(viewport={'width': W, 'height': H}, color_scheme='dark', has_touch=True, is_mobile=True)
            await c.add_init_script(SKIP_INTRO + ";window.__TE=0;document.addEventListener('touchend',()=>{window.__TE=performance.now()},true)")
            pg = await c.new_page(); cdp = await c.new_cdp_session(pg)
            bad = []
            for st in ['plan', 'gesellschaft', 'kolonien', 'kongo', 'personen', 'quiz']:
                await pg.goto(URL + '#' + st); await pg.wait_for_timeout(2500)
                await pg.evaluate('scrollTo(0,1e6)'); await pg.wait_for_timeout(800)
                await pg.evaluate(REC)
                await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': W // 2, 'y': H - 180}]})
                y = H - 180
                for i in range(16):
                    y -= 14; await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': W // 2, 'y': y}]}); await asyncio.sleep(0.016)
                await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
                await pg.wait_for_timeout(1600)
                R = await pg.evaluate('__R'); te = await pg.evaluate('__TE'); h = await pg.evaluate('location.hash')
                after = [r for r in R if r[0] > te and r[2] == '#' + st and r[1] is not None]
                y0 = after[0][1] if after else None
                moved = next((r[0] - te for r in after if y0 is not None and y0 - r[1] > 2), None)
                left = await pg.evaluate('document.documentElement.classList.contains("nomo")')
                ok = h != '#' + st and moved is not None and moved < 200 and not left
                if not ok: bad.append((st, h, moved, left))
                print(W, st, '->', h, 'Blatt fährt nach', None if moved is None else round(moved), 'ms', 'OK' if ok else 'FEHLER')
            print(W, 'Fehler:', bad or 'keine')
            await c.close()
        await b.close()

asyncio.run(main())
