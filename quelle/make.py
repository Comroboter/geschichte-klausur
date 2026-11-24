"""Baut app.html der Geschichts-Lernseite aus dem Antigone-Gerüst (template.html),
stations.html (Stationen) und data.js (Datenblock)."""
import re, sys

T = open('template.html', encoding='utf-8').read()
ST = open('stations.html', encoding='utf-8').read()
DATA = open('data.js', encoding='utf-8').read()

def must(cond, msg):
    if not cond:
        sys.exit('FEHLER: ' + msg)

def rep(s, old, new, count=1):
    n = s.count(old)
    must(n >= 1, 'nicht gefunden: ' + old[:90])
    if count == 1:
        must(n == 1, f'{n}x gefunden: ' + old[:90])
    return s.replace(old, new)

def resub(s, pat, new, flags=re.S):
    s2, n = re.subn(pat, new, s, count=1, flags=flags)
    must(n == 1, 'Regex ohne Treffer: ' + pat[:90])
    return s2

# ---------- Teile aus dem Gerüst für die Stationen holen ----------
def hero_inner(sid):
    m = re.search(r'id="s-' + re.escape(sid) + r'".*?<header class="hero" data-n="\d+">(.*?)\n    <div class="kicker">', T, re.S)
    must(m, 'Hero nicht gefunden: ' + sid)
    return m.group(1)

def art(sid):
    h = hero_inner(sid)
    return h.replace('<div class="deco" aria-hidden="true"></div>', '', 1)

ST = ST.replace('{{STARTDECO}}', hero_inner('start'))
for sid in ['plan', 'handwerk', 'einleitung-bauen', 'sortieren', 'figuren', 'quiz', 'kurz-vorher']:
    ST = ST.replace('{{ART:' + sid + '}}', art(sid))
must('{{' not in ST, 'Platzhalter übrig')

# ---------- Stations-IDs in CSS und JS umbenennen ----------
MAP = [('antigone-deuten', 'urteilen'), ('einleitung-bauen', 'einleitung'), ('einleitung', 'gesellschaft'),
       ('handlung', 'industrie'), ('antigone', 'quelle'), ('figuren', 'kolonien'), ('schluss', 'rassismus'),
       ('epochen', 'moderne'), ('vergleich', 'kongo')]
a = T.index('<!-- 1 START -->'); b = T.index('</main>')
head, tail = T[:a], T[b:]
def rename(s):
    for i, (old, new) in enumerate(MAP):
        tok = f'@@{i}@@'
        s = re.sub(r'#s-' + re.escape(old) + r'(?![a-z-])', '#s-' + tok, s)
        s = re.sub(r'data-sid="' + re.escape(old) + r'"', 'data-sid="' + tok + '"', s)
        s = re.sub(r'"s-' + re.escape(old) + r'"', '"s-' + tok + '"', s)
        s = s.replace('"' + old + '":function', '"' + tok + '":function')
        s = re.sub(r'(?<=[{,\s])' + re.escape(old) + r'(?=:function)', tok, s)
        s = s.replace('id==="' + old + '"', 'id==="' + tok + '"')
    for i, (old, new) in enumerate(MAP):
        s = s.replace(f'@@{i}@@', new)
    return s
head = rename(head); tail = rename(tail)
T = head + ST + '\n' + tail

# ---------- Kopf ----------
T = rep(T, '<meta name="apple-mobile-web-app-title" content="Dramenanalyse">', '<meta name="apple-mobile-web-app-title" content="Kaiserreich">')
T = rep(T, '<title>Dramenszenenanalyse lernen</title>', '<title>Kaiserreich und Kolonien lernen</title>')
T = resub(T, r'<meta name="description" content="[^"]*">', '<meta name="description" content="Lernpfad zur Geschichtsklausur: Gesellschaft im Kaiserreich, Industrialisierung, Moderne und Tradition, Kolonien, Rassismus, Kongokonferenz, Quellenanalyse und Quiz.">')
T = resub(T, r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Kaiserreich und Kolonien">')
T = resub(T, r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Lernpfad zur Geschichtsklausur: Gesellschaft, Industrialisierung, Kolonien, Quellen, Quiz.">')
T = T.replace('https://comroboter.github.io/dramenszenenanalyse-klausur/', 'https://comroboter.github.io/geschichte-klausur/')
T = rep(T, '/* Layout-Idee: ein Lernpfad mit 15 Stationen, verbunden durch einen roten Faden. Jede Station beginnt mit einer kleinen Bühne (Vorhang, Spotlight), darunter das Arbeitsblatt in den Textmarker-Farben der Unterrichtsnotizen. */',
        '/* Layout-Idee: ein Lernpfad mit 15 Stationen, verbunden durch einen roten Faden. Jede Station beginnt mit einer kleinen Bühne im Dunkeln, die Zeile über dem Titel ist wie eine Quellenangabe gesetzt. */')

# ---------- Seitenleiste ----------
T = rep(T, '<div class="brand">Dramenszene<br>analysieren<small><span class="dot" aria-hidden="true"></span>Klausur am 17. November</small></div>',
        '<div class="brand">Kaiserreich<br>und Kolonien<small><span class="dot" aria-hidden="true"></span>Geschichtsklausur</small></div>')
T = rep(T, '<span id="sxmin">135 min</span>', '<span id="sxmin">90 min</span>')
T = resub(T, r'<ul>\s*<li><small class="lb">Handlung</small>.*?</ul>',
          '<ul>\n'
          '        <li><span class="sx-hand">Randnotiz</span><small>so markierst du selbst</small></li>\n'
          '        <li><small class="lb">Stand</small><small>nach der Lernübersicht zur Klausur (ab Punkt 1c), wenige Lücken ergänzt</small></li>\n      </ul>')

# ---------- Datenblock ----------
a = T.index('/* ================= DATEN ================= */'); b = T.index('/* ================= ZUSTAND')
T = T[:a] + DATA + '\n' + T[b:]

# ---------- JS-Anpassungen ----------
T = T.replace('localStorage.getItem("dra_"+k)', 'localStorage.getItem("kr_"+k)').replace('localStorage.setItem("dra_"+k', 'localStorage.setItem("kr_"+k')
must('"dra_' not in T, 'Speicherpräfix')
T = rep(T, '"<h2>"+p.name+(pi===1?(a===0?", Teil A":", Teil B"):"")+"</h2>', '"<h2>"+esc(p.head||p.name)+"</h2>')
T = rep(T, 'cb.addEventListener("change",function(){chk[id]=cb.checked;store.set("chk",chk);d.classList.toggle("done",cb.checked);if(cb.checked)buzz(8);upd()});',
        'cb.addEventListener("change",function(){chk[id]=cb.checked;store.set("chk",chk);d.classList.toggle("done",cb.checked);if(cb.checked)buzz(8);upd();updGl()});')
T = rep(T, "+p.items.map(function(it){return\"<li>\"+esc(it.t)+\"</li>\"}).join(\"\")+\"</ol>\";gl.appendChild(b)})})();",
        "+p.items.map(function(it){return\"<li>\"+esc(it.t)+\"</li>\"}).join(\"\")+\"</ol>\";gl.appendChild(b)});updGl()})();\n/* Plan: Balken zeigen, wie viele Punkte je Block schon sitzen */\nfunction updGl(){var gl=document.getElementById(\"gl\");if(!gl)return;[].forEach.call(gl.querySelectorAll(\".glb\"),function(b,pi){var p=PARTS[pi];if(!p)return;var n=0;p.items.forEach(function(_,ii){if(chk[\"c\"+pi+\"_\"+ii])n++});var i=b.querySelector(\".glbar i\");if(i)i.style.width=Math.round(n/p.items.length*100)+\"%\";var s=b.querySelector(\"h3 .sub\");if(s)s.textContent=n+\" von \"+p.items.length+\" sitzen\"})}")
T = rep(T, 'if(it.x)body.appendChild(el("p",{class:"hand"},esc(it.x)));', 'if(it.x)body.appendChild(el("p",{class:"merk"},"<b>Merke</b>"+esc(it.x)));')
T = resub(T, r'var PLAN=\[\[.*?\]\];', 'var PLAN=[["Text lesen, markieren",.12,"var(--verdeckt)"],["Stichpunkte sammeln",.06,"var(--mint)"],["Aufgabe 1, Eckdaten",.10,"var(--offen)"],["Aufgabe 2, Zusammenfassen",.30,"var(--plum-t)"],["Aufgabe 3, Sachurteil",.36,"var(--teal-t)"],["Korrektur",.06,"var(--rule)"]];')
T = rep(T, 'if(!(m>0))m=135;', 'if(!(m>0))m=90;')
T = rep(T, """var tag=b[2]==="u"?'<span class="tag u">Unterlagen</span>':'<span class="tag">Ergänzung</span>';""", """var tag=b[2]==="u"?'<span class="tag u">Unterlagen</span>':'';""")
T = rep(T, '/* ================= ANTIGONE ================= */', '/* ================= QUELLE ================= */')
T = rep(T, 'showSt(1);', 'showSt(0);')
T = rep(T, 'bo=el("button",{class:"o"},"offen"),bv=el("button",{class:"v"},"verdeckt");', 'bo=el("button",{class:"o"},SOL.o),bv=el("button",{class:"v"},SOL.v);')
T = rep(T, '"Du hattest "+(a==="o"?"offen":"verdeckt")+"."', '"Du hattest "+(a==="o"?SOL.o:SOL.v)+"."')
T = resub(T, r'/\* ================= EPOCHEN ================= \*/\n\(function\(\)\{var tl=.*?\}\)\(\);\n',
          '/* ================= MODERNE ================= */\n(function(){var tl=document.getElementById("tl"),min=TL.min,max=TL.max;tl.innerHTML="";function x(y){return(y-min)/(max-min)*100}\n'
          ' TL.bars.forEach(function(e,j){\n'
          '   var bar=el("div",{class:"bar"});bar.style.left=x(e[1])+"%";bar.style.width="calc("+(x(e[2])-x(e[1]))+"% - 3px)";bar.style.background=e[3];bar.style.setProperty("--j",j);tl.appendChild(bar);\n'
          '   var lab=el("div",{class:"lab"},esc(e[0]));lab.style.left=x(e[1])+"%";tl.appendChild(lab)});\n'
          ' TL.years.forEach(function(y){var t=el("div",{class:"yr"},y);t.style.left=x(y)+"%";tl.appendChild(t)})})();\n')
T = rep(T, '(function(){var h="<thead><tr><th></th><th>Antike</th><th>Barock</th><th>Aufklärung</th></tr></thead><tbody>";',
        '(function(){var h="<thead><tr><th></th>"+CMPH.map(function(c){return"<th>"+esc(c)+"</th>"}).join("")+"</tr></thead><tbody>";')

# Generator: Einleitung einer Quellenanalyse
a = T.index('/* ================= EINLEITUNG BAUEN ================= */'); b = T.index('var out=document.getElementById("outtext")')
T = T[:a] + r'''/* ================= EINLEITUNG BAUEN ================= */
var F=["art","autor","funktion","datum","ort","adressat","thema","kontext","inhalt","absicht"];
function v(k){return document.getElementById("f-"+k).value.trim()}
function end(t){return /[.!?“"]$/.test(t)?t:t+"."}
function vt(k){return document.getElementById("f-"+k).value.trim()}
function compose(){var p1=[],p2=[];
  if(v("art")||v("autor")){var s="Bei der vorliegenden Quelle handelt es sich um "+(v("art")||"eine Quelle");
    if(v("autor"))s+=" von "+v("autor");
    if(v("funktion"))s+=", "+v("funktion")+",";
    var d=v("datum");if(d)s+=(/^\d{1,2}\./.test(d)?" vom ":/^\d{3,4}$/.test(d)?" aus dem Jahr ":" ")+d;
    p1.push(end(s.replace(/,$/,"")))}
  if(v("ort"))p1.push(end("Sie entstand "+v("ort")));
  if(v("adressat"))p1.push(end("Sie richtet sich an "+v("adressat")));
  if(v("thema"))p1.push(end("Thema ist "+v("thema")));
  if(vt("kontext"))p1.push(vt("kontext"));
  if(vt("inhalt"))p2.push(vt("inhalt"));
  if(v("absicht"))p2.push(end("Erkennbar wird dabei die Absicht, "+v("absicht").replace(/\.$/,"")));
  return[p1.join(" "),p2.join(" ")].filter(Boolean)}
'''.replace('\\d', '\\d') + T[b:]
T = rep(T, '''function checks(){var cs=[["Einstieg mit Aktualitätsbezug",v("einstieg")],["Autor, Titel, Jahr",v("autor")&&v("titel")&&v("jahr")],["Thema und Kontext",v("thema")&&v("kontext")],["Ort, Zeit, Figuren",v("ort")&&v("figuren")],["Inhalt im Präsens",v("inhalt")],["Einordnung",v("einordnung")],["Deutungshypothese",v("hypo")]];
  var tw=/\\b(war|hatte|ging|kam|sagte|erzählte|bat|lehnte|wollte|wurde)\\b/i.test(v("inhalt"));
  document.getElementById("checks").innerHTML=cs.map(function(c){return'<li class="'+(c[1]?"":"miss")+'"><span class="b">'+(c[1]?"✓":"")+'</span>'+c[0]+'</li>'}).join("")+(tw?'<li class="warn"><span class="b">!</span>Präteritum in der Inhaltsangabe: ins Präsens setzen</li>':"")}''',
        '''function checks(){var cs=[["Quellenart und Verfasser",v("art")&&v("autor")],["Datum",v("datum")],["Ort, Anlass, Adressat",v("ort")&&v("adressat")],["Thema",v("thema")],["Historischer Kontext",v("kontext")],["Kernaussagen",v("inhalt")],["Absicht",v("absicht")]];
  var tw=/\\b(sagte|forderte|erklärte|meinte|betonte|wollte|verlangte|kündigte|war|hatte)\\b/i.test(v("inhalt")),kj=v("inhalt")&&!/\\b(sei|seien|habe|müsse|müssten|werde|würden?|wolle|dürfe|könne|solle)\\b/i.test(v("inhalt"));
  document.getElementById("checks").innerHTML=cs.map(function(c){return'<li class="'+(c[1]?"":"miss")+'"><span class="b">'+(c[1]?"✓":"")+'</span>'+c[0]+'</li>'}).join("")+(tw?'<li class="warn"><span class="b">!</span>Präteritum bei den Kernaussagen: ins Präsens setzen</li>':"")+(kj?'<li class="warn"><span class="b">!</span>Indirekte Rede fehlt: Konjunktiv nutzen (sei, habe, müsse)</li>':"")}''')
T = rep(T, 'F.forEach(function(f){document.getElementById("f-"+f).value=EX.antigone[f]||""});', 'F.forEach(function(f){document.getElementById("f-"+f).value=EX.buelow[f]||""});')
T = rep(T, '''document.querySelector('[data-ex="antigone"]').setAttribute("aria-pressed","true");''', '''document.querySelector('[data-ex="buelow"]').setAttribute("aria-pressed","true");''')
T = rep(T, 'Geh die Stationen 4 bis 11 nochmal durch und mach das Quiz danach erneut.', 'Geh die Stationen 5 bis 13 nochmal durch und mach das Quiz danach erneut.')
T = rep(T, 'Sitzt. In der Klausur vor allem auf saubere Belege achten.', 'Sitzt. In der Klausur vor allem auf Zeilenbelege und ein klares Urteil achten.')
T = resub(T, r'var ACTS=\{[^}]*\}', 'var ACTS={"start":["I","Vorspiel"],"revolution":["II","Reich und Gesellschaft"],"kolonien":["III","Kolonien"],"aufgaben":["IV","Finale"]}')
T = resub(T, r'\(function\(\)\{var b=document\.querySelector\("\.path \.brand small"\);.*?\}\)\(\);',
          '''(function(){var b=document.querySelector(".path .brand small");if(!b)return;if(!KLAUSUR){b.innerHTML='<span class="dot" aria-hidden="true"></span>Geschichtsklausur, Datum offen';return}var n=new Date(),d=Math.round((KLAUSUR-new Date(n.getFullYear(),n.getMonth(),n.getDate()))/864e5);var w=d===0?"Klausur heute":d===1?"Klausur morgen":d>1?"Klausur in "+d+" Tagen":"Klausur geschrieben";b.innerHTML='<span class="dot" aria-hidden="true"></span>'+w})();''')
T = resub(T, r'"kurz-vorher":function\(\)\{\(function\(\)\{var t=document\.getElementById\("luckt"\),u=document\.getElementById\("lucks"\);if\(!t\)return;.*?\}\)\(\);var sp=',
          '''"kurz-vorher":function(){(function(){var t=document.getElementById("luckt"),u=document.getElementById("lucks");if(!t||!KLAUSUR)return;var n=new Date(),d=KLAUSUR,diff=Math.round((new Date(d.getFullYear(),d.getMonth(),d.getDate())-new Date(n.getFullYear(),n.getMonth(),n.getDate()))/864e5);
    t.textContent=diff>1?"Noch "+diff+" Tage":diff===1?"Morgen ist es so weit":diff===0?"Heute: viel Erfolg!":"Geschafft!";if(diff<0)u.textContent="Die Klausur ist geschrieben. Die Seite bleibt zum Nachschlagen."})();var sp=''')
T = rep(T, """'<h2>Alle 18 Punkte abgehakt</h2>""", """'<h2>Alle '+TOTAL_ITEMS+' Punkte abgehakt</h2>""")
T = rep(T, 'function buildMeander(st){', 'function buildMeander(st){return;')
T = rep(T, 'if(!btn||!NARR)return;', 'if(!btn)return;if(!NARR){btn.hidden=true;btn.style.display="none";return}')
T = resub(T, r'/\* Vergleich: blockweise oder verzahnt, Reißverschluss-Zeilen \*/\n.*?\n(?=/\* Zurück:)',
          '/* Kongo: Mythos oder Tatsache, Reißverschluss-Zeilen */\n(function(){[].forEach.call(document.querySelectorAll("#zip .zbtn"),function(b){b.addEventListener("click",function(){var r=b.parentNode,o=!r.classList.contains("open");r.classList.toggle("open",o);b.setAttribute("aria-expanded",o?"true":"false")})})})();\n')
T = rep(T, '/* Antigone deuten: Spannungsbogen */', '/* Kolonialzeit: sieben Etappen */')
T = T.replace('navigator.share({title:"Dramenszene analysieren",text:"Lernpfad zur Deutsch-Klausur",url:SITE})', 'navigator.share({title:"Kaiserreich und Kolonien",text:"Lernpfad zur Geschichtsklausur",url:SITE})')


# Kurze Seiten: In der Vorschau-Kopie fehlte der Abstand, den fixRest der echten Seite gibt, deshalb rutschte die
# übernächste Vorschau nach dem Wechsel nach (bekanntes Problem der Antigone-Seite). Jetzt rechnet die Kopie ihn selbst aus.
T = rep(T, 'into.setAttribute("data-look",st.getAttribute("data-look"));into.setAttribute("data-sid",ids[t]);syncSvg(h,into);fixInk(into);watchSvgs(into)}',
        'into.setAttribute("data-look",st.getAttribute("data-look"));into.setAttribute("data-sid",ids[t]);syncSvg(h,into);fixInk(into);watchSvgs(into);if(deep)fixCloneRest(into)}\n'
        'function fixCloneRest(into){try{var run=into.querySelector(":scope > .content > .runway"),h0=into.querySelector(":scope > .hero"),hc=cur>=0&&stations[cur]?stations[cur].querySelector(".hero"):null;if(!run||!h0||!hc)return;'
        'var r=into.getBoundingClientRect(),sc=into.offsetWidth?r.width/into.offsetWidth:1;if(!(sc>0))sc=1;var rel=(run.getBoundingClientRect().top-h0.getBoundingClientRect().top)/sc,abs=hc.getBoundingClientRect().top+scrollY+rel,need=innerHeight-padB()-abs;'
        'if(need>0){run.style.marginTop=need+"px";run.style.setProperty("--rw-up",Math.max(0,need-14)+"px")}else run.style.setProperty("--rw-up","0px")}catch(e){}}')

# ---------- Ruckler beim Scrollen und beim Seitenwechsel (Messung 19.11.) ----------
# 1. --ac-cur nur an der unteren Leiste setzen: an :root löste es bei jedem Wechsel eine Stilberechnung des ganzen Dokuments aus (30 bis 45 ms am PC).
T = rep(T, 'if(ac)document.documentElement.style.setProperty("--ac-cur",ac)}catch(e){}', 'if(ac&&BBAR)BBAR.style.setProperty("--ac-cur",ac)}catch(e){}')
# 2. Ruhe-Erkennung: Vorarbeiten nur, wenn seit 800 ms keine Eingabe kam
T = rep(T, 'var leaveAnim=null,viaPeek=false;',
        'var leaveAnim=null,viaPeek=false;\n'
        'var BBAR=document.querySelector(".bottombar"),lastInput=0;["wheel","touchstart","touchmove","keydown","pointerdown","scroll"].forEach(function(ty){window.addEventListener(ty,function(){lastInput=performance.now()},{passive:true,capture:true})});\n'
        'function quiet(ms){return !peekBusy&&!document.querySelector(".back-ov")&&performance.now()-lastInput>=(ms||800)}\n'
        'function quietIdle(f,ms){function go(){if(!quiet(ms)){setTimeout(go,350);return}if(window.requestIdleCallback)requestIdleCallback(function(){if(!quiet(ms)){setTimeout(go,350);return}f()},{timeout:1200});else f()}setTimeout(go,ms||800)}\n'
        '/* 3. Overlay für den nächsten Wechsel schon in Ruhephasen bauen statt beim ersten Mausrad-Schritt (25 bis 45 ms) */\n'
        'function schedPrep(){var c=cur;quietIdle(function(){if(cur===c&&!peekBusy&&c+1<N&&pFor!==c+1){try{preparePeek(c+1)}catch(e){}}})}\n'
        '["change","input"].forEach(function(ty){document.addEventListener(ty,function(){pFor=-1},true)});\n'
        'document.addEventListener("click",function(e){var t=e.target;if(t&&t.closest&&t.closest("#next,#prev,.path,#where,.nextcard,.runway,.schwelle,.topbar"))return;pFor=-1},true);')
T = rep(T, 'moreEl.classList.remove("on");setTimeout(reqMore,350);if(window.narrOnStation)window.narrOnStation(i);if(window.vvUpdate)window.vvUpdate()}',
        'moreEl.classList.remove("on");setTimeout(reqMore,350);if(window.narrOnStation)window.narrOnStation(i);if(window.vvUpdate)window.vvUpdate();schedPrep()}')
# 4. Vorrechnen der übrigen Stationen nur in Ruhe, nie mitten im Scrollen (jede Station 20 bis 190 ms)
T = rep(T, 'function step(){if(peekBusy||document.querySelector(".back-ov")){setTimeout(step,400);return}',
        'function step(){if(!quiet(900)){setTimeout(step,400);return}')

# 5. Vorschau der übernächsten Station nicht im selben Task wie der Wechsel bauen, wenn sie unter dem Bildschirm liegt.
#    Knapp darunter: gleich nach dem ersten Bild. Weit darunter: erst in Ruhe.
#    Sie liegt dann weit unter dem sichtbaren Bereich. Kommt man ihr beim Scrollen nahe, wird sie sofort gebaut. Beim Zurück-Wechsel immer sofort.
T = rep(T, 'flung=false;buildMeander(stations[i]);fillPreview(i,true);fixInk(stations[i]);',
        'flung=false;buildMeander(stations[i]);var _rn=stations[i].querySelector(".runway"),_tp=_rn?_rn.getBoundingClientRect().top:0;if(!FILLNOW&&_rn&&_tp>innerHeight+40){pendFill=i;var _ff=function(){if(pendFill===cur){pendFill=-1;fillPreview(cur,true)}};if(_tp>innerHeight*1.6)quietIdle(_ff,300);else requestAnimationFrame(function(){setTimeout(_ff,0)})}else{pendFill=-1;fillPreview(i,true)}fixInk(stations[i]);')
T = rep(T, 'swapTo(t,-1,true);', 'FILLNOW=true;try{swapTo(t,-1,true)}finally{FILLNOW=false}')
T = rep(T, 'var BBAR=document.querySelector(".bottombar"),lastInput=0;', 'var BBAR=document.querySelector(".bottombar"),lastInput=0,pendFill=-1,FILLNOW=false;')
T = rep(T, 'function updateMore(){ticking=false;if(cur<0)return;', 'function updateMore(){ticking=false;if(cur<0)return;if(pendFill===cur){var _r=stations[cur].querySelector(".runway");if(_r&&_r.getBoundingClientRect().top<innerHeight*1.4){pendFill=-1;fillPreview(cur,true)}}')

# 6. SMIL-Zeit nur in sichtbare Kopien übertragen. In versteckten Stationen (verschachtelte Vorschau) erzwang setCurrentTime
#    eine Stilberechnung, die niemand sieht; cloneNode übernimmt den Zeitstand ohnehin nicht.
T = rep(T, 'function syncSvg(from,to){if(!from||!to)return;', 'function syncSvg(from,to){if(!from||!to)return;if(to.closest&&to.closest(".station:not(.on)"))return;')

# ---------- 7. Seitenwechsel ohne Ruckler ----------
# a) Mausrad-Wechsel: Zielposition des Kickers direkt aus der Vorschau in der Seite lesen. Sie stimmt auf allen Stationen und
#    Größen mit dem Overlay überein (gemessen bei 1440, 1080, 390 px). Spart den Bau des Overlays (25 bis 40 ms vor dem Start).
T = rep(T, """  preparePeek(t);pIn.style.transform="";pSheet.style.transform="";
  var pk=pIn.querySelector(".kicker"),Kref=pk?pk.getBoundingClientRect().top-pSheet.getBoundingClientRect().top-pSheet.clientTop:0;
  var rs=inflow&&stations[cur]&&stations[cur].querySelector(".rw-sheet");
  if(rs&&rs.getClientRects().length&&rs.getBoundingClientRect().top<H-10){""", """  var rs=inflow&&stations[cur]&&stations[cur].querySelector(".rw-sheet"),rsIn=!!(rs&&rs.getClientRects().length&&rs.getBoundingClientRect().top<H-10),rsK=rsIn&&rs.querySelector(".rw-in .kicker"),Kref=0;
  if(rsK){Kref=rsK.getBoundingClientRect().top-tyOf(rs.querySelector(".rw-in"))-rs.getBoundingClientRect().top-rs.clientTop}
  else{rsIn=false;preparePeek(t);pIn.style.transform="";pSheet.style.transform="";var pk=pIn.querySelector(".kicker");Kref=pk?pk.getBoundingClientRect().top-pSheet.getBoundingClientRect().top-pSheet.clientTop:0}
  if(rsIn){""")
# b) Rand des Blatts: Farbe bleibt bis 55 % stehen, neu gezeichnet wird nur im letzten Stück.
T = rep(T, 'anims.push(sheet.animate([{borderTopLeftRadius:"28px",borderTopRightRadius:"28px",borderTopColor:getComputedStyle(sheet).borderTopColor,offset:0},{borderTopLeftRadius:"28px",borderTopRightRadius:"28px",offset:.55}',
        'var _btc=getComputedStyle(sheet).borderTopColor;anims.push(sheet.animate([{borderTopLeftRadius:"28px",borderTopRightRadius:"28px",borderTopColor:_btc,offset:0},{borderTopLeftRadius:"28px",borderTopRightRadius:"28px",borderTopColor:_btc,offset:.55}')
# c) Beim Wechsel nur alte und neue Station anfassen statt aller SVGs in allen Stationen. Neue Kopien in versteckten Stationen ruhen sofort.
T = rep(T, 'stations.forEach(function(x,k){x.querySelectorAll("svg").forEach(function(v){try{if(k===i)v.unpauseAnimations();else v.pauseAnimations()}catch(e){}})});',
        '(function(){function each(x,f){if(x)x.querySelectorAll("svg").forEach(function(v){try{f(v)}catch(e){}})}if(!old)stations.forEach(function(x,k){if(k!==i)each(x,function(v){v.pauseAnimations()})});else if(old!==s)each(old,function(v){v.pauseAnimations()});each(s,function(v){v.unpauseAnimations()})})();')
T = rep(T, 'into.setAttribute("data-look",st.getAttribute("data-look"));into.setAttribute("data-sid",ids[t]);syncSvg(h,into);fixInk(into);watchSvgs(into);',
        'into.setAttribute("data-look",st.getAttribute("data-look"));into.setAttribute("data-sid",ids[t]);syncSvg(h,into);if(into.closest&&into.closest(".station:not(.on)"))into.querySelectorAll("svg").forEach(function(v){try{v.pauseAnimations()}catch(e){}});fixInk(into);watchSvgs(into);')
# d) Untere Vorschau neu bauen, ohne das Ende des Wechsels zu bremsen: Liegt der Teil, in dem sich vorhandene und neue Kopie
#    unterscheiden, unter dem Bildschirm, wird erst nach dem ersten Bild gebaut. Die Zeichnung behält dabei ihre Zeit.
T = rep(T, 'var _rn=stations[i].querySelector(".runway"),_tp=_rn?_rn.getBoundingClientRect().top:0;if(!FILLNOW&&_rn&&_tp>innerHeight+40){pendFill=i;var _ff=function(){if(pendFill===cur){pendFill=-1;fillPreview(cur,true)}};',
        'var _rn=stations[i].querySelector(".runway"),_tp=_rn?_rn.getBoundingClientRect().top:0,_ri=_rn&&_rn.querySelector(".rw-in"),_sc=_ri&&_ri.children.length&&_ri.querySelector(":scope > .content"),_far=_tp>innerHeight+40,_soft=!_far&&!!_sc&&(!!_sc.querySelector(".schwelle")||_sc.getBoundingClientRect().bottom>innerHeight+40);if(!FILLNOW&&_rn&&(_far||_soft)){pendFill=i;var _ff=function(){if(pendFill===cur){pendFill=-1;refill(cur)}};')
T = rep(T, 'function fillPreview(i,deep){', 'function refill(i){var ri=stations[i]&&stations[i].querySelector(":scope > .content > .runway .rw-in");if(!ri){fillPreview(i,true);return}var tm=[];ri.querySelectorAll(":scope > .hero svg").forEach(function(v){try{tm.push(v.getCurrentTime())}catch(e){tm.push(null)}});fillPreview(i,true);ri.querySelectorAll(":scope > .hero svg").forEach(function(v,k){try{if(tm[k]!=null)v.setCurrentTime(tm[k])}catch(e){}})}\nfunction fillPreview(i,deep){')
T = rep(T, 'if(pendFill===cur){var _r=stations[cur].querySelector(".runway");if(_r&&_r.getBoundingClientRect().top<innerHeight*1.4){pendFill=-1;fillPreview(cur,true)}}',
        'if(pendFill===cur){var _r=stations[cur].querySelector(".runway");if(_r&&_r.getBoundingClientRect().top<innerHeight*1.4){pendFill=-1;refill(cur)}}')
#    Die Zeichnung in der unteren Vorschau übernimmt am Ende die Zeit aus der Kopie, die gerade hochgefahren ist.
T = rep(T, 'try{resetSw();pull=0;viaPeek=true;show(t);syncSvg(inner,stations[t].querySelector(".hero"));',
        'try{resetSw();pull=0;viaPeek=true;show(t);syncSvg(inner,stations[t].querySelector(".hero"));syncSvg(inner.querySelector(":scope > .content .runway .rw-in > .hero"),stations[t].querySelector(":scope > .content > .runway .rw-in"));')
# e) Mausrad: Der blockierende Listener hängt nur noch, solange die Schwelle scharf ist. Sonst scrollt der Browser,
#    ohne auf den Hauptthread zu warten. Oben am Seitenanfang braucht es keinen, overscroll-behavior ist schon none.
T = rep(T, 'var wdPrev=0,shownAt=0;window.addEventListener("wheel",function(e){var nw=performance.now(),gp=nw-wdPrev;if(e.deltaY>0)wdPrev=nw;if(peekBusy',
        'var wdPrev=0,wdGap=1e9,shownAt=0,wgOn=false;window.addEventListener("wheel",function(e){if(e.deltaY>0){var nw=performance.now();wdGap=nw-wdPrev;wdPrev=nw}},{passive:true});\nfunction syncWG(){var need=armed();if(need!==wgOn){wgOn=need;if(need)window.addEventListener("wheel",wheelFwd,{passive:false});else window.removeEventListener("wheel",wheelFwd,{passive:false})}}\nfunction wheelFwd(e){var nw=performance.now(),gp=wdGap;if(peekBusy')
T = rep(T, 'pullReady=true;flung=false;crossSw()},{passive:false});', 'pullReady=true;flung=false;crossSw()}')
T = rep(T, 'r.classList.add("armed");pausedAtRest=true;', 'r.classList.add("armed");pausedAtRest=true;syncWG();')
T = rep(T, 'if(r&&armed()){r.classList.remove("armed");var sw=curSw();if(sw)sw.classList.remove("armed")}pausedAtRest=false}', 'if(r&&armed()){r.classList.remove("armed");var sw=curSw();if(sw)sw.classList.remove("armed")}pausedAtRest=false;syncWG()}')
T = rep(T, 'if(gap<280||now-lastScrollT<350)return;e.preventDefault();backTo(cur-1,true)},{passive:false});', 'if(gap<280||now-lastScrollT<350)return;backTo(cur-1,true)},{passive:true});')

# f) Beim Wechsel über die Vorschau laufen keine Einstiegs-Animationen (via-peek schaltet sie ab). Dann auch keine
#    Zufallsvarianten und Staffelwerte setzen, das spart eine Stilberechnung am Ende des Wechsels.
T = rep(T, 's.setAttribute("data-in",pick(["slide","blur","drop","wipe"]));', 'if(!pk){s.setAttribute("data-in",pick(["slide","blur","drop","wipe"]));')
T = rep(T, 's.querySelectorAll(".content > *").forEach(function(c,k){c.style.setProperty("--i",Math.min(k,5))});', 's.querySelectorAll(".content > *").forEach(function(c,k){c.style.setProperty("--i",Math.min(k,5))})}')

# ---------- 8. Hochwischen am Seitenende ohne Geschwindigkeitsbruch (iPad, Handy) ----------
# Vorher: Nach dem Loslassen lief der Schwung aus, die Seite stand 200 bis 240 ms still, erst dann fuhr die nächste Seite hoch.
# Jetzt: Beim Loslassen hinter der Schwelle startet der Wechsel sofort, mit der Geschwindigkeit des Fingers als Startgeschwindigkeit.
# Der native Schwung hat keinen Weg mehr: Die Strecke unter dem Blatt wird beim Loslassen genau auf die aktuelle Position gekürzt.
# (Erster Versuch mit overflow:hidden und Zurückscrollen hat auf iOS gezittert und geflackert.)
T = rep(T, 'document.addEventListener("touchstart",function(e){touching=e.touches.length;clearTimeout(idleT)},{passive:true});',
        'var tSm=[],relV=null,tEndAt=0;document.addEventListener("touchstart",function(e){touching=e.touches.length;clearTimeout(idleT);tSm=[]},{passive:true});\n'
        'document.addEventListener("touchmove",function(e){if(e.touches.length!==1)return;var n=performance.now();tSm.push([n,e.touches[0].clientY]);while(tSm.length>2&&n-tSm[0][0]>90)tSm.shift()},{passive:true});\n'
        'function fingerV(){var n=performance.now();if(tSm.length<2||n-tSm[tSm.length-1][0]>70)return 0;var a=tSm[0],z=tSm[tSm.length-1];return Math.max(0,(a[1]-z[1])/Math.max(8,z[0]-a[0]))}\n'
        'function touchGo(v){if(peekBusy||cur<0||!armed()||!pullReady||flung||backing||performance.now()-shownAt<900)return false;clearTimeout(idleT);relV=v;zeroRoom();lastUser=performance.now();crossSw();if(!peekBusy){relV=null;freeRoom()}return true}\nvar roomRun=null;function zeroRoom(){var run=curRun();if(!run)return;mainEl.style.overflowY="clip";var extra=document.documentElement.scrollHeight-innerHeight-scrollY;if(extra>0){run.style.height=Math.max(0,run.offsetHeight-extra)+"px";roomRun=run}}\nfunction freeRoom(){if(roomRun){roomRun.style.height="";roomRun=null}mainEl.style.overflowY=""}')
T = rep(T, 'function tEnd(e){touching=e.touches?e.touches.length:0;if(!touching){clearTimeout(idleT);idleT=setTimeout(onIdle,200)}}',
        'function tEnd(e){touching=e.touches?e.touches.length:0;if(!touching){tEndAt=performance.now();if(touchGo(fingerV()))return;clearTimeout(idleT);idleT=setTimeout(onIdle,200)}}')
#    Loslassen vor der Schwelle, der Schwung trägt drüber: dann ebenso sofort weiter, mit der Scrollgeschwindigkeit.
T = rep(T, '  setPull(armed()&&over>0?over/PEEK_TH:0)}',
        '  setPull(armed()&&over>0?over/PEEK_TH:0);if(!touching&&pullReady&&now-tEndAt<1200&&scrollY>lastSY0)touchGo(Math.max(0,(scrollY-lastSY0)/Math.max(8,now-lastT0)));lastSY0=scrollY;lastT0=now}\nvar lastSY0=0,lastT0=0;')
T = rep(T, 'var dy=-OV-top0,dist=Math.abs(dy),dur=Math.round(380+240*Math.min(1,dist/H));',
        'var dy=-OV-top0,dist=Math.abs(dy),dur=Math.round(380+240*Math.min(1,dist/H));if(relV!=null&&!ov){var _r=Math.max(.6,Math.min(6,relV*dur/Math.max(1,dist)));ez=_r>3.33?"cubic-bezier("+(1/_r).toFixed(3)+",1,.36,1)":"cubic-bezier(.3,"+(.3*_r).toFixed(3)+",.36,1)"}relV=null;')
T = rep(T, 'function lockScroll(on){', 'function lockScroll(on){if(!on)freeRoom();')


# ---------- 9. Obere Leiste löst sich am iPad nicht mehr vom Rand ----------
# iPadOS-Safari meldet beim Ein- und Ausfahren der Adressleiste kurz einen Versatz oben (rund 50 px), hat die festen Leisten
# dabei aber selbst schon richtig gesetzt. Die Korrektur hat sie dann doppelt verschoben. Oben wird jetzt nur noch korrigiert,
# solange die Tastatur offen ist (dann verschiebt Safari wirklich den sichtbaren Bereich).
T = rep(T, 't=Math.round(vv.offsetTop-r.top);b=Math.round(r.bottom-(vv.offsetTop+vv.height));if(t<0||t>140)t=0;',
        't=typing?Math.round(vv.offsetTop-r.top):0;b=Math.round(r.bottom-(vv.offsetTop+vv.height));if(t<0||t>140)t=0;')

# ---------- 10. Klarer Weg: Schritte statt Stationen, Startbildschirm, Mini-Quiz, Handy-Leisten ----------
T = rep(T, '\nfromHash();\n', '\n' + open('mobil.js', encoding='utf-8').read() + '\nfromHash();\n')
T = rep(T, 'document.getElementById("tbn").textContent="Station "+(i+1)+" von "+N;', 'var _sl=i===0?"Übersicht":"Schritt "+i+" von "+(N-1);document.getElementById("tbn").textContent=_sl;')
T = rep(T, 'document.getElementById("wsmall").textContent="Station "+(i+1)+" von "+N;', 'document.getElementById("wsmall").textContent=_sl;')
T = rep(T, 'next.classList.toggle("nudge",i===0);measurePath();setProg(i,0)}', 'next.classList.toggle("nudge",i===0);measurePath();setProg(i,0);try{updTabs(i)}catch(e){}}')
T = rep(T, 'document.getElementById("nexttxt").textContent=i===0?"Los":i<N-1?"Weiter":"Zum Start";', 'document.getElementById("nexttxt").textContent=i===0?"Starten":i<N-1?"Weiter":"Übersicht";')
T = rep(T, 'document.getElementById("ringtx").textContent=i+1}', 'document.getElementById("ringtx").textContent=i?i:""}')
T = rep(T, 'fg.style.strokeDashoffset=String(C-C*(i+1)/N);', 'fg.style.strokeDashoffset=String(C-C*i/(N-1));')
T = rep(T, 'tt=last?"Zurück zum Start":stations[i+1].dataset.title,lab=last?"Ende des roten Fadens":"Als Nächstes, Station "+(i+2);',
        'tt=last?"Zurück zur Übersicht":stations[i+1].dataset.title,lab=last?"Fertig, alle Schritte geschafft":i===0?"Los geht es mit Schritt 1":"Weiter mit Schritt "+(i+1);')
T = rep(T, '<span class="tx"><span class="ti">\'+esc(t)+\'</span>', '<span class="tx"><span class="ti">\'+(i?\'<span class="no">\'+i+\'</span>\':\'\')+esc(t)+\'</span>')
T = rep(T, 'cur=i;visited[ids[i]]=1;', 'if(old&&i===cur+1){try{markDone(ids[cur])}catch(e){}}cur=i;visited[ids[i]]=1;')
T = rep(T, 'bh.querySelector("small").textContent="Zurück zu Station "+(t+1);', 'bh.querySelector("small").textContent=t?"Zurück zu Schritt "+t:"Zurück zur Übersicht";')
T = T.replace('Geh die Stationen 5 bis 13 nochmal durch', 'Geh die Schritte 2 bis 8 nochmal durch')
T = T.replace('aria-label="Alle Stationen anzeigen"', 'aria-label="Lernpfad anzeigen"').replace('aria-label="Vorherige Station"', 'aria-label="Ein Schritt zurück"')
T = T.replace('<span class="n" id="tbn">Station 1 von 13</span>', '<span class="n" id="tbn">Übersicht</span>').replace('<small id="wsmall">Station 1 von 13</small>', '<small id="wsmall">Übersicht</small>')
T = T.replace('alle Stationen untereinander', 'alle Schritte untereinander')

# ---------- 11. Zuschnitt auf die Lernansicht ab 1c: Code von entfernten Schritten läuft ins Leere statt zu brechen ----------
T = rep(T, 'var mg=document.getElementById("margin"),stepper=document.getElementById("stepper"),stIdx=1;', 'var mg=document.getElementById("margin")||el("div"),stepper=document.getElementById("stepper")||el("div"),stIdx=1;')

# Bereich QUELLE bis QUIZ: fehlende Elemente werden zu losgelösten Platzhaltern, damit die Logik der entfernten Schritte nicht bricht
_a = T.find('/* ================= QUELLE ================= */'); _b = T.find('/* ================= QUIZ ================= */')
assert 0 < _a < _b
T = T.replace('document.querySelector(\'[data-ex="buelow"]\').setAttribute("aria-pressed","true");', 'var _exb=document.querySelector(\'[data-ex="buelow"]\');if(_exb)_exb.setAttribute("aria-pressed","true");')
T = T[:_a] + 'function gid(i){return document.getElementById(i)||gid.d[i]||(gid.d[i]=document.createElement("input"))}gid.d={};\n' + T[_a:_b].replace('document.getElementById(', 'gid(') + T[_b:]

T = T.replace('". Alle 15 Stationen dauern zusammen etwa "', '". Alle Schritte dauern zusammen etwa "')

# ---------- Kommentare im CSS an das neue Thema anpassen ----------
for a_, b_ in [('/* Grundriss: Handlung, Zeit, Raum */', '/* Grundriss: Industrie */'), ('/* Antike: Antigone */', '/* Antike: hier nicht genutzt */'),
               ('/* Dialog: Figuren und Gespräch */', '/* Dialog: Gründe für Kolonien */'), ('/* Epochen */', '/* Moderne und Vergangenheit */'),
               ('/* Tragik: Antigone deuten */', '/* Tragik: Kolonialzeit beurteilen */'), ('/* Zwei: Szenen vergleichen */', '/* Zwei: Kongokonferenz */'),
               ('/* ---------- Antigone ---------- */', '/* ---------- Quelle mit Randnotizen ---------- */'), ('/* ---------- Epochen ---------- */', '/* ---------- Zeitstrahl und Tabelle ---------- */'),
               ('/* ---------- Antigone deuten ---------- */', '/* ---------- Etappen, Akteure, Streitfragen ---------- */'), ('/* ---------- Szenen vergleichen ---------- */', '/* ---------- Reißverschluss ---------- */'),
               ('/* ===== Design 19.11.: Regiebuch im Bühnendunkel =====\n   Laut ist nur das Licht. Text folgt den Regeln eines Dramentexts:\n   Regieanweisungen (Hinweise, Ortsangaben, Metainfos) kursiv in der Serif, normale Schreibung;',
                '/* ===== Design: Quellenangaben im Bühnendunkel =====\n   Laut ist nur das Licht. Text folgt den Regeln einer Quellenedition:\n   Angaben zu Ort, Zeit und Herkunft kursiv in der Serif, normale Schreibung;')]:
    T = T.replace(a_, b_)

# ---------- CSS-Ergänzungen ----------
CSS = open('extra.css', encoding='utf-8').read() + open('mobil.css', encoding='utf-8').read() + open('intro.css', encoding='utf-8').read()
T = rep(T, '</style>\n</head>', CSS + '\n</style>\n</head>')

# ---------- Farbsystem: eine Farbe pro Station ----------
# ---- #12 Zurückwischen oben: kürzerer Weg, Schwung zählt, Seite wird beim Ziehen zum Blatt,
#      Overlay animiert nur noch transform (läuft auf dem Compositor), Kopie nur vom sichtbaren Teil
T = rep(T, 'var tY0=null,tPull=0,BTH=96;', 'var tY0=null,tPull=0,BTH=72,bSm=[],bpE=null;\n'
  'function bpOn(st){if(bpE)return;var r=st.getBoundingClientRect(),_L=matchMedia("(min-width:1100px)").matches?(parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--side"))||0):0,m={left:_L,right:document.documentElement.clientWidth,width:document.documentElement.clientWidth-_L},hh=st.querySelector(".hero"),ac=(hh&&getComputedStyle(hh).getPropertyValue("--accent").trim())||"";'
  'st.style.clipPath="inset(0 "+(-(m.right-r.right)).toFixed(1)+"px -100000px "+(-(r.left-m.left)).toFixed(1)+"px round 28px 28px 0 0)";'
  'bpE=document.createElement("div");bpE.className="bp-edge";bpE.setAttribute("aria-hidden","true");bpE.style.left=m.left+"px";bpE.style.width=m.width+"px";bpE.style.top=r.top+"px";if(ac){bpE.style.borderTopColor=ac;bpE.style.setProperty("--bpk",ac)}document.body.appendChild(bpE)}\n'
  'function bpOff(st){if(st)st.style.clipPath="";if(bpE){bpE.remove();bpE=null}}')
T = rep(T, 'function setBack(px){tPull=px;var st=stations[cur];if(!st)return;var k=Math.min(1,px/BTH);\n  st.style.transform=px>0?"translate3d(0,"+px.toFixed(1)+"px,0)":"";',
        'function setBack(px){tPull=px;var st=stations[cur];if(!st)return;var k=Math.min(1,px/BTH);\n  if(px>0)bpOn(st);else bpOff(st);st.style.transform=px>0?"translate3d(0,"+px.toFixed(1)+"px,0)":"";if(bpE)bpE.style.transform=st.style.transform;')
T = rep(T, 'document.addEventListener("touchstart",function(e){tY0=null;', 'document.addEventListener("touchstart",function(e){tY0=null;bSm=[];')
T = rep(T, 'if(!tPull)fillBack();setBack(Math.min(150,dy*.5))', 'bSm.push([performance.now(),y]);if(bSm.length>6)bSm.shift();if(!tPull)fillBack();setBack(Math.min(150,dy*.6))')
T = rep(T, 'function endBack(){if(!tPull)return;var st=stations[cur],px=tPull;tPull=0;\n  if(px>=BTH){',
        'function endBack(){if(!tPull)return;var st=stations[cur],px=tPull;tPull=0;var bv=0;if(bSm.length>1){var b0=bSm[0],b1=bSm[bSm.length-1];if(performance.now()-b1[0]<90)bv=(b1[1]-b0[1])/Math.max(8,b1[0]-b0[0])}bSm=[];\n  if(px>=BTH||(px>=30&&bv>.45)){')
T = rep(T, 'if(st&&st.animate){var a=st.animate([{transform:"translate3d(0,"+px+"px,0)"},{transform:"translate3d(0,0,0)"}],{duration:320,easing:"cubic-bezier(.16,1,.3,1)"});st.style.transform="";}else if(st)st.style.transform=""}',
        'if(st&&st.animate){var kf=[{transform:"translate3d(0,"+px+"px,0)"},{transform:"translate3d(0,0,0)"}],op={duration:320,easing:"cubic-bezier(.16,1,.3,1)"},a=st.animate(kf,op);if(bpE){bpE.animate(kf,op);bpE.style.transform=""}st.style.transform="";a.onfinish=function(){if(!tPull)bpOff(st)}}else if(st){st.style.transform="";bpOff(st)}}')
# backTo: nur der sichtbare Teil wird kopiert, das Overlay beginnt genau an der Oberkante der Seite und sieht aus wie das gezogene Blatt
T = rep(T, '  var cl=old.cloneNode(true);cl.removeAttribute("id");',
        '  var _cc=old.querySelector(":scope > .content"),_cut=[];if(_cc)[].forEach.call(_cc.children,function(n,k){if(n.getBoundingClientRect().top>H+60)_cut.push(k)});\n'
        '  if(bpE&&bpE.style.borderTopColor)ov.style.borderTopColor=bpE.style.borderTopColor;ov.style.top=r.top.toFixed(1)+"px";ob=ov.getBoundingClientRect();\n'
        '  var cl=old.cloneNode(false);[].forEach.call(old.children,function(x){if(x!==_cc){cl.appendChild(x.cloneNode(true));return}var kc=x.cloneNode(false);[].forEach.call(x.children,function(n,k){if(_cut.indexOf(k)<0)kc.appendChild(n.cloneNode(true))});cl.appendChild(kc)});cl.style.clipPath="";cl.removeAttribute("id");')
T = rep(T, 'cl.style.top=r.top+"px";cl.style.width=r.width+"px";ov.appendChild(cl);', 'cl.style.top=(-ov.clientTop)+"px";cl.style.width=r.width+"px";ov.appendChild(cl);')
T = rep(T, '  old.style.transform="";\n  FILLNOW=true;', '  old.style.transform="";bpOff(old);\n  FILLNOW=true;')
T = rep(T, 'a=ov.animate([{transform:"translate3d(0,0,0)",borderTopLeftRadius:"0px",borderTopRightRadius:"0px",borderTopColor:"rgba(0,0,0,0)",boxShadow:"0 -30px 70px -10px rgba(0,0,0,.55)"},{transform:"translate3d(0,"+dy+"px,0)",borderTopLeftRadius:"28px",borderTopRightRadius:"28px",borderTopColor:getComputedStyle(rs).borderTopColor,boxShadow:"0 -30px 70px -10px rgba(0,0,0,0)"}],{duration:du,easing:ez,fill:"forwards"});',
        'ov.style.borderTopColor=getComputedStyle(rs).borderTopColor;a=ov.animate([{transform:"translate3d(0,0,0)"},{transform:"translate3d(0,"+dy+"px,0)"}],{duration:du,easing:ez,fill:"forwards"});')
T = rep(T, '.back-ov{position:fixed;inset:0;z-index:27;overflow:hidden;background-color:var(--paper);border-radius:26px 26px 0 0;border-top:1px solid var(--rule);pointer-events:none;will-change:transform;box-shadow:0 -30px 70px -10px rgba(0,0,0,.55)}',
        '.back-ov{position:fixed;inset:0;z-index:27;overflow:hidden;background-color:var(--paper);border-radius:28px 28px 0 0;border-top:2px solid var(--rule);pointer-events:none;will-change:transform;box-shadow:none}\n'
        '.bp-edge{position:fixed;z-index:26;height:40px;pointer-events:none;border-top:2px solid var(--rule);border-radius:28px 28px 0 0}\n'
        '.bp-edge::before{content:"";position:absolute;top:10px;left:50%;width:44px;height:5px;margin-left:-22px;border-radius:5px;background:var(--bpk,var(--rule));opacity:.8}\n'
        '')

# ---- #12b Loslassen: Die Seite fährt sofort auf dem Compositor weiter (gleiche Kurve wie das spätere Overlay),
#      die teure Umschaltung läuft erst danach. Ziel der Kurve kommt aus einem Cache der Ruheposition je Station.
T = rep(T, 'if(px>=BTH||(px>=30&&bv>.45)){bh.classList.remove("ready");bh.style.opacity="0";backTo(cur-1,true);return}',
        'if(px>=BTH||(px>=30&&bv>.45)){bh.classList.remove("ready");bh.style.opacity="0";var bt=cur-1,bc=SHC[ids[bt]],bk=st.querySelector(":scope > .hero > .kicker");'
        'if(bc&&bk&&st.animate&&!RM){var dyE=bc.p-bk.getBoundingClientRect().top,bdu=Math.round(420+260*Math.min(1,dyE/innerHeight)),kf=[{transform:"translate3d(0,"+px+"px,0)"},{transform:"translate3d(0,"+(px+dyE)+"px,0)"}],_r=Math.max(.6,Math.min(6,Math.max(0,bv)*.6*bdu/Math.max(1,dyE))),bez=_r>3.33?"cubic-bezier("+(1/_r).toFixed(3)+",1,.36,1)":"cubic-bezier(.3,"+(.3*_r).toFixed(3)+",.36,1)",op={duration:bdu,easing:bez,fill:"forwards"};'
        'var _t0=document.timeline.currentTime;BHO={a:[st.animate(kf,op),bpE?bpE.animate(kf,op):null],du:bdu,ez:bez,t0:_t0};BHO.a.forEach(function(x){if(x)try{x.startTime=_t0}catch(e){}});requestAnimationFrame(function(){setTimeout(function(){backTo(bt,true)},0)})}else backTo(bt,true);return}')
T = rep(T, 'var tY0=null,tPull=0,BTH=72,', 'var BHO=null,SHC={},tY0=null,tPull=0,BTH=72,')
T = rep(T, 'function arm(){var r=curRun(),sw=curSw();if(!r||armed())return;',
        'function cacheRest(){try{var r=curRun(),_rs=r&&r.querySelector(".rw-sheet"),_pk=_rs&&_rs.querySelector(".rw-in .hero > .kicker");if(_pk&&Math.abs(scrollY-restY())<=4){var q=_pk.getBoundingClientRect().top;if(q>0&&q<innerHeight*1.5)SHC[ids[cur]]={p:q}}}catch(e){}}\n'
        'function arm(){var r=curRun(),sw=curSw();if(!r||armed())return;cacheRest();')
T = rep(T, 'function onIdle(){if(peekBusy||cur<0||!curRun()||touching)return;var r=restY(),over=scrollY-r;', 'function onIdle(){if(peekBusy||cur<0||!curRun()||touching)return;var r=restY(),over=scrollY-r;if(Math.abs(over)<=4)cacheRest();')
T = rep(T, 'function refill(i){', 'function refill(i){setTimeout(function(){if(i===cur&&!peekBusy)cacheRest()},60);')
T = rep(T, 'function backTo(t,atEnd){if(t<0||t>=N||t===cur)return;if(peekBusy)return;var old=stations[cur];',
        'function backTo(t,atEnd){var ho=BHO;BHO=null;if(ho)ho.a.forEach(function(x){if(x)x.cancel()});if(t<0||t>=N||t===cur)return;if(peekBusy)return;var old=stations[cur];')
T = rep(T, 'var ez="cubic-bezier(.22,1,.36,1)",du=Math.round(420+260*Math.min(1,dy/H));', 'var ez=ho?ho.ez:"cubic-bezier(.22,1,.36,1)",du=ho?ho.du:Math.round(420+260*Math.min(1,dy/H));')
T = rep(T, 'gl.animate([{opacity:0},{opacity:1}],{duration:du,easing:"ease-in",fill:"forwards"});',
        'var ga=gl.animate([{opacity:0},{opacity:1}],{duration:du,easing:"ease-in",fill:"forwards"});if(ho&&ho.t0!=null){try{a.startTime=ho.t0;ga.startTime=ho.t0}catch(e){}}')

# ---- #13 Schwung am Seitenende (Ruheposition) und am Seitenanfang federt weich nach, statt hart zu stoppen.
#      Nur transform auf der Station (Compositor), Stärke aus der Geschwindigkeit, Ruhe-Logik wartet die Feder ab.
T = rep(T, 'function onScrollPull(){if(peekBusy||cur<0||!curRun())return;var r=restY(),over=scrollY-r,prev=lastSY-r,now=performance.now(),v=Math.abs(scrollY-lastSY)/Math.max(1,now-lastT);',
        'var eSV=0,bounceUntil=0,bA=null;\n'
        'function edgeBounce(now){var dt=Math.max(1,now-lastT),sv=(scrollY-lastSY)/dt,mx=document.documentElement.scrollHeight-innerHeight,vv=Math.abs(sv)>Math.abs(eSV)?sv:eSV;eSV=dt>120?0:sv;'
        'if(!touchUI||touching||RM||now<bounceUntil||peekBusy)return;if(mx>40&&scrollY>=mx-1&&lastSY<mx-1&&vv>.7&&!armed())bounce(-1,vv);else if(scrollY<=1&&lastSY>1&&vv<-.7)bounce(1,-vv)}\n'
        'function bounce(d,v){var st=stations[cur];if(!st||!st.animate||st.style.transform)return;var A=Math.round(Math.min(34,Math.max(10,v*15)));bounceUntil=performance.now()+500;if(d<0)setTimeout(function(){try{if(!peekBusy){arm();flung=false}}catch(e){}},170);'
        'bA=st.animate([{transform:"translate3d(0,0,0)",easing:"cubic-bezier(.12,.85,.3,1)"},{transform:"translate3d(0,"+(d*A)+"px,0)",offset:.3,easing:"cubic-bezier(.45,0,.2,1)"},{transform:"translate3d(0,0,0)"}],{duration:480})}\n'
        'function onScrollPull(){if(peekBusy||cur<0)return;edgeBounce(performance.now());if(!curRun()){lastSY=scrollY;lastT=performance.now();return}var r=restY(),over=scrollY-r,prev=lastSY-r,now=performance.now(),v=Math.abs(scrollY-lastSY)/Math.max(1,now-lastT);')
T = rep(T, 'document.addEventListener("touchstart",function(e){tY0=null;bSm=[];', 'document.addEventListener("touchstart",function(e){tY0=null;bSm=[];if(bA){try{if(bA.playState==="running"){var _st=stations[cur],_m=getComputedStyle(_st).transform;bA.cancel();if(_m&&_m!=="none"&&_st.animate)_st.animate([{transform:_m},{transform:"translate3d(0,0,0)"}],{duration:140,easing:"cubic-bezier(.2,.7,.3,1)"})}else bA.cancel()}catch(_){}bA=null;bounceUntil=0}')
T = rep(T, 'function onIdle(){if(peekBusy||cur<0||!curRun()||touching)return;', 'function onIdle(){if(performance.now()<bounceUntil){clearTimeout(idleT);idleT=setTimeout(onIdle,bounceUntil-performance.now()+20);return}if(peekBusy||cur<0||!curRun()||touching)return;')

# ---- #14 Spickzettel: offene Punkte nur als kurze Auswahl, nicht die ganze Liste
T = rep(T, """'<h2>Noch nicht abgehakt</h2><div class="chips todo-chips" style="margin-top:12px">'+open.map(""", """'<h2>Noch offen: '+open.length+(open.length===1?' Punkt':' Punkte')+'</h2><div class="chips todo-chips" style="margin-top:12px">'+open.slice(0,6).map(""")
T = rep(T, """return'<a class="chip" href="#'+o[0]+'">'+esc(o[1])+'</a>'}).join("")+'</div>'""", """return'<a class="chip" href="#'+o[0]+'">'+esc(o[1])+'</a>'}).join("")+(open.length>6?'<span class="chip ghost" style="cursor:default">und '+(open.length-6)+' weitere</span>':'')+'</div>'""")

# ---- #15 Roter Faden oben: folgt dem Scrollen direkt (ohne nachlaufende CSS-Transition), Sprünge werden
#      als eine weiche transform-Animation gezeigt. Fortschritt = 0 oben bis 1 an der Ruheposition, also
#      gleicher Wert am Ende von Schritt i und am Anfang von Schritt i+1, nichts springt hin und her.
T = rep(T, '.tb-thread{position:absolute;left:0;right:0;bottom:-1px;height:3px;background:transparent}',
        '.tb-thread{position:absolute;left:0;right:0;bottom:-1px;height:3px;background:transparent;clip-path:inset(-14px -14px -14px 0)}')
T = rep(T, '.tb-thread i{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--thread);border-radius:0 3px 3px 0;transition:width .6s var(--ease)}',
        '.tb-thread i{position:absolute;left:0;top:0;bottom:0;width:100%;background:var(--thread);border-radius:0 3px 3px 0;transform:translate3d(-100%,0,0);will-change:transform}')
T = rep(T, 'function progF(){return .9*scrollFrac()+.1*Math.min(1,pull||0)}',
        'function progF(){var r=restY();if(!isFinite(r)){var m=document.documentElement.scrollHeight-innerHeight;return m<=4?1:Math.min(1,Math.max(0,scrollY/m))}return r<=4?1:Math.min(1,Math.max(0,scrollY/r))}\n'
        'var tbV=-1,tbA=null,tbEl=null;function tbTf(x){return"translate3d("+((x-1)*100).toFixed(3)+"%,0,0)"}\n'
        'function tbSet(v){tbEl=tbEl||document.getElementById("tbfill");if(!tbEl)return;v=Math.max(0,Math.min(1,v));if(Math.abs(v-tbV)<5e-5)return;'
        'if(tbV>=0&&Math.abs(v-tbV)>.2/N&&tbEl.animate&&!RM){var from=tbA?getComputedStyle(tbEl).transform:tbTf(tbV);if(tbA)tbA.cancel();tbEl.style.transform=tbTf(v);'
        'tbA=tbEl.animate([{transform:from},{transform:tbTf(v)}],{duration:520,easing:"cubic-bezier(.22,1,.36,1)"});tbA.onfinish=function(){tbA=null}}'
        'else tbEl.style.transform=tbTf(v);tbV=v}')
T = rep(T, 'document.getElementById("tbfill").style.width=((i+f)/N*100)+"%"}', 'tbSet((i+f)/N)}')
T = rep(T, 'next.classList.toggle("nudge",i===0);measurePath();setProg(i,0);', 'next.classList.toggle("nudge",i===0);measurePath();reqMore();')

# ---- #16 Start-Intro „Zündung“ (intro.js/intro.css): Linie wird zum Faden, Elemente zünden statt hereinzugleiten
T = rep(T, '\nfromHash();\n', '\n' + open('intro.js', encoding='utf-8').read() + '\nfromHash();\n')
T = rep(T, 'setTimeout(function(){if(vh)d.classList.add("vh-open");', 'setTimeout(function(){try{introPlan(vh)}catch(e){}if(vh)d.classList.add("vh-open");')
T = rep(T, 'requestAnimationFrame(function(){var d=document.documentElement;if(d.classList.contains("hold"))openStage();', 'requestAnimationFrame(function(){var d=document.documentElement;try{introPrime()}catch(e){}if(d.classList.contains("hold"))openStage();')
T = rep(T, 'w=vh?Math.max(0,480-performance.now()):0', 'w=vh?Math.max(0,((window.INTRO&&INTRO.litAt)||0)+480-performance.now()):0')
T = rep(T, 'if(vh)setTimeout(function(){d.classList.remove("vh","vh-open")},700)},w)}', 'if(vh)setTimeout(function(){d.classList.remove("vh","vh-open")},Math.max(700,(window.INTRO&&INTRO.end)||0))},w)}')

# ---- #17 Scrollen ohne Layout-Thrash: Positionen werden gecacht (ResizeObserver macht sie ungültig),
#      pro Frame wird nur noch geschrieben, was sich wirklich ändert.
T = rep(T, 'function padB(){return parseFloat(getComputedStyle(mainEl).paddingBottom)||0}',
        'var GEO={v:0};function geoDirty(){GEO.v++}window.addEventListener("resize",geoDirty,{passive:true});'
        'try{var _ro=new ResizeObserver(geoDirty);document.querySelectorAll(".station").forEach(function(x){_ro.observe(x)})}catch(e){}\n'
        'var _pb=null,_pbV=-1;function padB(){if(_pbV!==GEO.v){_pb=parseFloat(getComputedStyle(mainEl).paddingBottom)||0;_pbV=GEO.v}return _pb}\n'
        'function docTop(el){var st=el.closest&&el.closest(".station");if(st&&(st.style.transform||(bA&&bA.playState==="running")))return el.getBoundingClientRect().top+scrollY;'
        'var c=el._gt;if(c&&c.v===GEO.v&&c.c===cur)return c.t;var t=el.getBoundingClientRect().top+scrollY;el._gt={v:GEO.v,c:cur,t:t};return t}\n'
        'var _mx=0,_mxV=-1,_mxC=-2;function maxScroll(){if(_mxV!==GEO.v||_mxC!==cur){_mx=document.documentElement.scrollHeight-innerHeight;_mxV=GEO.v;_mxC=cur}return _mx}')
T = rep(T, 'function restY(){var r=curRun();if(!r)return Infinity;return Math.max(0,r.getBoundingClientRect().top+scrollY+padB()-innerHeight)}',
        'function restY(){var r=curRun();if(!r)return Infinity;return Math.max(0,docTop(r)+padB()-innerHeight)}')
T = rep(T, 'function edgeBounce(now){var dt=Math.max(1,now-lastT),sv=(scrollY-lastSY)/dt,mx=document.documentElement.scrollHeight-innerHeight,vv=Math.abs(sv)>Math.abs(eSV)?sv:eSV;eSV=dt>120?0:sv;'
        'if(!touchUI||touching||RM||now<bounceUntil||peekBusy)return;',
        'function edgeBounce(now){var dt=Math.max(1,now-lastT),sv=(scrollY-lastSY)/dt,vv=Math.abs(sv)>Math.abs(eSV)?sv:eSV;eSV=dt>120?0:sv;'
        'if(!touchUI||touching||RM||now<bounceUntil||peekBusy||Math.abs(vv)<.7)return;var mx=maxScroll();')
T = rep(T, 's.querySelectorAll(".content h2").forEach(function(h){var t=h.getBoundingClientRect().top;if(t>limit&&h.offsetParent&&!h.closest(".runway")){if(!next)next=h;left++}});',
        'if(!s._h2||s._h2v!==GEO.v){s._h2=[].filter.call(s.querySelectorAll(".content h2"),function(h){return !h.closest(".runway")});s._h2v=GEO.v}s._h2.forEach(function(h){var t=docTop(h)-scrollY;if(t>limit&&(h.offsetWidth||h.offsetHeight)){if(!next)next=h;left++}});')
T = rep(T, 'var sw0=curSw(),nearEnd=sw0?sw0.getBoundingClientRect().top<innerHeight:document.documentElement.scrollHeight-innerHeight-scrollY<60;',
        'var sw0=curSw(),nearEnd=sw0?docTop(sw0)-scrollY<innerHeight:maxScroll()-scrollY<60;')
T = rep(T, 'moreTarget=next;moreTxt.textContent=next.textContent.replace(/\\s+/g," ").trim()+(left>1?"  +"+(left-1):"");moreEl.classList.add("on")',
        'moreTarget=next;var _mt=next.textContent.replace(/\\s+/g," ").trim()+(left>1?"  +"+(left-1):"");if(moreTxt.textContent!==_mt)moreTxt.textContent=_mt;if(!moreEl.classList.contains("on"))moreEl.classList.add("on")')
T = rep(T, 'function setProg(i,f){if(!pathY)measurePath();if(pathY&&stLis[i]){f=Math.min(1,f);var y=pathY[i],y2=stLis[i+1]?pathY[i+1]:y;pathThr.style.height=Math.max(0,y+(y2-y)*f-pathY.y0)+"px";stLis[i].firstChild.style.setProperty("--f",f.toFixed(3))}',
        'var _spK="";function setProg(i,f){f=Math.min(1,f);var showP=DESK.matches||pathEl.classList.contains("open"),k=i+":"+f.toFixed(3)+":"+showP;if(k===_spK)return;_spK=k;'
        'if(showP){if(!pathY)measurePath();if(pathY&&stLis[i]){var y=pathY[i],y2=stLis[i+1]?pathY[i+1]:y;pathThr.style.height=Math.max(0,y+(y2-y)*f-pathY.y0).toFixed(1)+"px";stLis[i].firstChild.style.setProperty("--f",f.toFixed(3))}}')
T = rep(T, '  else{moreEl.classList.remove("on");moreTarget=null}\n  setProg(cur', '  else{if(moreEl.classList.contains("on"))moreEl.classList.remove("on");moreTarget=null}\n  setProg(cur')
T = rep(T, 'function updateMore(){ticking=false;if(cur<0)return;', 'function updateMore(){ticking=false;if(cur<0)return;if(peekBusy){clearTimeout(updateMore._t);updateMore._t=setTimeout(reqMore,120);return}')
T = rep(T, 'function openSheet(){if(DESK.matches)return;pathEl.classList.add("open");', 'function openSheet(){if(DESK.matches)return;pathEl.classList.add("open");_spK="";try{reqMore()}catch(e){}')

# ---- #18 Ende eines Wechsels entlasten: Zeigt die Vorschau schon Inhalt, wird die vollständige Kopie erst in Ruhe nachgeladen
T = rep(T, 'if(_tp>innerHeight*1.6)quietIdle(_ff,300);else requestAnimationFrame(function(){setTimeout(_ff,0)})', 'if(_tp>innerHeight*1.6||_soft)quietIdle(_ff,300);else requestAnimationFrame(function(){setTimeout(_ff,0)})')

# ---- #19 Zurück entlasten: Die Vorschau der vorigen Seite bekommt beim Umschalten nur den sichtbaren oberen Teil
#      der Kopie, die volle Kopie folgt in Ruhe. Nächste und vorige Station werden in Ruhe vorgewärmt.
T = rep(T, 'function cloneStation(t,into,deep){var st=stations[t];prepStation(t);if(deep)fillPreview(t,false);',
        'var FILLPART=null;function cloneStation(t,into,deep){var st=stations[t],part=FILLPART&&FILLPART.t===t?FILLPART.keep:null;prepStation(t);if(deep&&!part)fillPreview(t,false);')
T = rep(T, '  [h,c].forEach(function(x){if(!x)return;var k=x.cloneNode(true);k.removeAttribute("id");',
        '  [h,c].forEach(function(x){if(!x)return;var k;if(part&&x===c){k=x.cloneNode(false);[].forEach.call(x.children,function(n,ix){if(part.indexOf(ix)>=0)k.appendChild(n.cloneNode(true))})}else k=x.cloneNode(true);k.removeAttribute("id");')
T = rep(T, '  old.style.transform="";bpOff(old);\n  FILLNOW=true;try{swapTo(t,-1,true)}finally{FILLNOW=false}',
        '  old.style.transform="";bpOff(old);var _oc=old.querySelector(":scope > .content"),_or=old.getBoundingClientRect().top,_keep=[];if(_oc)[].forEach.call(_oc.children,function(n,ix){if(n.getBoundingClientRect().top-_or<H*1.25)_keep.push(ix)});\n'
        '  FILLPART={t:cur,keep:_keep};FILLNOW=true;try{swapTo(t,-1,true)}finally{FILLNOW=false;FILLPART=null}pendFill=t;quietIdle(function(){if(pendFill===cur){pendFill=-1;refill(cur)}},300);')
T = rep(T, 'function arm(){var r=curRun(),sw=curSw();if(!r||armed())return;cacheRest();',
        'function warmSt(i){var s=stations[i];if(!s||i===cur||s._wv===GEO.v)return;quietIdle(function(){if(s.classList.contains("on")||peekBusy)return;s._wv=GEO.v;s.classList.add("warm");void s.offsetHeight;requestAnimationFrame(function(){s.classList.remove("warm")})},400)}\n'
        'function arm(){var r=curRun(),sw=curSw();if(!r||armed())return;cacheRest();warmSt(cur+1);')
T = rep(T, 'if(peekBusy||cur<0||!curRun()||touching)return;var r=restY(),over=scrollY-r;if(Math.abs(over)<=4)cacheRest();',
        'if(peekBusy||cur<0||!curRun()||touching)return;var r=restY(),over=scrollY-r;if(Math.abs(over)<=4)cacheRest();if(scrollY<=4&&cur>0)warmSt(cur-1);')

# ---- #20 Umschalten nach einem Blatt-Wechsel ohne Einstiegsklassen: Die Kopie zeigt schon den Endzustand,
#      enter/fwd/via-peek würden nur alle Nachfahren neu berechnen lassen (via-peek hat eine *-Regel).
T = rep(T, 'if(pk)s.classList.add("via-peek");void s.offsetWidth;\n  s.classList.add("on","enter",dir>0?"fwd":dir<0?"back":"first");',
        'if(pk)s.classList.add("on");else{void s.offsetWidth;s.classList.add("on","enter",dir>0?"fwd":dir<0?"back":"first")}')

# ---- #21 Leerlauf-Arbeit nie, solange ein Finger oder eine Maustaste unten ist (sonst hakt Festhalten und Ziehen)
T = rep(T, 'function quiet(ms){return !peekBusy&&!document.querySelector(".back-ov")&&performance.now()-lastInput>=(ms||800)}',
        'var PDOWN=0;["pointerdown"].forEach(function(t){addEventListener(t,function(){PDOWN++},{passive:true,capture:true})});["pointerup","pointercancel"].forEach(function(t){addEventListener(t,function(){PDOWN=Math.max(0,PDOWN-1)},{passive:true,capture:true})});'
        'addEventListener("blur",function(){PDOWN=0});\n'
        'function quiet(ms){return !peekBusy&&!PDOWN&&!touching&&!document.querySelector(".back-ov")&&performance.now()-lastInput>=(ms||800)}')

# ---- #22 Festhalten beim Zurückziehen: Ein touchcancel (Langdruck, die umgebende App übernimmt die Geste) ist kein
#      Loslassen. Dann federt die Seite zurück statt umzublättern, und vorwärts startet ebenfalls kein Wechsel.
#      Während des Ziehens keine Textauswahl und kein Kontextmenü, die den Langdruck auslösen.
T = rep(T, 'document.addEventListener("touchend",function(){tY0=null;endBack()},{passive:true});document.addEventListener("touchcancel",function(){tY0=null;endBack()},{passive:true});',
        'document.addEventListener("touchend",function(){tY0=null;endBack()},{passive:true});document.addEventListener("touchcancel",function(){tY0=null;endBack(true)},{passive:true});'
        'document.addEventListener("contextmenu",function(e){if(tPull||document.documentElement.classList.contains("bpull"))e.preventDefault()});')
T = rep(T, 'function endBack(){if(!tPull)return;var st=stations[cur],px=tPull;tPull=0;', 'function endBack(cn){if(!tPull)return;var st=stations[cur],px=tPull;tPull=0;')
T = rep(T, 'if(px>=BTH||(px>=30&&bv>.45)){bh.classList.remove("ready");', 'if(!cn&&(px>=BTH||(px>=30&&bv>.45))){bh.classList.remove("ready");')
T = rep(T, 'function tEnd(e){touching=e.touches?e.touches.length:0;if(!touching){tEndAt=performance.now();if(touchGo(fingerV()))return;',
        'function tEnd(e){touching=e.touches?e.touches.length:0;if(!touching){tEndAt=performance.now();if(e.type!=="touchcancel"&&touchGo(fingerV()))return;')
T = rep(T, 'function bpOn(st){if(bpE)return;', 'function bpOn(st){if(bpE)return;document.documentElement.classList.add("bpull");')
T = rep(T, 'function bpOff(st){if(st)st.style.clipPath="";', 'function bpOff(st){document.documentElement.classList.remove("bpull");if(st)st.style.clipPath="";')

# ---- #23 Feder ohne Ruckler: Nahe Anfang und Ende der Seite liegt die Station schon vorher auf einer eigenen Ebene
#      (will-change), dann muss beim Aufprall nichts neu gerastert werden. Scharfschalten erst 170 ms nach dem Aufprall.
T = rep(T, 'function edgeBounce(now){', 'function wcZone(){var st=stations[cur];if(!st)return;var H=innerHeight,near=scrollY<H*1.2||maxScroll()-scrollY<H*1.2;if(near&&!st._wc){st.style.willChange="transform";st._wc=1}return near}\n'
        'function wcIdle(){stations.forEach(function(x,k){if(x._wc&&(k!==cur||!wcZone())){x.style.willChange="";x._wc=0}})}\n'
        'function edgeBounce(now){if(Math.abs(scrollY-lastSY)>2)wcZone();')
T = rep(T, 'if(peekBusy||cur<0||!curRun()||touching)return;var r=restY(),over=scrollY-r;if(Math.abs(over)<=4)cacheRest();',
        'if(peekBusy||cur<0||!curRun()||touching)return;try{wcIdle();wcZone()}catch(e){}var r=restY(),over=scrollY-r;if(Math.abs(over)<=4)cacheRest();')

# ---- #24 Zurückziehen festhalten, Teil 2: Oben auf der Seite liegt ein nicht-passiver touchmove-Wächter, der beim
#      Ziehen preventDefault ruft. Damit gehört die Geste der Seite, Browser und umgebende App übernehmen sie nicht
#      nach einer Sekunde (touchcancel). Nur oben aktiv, damit normales Scrollen nie auf JavaScript warten muss.
T = rep(T, 'function endBack(cn){', 'var tmBlock=false;function tmGuard(e){if(tPull>0&&e.cancelable)e.preventDefault()}\n'
        'function tmSync(){var want=scrollY<=1&&cur>0&&touchUI;if(want!==tmBlock){tmBlock=want;if(want)document.addEventListener("touchmove",tmGuard,{passive:false});else document.removeEventListener("touchmove",tmGuard,{passive:false})}}\n'
        'addEventListener("scroll",tmSync,{passive:true});setInterval(tmSync,700);\n'
        'function endBack(cn){')

# ---- #25 „Muss sitzen“: die wichtigsten Punkte als Knoten im roten Faden (Daten: k = Begründung)
T = rep(T, 'var d=el("div",{class:"item"+(chk[id]?" done":"")}),row=el("div",{class:"row"});', 'var d=el("div",{class:"item"+(chk[id]?" done":"")+(it.k?" knot":"")}),row=el("div",{class:"row"});')
T = rep(T, 'var sum=el("button",{class:"sum","aria-expanded":"false","aria-controls":did},esc(it.t));', 'var sum=el("button",{class:"sum","aria-expanded":"false","aria-controls":did},esc(it.t)+(it.k?\'<span class="kn">Muss sitzen</span>\':""));')
T = rep(T, '    body.appendChild(el("p",null,esc(it.d)));\n', '    if(it.k)body.appendChild(el("p",{class:"kn-why"},esc(it.k)));body.appendChild(el("p",null,esc(it.d)));\n')

# ---- #26 Quiz: Antworten bei jeder Frage neu mischen. Zeitplan: Minuten so runden, dass die Summe stimmt
T = rep(T, 'q[1].forEach(function(o,i){var b=el("button",{class:"opt","data-l":String(i+1)},esc(o));b.style.setProperty("--i",i);',
        'var ord=q[1].map(function(_,k){return k});for(var z=ord.length-1;z>0;z--){var y=Math.floor(Math.random()*(z+1)),w=ord[z];ord[z]=ord[y];ord[y]=w}var cq=ord.indexOf(q[2]);\n'
        '  ord.forEach(function(oi,i){var o=q[1][oi];var b=el("button",{class:"opt","data-l":String(i+1)},esc(o));b.style.setProperty("--i",i);')
T = rep(T, 'var ok=i===q[2];\n      opts.querySelectorAll(".opt").forEach(function(x,k){x.disabled=true;x.style.animationDelay="0s";if(k===q[2])x.classList.add("right");',
        'var ok=i===cq;\n      opts.querySelectorAll(".opt").forEach(function(x,k){x.disabled=true;x.style.animationDelay="0s";if(k===cq)x.classList.add("right");')
T = rep(T, 'function plan(){var m=parseInt(document.getElementById("mins").value,10);if(!(m>0))m=90;var t=0,',
        'function planMins(m){var u=Math.max(PLAN.length,Math.round(m/5)),raw=PLAN.map(function(r){return u*r[1]}),fl=raw.map(function(x){return Math.max(1,Math.floor(x))}),sum=fl.reduce(function(a,b){return a+b},0),ord=raw.map(function(x,k){return k}).sort(function(a,b){return (raw[b]-Math.floor(raw[b]))-(raw[a]-Math.floor(raw[a]))});\n'
        '  for(var k=0;sum<u;k=(k+1)%ord.length){fl[ord[k]]++;sum++}while(sum>u){var mx=fl.indexOf(Math.max.apply(null,fl));fl[mx]--;sum--}return fl.map(function(x){return x*5})}\n'
        'function plan(){var m=parseInt(document.getElementById("mins").value,10);if(!(m>0))m=90;var MM=planMins(m),t=0,')
T = rep(T, '  PLAN.forEach(function(r,j){var mm=Math.max(5,Math.round(m*r[1]/5)*5),from=t;', '  PLAN.forEach(function(r,j){var mm=MM[j],from=t;')
T = rep(T, 'PLAN.forEach(function(r){var mm=Math.max(5,Math.round(m*r[1]/5)*5);bh+=', 'PLAN.forEach(function(r,j){var mm=MM[j];bh+=')

# ---- #27 Nach dem Wechsel: Rest-Versatz zwischen Kopie und echter Seite gleitet die ganze Seite aus (Kopf UND Inhalt),
#      statt nur den Kopf zu verschieben und den Inhalt springen zu lassen (am Handy z. B. durch Nachschwingen am Seitenende)
T = rep(T, 'if(Math.abs(dX)>.5||Math.abs(dY)>.5)hero.animate([{transform:"translate3d("+dX+"px,"+dY+"px,0)"},{transform:"translate3d(0,0,0)"}],{duration:300,easing:ez})}',
        'if(Math.abs(dX)>.5||Math.abs(dY)>.5){var _ct=stations[t].querySelector(":scope > .content"),_kf=[{transform:"translate3d("+dX.toFixed(2)+"px,"+dY.toFixed(2)+"px,0)"},{transform:"translate3d(0,0,0)"}],_op={duration:Math.round(Math.min(340,220+Math.abs(dY)*2)),easing:"cubic-bezier(.25,.8,.3,1)"};'
        'hero.animate(_kf,_op);if(_ct){var _ca=_ct.animate(_kf,_op);_ca.onfinish=function(){GEO.v++;try{fixRest()}catch(e){}}}}}')

# ---- #28 iPad: feste Leisten ziehen nicht mehr hinterher, weniger Dauerarbeit pro Bild
#  a) Viewport-Versatz nur im Ruhezustand (150 ms ohne Scrollen) neu setzen, beim Tippen sofort.
#     Und nur an den Leisten selbst statt an <html>: eine Variable an <html> rechnet die Stile der ganzen Seite neu.
T = rep(T, '    if(t!==lt){lt=t;root.style.setProperty("--vvt",t+"px")}if(b!==lb){lb=b;root.style.setProperty("--vvb",b+"px")}}\n  function req(){if(!pend){pend=true;requestAnimationFrame(upd)}}',
        '    if(t!==lt){lt=t;VVEL().forEach(function(x){x.style.setProperty("--vvt",t+"px")})}if(b!==lb){lb=b;VVEL().forEach(function(x){x.style.setProperty("--vvb",b+"px")})}}\n'
        '  var _ve=null;function VVEL(){if(!_ve)_ve=[].slice.call(document.querySelectorAll(".topbar,.bottombar,.morepill,.narr-cap,.bfade,.path"));return _ve}\n'
        '  var lastSc=0,wt=0;window.addEventListener("scroll",function(){lastSc=performance.now()},{passive:true,capture:true});\n'
        '  function req(){var ae=document.activeElement,typing=ae&&/^(INPUT|TEXTAREA|SELECT)$/.test(ae.tagName),w=150-(performance.now()-lastSc);\n'
        '    if(!typing&&w>0){clearTimeout(wt);wt=setTimeout(req,w+10);return}if(!pend){pend=true;requestAnimationFrame(upd)}}')
#  b) Unsichtbare Zeichnungen anhalten: das Overlay-Blatt liegt unter dem Rand und lief sonst mit 15 SMIL-Animationen weiter
T = rep(T, 'ok=e.isIntersecting&&e.boundingClientRect.width>0&&(!st||st.classList.contains("on")||!!v.closest(".back-ov"));',
        'ok=e.isIntersecting&&e.boundingClientRect.width>0&&(!st||st.classList.contains("on")||!!v.closest(".back-ov"))&&!(v.closest(".peek")&&!v.closest(".peek.on"));')
T = rep(T, 'function watchSvgs(root){',
        'try{new MutationObserver(function(){var on=peek.classList.contains("on");peek.querySelectorAll("svg").forEach(function(v){try{if(on)v.unpauseAnimations();else v.pauseAnimations()}catch(e){}})}).observe(peek,{attributes:true,attributeFilter:["class"]})}catch(e){}\n'
        'function watchSvgs(root){')

# ---- #29 Viewport-Versatz: Scrollen darf nie einen neuen Versatz erzeugen, nur einen alten auf 0 zurücknehmen.
#      Beim Scrollen schwanken die Werte in Safari nur kurz (Adressleiste fährt ein und aus), echte Fälle sind
#      Seitenwechsel, Drehen und Tastatur. Danach 1 s lang freie Fahrt.
T = rep(T, '    if(t!==lt){lt=t;VVEL()',
        '    if(!typing&&performance.now()>vvF&&performance.now()-lastSc<600&&b!==0)b=lb<0?0:lb;\n    if(t!==lt){lt=t;VVEL()')
T = rep(T, '  var lastSc=0,wt=0;', '  var lastSc=0,wt=0,vvF=performance.now()+2500;window.addEventListener("orientationchange",function(){vvF=performance.now()+1500;req()});')
T = rep(T, 'window.addEventListener("hashchange",function(){req();setTimeout(req,350);setTimeout(req,900)})',
        'window.addEventListener("hashchange",function(){vvF=performance.now()+1000;req();setTimeout(req,350);setTimeout(req,900)})')
T = rep(T, 'window.vvUpdate=function(){req();', 'window.vvUpdate=function(){vvF=performance.now()+1000;req();')

# ---- #30 Touch-Geräte: Zeichnungen (SMIL) halten während des Scrollens an und laufen danach an derselben Stelle weiter.
#      Der IntersectionObserver merkt sich den Wunschzustand in v._io, solange gescrollt wird.
T = rep(T, 'try{if(ok)v.unpauseAnimations();else v.pauseAnimations()}catch(x){}})},{rootMargin:"120px 0px"})',
        'v._io=ok;try{if(ok){if(!window.SCRL)v.unpauseAnimations()}else v.pauseAnimations()}catch(x){}})},{rootMargin:"120px 0px"})')

# Zurücksetzen löscht auch den Schritt-Fortschritt (kr_done)
T = rep(T, 'document.getElementById("resetpath").addEventListener("click",function(){visited={};store.set("visited",visited);store.set("last","start");go(0)});',
        'document.getElementById("resetpath").addEventListener("click",function(){visited={};store.set("visited",visited);store.set("last","start");DONE={};store.set("done",DONE);go(0);refreshDone()});')
T = rep(T, 'store.set("best",0);location.reload()', 'store.set("best",0);store.set("done",{});location.reload()')

import farben
T = farben.run(T)

open('app.html', 'w', encoding='utf-8').write(T)
print('app.html', len(T))
