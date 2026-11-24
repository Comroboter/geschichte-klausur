/* ================= KLARER WEG: Schritte, Startbildschirm, Mini-Quiz, Handy-Navigation =================
   Schritt 0 ist die Übersicht, danach Schritt 1 bis N-1. Erledigt ist ein Schritt, wenn man ihn nach vorn verlässt
   (Weiter-Knopf, Hochwischen, Mausrad) oder das Mini-Quiz beendet. Alles bleibt im Browser gespeichert (kr_done). */
var DONE=store.get("done",{}),THEMEN=["revolution","gesellschaft","industrie","kolonien","kongo","personen"];
function markDone(id){if(!id||id==="start"||DONE[id])return;DONE[id]=1;store.set("done",DONE);refreshDone()}
function themesDone(){return THEMEN.filter(function(t){return DONE[t]}).length}
function stepsDone(){var n=0;for(var k=1;k<N;k++)if(DONE[ids[k]])n++;return n}
function nextOpen(){for(var k=1;k<N;k++)if(!DONE[ids[k]])return k;return 1}
function fmtMin(m){m=Math.round(m/5)*5;var h=Math.floor(m/60),r=m%60;return h?h+" h"+(r?" "+r+" min":""):r+" min"}
function goStep(k){if(k<0||k>=N)return;closeSheet();if(k===cur){window.scrollTo({top:0,behavior:RM?"auto":"smooth"});return}if(k===cur+1)go(k);else nav(k)}
var ARR='<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
var CHK='<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 7.4l2.6 2.6L11 4.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

/* Startbildschirm: worum es geht, wie lange, ein Knopf, Fortschritt. Darunter der ganze Weg. */
function renderHome(){var h=document.getElementById("home");if(!h)return;var tot=0;for(var k=1;k<N;k++)tot+=MIN[k];
  var sd=stepsDone(),nx=nextOpen(),td=themesDone(),started=sd>0||store.get("last","start")!=="start";
  var main=started?(sd>=N-1?"Alles geschafft":"Weitermachen"):"Jetzt starten",sub="Schritt "+nx+": "+esc(stations[nx].dataset.title);
  var list="";for(var k2=1;k2<N;k2++){var d=!!DONE[ids[k2]],ty=stations[k2].dataset.type;
    list+='<li class="'+(d?"fin":"")+(k2===nx&&!d?" nx":"")+'"><a href="#'+ids[k2]+'"><span class="sn" aria-hidden="true">'+(d?CHK:k2)+'</span><span class="stx"><b>'+esc(stations[k2].dataset.title)+'</b><small>'+MIN[k2]+' min'+(ty?", "+esc(ty):"")+(d?", erledigt":"")+'</small></span></a></li>'}
  h.innerHTML='<p class="h-what">In '+(N-1)+' kurzen Schritten lernst du alles für die Geschichtsklausur: von der Revolution 1848 über das Kaiserreich und die Industrialisierung bis zu den Kolonien und der Kongokonferenz.</p>'+
    '<p class="h-time"><b>Ungefähr '+fmtMin(tot)+' für alles.</b> Mach ruhig Pausen, dein Fortschritt bleibt auf diesem Gerät gespeichert.</p>'+
    '<button class="bigbtn" id="homego"><span class="bt"><b>'+main+'</b><small>'+sub+'</small></span>'+ARR+'</button>'+
    '<div class="h-prog"><div class="hp-bar" role="progressbar" aria-valuemin="0" aria-valuemax="6" aria-valuenow="'+td+'"><i style="width:'+(td/6*100)+'%"></i></div><span><b>'+td+' von 6 Themen</b> geschafft, '+sd+' von '+(N-1)+' Schritten erledigt</span></div>'+
    '<h2 class="h-list">Dein Lernpfad</h2><ol class="steplist">'+list+'</ol>';
  document.getElementById("homego").addEventListener("click",function(){goStep(nx)})}
var _hs=hooks.start;hooks.start=function(){if(_hs)_hs();renderHome()};

/* Häkchen in der Seitenleiste und im Lernpfad-Blatt */
function refreshDone(){try{updRing()}catch(e){}stLis.forEach(function(li,k){li.classList.toggle("fin",!!DONE[ids[k]])});var pc=document.getElementById("pcdone");if(pc)pc.textContent=stepsDone()+" von "+(N-1)+" erledigt";if(cur===0)renderHome()}

/* Mini-Quiz am Ende von Schritt 1: drei leichte Fragen zum Plan, ein schneller erster Erfolg */
var MQ=[["Was bekommst du in der Klausur?",["Einen Text mit drei Aufgaben","Nur Fragen zum Ankreuzen","Ein Bild ohne Text"],0,"Einen Text, dazu drei Aufgaben: Eckdaten, Zusammenfassung, Sachurteil."],
  ["Was gehört in Aufgabe 1?",["Deine eigene Meinung","Die Eckdaten des Textes: Autor, Textart, Datum, Adressat","Möglichst viele Zitate"],1,"Autor und Rolle, Titel und Textart, Ort und Datum, Adressat, Anlass und Thema. Wie das geht, zeigt Schritt 9."],
  ["Wonach richtet sich ein Sachurteil?",["Nach heutigen Maßstäben","Nach deinem Bauchgefühl","Nach den Maßstäben der damaligen Zeit"],2,"Genau. Nach heutigen Maßstäben wäre es ein Werturteil."]];
function renderMini(){var box=document.getElementById("miniq");if(!box)return;var pos=0,right=0;
  function head(){return '<div class="mq-h"><b>Kurzer Check</b><span>3 leichte Fragen, ohne Punkte</span></div><div class="mq-dots" aria-hidden="true">'+MQ.map(function(_,k){return '<i class="'+(k<pos?"d":k===pos?"c":"")+'"></i>'}).join("")+'</div>'}
  function ask(){var q=MQ[pos];box.innerHTML=head()+'<p class="mq-q">'+esc(q[0])+'</p><div class="mq-o"></div><div class="mq-f" aria-live="polite"></div>';
    var o=box.querySelector(".mq-o");q[1].forEach(function(a,k){var b=el("button",{class:"mq-b"},esc(a));b.addEventListener("click",function(){
      if(o.dataset.done)return;o.dataset.done=1;var ok=k===q[2];if(ok)right++;b.classList.add(ok?"ok":"no");if(!ok)o.children[q[2]].classList.add("ok");
      var f=box.querySelector(".mq-f");f.innerHTML='<p><b>'+(ok?["Richtig!","Genau!","Stimmt!"][pos]:"Fast. Richtig ist „"+esc(q[1][q[2]])+"“.")+'</b> '+esc(q[3])+'</p>';
      var n=el("button",{class:"bigbtn sm"},'<span class="bt"><b>'+(pos+1<MQ.length?"Nächste Frage":"Fertig")+'</b></span>'+ARR);n.addEventListener("click",function(){pos++;if(pos<MQ.length)ask();else end()});f.appendChild(n)});o.appendChild(b)})}
  function end(){store.set("mini",right);markDone("plan");if(right===MQ.length)confetti(60);
    box.innerHTML='<div class="mq-end"><span class="mq-ok" aria-hidden="true">'+CHK+'</span><div><b>'+(right===MQ.length?"Stark, 3 von 3!":right+" von 3, gut gemacht!")+'</b><p>Schritt 1 ist geschafft. Du weißt jetzt, was in der Klausur kommt und wie du die Zeit einteilst.</p><p class="mq-p">'+stepsDone()+" von "+(N-1)+' Schritten erledigt. Weiter geht es mit der Revolution von 1848.</p></div></div>'+
      '<button class="mq-again">Nochmal versuchen</button>';box.querySelector(".mq-again").addEventListener("click",function(){pos=0;right=0;ask()});reqFit()}
  function reqFit(){try{fixRest()}catch(e){}}
  var prev=store.get("mini",null);if(prev!=null&&DONE.plan){right=prev;end()}else ask()}

/* Kleine Happen auf dem Handy: Abschnitte mit Überschrift klappen auf, Füllkästen stehen hinter „Mehr dazu“ */
stations.forEach(function(s,i){var c=s.querySelector(":scope > .content");if(!c)return;
  var kids=[].slice.call(c.children).filter(function(x){return !x.matches(".schwelle,.runway")}),hs=kids.filter(function(x){return x.tagName==="H2"&&!x.classList.contains("gl-more")});
  if(hs.length>=2&&ids[i]!=="kurz-vorher"){c.classList.add("secs");var k=-1,tot=hs.length;
    kids.forEach(function(x){if(x.tagName==="H2"){k++;x.classList.add("sec-h");x.setAttribute("role","button");x.setAttribute("tabindex","0");x.dataset.k=k;x.dataset.n=(k+1)+" von "+tot;x.setAttribute("aria-expanded",k===0?"true":"false")}
      else if(k>=0){x.dataset.sk=k;if(k>0)x.classList.add("sk-shut")}});
    function tog(h){var kk=h.dataset.k,open=h.getAttribute("aria-expanded")!=="true";h.setAttribute("aria-expanded",open?"true":"false");
      c.querySelectorAll(':scope > [data-sk="'+kk+'"]').forEach(function(x){x.classList.toggle("sk-shut",!open)});if(open&&PHONE.matches){var t=h.getBoundingClientRect().top;if(t>innerHeight*.5)h.scrollIntoView({block:"start",behavior:RM?"auto":"smooth"})}}
    c.querySelectorAll(":scope > .sec-h").forEach(function(h){var kk=h.dataset.k;if(kk!=="0"&&c.querySelector(':scope > [data-sk="'+kk+'"] .item.knot, :scope > [data-sk="'+kk+'"].knot-p, :scope > [data-sk="'+kk+'"] .knot-p')){h.classList.add("has-kn");h.insertAdjacentHTML("afterbegin",'<i class="sec-kn" aria-hidden="true"></i>')}});
    c.querySelectorAll(":scope > .sec-h").forEach(function(h){h.addEventListener("click",function(e){if(!PHONE.matches)return;tog(h)});h.addEventListener("keydown",function(e){if(PHONE.matches&&(e.key==="Enter"||e.key===" ")){e.preventDefault();tog(h)}})})}
  c.querySelectorAll(".fill").forEach(function(f){var fh=f.querySelector(":scope > .fill-h");if(!fh)return;f.classList.add("more");fh.setAttribute("role","button");fh.setAttribute("tabindex","0");fh.setAttribute("aria-expanded","false");
    fh.insertAdjacentHTML("beforeend",'<em class="more-l" aria-hidden="true">Mehr dazu</em>');
    function t2(){if(!PHONE.matches)return;var o=!f.classList.contains("open");f.classList.toggle("open",o);fh.setAttribute("aria-expanded",o?"true":"false")}
    fh.addEventListener("click",t2);fh.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();t2()}})})});

/* Weiter-Knopf am Ende jedes Schritts: die Schwelle zählt den Schritt als erledigt */
stations.forEach(function(s,i){var sw=s.querySelector(":scope > .content > .schwelle");if(sw)sw.addEventListener("click",function(){markDone(ids[i])},true)});

/* Handy: obere Leiste mit Zurück statt Menü, untere Leiste mit Lernpfad, Quiz, Spickzettel und Weiter */
var PHONE=window.matchMedia?matchMedia("(max-width:759px)"):{matches:false};
(function(){var tb=document.querySelector(".topbar"),bk=el("button",{class:"iconbtn tb-back",id:"tbback","aria-label":"Ein Schritt zurück"},'<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M13.5 4.5L7 11l6.5 6.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>');
  tb.insertBefore(bk,tb.firstChild);bk.addEventListener("click",function(){if(cur>0)backTo(cur-1,false)});
  var tabs=el("div",{class:"tabs",role:"navigation","aria-label":"Bereiche"});
  var T=[["tab-path","Lernpfad",'<circle class="rg-bg" cx="10" cy="10" r="8.2"/><circle class="rg-fg" id="tabring" cx="10" cy="10" r="8.2" pathLength="1" transform="rotate(-90 10 10)"/><text class="rg-tx" id="tabnum" x="10" y="10.6">0</text>'],["tab-quiz","Quiz",'<circle cx="10" cy="10" r="7"/><path d="M8 8a2 2 0 1 1 2.6 1.9c-.4.2-.6.5-.6 1v.6M10 14v.1"/>'],["tab-spick","Spickzettel",'<path d="M5 3h7l3 3v11H5z"/><path d="M8 9h5M8 12h5M8 6h2"/>']];
  T.forEach(function(t){var b=el("button",{class:"tab",id:t[0]},'<svg width="22" height="22" viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+t[2]+'</svg><span>'+t[1]+'</span>');tabs.appendChild(b)});
  var bb=document.querySelector(".bb-in"),nx=document.getElementById("next");bb.insertBefore(tabs,nx);
  document.getElementById("tab-path").addEventListener("click",function(){if(pathEl.classList.contains("open"))closeSheet();else openSheet()});
  document.getElementById("tab-quiz").addEventListener("click",function(){goStep(ids.indexOf("quiz"))});
  document.getElementById("tab-spick").addEventListener("click",function(){goStep(ids.indexOf("kurz-vorher"))});
  var h2=pathEl.querySelector("h2");if(h2)h2.insertAdjacentHTML("afterend",'<p class="pc-done" id="pcdone"></p>')})();
function updTabs(i){var q=ids.indexOf("quiz"),s=ids.indexOf("kurz-vorher");document.getElementById("tab-quiz").classList.toggle("on",i===q);document.getElementById("tab-spick").classList.toggle("on",i===s);
  document.getElementById("tbback").disabled=i===0;updRing(i)}
/* Ring im Lernpfad-Knopf: Zahl = aktueller Schritt, roter Bogen = erledigte Schritte */
function updRing(i){var r=document.getElementById("tabring"),t=document.getElementById("tabnum"),tb=document.getElementById("tab-path");if(!r)return;if(i==null)i=cur;var d=stepsDone(),n=N-1;
  r.style.strokeDashoffset=String(1-d/n);t.textContent=i>0?String(i):"·";tb.setAttribute("aria-label","Lernpfad öffnen, Schritt "+(i>0?i:0)+" von "+n+", "+d+" erledigt")}
/* Blatt mit dem Lernpfad: nach unten ziehen schließt es */
(function(){var y0=null,dy=0;pathEl.addEventListener("touchstart",function(e){if(DESK.matches||!pathEl.classList.contains("open")||pathEl.scrollTop>2||e.touches.length!==1){y0=null;return}y0=e.touches[0].clientY;dy=0},{passive:true});
  pathEl.addEventListener("touchmove",function(e){if(y0==null)return;dy=e.touches[0].clientY-y0;if(dy>0&&pathEl.scrollTop<=0){pathEl.style.transition="none";pathEl.style.transform="translate3d(0,"+(dy*.9).toFixed(1)+"px,0)"}},{passive:true});
  function end(){if(y0==null)return;y0=null;pathEl.style.transition="";pathEl.style.transform="";if(dy>90)closeSheet();dy=0}
  pathEl.addEventListener("touchend",end,{passive:true});pathEl.addEventListener("touchcancel",end,{passive:true})})();

/* Startbildschirm: auch „Weiter“ unten führt zum nächsten offenen Schritt; Blatt heißt auf dem Handy „Dein Lernpfad“ */
document.getElementById("next").addEventListener("click",function(e){if(cur===0){var k=nextOpen();if(k!==1){e.stopImmediatePropagation();goStep(k)}}},true);
(function(){var h=pathEl.querySelector("h2");if(!h||!h.firstChild||h.firstChild.nodeType!==3)return;function f(){h.firstChild.nodeValue=PHONE.matches?"Dein Lernpfad ":"Roter Faden "}f();if(PHONE.addEventListener)PHONE.addEventListener("change",f)})();
var _un=updTabs;updTabs=function(i){_un(i);if(i===0&&stepsDone()>0)document.getElementById("nexttxt").textContent="Weiter"};
refreshDone();renderMini();
/* Knoten im roten Faden zünden einmal, wenn sie zum ersten Mal ins Bild kommen */
(function(){if(!("IntersectionObserver" in window)||RM)return;var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var n=e.target;if(n.closest(".rw-in,.peek-in,.back-ov")||!n.closest(".station.on"))return;n.classList.add("kn-on");io.unobserve(n)})},{rootMargin:"0px 0px -18% 0px",threshold:.6});
  document.querySelectorAll(".station .item.knot").forEach(function(n){io.observe(n)})})();
/* Selbst üben: eigene Antworten speichern, Wörter zählen, Musterlösung und Abhakliste aufklappen */
(function(){var U=store.get("ueb",{}),tm=null;function save(){clearTimeout(tm);tm=setTimeout(function(){store.set("ueb",U)},300)}
  document.querySelectorAll(".station > .content .ueb .ueb-t").forEach(function(t){var k=t.dataset.k,ta=t.querySelector("textarea"),n=t.querySelector(".ueb-n"),b=t.querySelector(".ueb-b"),l=t.querySelector(".ueb-l"),warn=false;
    function words(){var w=(ta.value.trim().match(/\S+/g)||[]).length;n.textContent=w+(w===1?" Wort":" Wörter");return w}
    ta.value=U[k]||"";words();
    ta.addEventListener("input",function(){U[k]=ta.value;words();save();if(warn){warn=false;b.textContent="Mit Musterlösung vergleichen"}});
    var cs=l.querySelectorAll("input[type=checkbox]"),cv=U[k+"_c"]||[];cs.forEach(function(c,i){c.checked=!!cv[i];c.addEventListener("change",function(){U[k+"_c"]=[].map.call(cs,function(x){return x.checked});save()})});
    function show(o){l.hidden=!o;b.textContent=o?"Musterlösung ausblenden":"Mit Musterlösung vergleichen";t.classList.toggle("open",o);try{fixRest()}catch(e){}}
    b.addEventListener("click",function(){if(!l.hidden){show(false);return}if(words()<15&&!warn){warn=true;b.textContent="Erst selbst schreiben? Nochmal tippen zeigt sie trotzdem";return}warn=false;show(true);if(PHONE.matches)setTimeout(function(){l.scrollIntoView({block:"start",behavior:RM?"auto":"smooth"})},60)});
    if(U[k+"_o"])show(true)})})();
/* Touch-Geräte (auch iPad mit Tastatur oder Trackpad): Während gescrollt wird, halten Zeichnungen und Dauer-Animationen an.
   Safari zeichnet sonst bei jedem Schritt einer Schleife die leuchtende Zeichnung samt Schein neu, das bremst das Scrollen. */
(function(){if(!(navigator.maxTouchPoints>0))return;var R=document.documentElement,tm=0,held=[];R.classList.add("touch");window.SCRL=false;
  function start(){if(window.SCRL)return;window.SCRL=true;R.classList.add("scrl");held=[];document.querySelectorAll(".station.on svg").forEach(function(v){try{if(!v.animationsPaused()){v.pauseAnimations();held.push(v)}}catch(e){}})}
  function stop(){window.SCRL=false;R.classList.remove("scrl");document.querySelectorAll(".station.on svg").forEach(function(v){try{if(v._io&&v.animationsPaused())v.unpauseAnimations()}catch(e){}});held.forEach(function(v){try{if(v._io!==false&&v.animationsPaused())v.unpauseAnimations()}catch(e){}});held=[]}
  window.addEventListener("scroll",function(){if(peekBusy||document.querySelector(".back-ov")){if(window.SCRL){clearTimeout(tm);stop()}return}start();clearTimeout(tm);tm=setTimeout(stop,220)},{passive:true})})();
