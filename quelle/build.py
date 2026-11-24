import base64, glob, json, os, shutil
from PIL import Image, ImageDraw, ImageFont
FD=next((d for d in ('node_modules/@fontsource','/home/claude/fonts/node_modules/@fontsource') if os.path.isdir(d)),'node_modules/@fontsource')  # npm install legt die Schriften hier ab
fonts=[("Bricolage Grotesque","bricolage-grotesque","500","normal"),("Bricolage Grotesque","bricolage-grotesque","700","normal"),("Bricolage Grotesque","bricolage-grotesque","800","normal"),
("Literata","literata","400","normal"),("Literata","literata","600","normal"),("Literata","literata","400","italic"),
("Caveat","caveat","600","normal")]
css=""
for fam,pkg,w,st in fonts:
    p=f"{FD}/{pkg}/files/{pkg}-latin-{w}-{st}.woff2"
    b=base64.b64encode(open(p,'rb').read()).decode()
    css+=f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}\n"
src=open('app.html',encoding='utf-8').read().replace('/*FONTS*/',css)
import subprocess, re, html as H
a=src.index("/* ================= DATEN ================= */"); b=src.index("/* ================= ZUSTAND")
js=src[a:b]+"\nconsole.log(JSON.stringify({PARTS:PARTS,B:B,ST:ST,SO:SO,SOL:SOL,CMP:CMP,CMPH:CMPH,TL:TL,EX:EX,Q:Q}))"
D=json.loads(subprocess.run(['node','-e',js],capture_output=True,text=True,check=True).stdout)
e=lambda t:H.escape(str(t),quote=False)
st=re.findall(r'<section class="station" id="s-([a-z-]+)" data-look="[a-z]+" data-title="([^"]+)" data-min="(\d+)"(?: data-type="([^"]+)")?',src)
assert len(st)>0 and len(st)==open('stations.html',encoding='utf-8').read().count('<section class="station"'), len(st)  # alle Stationen aus stations.html gefunden
def items(pi,a,b):
    p=D['PARTS'][pi]; h=f'<div class="items-head"><h2>{e(p.get("head") or p["name"])}</h2><span class="sub">{e(p["sub"])}</span></div><div class="items">'
    for it in p['items'][a:b+1]:
        h+=f'<details class="s-item"><summary>{e(it["t"])}</summary><div class="body"><p>{e(it["d"])}</p><div class="baustein"><b>Satzbaustein</b>{e(it["b"])}</div>'+(f'<p class="merk"><b>Merke</b>{e(it["x"])}</p>' if it["x"] else '')+'</div></details>'
    return h+'</div>'
def deck(cats):
    cs=cats.split(','); h='<p class="sub">Karte antippen zum Aufdecken</p><div class="s-deck">'
    for t,c,src_,d,x in D['B']:
        if c in cs: h+=f'<details class="s-card"><summary><small>{e(c)}</small><b>{e(t)}</b></summary><p>{e(d)}</p>'+(f'<p class="merk"><b>Beispiel</b>{e(x)}</p>' if x else '')+'</details>'
    return h+'</div>'
def gl():
    return ''.join(f'<div class="glb"><h3>{e(p["name"])}<span class="sub">{e(p["sub"])}</span></h3><div class="glbar"><i style="width:0%"></i></div><ol>'+''.join(f'<li>{e(i["t"])}</li>' for i in p['items'])+'</ol></div>' for p in D['PARTS'])
def tl():
    T_=D['TL']; mn,mx=T_['min'],T_['max']; x=lambda y:(y-mn)/(mx-mn)*100; h=''
    for j,(n,a_,b_,c) in enumerate(T_['bars']):
        h+=f'<div class="bar" style="left:{x(a_):.2f}%;width:calc({x(b_)-x(a_):.2f}% - 3px);background:{c};--j:{j}"></div><div class="lab" style="left:{x(a_):.2f}%">{e(n)}</div>'
    return h+''.join(f'<div class="yr" style="left:{x(y):.2f}%">{y}</div>' for y in T_['years'])
def cmp():
    h='<thead><tr><th></th>'+''.join(f'<th>{e(c)}</th>' for c in D['CMPH'])+'</tr></thead><tbody>'
    for r in D['CMP']: h+='<tr><th>'+e(r[0])+'</th>'+''.join(f'<td>{e(c)}</td>' for c in r[1:])+'</tr>'
    return h+'</tbody>'
def pool():
    return '<ul class="s-list">'+''.join(f'<li>{e(t)}<details class="s-sol"><summary>Lösung</summary><p><b>{e(D["SOL"][k])}.</b> {e(w)}</p></details></li>' for t,k,w in D['SO'])+'</ul>'
def margin():
    return '<div class="s-notes">'+''.join(f'<div><span class="q">{e(n["q"])}</span><p class="hand">{e(n["y"])}</p><p>{e(n["a"])}</p></div>' for n in D['ST'])+'</div>'
def quiz():
    h='<ol class="s-list">'
    for q,opts,c,ex in D['Q']:
        h+=f'<li><div class="q">{e(q)}</div><ol type="A">'+''.join(f'<li>{e(o)}</li>' for o in opts)+f'</ol><details class="s-sol"><summary>Lösung</summary><p><b>{"ABCD"[c]}: {e(opts[c])}</b></p><p>{e(ex)}</p></details></li>'
    return h+'</ol>'
def route():
    return ''.join(f'<li><a href="#s-{i}"><span class="n">{k+2:02d}</span><span>{e(t)}</span><span class="m">{m}′</span></a></li>' for k,(i,t,m,ty) in enumerate(st[1:]))
def pathlist():
    return ''.join(f'<li class="st"><a href="#s-{i}"><span class="d" aria-hidden="true"></span><span class="tx"><span class="ti">{e(t)}</span>'+(f'<span class="u">{ty}</span>' if ty else '')+f'</span><span class="m">{m}′</span></a></li>' for i,t,m,ty in st)
def spick():
    return ''.join(f'<div class="glb"><h3>{e(p["name"])}<span class="sub">{e(p["sub"])}</span></h3><ul style="margin-top:12px">'+''.join(f'<li>{e(i["t"])}</li>' for i in p['items'])+'</ul></div>' for p in D['PARTS'])
def outtext():
    x=D['EX']['buelow']
    p1=f'Bei der vorliegenden Quelle handelt es sich um {x["art"]} von {x["autor"]}, {x["funktion"]}, vom {x["datum"]}. Sie entstand {x["ort"]}. Sie richtet sich an {x["adressat"]}. Thema ist {x["thema"]}. {x["kontext"]}'
    p2=f'{x["inhalt"]} Erkennbar wird dabei die Absicht, {x["absicht"]}.'
    return f'<p class="sub" style="margin-bottom:10px">Beispiel an der Bülow-Rede:</p><p>{e(p1)}</p><p>{e(p2)}</p>'
def plan():
    h,t='',0
    for n,f,c in [("Text lesen, markieren",.12,"var(--verdeckt)"),("Stichpunkte sammeln",.06,"var(--mint)"),("Aufgabe 1, Eckdaten",.10,"var(--offen)"),("Aufgabe 2, Zusammenfassen",.30,"var(--plum-t)"),("Aufgabe 3, Sachurteil",.36,"var(--teal-t)"),("Korrektur",.06,"var(--rule)")]:
        mm=max(5,round(90*f/5)*5); h+=f"<tr><td><i style='background:{c}'></i>{n}</td><td>{mm} min</td><td>{t}–{t+mm}</td></tr>"; t+=mm
    return h
def resume(): return '<a class="nextcard" style="margin-top:0" href="#s-plan"><span><small>Beginnt mit dem Plan für die Klausur</small><b>Lernpfad starten</b></span></a>'
def gen(tag):
    k,_,arg=tag.partition(':')
    if k=='items': pi,r=arg.split(':'); a_,b_=map(int,r.split('-')); return items(int(pi),a_,b_)
    if k=='deck': return deck(arg)
    return {'gl':gl,'tl':tl,'cmp':cmp,'pool':pool,'margin':margin,'quiz':quiz,'route':route,'resume':resume,'spick':spick,'outtext':outtext,'pathlist':pathlist,'plan':plan}[k]()
import datetime
src=src.replace('__BUILD__',datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))).strftime('%d.%m.%Y, %H:%M'))
src=re.sub(r'<!--S:([^>]+?)-->',lambda m:gen(m.group(1)),src)
# Erklär-Audio: noch keins für diese Seite, NARR bleibt null
assert '<!--S:' not in src
os.makedirs('dist/website',exist_ok=True)
import io as _io
pwa='<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="icon-180.png"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">'
open('dist/website/index.html','w',encoding='utf-8').write(src.replace('<!--PWA-->',pwa))
# Icon und Vorschaubild mit den echten Schriften (aus den Fontsource-WOFF in ttf/ umgewandelt)
TT='ttf/'
def icon(S):
    im=Image.new('RGB',(512,512),'#17181d'); d=ImageDraw.Draw(im)
    for x in range(0,120):
        k=1-x/120; c=(int(23+40*k),int(24+20*k),int(29+70*k))
        d.line([(x,0),(x,512)],fill=c); d.line([(511-x,0),(511-x,512)],fill=c)
    d.rounded_rectangle([64,118,448,354],radius=26,fill='#e3d6f3')
    F=ImageFont.truetype(TT+'bricolage-grotesque-800-normal.ttf',176)
    w=d.textlength("Kr",font=F); d.text(((512-w)/2,118+18),"Kr",font=F,fill='#16181b')
    d.line([(40,420),(472,420)],fill='#3a3c42',width=10)
    d.line([(40,420),(250,420)],fill='#e2523f',width=22); d.ellipse([238,408,262,432],fill='#e2523f')
    return im.resize((S,S),Image.LANCZOS)
icon(32).save('dist/website/favicon-32.png')
for s_ in (180,192,512): icon(s_).save(f'dist/website/icon-{s_}.png')
# Vorschaubild für geteilte Links (WhatsApp, iMessage, Discord)
def og():
    W,Hh=1200,630; im=Image.new('RGB',(W,Hh),'#17181d'); d=ImageDraw.Draw(im)
    for x in range(0,160):
        k=1-x/160; c=(int(23+40*k),int(24+20*k),int(29+70*k))
        d.line([(x,0),(x,Hh)],fill=c); d.line([(W-1-x,0),(W-1-x,Hh)],fill=c)
    I_=ImageFont.truetype(TT+'literata-400-italic.ttf',34); B_=ImageFont.truetype(TT+'bricolage-grotesque-800-normal.ttf',96); R_=ImageFont.truetype(TT+'literata-400-normal.ttf',32)
    d.text((140,150),"Lernpfad zur Geschichtsklausur, 1871 bis 1918",font=I_,fill='#c9b3ef')
    d.text((140,210),"Kaiserreich",font=B_,fill='#f2f0e8'); d.text((140,318),"und Kolonien",font=B_,fill='#f2f0e8')
    d.text((140,460),"Gesellschaft, Industrialisierung, Kongokonferenz, Quellen, Quiz",font=R_,fill='#b8b9b4')
    d.line([(140,545),(1060,545)],fill='#3a3c42',width=5); d.line([(140,545),(560,545)],fill='#e2523f',width=6); d.ellipse([552,537,568,553],fill='#e2523f')
    im.save('dist/website/og.png',optimize=True)
og()

json.dump({"name":"Kaiserreich und Kolonien","short_name":"Kaiserreich","start_url":"./","scope":"./","display":"standalone","background_color":"#17181d","theme_color":"#17181d","lang":"de",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},open('dist/website/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
open('dist/website/sw.js','w').write("""// Immer zuerst die neueste Fassung von GitHub holen (am HTTP-Cache vorbei), offline aus dem Speicher.
// Löscht nur eigene alte Caches: Auf comroboter.github.io teilen sich alle Lernseiten denselben Speicher.
const P='kaiserreich-';const C=P+'v1';const A=['./','./index.html','./manifest.webmanifest','./icon-180.png','./icon-192.png','./icon-512.png','./favicon-32.png','./og.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A.map(u=>new Request(u,{cache:'reload'})))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith(P)&&n!==C).map(n=>caches.delete(n)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
  e.respondWith(fetch(r.url,{cache:'no-cache',credentials:'same-origin'}).then(res=>{if(res.ok){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res})
    .catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||caches.match('./index.html'))))});
""")
_b=_io.BytesIO();icon(32).save(_b,'PNG')
open('dist/kaiserreich.html','w',encoding='utf-8').write(src.replace('<!--PWA-->','<link rel="icon" type="image/png" href="data:image/png;base64,'+base64.b64encode(_b.getvalue()).decode()+'">'))
shutil.make_archive('dist/kaiserreich-website','zip','dist/website')
for f in sorted(glob.glob('dist/**',recursive=True)):
    if os.path.isfile(f): print(f, os.path.getsize(f))
