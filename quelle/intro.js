/* ================= START-INTRO „ZÜNDUNG“ (wiederverwendbar) =================
   Ablauf beim ersten Besuch pro Sitzung (html.vh):
   1. Sobald Schriften und Layout stehen, zündet die Neonlinie direkt auf der Höhe des roten Fadens im Kopf
      der Startseite (.fadenline), dort, wo er gleich liegen wird (introPrime). Vorher bleibt der Schirm dunkel.
   2. Beim Startsignal teilt sich der Schirm genau dort mit weichen Kanten. Die Linie wird zum Faden: erst gerade, dann biegt sie
      sich in ihre Welle.
   4. Jedes Startelement zündet wie eine Leuchtröhre in dem Moment, in dem die Kante des Dunkels es freigibt.
      Nichts gleitet herein, es gibt nur Licht (opacity und filter).
   Ohne Intro (spätere Ladevorgänge) läuft dieselbe Welle weich von oben, ohne Flackern.
   Einbinden: intro.css ans CSS hängen, diese Datei vor fromHash() einsetzen. In go2 direkt vor openStage()
   introPrime() aufrufen, in openStage() die Wartezeit 480-performance.now() durch
   (INTRO.litAt||0)+480-performance.now() ersetzen, vor d.classList.add("vh-open") introPlan(vh) aufrufen und
   die 700 im Timer, der "vh" entfernt, durch Math.max(700,INTRO.end||0) ersetzen. Anpassen: nur INTRO. */
var INTRO={
  thread:":scope > .hero > .fadenline",          /* Faden im Kopf der Startseite, fehlt er, teilt sich der Schirm unter dem Titel */
  skip:".deco,.sg,.fadenline,.cur,.val,script",  /* Deko, die nicht einzeln zündet */
  bars:[".topbar",".bottombar"],                 /* feste Leisten */
  side:".path .brand,.path h2,.path ol > li,.side-extra > *", /* Seitenleiste ab 1100 px */
  glide:70,           /* ms, kurzer Moment zwischen fertig gezündeter Linie und Teilung */
  split:860,          /* ms, Schirm öffnet sich vom Faden aus, zwei Lichtkanten laufen nach außen */
  feather:190,        /* px, weiche Kante des Dunkels */
  bend:620,           /* ms, gerade Linie biegt sich in die Welle */
  lead:.06,           /* s, so viel früher als die Kante zündet ein Element */
  softBase:.02, softSpread:.3,
  end:0, litAt:0, fy:null  /* werden gesetzt */
};
function introBez(x1,y1,x2,y2){function c(a,b,t){return((1-3*b+3*a)*t+(3*b-6*a))*t*t+3*a*t}   /* cubic-bezier als Funktion t→y */
  return function(x){var lo=0,hi=1,t=x;for(var i=0;i<22;i++){var v=c(x1,x2,t);if(v<x)lo=t;else hi=t;t=(lo+hi)/2}return c(y1,y2,t)}}
function introFy(st){var H=innerHeight,thr=st.querySelector(INTRO.thread),tr=thr&&thr.getBoundingClientRect();
  if(tr&&tr.height>0&&tr.bottom>0&&tr.top<H)return{fy:Math.round(tr.top+tr.height/2),thr:thr,tr:tr};
  var h1=st.querySelector(".hero h1"),hr=h1&&h1.getBoundingClientRect();return{fy:Math.round(hr?Math.min(H*.7,hr.bottom+14):H*.35),thr:null,tr:null}}
/* Die Linie zündet gleich dort, wo der Faden liegen wird: Vorhang dort teilen, Linie und Lichthof dorthin, dann erst zünden */
function introPrime(){var d=document.documentElement;if(!d.classList.contains("vh")||RM)return;var cu=document.querySelector(".curtain"),st=cur>=0?stations[cur]:null;if(!cu||!st)return;
  var H=innerHeight,f=introFy(st).fy,hz=cu.querySelector(".hz"),bl=cu.querySelector(".bloom"),top=cu.querySelector(".nc-top"),bot=cu.querySelector(".nc-bot");
  if(hz)hz.style.top=f+"px";if(bl)bl.style.top=f+"px";if(top)top.style.height=(f+1)+"px";if(bot){bot.style.top=f+"px";bot.style.height=(H-f)+"px";bot.style.bottom="auto"}
  INTRO.fy=f;INTRO.litAt=performance.now();cu.classList.add("lit")}
function introPlan(vh){
  var d=document.documentElement;if(RM||!Element.prototype.animate)return;
  var H=innerHeight,st=cur>=0?stations[cur]:null;if(!st)return;
  var _f=introFy(st),thr=_f.thr,tr=_f.tr,fy=_f.fy;
  /* Was zündet? Große Blöcke werden in ihre Kinder zerlegt, damit die Welle sichtbar läuft */
  var els=[];
  function vis(r){return r.width>0&&r.height>0&&r.bottom>0&&r.top<H}
  function add(n,depth){if(!n||n.nodeType!==1||n.matches(INTRO.skip)||n.hidden)return;var r=n.getBoundingClientRect();if(!vis(r))return;
    if(depth<3&&r.height>H*.4&&n.children.length>1){[].forEach.call(n.children,function(k){add(k,depth+1)});return}els.push([n,r])}
  [].forEach.call(st.querySelectorAll(":scope > .hero > *"),function(n){add(n,9)});
  [].forEach.call(st.querySelectorAll(":scope > .content > *"),function(n){add(n,0)});
  document.querySelectorAll(INTRO.side).forEach(function(n){add(n,9)});
  INTRO.bars.forEach(function(s){add(document.querySelector(s),9)});
  var cu=document.querySelector(".curtain"),hz=cu&&cu.querySelector(".hz"),top=cu&&cu.querySelector(".nc-top"),bot=cu&&cu.querySelector(".nc-bot"),bl=cu&&cu.querySelector(".bloom");
  var full=vh&&cu&&hz&&top&&bot,F=INTRO.feather,EZ=[.42,0,.22,1],E=introBez(EZ[0],EZ[1],EZ[2],EZ[3]);
  /* Zündzeit je Element: wann gibt die Kante des Dunkels seine Mitte frei? */
  function edgeTime(c){var need=c<fy?(fy-c)/(fy+F+4):(c-fy)/(H-fy+F+4);need=Math.min(1,Math.max(0,need));var lo=0,hi=1;for(var i=0;i<20;i++){var m=(lo+hi)/2;if(E(m)<need)lo=m;else hi=m}return hi}
  var last=0;
  els.forEach(function(e){var c=e[1].top+e[1].height/2,dl;
    if(full)dl=Math.max(0,(INTRO.glide+edgeTime(c)*INTRO.split)/1000-INTRO.lead);
    else dl=INTRO.softBase+Math.min(1,Math.max(0,c)/H)*INTRO.softSpread;
    last=Math.max(last,dl);e[0].classList.add("ig-el");e[0].style.setProperty("--igd",dl.toFixed(3)+"s")});
  d.classList.add("ig");if(!vh)d.classList.add("ig-soft");
  if(full){
    cu.classList.add("hand");
    /* Vorhang an der Fadenhöhe teilen: Hälften neu zuschneiden (beide noch schwarz, unsichtbar), weiche Kanten anhängen */
    top.style.height=(fy+1)+"px";bot.style.top=fy+"px";bot.style.height=(H-fy)+"px";bot.style.bottom="auto";
    [top,bot].forEach(function(h){if(!h.querySelector(".nf")){var f=document.createElement("i");f.className="nf";h.appendChild(f);var l=document.createElement("i");l.className="ne";h.appendChild(l)}});
    var G=INTRO.glide,S=INTRO.split,ez="cubic-bezier("+EZ.join(",")+")";
    top.animate([{transform:"translate3d(0,0,0)"},{transform:"translate3d(0,"+(-(fy+F+4))+"px,0)"}],{duration:S,delay:G,easing:ez,fill:"both"});
    bot.animate([{transform:"translate3d(0,0,0)"},{transform:"translate3d(0,"+(H-fy+F+4)+"px,0)"}],{duration:S,delay:G,easing:ez,fill:"both"});
    /* Aus der einen Linie werden beim Teilen drei: der Faden bleibt, zwei Lichtkanten laufen mit dem Dunkel nach außen */
    cu.querySelectorAll(".ne").forEach(function(l){l.animate([{opacity:0,transform:"scaleX(.55)"},{opacity:.95,transform:"scaleX(.9)",offset:.1},{opacity:.55,transform:"scaleX(1.1)",offset:.55},{opacity:0,transform:"scaleX(1.25)"}],{duration:S,delay:G-20,easing:"ease-out",fill:"both"})});
    /* Linie: gleitet auf den Faden, wird beim Teilen zum Faden und verlischt */
    var r=hz.getBoundingClientRect(),cy=r.top+r.height/2,dy=fy-cy;
    var sx=thr?Math.max(.2,tr.width/Math.max(1,r.width)):1.15,dx=thr?(tr.left+tr.width/2)-(r.left+r.width/2):0;
    hz.animate([{transform:"translate3d(0,"+dy.toFixed(1)+"px,0) scaleX(1)",opacity:1,easing:"ease-out"},{transform:"translate3d("+dx.toFixed(1)+"px,"+dy.toFixed(1)+"px,0) scaleX("+sx.toFixed(3)+")",opacity:0}],
      {duration:300,delay:G,fill:"both"});
    if(bl)bl.animate([{transform:"translate3d(0,"+dy.toFixed(1)+"px,0) scale(1)",opacity:1,easing:"ease-out"},{transform:"translate3d(0,"+dy.toFixed(1)+"px,0) scale(1.9,3)",opacity:0}],
      {duration:S,delay:G,fill:"both"});
    if(thr){
      thr.classList.add("ig-thr");
      thr.animate([{opacity:0},{opacity:1}],{duration:200,delay:G,fill:"backwards"});
      var vb=(thr.getAttribute("viewBox")||"0 0 0 140").split(/[\s,]+/),mid=(+vb[3]||140)/2,NUM=/-?\d*\.?\d+/g;
      var jobs=[].map.call(thr.querySelectorAll("path"),function(p){var w=p.getAttribute("d")||"",fl=w.replace(/(-?\d*\.?\d+)([\s,]+)(-?\d*\.?\d+)/g,function(m,x,s){return x+s+mid});
        p.setAttribute("d",fl);return{p:p,w:w,a:(w.match(NUM)||[]).map(Number),b:(fl.match(NUM)||[]).map(Number)}});
      var bend=introBez(.3,0,.15,1);
      setTimeout(function(){var t0=performance.now();(function step(now){var k=Math.min(1,(now-t0)/INTRO.bend),e=bend(k);
        jobs.forEach(function(j){var i=0;j.p.setAttribute("d",j.a.length!==j.b.length?j.w:j.w.replace(NUM,function(){var v=j.b[i]+(j.a[i]-j.b[i])*e;i++;return v.toFixed(2)}))});
        if(k<1)requestAnimationFrame(step);else jobs.forEach(function(j){j.p.setAttribute("d",j.w)})})(t0)},G+40);
    }
    INTRO.end=G+S+60;
  }
  /* Aufräumen: Die Elemente behalten ihren Endzustand. animation:none verhindert, dass ihre alten
     Einstiegsanimationen (boot, .station.first) beim Entfernen der Klasse neu starten und aufblitzen. */
  setTimeout(function(){els.forEach(function(e){e[0].style.animation="none";e[0].classList.remove("ig-el");e[0].style.removeProperty("--igd")});d.classList.remove("ig","ig-soft");
    if(cu){cu.classList.remove("hand");[top,bot].forEach(function(h){if(h){h.removeAttribute("style");h.getAnimations().forEach(function(a){a.cancel()})}});[hz,bl].forEach(function(x){if(x)x.getAnimations().forEach(function(a){a.cancel()})})}},
    Math.round((last+.7)*1000)+60);
}
