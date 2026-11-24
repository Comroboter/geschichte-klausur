"""Screenshots aller 15 Stationen in den echten Gerätegrößen von Leopold.
Aufruf: python3 screens.py [dark|light] [station ...]   -> tests/out/screens/<groesse>_<station>.png + Übersicht"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, OUT, SKIP_INTRO
from playwright.async_api import async_playwright
IDS = ["start","plan","revolution","gesellschaft","industrie","sortieren","kolonien","kongo","personen","aufgaben","quiz","kurz-vorher"]
SIZES = {"s24": (384, 832, True), "ipad-quer": (1080, 810, True), "ipad-hoch": (810, 1080, True),
         "pc-leopold": (1287, 1241, False), "laptop": (1440, 900, False), "breit": (2560, 1300, False)}
async def main():
    theme = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("dark", "light") else "dark"
    only = [a for a in sys.argv[1:] if a in IDS] or IDS
    d = os.path.join(OUT, "screens"); os.makedirs(d, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        for name, (w, h, mob) in SIZES.items():
            c = await b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, color_scheme=theme)
            await c.add_init_script(SKIP_INTRO)
            pg = await c.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
            for st in only:
                await pg.goto(URL + "#" + st); await pg.wait_for_timeout(1800)
                await pg.screenshot(path=os.path.join(d, f"{name}_{st}.png"))
            await c.close()
        await b.close()
    print("fertig:", d, "Fehler:", errs or "keine")
asyncio.run(main())
