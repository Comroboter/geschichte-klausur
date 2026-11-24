"""Pflicht-Regression nach jeder Änderung: python3 tests/run_all.py
Vergleicht Vorschau-Kopie und echte Seite bei jedem Übergang (3 Größen), Mausrad an der Schwelle,
Zurück-Wischen/Leiste/Browser-Zurück und die Safari-Viewport-Simulation."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
runs = [["uebergang_kopie_vs_echt.py", "1440", "900"], ["uebergang_kopie_vs_echt.py", "1080", "810"], ["uebergang_kopie_vs_echt.py", "390", "844"],
        ["mausrad_schwelle.py"], ["zurueck_wischen_leiste.py"], ["safari_viewport_sim.py"], ["hochwischen.py"]]
for r in runs:
    print("\n==", " ".join(r))
    out = subprocess.run([sys.executable, os.path.join(here, r[0])] + r[1:], capture_output=True, text=True, timeout=600)
    print((out.stdout + out.stderr).strip()[-2500:])
