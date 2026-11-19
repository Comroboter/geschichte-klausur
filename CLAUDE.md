# Kaiserreich und Kolonien · Projektwissen

Interaktive Lernseite zur Geschichtsklausur: Gesellschaft im Kaiserreich (Industrialisierung, Moderne und Vergangenheit) und Kolonien (Gründe, Rassismus, Kongokonferenz). Jahrgang Abi 2028.
Geplant: https://comroboter.github.io/kaiserreich-klausur/ · Repo: Comroboter/kaiserreich-klausur (GitHub Pages aus `main`, Wurzelverzeichnis).
Gerüst ist die Antigone-Seite (Comroboter/dramenszenenanalyse-klausur). Maschinerie, Gesetze und Tests stammen von dort und sind in deren CLAUDE.md ausführlich beschrieben.

## Mit Leopold arbeiten
- Deutsch, locker und direkt. Keine Gedankenstriche (– —) im Fließtext, keine KI-Floskeln, keine dramatischen Schlusssätze, kein unnötiges Fett.
- Ehrlich statt Lob. Zahlen konkret nennen und dazuschreiben, wie sicher sie sind.
- Geräte: Samsung S24, Schul-iPad (Safari), PC-Monitor. Was nicht auf echter Hardware geprüft ist, offen sagen.
- Geschmack: neon-modern, aber minimalistisch. Nicht generisch, nicht „claudisch“.

## Stand der Inhalte (wichtig)
- **Noch ohne Unterrichtsunterlagen gebaut.** Alles ist recherchiert (bpb, LeMO des DHM, German History in Documents and Images) und gängiger Schulstoff. Sobald Unterlagen kommen: abgleichen, Abweichungen der Lehrkraft übernehmen, Material aus den Unterlagen mit `"u"` (Karten) markieren.
- **Annahmen:** 90 Minuten, Arbeit mit einer Quelle oder Karikatur, drei Aufgaben nach Anforderungsbereichen. Datum unbekannt: `KLAUSUR=null` oben im Datenblock. Mit Datum (`new Date(2026,11,3)`) erscheinen Countdown in der Leiste und auf der letzten Seite.
- **Kein Erklär-Audio** bisher (`NARR` bleibt `null`, der Knopf blendet sich aus). Nachrüsten wie bei Antigone: narration.json, Audio, `import_audio.py`.
- **Sensible Inhalte:** Völkermord an Herero und Nama, Maji-Maji, Rassismus. Sachlich bleiben, Opferzahlen immer als Schätzungen kennzeichnen, abwertende Quellensprache („Hottentotten“, „Eingeborene“) nur in Anführungszeichen.
- **Bülow-Rede (Station „Platz an der Sonne“):** Wortlaut geprüft an German History in Documents (PDF der GHDI), Rechtschreibung angepasst, 24 Zeilen. Zeilenangaben im Handwerk und im Musterabsatz beziehen sich auf diese Zählung. Wer Zeilen umbricht, muss alle „Z. …“-Angaben nachziehen.
- **Stand der Anerkennung 2021:** Gemeinsame Erklärung nur paraphiert, nicht abgeschlossen, Klage in Namibia (Stand November 2026). Vor der Klausur noch einmal prüfen.

## Stationen
start, plan, handwerk, einleitung (Übung: Einleitung einer Quellenanalyse), gesellschaft, industrie, sortieren (Zuckerbrot oder Peitsche), moderne, kolonien, kongo, quelle (Bülow annotiert), rassismus, urteilen, quiz, kurz-vorher. Akte: I Vorspiel, II Das Kaiserreich, III Kolonien, IV Finale.

Looks und Akzente (Nachbarn nie gleich): buehne/Pflaume, bauplan/Schiefer, lineal/Ocker, papier/Rost, **pyramide**/Pflaume (neu), zeitraum/Schiefer (umgefärbt), split/Petrol, epochen/Ocker (ohne Mäander), dialog/Rost (umgefärbt), zwei/Petrol, **akte**/Pflaume (neu), **stufen**/Schiefer (neu), tragik/Ocker (umgefärbt, ohne Mäander), probe/Pflaume, morgen/Rost. Die Ergänzungen stehen gesammelt am Ende des `<style>` unter „Geschichte: Looks und Bausteine“.

## Aufbau
```
/ (Repo-Wurzel = GitHub Pages)
  index.html sw.js manifest.webmanifest icon-*.png favicon-32.png og.png   ← Build-Ergebnis
  CLAUDE.md
  quelle/
    app.html   alles in einer Datei, Datenblock zwischen /* DATEN */ und /* ZUSTAND */
    build.py   baut dist/kaiserreich.html (Einzeldatei) und dist/website/, --deploy kopiert in die Wurzel
    tests/     Playwright (Chromium)
```
Build: `cd quelle && npm install && pip install -r requirements.txt && python3 build.py --deploy`. Braucht Node und Pillow, fontTools wandelt die WOFF für Icon und Vorschaubild.

## Unterschiede zur Antigone-Seite
- Speicher-Präfix `kr_` statt `dra_`, Service-Worker-Cache `kaiserreich-v1`. Der Worker löscht nur Caches mit Präfix `kaiserreich-`, weil sich alle Seiten auf comroboter.github.io denselben Speicher teilen.
- Quellentext: Zeilen als `.qz` (nicht `.zl`, das ist schon im Reißverschluss vergeben). Ab 760 px passt sich die Schrift per Container-Einheiten der Spalte an, damit jede Zeile eine Zeile bleibt. Auf dem Handy brechen Zeilen um, dort wird jede Zeile nummeriert.
- Handschrift (Caveat) nur noch in Randnotizen der Quelle. Merksätze in den Gliederungspunkten stehen als „Merke“ in normaler Schrift, weil es keine echten Tafelnotizen gibt.
- Plan: Die Balken der vier Blöcke zeigen den eigenen Fortschritt (`updGl`).
- **Fix gegen das Nachrutschen auf kurzen Seiten:** `fixCloneRest` rechnet im tiefen Klon den Abstand aus, den `fixRest` der echten Seite geben wird. Die Vorschau steht dadurch schon im Übergang an der richtigen Stelle. Gehört auch in die Antigone-Seite.

## Tests (aus `quelle/`)
`tests/run_all.py` (Übergänge in drei Größen, Mausrad, Zurück, Safari-Simulation, Hochwischen ohne Stillstand), `tests/smoke.py` (Screenshots aller Stationen, Konsolenfehler), `tests/interaktion.py` (Quiz, Sortieren, Quelle, Stapel, Häkchen), `tests/leere_stellen.py W H`.
Erwartete Restmeldungen in `uebergang_kopie_vs_echt.py`: `#einleitung` Element 1 (ausgeblendeter Umschalter mit Höhe 0, unsichtbar) und `#gesellschaft` Element 2 nur in der Höhe (scharfe Strecke unterhalb des Bildschirms, per Frame-Aufnahme geprüft: nichts springt). 1 px Differenz bei `#industrie` taucht gelegentlich auf.
