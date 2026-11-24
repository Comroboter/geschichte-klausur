# Kaiserreich und Kolonien · Projektwissen und Gerüst

Lernseite zur Geschichtsklausur (Kaiserreich, Industrialisierung, soziale Frage, Kolonien, Kongokonferenz), Jahrgang Abi 2028.
Live: https://comroboter.github.io/geschichte-klausur/ · Repo: Comroboter/geschichte-klausur (GitHub Pages aus `main`, Wurzel).
**Diese Seite ist das Gerüst für alle neuen Lernseiten.** Sie ist aus der Antigone-Seite (Comroboter/dramenszenenanalyse-klausur) entstanden und hat danach viele Runden auf echten Geräten bekommen: Intro „Zündung“, Gesten, Dock, Knoten, Selbst üben, iPad-Leistung. Neue Seiten starten von hier, nicht von Antigone.

## Mit Leopold arbeiten
- Deutsch, locker und direkt. Keine Gedankenstriche (– —) im Fließtext, keine KI-Floskeln, keine dramatischen Schlusssätze, kein unnötiges Fett.
- Ehrlich statt Lob. Zahlen konkret nennen und dazuschreiben, wie sicher sie sind.
- Geräte: Samsung S24, Schul-iPad (Safari), PC-Monitor. Was nicht auf echter Hardware geprüft ist, offen sagen.
- Geschmack: neon-modern, aber minimalistisch. Nicht generisch, nicht „claudisch“.
- Er lädt selbst auf GitHub hoch (Weboberfläche). Ausliefern heißt: Website-zip (Inhalt in die Repo-Wurzel) und bei Bedarf dieses Projekt-zip mit `quelle/`.

## Stand der Inhalte
- Grundlage ist die selbst erstellte Lernübersicht aus dem Kurs ab Punkt 1c (ohne Namen nennen). Ergänzungen sind recherchiert (bpb, LeMO, German History in Documents and Images).
- Klausurformat laut Blatt: ein Text, Aufgabe 1 Eckdaten, Aufgabe 2 Zusammenfassung, Aufgabe 3 Sachurteil. Dauer steht nicht auf dem Blatt, angenommen 90 Minuten. Datum: `KLAUSUR=null` oben im Datenblock (mit Datum erscheinen Countdowns).
- Kein Erklär-Audio (`NARR=null`, der Knopf blendet sich aus).
- Sensible Inhalte: Völkermord an Herero und Nama, Rassismus. Sachlich bleiben, Opferzahlen als Schätzungen kennzeichnen, abwertende Quellensprache nur in Anführungszeichen.
- „Selbst üben“ nutzt eine vereinfachte, sinngemäße Fassung der Kaiserlichen Botschaft vom 17.11.1881, ausdrücklich kein Originalwortlaut. Das Bülow-Beispiel steht noch als Musterabsatz in der Station Aufgaben und in der Lesefassung (`EX.buelow`).

## Schritte
start (Übersicht), plan, revolution, gesellschaft, industrie, sortieren (Übung Zuckerbrot oder Peitsche), kolonien, kongo, personen, aufgaben (mit Selbst üben), quiz, kurz-vorher. Akte über `ACTS` in make.py.

## Aufbau
```
/ (Repo-Wurzel = GitHub Pages)
  index.html sw.js manifest.webmanifest icon-*.png favicon-32.png og.png   ← Build-Ergebnis
  CLAUDE.md
  quelle/
    template.html  Grundgerüst (Antigone-App mit aller Maschinerie). Nie direkt ändern, nur über make.py.
    make.py        baut app.html: liest template.html, setzt stations.html und data.js ein, hängt extra.css, mobil.css,
                   intro.css, mobil.js, intro.js an und wendet nummerierte Patches an (rep(): Text muss genau einmal
                   vorkommen, sonst bricht der Build ab). Neue Patches vor der Zeile „# Zurücksetzen löscht auch …“.
    farben.py      eine Farbe pro Station (--st), läuft am Ende von make.py
    stations.html  alle Stationen (Markup)          data.js  Datenblock: PARTS, B, Q, SO, EX, KLAUSUR …
    extra.css      Looks und Bausteine des Themas    mobil.css / mobil.js  Handy, Dock, Knoten, Selbst üben, Touch-Leistung
    intro.css / intro.js  Start-Intro „Zündung“ (wiederverwendbar)
    build.py       Schriften einbetten, Lesefassung ohne JS, Icons, og.png, Manifest, Service Worker → dist/
    ttf/           Schriften für Icon und og.png      tests/  Playwright
```
Build: `cd quelle && npm install && pip install -r requirements.txt --break-system-packages && python3 make.py && python3 build.py`. Ergebnis: `dist/kaiserreich.html` (Einzeldatei, auch fürs Artefakt) und `dist/website/` (Inhalt in die Repo-Wurzel). Tests laufen gegen `dist/kaiserreich.html`, also immer erst bauen.

## Neue Lernseite aus diesem Gerüst
1. `quelle/` kopieren, `npm install`, bauen, Tests laufen lassen: muss vor jeder Änderung grün sein.
2. Inhalt tauschen: `stations.html` (Stationen, `data-look`, `data-title`, `data-min`), `data.js` (alles zwischen DATEN und ZUSTAND), `extra.css` (Looks des neuen Themas).
3. Themenstellen in make.py (`grep -n "Kaiserreich\|Kolonien\|geschichte-klausur\|Geschichtsklausur" make.py`): Titel, Beschreibung, og-Tags samt URL (muss auf das neue Repo zeigen, sonst fehlt beim Teilen das Vorschaubild), Marke in der Seitenleiste, Legende, `ACTS`, Teilen-Text, CSS-Kommentare. Stations-IDs, die Patches direkt nennen (z. B. `kurz-vorher`, `aufgaben`), prüfen.
4. Themenstellen in build.py: Lesefassung (eine Funktion pro Station, liest den Datenblock), Text auf og.png und Icon, Manifest-Name, Service-Worker-Präfix (eigenes Präfix pro Seite, alle Seiten auf comroboter.github.io teilen sich den Speicher), Dateinamen in dist/. Speicher-Präfix `kr_` im Datenblock ändern.
5. Suche nach Resten: `grep -rn "Kaiserreich\|Kolonie\|Bismarck\|Bülow" quelle/*.html quelle/*.js quelle/*.py` muss leer sein (außer das Thema ist wieder dasselbe).
6. Tests anpassen, die Stationen beim Namen nennen (`tests/*.py`, z. B. Startstation in hochwischen.py).

## Tests (aus `quelle/`)
`tests/run_all.py` (Übergänge in drei Größen, Mausrad, Zurück, Safari-Viewport-Simulation, Hochwischen), `tests/smoke.py` (Screenshots, Konsolenfehler), `tests/interaktion.py` (Quiz, Sortieren, Stapel, Häkchen), `tests/leere_stellen.py W H`, `tests/longtasks_scroll.py`, `tests/animationskosten.py`.
Erwartete Restmeldungen in `uebergang_kopie_vs_echt.py`: 1 px bei `#industrie`, `#kolonien`, `#aufgaben`, `#plan`. Per Element-Vergleich geprüft: Rundung, kein echter Unterschied.

## Handy-Fassung (19.11.)
- Schritte statt Stationen: Start ist die Übersicht, danach Schritt 1 bis 14. Erledigt ist ein Schritt, wenn man ihn nach vorn verlässt oder das Mini-Quiz in Schritt 1 beendet (`localStorage kr_done`).
- Startbildschirm (`#home`): ein Satz, Gesamtzeit, ein großer Knopf zum nächsten offenen Schritt, Fortschritt „x von 6 Themen“, darunter der Lernpfad.
- Unter 760 px: obere Leiste mit Zurück statt Menü, untere Leiste mit Lernpfad, Quiz, Spickzettel und Weiter. Die Schwelle am Ende jedes Schritts wird zum großen Weiter-Knopf. Abschnitte mit Überschrift klappen auf, Füllkästen stehen hinter „Mehr dazu“.
- Regeln fürs Handy: Fließtext mindestens 16 px, alles Antippbare mindestens 44 px. CSS-Regeln, die auch in Vorschau-Kopien gelten sollen, nie an `.station` hängen (Kopien haben die Klasse nicht), sonst bricht „Vorschau = echte Seite“.
- Farbsystem: eine Farbe pro Station über `--st` (Look-Palette am Ende des CSS).
- Test dazu: `tests/hochwischen.py`, und `uebergang_kopie_vs_echt.py` vergleicht jetzt das Overlay, wenn es aktiv ist.

## Zuschnitt auf die Lernansicht (19.11., abends)
- Inhaltliche Grundlage ist nur noch die Lernansicht aus dem Unterricht ab Schritt 1c. Entfernt: Handwerk, Einleitung bauen, Moderne und Vergangenheit, Quelle Bülow, Rassismus (als eigener Schritt), Kolonialzeit beurteilen.
- Schritte: Übersicht, 1 Plan, 2 Revolution 1848 und Reichsgründung, 3 Gesellschaft, 4 Industrialisierung und soziale Frage, 5 Zuckerbrot oder Peitsche (Übung), 6 Gründe für Kolonialismus, 7 Kongokonferenz, 8 Bismarck und die Kaiser, 9 Die drei Klausuraufgaben, 10 Generalprobe, 11 Spickzettel.
- Daten: PARTS hat sechs Themen (ITEMSTATION revolution, gesellschaft, industrie, kolonien, kongo, personen), 39 Karten, 6 Sortierkarten, 25 Quizfragen. ST, CMP, TL und EX sind Altlasten ohne Schritt, der Code dazu läuft über `gid()` ins Leere.
- Klausurformat laut Blatt: ein Text, Aufgabe 1 Eckdaten, Aufgabe 2 Zusammenfassung, Aufgabe 3 Sachurteil.

## Runde 19.11. abends (Gesten und Spickzettel)
- Weiter-Knopf am Ende jedes Schritts (Handy): dunkle Fläche mit Haarlinie in Stationsfarbe, Ring links füllt sich beim Hochziehen rot, keine Skalier-Animation am ganzen Knopf (`mobil.css`).
- Zurückwischen oben: 120 px Fingerweg (vorher 192), schneller Wisch ab 50 px reicht. Beim Ziehen wird die Seite zum Blatt (clip-path plus `.bp-edge`). Beim Loslassen fährt die Seite sofort per WAAPI auf dem Compositor weiter (Geschwindigkeit vom Finger), die teure Umschaltung läuft einen Frame später, das Overlay übernimmt mit gleicher `startTime`. Ziel kommt aus `SHC` (Ruheposition je Station, gecacht in `arm`/`onIdle`). Overlay animiert nur noch transform.
- Schwung am Seitenende und -anfang federt weich nach (`edgeBounce`, nur Touch, nur transform), `onIdle` wartet die Feder ab.
- Roter Faden oben: transform statt width, keine CSS-Transition mehr, Sprünge als eine WAAPI-Animation. Fortschritt = 0 oben bis 1 an der Ruheposition, deshalb bewegt er sich beim Zurückgehen nicht hin und her.
- Spickzettel: pro Thema drei Merksätze statt aller Punkte, 11 Daten, vier Regeln, offene Punkte nur als Auswahl (6 plus „und x weitere“). Grundlage ist eine selbst erstellte Lernübersicht (ohne Namen).
- „Fortschritt zurücksetzen“ löscht auch `kr_done`, „Häkchen und Stempel löschen“ ebenso.

## Start-Intro „Zündung“ (wiederverwendbares Modul, quelle/intro/)
- Ablauf: Sobald Schriften und Layout stehen (`introPrime` in go2), zündet die Neonlinie direkt auf der Höhe des roten Fadens im Kopf der Startseite (`.fadenline`), vorher bleibt der Schirm dunkel. Kein Gleiten, das sah aus wie ein verrutschter Keyframe. Beim Startsignal teilt sich genau dort der Schirm mit weichen Kanten, aus einer Linie werden drei: Der Faden bleibt und biegt sich in seine Welle, zwei Lichtkanten laufen mit dem Dunkel nach oben und unten. Jedes Element zündet wie eine Leuchtröhre in dem Moment, in dem eine Kante es freigibt (Zeit aus der Easing-Kurve zurückgerechnet). Nichts gleitet herein.
- Einbau: `intro.css` ans CSS hängen, `intro.js` vor `fromHash();`, in go2 direkt vor `openStage()` den Aufruf `try{introPrime()}catch(e){}`, in `openStage()` die Wartezeit `480-performance.now()` durch `((window.INTRO&&INTRO.litAt)||0)+480-performance.now()` ersetzen, vor `d.classList.add("vh-open")` den Aufruf `try{introPlan(vh)}catch(e){}`, und im Timer, der `vh` entfernt, `700` durch `Math.max(700,(window.INTRO&&INTRO.end)||0)` ersetzen. Anpassen nur über `INTRO`.
- Aufräumen setzt `animation:none` inline, bevor die Klasse fällt. Sonst starten die alten Einstiegsanimationen (`.boot`, `.station.first`, `drawThread`) neu und die Seite blitzt kurz auf.
- Fehlt `.fadenline`, teilt sich der Schirm unter dem Titel. Ohne Intro (spätere Ladevorgänge) läuft dieselbe Welle weich von oben.

## Leistung auf Handys (19.11., spät)
- Auf Touch-Geräten keine backdrop-filter-Ebenen mehr (Leisten fast deckend, `.bfade` nur Farbverlauf). Fünf gestapelte Weichzeichner haben auf dem Handy beim Scrollen und bei Wechseln die GPU ausgelastet.
- Scroll-Handler ohne Layout-Thrash: `docTop()`, `maxScroll()`, `padB()` gecacht, ungültig über `ResizeObserver` (`GEO.v`). `classList.remove` nur, wenn die Klasse da ist (sonst entsteht trotzdem eine Mutation mit Stil-Neuberechnung). Messung: pro Scroll-Frame etwa 15 ms auf 9 ms (1x CPU).
- Unter der unteren Leiste verlängert `.bottombar::after` den Hintergrund um 80 px, gegen einen Spalt in Android-WebViews.
- Schwung am Seitenende: Die Strecke wird beim Aufprall sofort scharf, ein erneuter Wisch während der Feder geht direkt zur nächsten Seite.
- Wechsel entlastet (19.11., 21 Uhr): Beim Zurück bekommt die Vorschau der vorigen Seite nur den sichtbaren oberen Teil der Kopie (`FILLPART`), die volle Kopie folgt in Ruhe. Nach Blatt-Wechseln bekommt die Station nur noch `on` statt `enter fwd via-peek` (die `*`-Regel von via-peek hat alle Nachfahren neu berechnen lassen). `updateMore` pausiert während eines Wechsels. Nächste und vorige Station werden in Ruhe vorgewärmt (`warmSt`). Gemessen (1x CPU): Umschalten beim Zurück 65 auf 33 ms, danach 47 auf 15 ms.
- Festhalten und Ziehen (19.11., 21:30): Leerlauf-Arbeit (`quiet()`, also Vorwärmen, Nachladen der Vorschau, Vorbereitung) läuft nie, solange ein Finger oder eine Maustaste unten ist (`touching`, `PDOWN`). Vorher konnte sie genau dann starten, wenn man eine Karte kurz still festhielt, und das Ziehen danach hakte. Ein Fingertipp während der Feder am Seitenende lässt die Seite in 140 ms weich zurückgleiten statt zu springen.
- Zurückziehen festhalten: `touchcancel` zählt nicht als Loslassen (Seite federt zurück, kein Wechsel, auch vorwärts nicht). Während des Ziehens `html.bpull` ohne Textauswahl und Callout, `contextmenu` wird unterdrückt. Vorher löste etwa 1 s Festhalten auf dem Handy einen Abbruch aus, der als Loslassen galt und zurückblätterte.
- Zurückziehen festhalten, Teil 2: Oben auf der Seite (scrollY ≤ 1, nur Touch) hängt ein nicht-passiver touchmove-Wächter (`tmGuard`, `tmSync`), der während des Ziehens `preventDefault` ruft. So übernimmt weder der Browser noch eine umgebende App (Claude-App-Fenster) die Geste. Weiter unten bleibt alles passiv, damit Scrollen nie auf JavaScript wartet.
- Feder am Ende: Die Station liegt nahe Anfang und Ende der Seite schon vorher auf eigener Ebene (`wcZone`, `will-change:transform`, im Leerlauf wieder entfernt), Scharfschalten 170 ms nach dem Aufprall statt im selben Frame.

## „Muss sitzen“: Knoten im roten Faden (19.11., 22 Uhr)
- In `data.js` bekommt ein Punkt `k:"Begründung"`. Dann hat er links eine leuchtende Fadenlinie mit Knoten, im Titel die kursive Regieanweisung „Muss sitzen“, im aufgeklappten Teil die Begründung in Fadenrot, und der Knoten zündet einmal, wenn er ins Bild kommt (Animation startet und endet im Ruhezustand). Abschnittsköpfe mit Knoten bekommen am Handy einen roten Rand und Punkt.
- Markiert: Reichsgründung 1871, Obrigkeitsstaat und Militarismus, Bismarcks Sozialversicherung, Politische Gründe (Platz an der Sonne), Effektive Besetzung und Anzeigepflicht, Bismarck und die Kolonien, dazu der Kasten Sachurteil gegen Werturteil (`.panel.knot-p`) und die passenden Zeilen im Spickzettel (`li.kn`).

## Dock statt Leiste (Handy, 19.11., 22:45)
- Unten schwebt ein Dock (10 px Abstand zum Rand, Radius 22, deckend, Schatten), kein randloser Balken mehr: kein Spalt mehr möglich, `.bfade` läuft bis zum unteren Rand.
- Lernpfad ist ein Fortschrittsring (Zahl = aktueller Schritt, roter Bogen = erledigte Schritte, `updRing`), daneben Quiz und Spickzettel. Der aktive Bereich trägt einen kurzen roten Faden über dem Symbol.
- Weiter in der Sprache der Schwelle: dunkle Fläche mit Schein und Rand in der Farbe der aktuellen Station (`--ac-cur`), runder Pfeil in Stationsfarbe, kein weißer Knopf mehr.
- Lernpfad-Blatt: nach unten ziehen (ab 90 px) schließt es, außerdem Tippen daneben.

## Selbst üben, Quiz-Mischen, Faktenkorrekturen (Runde nach externer Durchsicht)
- Station Aufgaben hat am Ende „Selbst üben“ (`.ueb`, nur mit JS): vereinfachte Fassung der Kaiserlichen Botschaft vom 17.11.1881 (ausdrücklich kein Originalwortlaut), drei Aufgaben mit Textfeld, Wortzähler, Abhakliste und Musterlösung. Speicher: `store` Schlüssel `ueb` (Texte, Häkchen). Unter 15 Wörtern fragt der Knopf einmal nach, bevor er die Lösung zeigt.
- Quiz: Antwortoptionen werden pro Frage zufällig gemischt (`ord`, richtige Position `cq`). Die gespeicherten Positionen in `Q` sind zusätzlich gestreut, damit die Lesefassung kein Muster zeigt. Ablenker sind plausible Beinahe-Treffer, keine Witzantworten.
- Zeitplan: `planMins(m)` rundet nach größtem Rest auf 5-Minuten-Blöcke, die Summe stimmt immer mit der Klausurdauer überein.
- Fakten: Kongokonferenz 14 Staaten inklusive USA und Osmanisches Reich, Grenzen meist erst danach in Einzelverträgen. Arbeitszeit im Kaiserreich meist 11 bis 12 h, um 1900 rund 10 h (14 bis 16 h war frühe Industrialisierung).
- og:url/og:image zeigen auf comroboter.github.io/geschichte-klausur/.

## Rest-Versatz nach dem Wechsel (make.py #27)
- Am Handy kann die Seite beim Hochwischen noch nachschwingen (Gummiband am Seitenende, Restschwung), während das Blatt in der Seite hochfährt. Dann endet die Kopie ein paar Pixel neben der echten Seite.
- Früher glitt danach nur `.hero` an die richtige Stelle, der Inhalt sprang. Jetzt gleiten `.hero` und `.content` gemeinsam (220 bis 340 ms), danach `GEO.v++` und `fixRest()`, weil Messungen während der Transform verschoben wären.
- Test: /tmp-artiges Skript, das nach touchend 24 px zurückscrollt und prüft, dass Kicker und Inhalt beim Tausch an derselben Stelle stehen und dann gemeinsam gleiten.

## iPad: Leiste zieht nicht mehr hinterher, weniger Dauerarbeit (make.py #28, Ende von mobil.css)
- Viewport-Fix: `--vvt`/`--vvb` werden nur noch an den Leisten selbst gesetzt (`.topbar,.bottombar,.morepill,.narr-cap,.bfade,.path`), nicht an `<html>`. Eine Variable an `<html>` hat bei jedem Wert die Stile der ganzen Seite neu berechnet.
- Neu gesetzt wird erst 150 ms nach dem letzten Scrollen (beim Tippen sofort). Während Safari scrollt und die Werte schwanken, rührt JS die Leiste nicht an. Vorher lief sie mit einem Bild Verzug hinterher und rastete erst später ein.
- Unsichtbares Overlay-Blatt (`.peek` ohne `on`) pausiert seine SMIL-Animationen (15 Stück liefen dauernd). Glanzpunkt der Startlinie (stroke-dashoffset), Pfeile der Schwellen auf versteckten Stationen und Lichtpunkt/Puls im geschlossenen Handy-Menü sind angehalten.
- Gemessen (Chromium, 820×1180, CPU ×4, 6 Wischgesten): Stil-Neuberechnungen 1267 → 543, neu berechnete Elemente 3270 → 1426. Den Rest machen die Zeichnung der aktuellen Station und ihr Schwellen-Pfeil.
- Test `safari_viewport_sim.py` liest die Variablen jetzt an `.topbar`/`.bottombar`.
- Nachtrag (#29): Scrollen erzeugt nie einen neuen Versatz, es darf ihn nur auf 0 zurücknehmen. Am Seitenende fährt Safari die Adressleiste wieder aus, die Messwerte schwanken kurz, das hat die Leiste nach dem Scrollen springen lassen. Neuer Versatz nur in den ersten 2,5 s nach dem Laden, 1 s nach Seitenwechsel oder `vvUpdate()`, nach Drehen und beim Tippen. Leisten gleiten bei Korrekturen (transition auf bottom/top, 240 ms).

## Touch-Geräte: Ruhe beim Scrollen (make.py #30, Ende von mobil.js und mobil.css)
- `html.touch` bei `navigator.maxTouchPoints>0` (greift auch am iPad mit Tastatur oder Trackpad, wo `hover:none` nicht zutrifft). Dann keine `backdrop-filter` unter Leisten und im Auslauf.
- Während gescrollt wird (`html.scrl`, bis 220 ms nach dem letzten scroll-Ereignis, nicht während Wechseln): SMIL der sichtbaren Station pausiert, Dauer-Animationen (`.art *`, Schwellen-Pfeil, Lichtpunkt, Puls, Glanz) angehalten. Danach laufen sie an derselben Stelle weiter. Grund: `.art` hat zwei drop-shadow-Filter, Safari zeichnet bei jedem Schleifenschritt alles samt Schein neu, das bremst das Scrollen in unregelmäßigen Abständen.
- Der SVG-IntersectionObserver merkt sich den Wunschzustand in `v._io` und startet während `window.SCRL` nichts.
