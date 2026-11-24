"""Gemeinsame Pfade für alle Tests. Vorher bauen: python3 ../build.py"""
import os, sys
Q = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))          # quelle/
URL = 'file://' + os.path.join(Q, 'dist', 'kaiserreich.html')              # Einzeldatei-Build
SITE = 'file://' + os.path.join(Q, 'dist', 'website', 'index.html')          # Website-Build
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')       # Screenshots, Videos
os.makedirs(OUT, exist_ok=True)
# Neon-Start nur einmal pro Sitzung: in Tests überspringen, außer ein Test will ihn sehen
SKIP_INTRO = "try{sessionStorage.setItem('vh','1')}catch(e){}"
