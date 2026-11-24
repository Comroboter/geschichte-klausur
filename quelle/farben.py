"""Farbsystem pro Station: jede Station hat genau eine Farbe, in Licht, Zeichnung, Kopf, Mustern und Bausteinen.
Wird von make.py am Ende aufgerufen: ersetzt feste Akzentfarben im CSS durch var(--st) bzw. var(--sd) und hängt die Palette an.
--sd: tiefer Ton (helles Design, Muster in beiden Designs), --sl: heller Ton (dunkles Design), --st: der jeweils passende."""
import re

# Look -> (tief, hell). Jede Look gehört zu genau einer Station.
PAL = {
    'buehne':   ('#6b3fa0', '#b392e6'),  # Start: Violett, Kaiserreich-Vorhang
    'bauplan':  ('#2f6fb2', '#88aee0'),  # Plan: Blaupause
    'lineal':   ('#9a6a1c', '#d9a46e'),  # Handwerk: Holzlineal
    'papier':   ('#3f7a45', '#8fc48a'),  # Einleitung: grünes Heft
    'pyramide': ('#8f3c78', '#df8fc4'),  # Gesellschaft: Magenta
    'zeitraum': ('#2a6f86', '#7cbfd6'),  # Industrie: Stahl
    'split':    ('#2c8078', '#6cc3b8'),  # Zuckerbrot und Peitsche: Petrol
    'epochen':  ('#4a52b4', '#9ea6f2'),  # Moderne: Indigo
    'dialog':   ('#b8503a', '#ee8a78'),  # Kolonien: Rost
    'zwei':     ('#7a7020', '#cdbf62'),  # Kongokonferenz: Oliv
    'akte':     ('#a0405e', '#e88fa6'),  # Quelle: Siegelrot-Rosé
    'stufen':   ('#4f6478', '#a2b3c6'),  # Rassismus: nüchternes Grau-Blau
    'tragik':   ('#c43a2e', '#f06a5c'),  # Urteilen: Rot
    'probe':    ('#8f6a00', '#e6c157'),  # Generalprobe: Bühnengold
    'morgen':   ('#b85a1e', '#f29c62'),  # Kurz vorher: Morgenorange
}

# Feste Akzentfarben aus Gerüst und Looks, die jetzt der Stationsfarbe folgen
HEX = set('c44634 2c8078 aa703c 9a7420 6b3fa0 b7791f 2f6fb2 d24b3e 1f8a7a 3d8a5a 7440cc b8503a 8a55d8 9b6be0 5aa36f 3f6ca0'
          ' b392e6 d9a46e 6cc3b8 88aee0 ee8a78 f0c48a 9fdcd2 f3d27a ffd96b bcd8f5 d9c3ff f6c3ad ffd08a ffe45c c6f164 84d9f0'.split())
RGB = {(196,70,52),(44,128,120),(170,112,60),(107,63,160),(63,108,160),(67,36,112),(220,160,100),(222,120,80),(236,170,130),
       (255,170,90),(255,206,140),(255,226,170),(198,241,100),(132,217,240),(255,228,92)}
VARS = {'plum','ochre','teal','slate','rust'}

def _val(v):
    def rgba(m):
        r,g,b=int(m.group(1)),int(m.group(2)),int(m.group(3)); a=float(m.group(4)) if m.group(4) else 1.0
        if (r,g,b) not in RGB: return m.group(0)
        return 'color-mix(in srgb,var(--sd) %s%%,transparent)' % (round(a*100,1))
    v=re.sub(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)', rgba, v)
    v=re.sub(r'#([0-9a-fA-F]{6})\b', lambda m: 'var(--st)' if m.group(1).lower() in HEX else m.group(0), v)
    v=re.sub(r'var\(--(plum|ochre|teal|slate|rust)\)', 'var(--st)', v)
    v=re.sub(r'var\(--(plum|ochre|teal|slate|rust)-t\)', 'color-mix(in srgb,var(--st) 28%,var(--sheet))', v)
    return v

def _body(body):
    out=[];i=0
    # Deklarationen trennen, ohne in url(...) zu schneiden
    parts=[];depth=0;cur=''
    for ch in body:
        if ch=='(': depth+=1
        elif ch==')': depth-=1
        if ch==';' and depth==0: parts.append(cur); cur=''
        else: cur+=ch
    parts.append(cur)
    for p in parts:
        name=p.split(':',1)[0].strip()
        out.append(p if name.startswith('--') or ':' not in p else _val(p))
    return ';'.join(out)

def apply(css):
    return re.sub(r'\{([^{}]*)\}', lambda m: '{'+_body(m.group(1))+'}', css)

def palette():
    L=['\n/* ===== Farbsystem: eine Farbe pro Station (Licht, Zeichnung, Kopf, Muster, Bausteine) ===== */',
       ':root{--sd:#c43a2e;--sl:#f06a5c;--st:var(--sd)}']
    for look,(d,l) in PAL.items(): L.append('[data-look="%s"]{--sd:%s;--sl:%s}' % (look,d,l))
    L.append('[data-look]{--st:var(--sd);--pen:var(--st);--pen-soft:color-mix(in srgb,var(--st) 14%,transparent);--pen-mid:color-mix(in srgb,var(--st) 28%,transparent);--accent-c:var(--st);'
             '--sh1:var(--st);--sh2:color-mix(in srgb,var(--st) 55%,var(--ink));--sh3:color-mix(in srgb,var(--st) 50%,var(--muted));--sh4:color-mix(in srgb,var(--st) 40%,var(--rule))}')
    L.append('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) [data-look]{--st:var(--sl)}:root:not([data-theme="light"]){--st:var(--sl)}}')
    L.append(':root[data-theme="dark"] [data-look],:root[data-theme="dark"]{--st:var(--sl)}')
    L.append('[data-look] > .hero{--accent:var(--st)!important;--hl:color-mix(in srgb,var(--st) 30%,var(--sheet))!important;--glow:color-mix(in srgb,var(--sd) 14%,transparent)!important}')
    L.append('[data-look] .fill{--accent:var(--st)!important}')
    return '\n'.join(L)+'\n'

def run(T):
    i=0;out='';
    for m in re.finditer(r'(<style[^>]*>)(.*?)(</style>)', T, re.S):
        out+=T[i:m.start()]+m.group(1)+apply(m.group(2))+m.group(3); i=m.end()
    out+=T[i:]
    return out.replace('</style>\n</head>', palette()+'</style>\n</head>',1)
