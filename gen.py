"""
Genera el README del perfil de GitHub y todos sus SVG animados.

Uso:   python gen.py
Crea:  README.md  y  assets/*.svg

Edita solo el bloque CONTENIDO EDITABLE; lo demás es el motor de dibujo.
"""
import math
import os
import random
import json
import re
import urllib.request

OUT = "assets"

# =====================================================================
#  CONTENIDO EDITABLE
# =====================================================================

NAME = "Gonzalo Méndez"
GITHUB_USER = "l-gonzo"

# Puestos que se escriben/borran en el header (en ciclo)
ROLES = ["AI / ML Engineer", "Web Developer"]

# In [1]  Gonzalo.summary()   -> (clave, valor); clave "" = continúa la línea anterior
SUMMARY = [
    ("role", "AI / Machine Learning Engineer · Web Developer"),
    ("degree", "B.Eng. Computer Systems"),
    ("", "M.Sc. Computer Science (in progress)"),
]

# In [2]  Gonzalo.focus_areas()  -> tarjetas animadas.
# El segundo valor elige la animación: "ml", "dl", "cv", "opt", "web"
FOCUS = [
    ("Machine Learning", "ml"),
    ("Deep Learning", "dl"),
    ("Computer Vision", "cv"),
    ("Optimization & Heuristics", "opt"),
    ("Web Development", "web"),
    ("Probability & Statistics", "stats"),
]

# In [3]  Gonzalo.stack()  -> tabla de íconos en el README.
# (grupo, ids de https://skillicons.dev, texto que se muestra)
# Los íconos se descargan una sola vez a assets/icons/ (ver "ICONOS LOCALES").
STACK = [
    ("Machine Learning", ["py", "tensorflow", "pytorch", "sklearn"], "Python · TensorFlow · PyTorch · scikit-learn ·Jupyter"),
    ("Web", ["ts", "js", "react", "nodejs", "css", "html", "php"], "TypeScript · JavaScript · React · Node.js · CSS · HTML · PHP"),
    ("Mobile", ["dart", "flutter"], "Dart · Flutter"),
    ("Databases", ["mongodb", "mysql"], "MongoDB · MySQL"),
    ("Version Control", ["git", "github"], "Git · GitHub"),
    ("Cloud & Containers", ["aws", "docker"], "AWS · Docker"),
    ("Operating Systems", ["linux", "windows"], "Linux · Windows")
]

# In [4]  Gonzalo.contact()  -> badges con enlace en el README.
# (texto, color hex sin #, logo de https://simpleicons.org o "" = sobre de correo, enlace)
# Los badges se generan como SVG locales en assets/badges/ (sin shields.io).
CONTACT = [
    ("LinkedIn", "7aa2f7", "linkedin", "https://www.linkedin.com/in/thegonzo/"),
    ("Email", "73daca", "", "mailto:go.mendez@outlook.com"),
    ("GitHub", "bb9af7", "github", "https://github.com/l-gonzo"),
]

# =====================================================================

# Tokyo Night palette
BG = "#1a1b26"
BG2 = "#16161e"
PANEL = "#1f2335"
BORDER = "#2f334d"
TEXT = "#c0caf5"
MUTED = "#8b93b8"
DIM = "#3b4261"
BLUE = "#7aa2f7"
CYAN = "#7dcfff"
PURPLE = "#bb9af7"
GREEN = "#9ece6a"
ORANGE = "#ff9e64"
RED = "#f7768e"
TEAL = "#73daca"
YELLOW = "#e0af68"

MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 250
    rng = random.Random(3)

    # role typing loop -------------------------------------------------
    roles = ROLES
    FS = 26
    CW = FS * 0.6          # enforced with textLength
    RX, RY = 96, 176       # role text origin
    TYPE, DEL, HOLD, GAP = 0.055, 0.025, 2.6, 0.45

    # timeline of (time, role_index, visible_chars)
    tl, t = [], 0.0
    for i, r in enumerate(roles):
        for k in range(len(r) + 1):
            tl.append((t, i, k)); t += TYPE
        t += HOLD - TYPE
        for k in range(len(r) - 1, -1, -1):
            t += DEL; tl.append((t, i, k))
        t += GAP
    total = t
    key_times = ";".join(f"{x/total:.5f}" for x, _, _ in tl) + ";1"

    def vals(fn):
        v = [fn(i, k) for _, i, k in tl]
        return ";".join(v + [v[-1]])

    s = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Gonzalo Méndez — AI / Machine Learning Engineer · Web Developer">
<title>Gonzalo Méndez — AI / Machine Learning Engineer · Web Developer</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>
  <linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="1"/><stop offset=".55" stop-color="{BG}" stop-opacity=".85"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
  <linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
  <mask id="bm"><rect x="520" width="680" height="{H}" fill="url(#mg)"/></mask>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<style>
  .rise {{ opacity:0; animation: rise .8s cubic-bezier(.2,.7,.2,1) forwards; }}
  .scroll {{ animation: scroll 40s linear infinite; }}
  .flick {{ animation: flick 3s steps(1) infinite; }}
  .cur {{ animation: blink 1s steps(1) infinite; }}
  @keyframes rise {{ from {{ opacity:0; transform: translateY(10px); }} to {{ opacity:1; transform:none; }} }}
  @keyframes scroll {{ to {{ transform: translateY(-{H}px); }} }}
  @keyframes flick {{ 0% {{ fill:{TEAL}; opacity:.9; }} 30% {{ fill:{DIM}; opacity:.6; }} }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .rise {{ animation:none; opacity:1; }} .scroll,.flick {{ animation:none; }} }}
</style>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
''']

    # scrolling binary columns on the right half (content duplicated for seamless loop)
    s.append(f'<g mask="url(#bm)"><g font-family="{MONO}" font-size="13" fill="{DIM}"><g class="scroll">')
    rows = H // 18 + 1
    for c in range(34):
        x = 540 + c * 19
        col = [rng.choice("01") for _ in range(rows)]
        for rep in range(2):
            for r_, ch in enumerate(col):
                y = 14 + r_ * 18 + rep * H
                if rng.random() < 0.035:
                    d = rng.uniform(0, 3)
                    s.append(f'<text class="flick" style="animation-delay:{d:.2f}s" x="{x}" y="{y}">{ch}</text>')
                else:
                    s.append(f'<text x="{x}" y="{y}">{ch}</text>')
    s.append('</g></g></g>')
    s.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{BORDER}"/>')

    # prompt + name
    s.append(f'''<g font-family="{MONO}">
  <text class="rise" style="animation-delay:.1s" x="64" y="70" font-size="16"><tspan fill="{GREEN}">l-gonzo@github</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{BLUE}">~</tspan><tspan fill="{MUTED}">$ whoami</tspan></text>
  <text class="rise" style="animation-delay:.35s" x="62" y="126" font-size="46" font-weight="700" fill="{TEXT}">{esc(NAME)}</text>
  <text class="rise" style="animation-delay:.6s" x="64" y="{RY}" font-size="{FS}" fill="{TEAL}">&gt;</text>
''')
    # typed roles
    for i, r in enumerate(roles):
        steps = vals(lambda j, k, i=i: f"{(k if j == i else 0) * CW:.1f}")
        s.append(f'  <clipPath id="r{i}"><rect x="{RX}" y="{RY-FS}" height="{FS+10}" width="0">'
                 f'<animate attributeName="width" dur="{total:.2f}s" begin="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="{key_times}" values="{steps}"/></rect></clipPath>')
        s.append(f'  <text x="{RX}" y="{RY}" font-size="{FS}" fill="{TEXT}" textLength="{len(r)*CW:.1f}" lengthAdjust="spacing" clip-path="url(#r{i})">{esc(r)}</text>')
    cx = vals(lambda j, k: f"{RX + k * CW + 3:.1f}")
    s.append(f'  <g class="cur"><rect x="{RX+3}" y="{RY-FS+3}" width="{CW*0.62:.1f}" height="{FS+2}" fill="{TEAL}">'
             f'<animate attributeName="x" dur="{total:.2f}s" begin="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="{key_times}" values="{cx}"/></rect></g>')
    s.append('</g>\n</g>\n</svg>\n')
    with open(f"{OUT}/header.svg", "w", encoding="utf-8") as fh:
        fh.write("\n".join(s))


# ---------------------------------------------------------------- notebook cells
CW_W = 1000            # width of every cell image
FS = 16                # code font size
CW = FS * 0.6          # monospace char width (enforced with textLength)
LH = 26                # line height
GX = 128               # x where code / output starts
TYPE = 0.05            # seconds per typed character

BASE_CSS = f"""
  .fade {{ opacity:0; animation: fade .45s ease-out forwards; }}
  .ln   {{ opacity:0; animation: ln .45s ease-out forwards; }}
  .up   {{ opacity:0; animation: up .6s cubic-bezier(.2,.7,.2,1) forwards; }}
  .cur  {{ animation: blink 1s steps(1) infinite; }}
  @keyframes fade {{ to {{ opacity:1; }} }}
  @keyframes ln   {{ from {{ opacity:0; transform: translateX(-6px); }} to {{ opacity:1; transform:none; }} }}
  @keyframes up   {{ from {{ opacity:0; transform: translateY(14px); }} to {{ opacity:1; transform:none; }} }}
  @keyframes blink{{ 50% {{ opacity:0; }} }}
"""
REDUCED = "  @media (prefers-reduced-motion: reduce) { *{ animation:none !important; opacity:1 !important; } }\n"


def highlight(code):
    """very small Python highlighter -> [(text, color)]"""
    out = []
    prev = ""
    for tok in re.findall(r"\s+|[A-Za-z_]\w*|.", code):
        if tok in ("from", "import", "def", "return"):
            c = PURPLE
        elif re.match(r"[A-Za-z_]", tok):
            c = BLUE if prev == "." else TEXT
        elif tok.strip():
            c = CYAN
        else:
            c = TEXT
        out.append((tok, c))
        if tok.strip():
            prev = tok
    return out


class Cell:
    """Builds one notebook cell as an SVG: prompt, typed code, output."""

    def __init__(self, n, code_lines, toolbar=False):
        self.n = n
        self.code = code_lines
        self.toolbar = toolbar
        self.body = []
        self.defs = []
        self.css = ""
        self.y = (44 + 40) if toolbar else 36
        self.t = 0.3

    def input(self):
        y0 = self.y
        n_label = f"In [{self.n}]:"
        box_h = len(self.code) * LH + 14
        b = self.body
        b.append(f'<text class="fade" x="{GX-26}" y="{y0}" text-anchor="end" fill="{BLUE}">{n_label}</text>')
        b.append(f'<rect class="fade" x="{GX-14}" y="{y0-22}" width="{CW_W-GX-10}" height="{box_h}" rx="7" fill="{PANEL}" stroke="{BORDER}"/>')
        b.append(f'<rect class="fade" x="{GX-14}" y="{y0-22}" width="3" height="{box_h}" rx="1.5" fill="{BLUE}"/>')
        t = self.t + 0.2
        for li, line in enumerate(self.code):
            y = y0 + li * LH
            n = len(line)
            steps = ";".join(f"{k*CW:.1f}" for k in range(n + 1))
            cid = f"c{self.n}_{li}"
            self.defs.append(f'<clipPath id="{cid}"><rect x="{GX-2}" y="{y-19}" height="26" width="0">'
                             f'<animate attributeName="width" begin="{t:.2f}s" dur="{n*TYPE:.2f}s" values="{steps}" calcMode="discrete" fill="freeze"/></rect></clipPath>')
            spans = "".join(f'<tspan fill="{c}">{esc(p)}</tspan>' for p, c in highlight(line))
            b.append(f'<text x="{GX}" y="{y}" clip-path="url(#{cid})" xml:space="preserve" textLength="{n*CW:.1f}" lengthAdjust="spacing">{spans}</text>')
            t += n * TYPE + 0.15
        self.t = t + 0.25
        self.y = y0 + box_h + 26

    def out_label(self):
        self.body.append(f'<text class="fade" style="animation-delay:{self.t:.2f}s" x="{GX-26}" y="{self.y}" text-anchor="end" fill="{RED}">Out[{self.n}]:</text>')

    def kv(self, rows):
        self.out_label()
        kw = max(len(k) for k, _ in rows) + 1
        for i, (k, v) in enumerate(rows):
            key = (k.ljust(kw) + ":") if k else " " * (kw + 1)
            self.body.append(f'<text class="ln" style="animation-delay:{self.t + i*0.15:.2f}s" x="{GX}" y="{self.y + i*LH}" xml:space="preserve">'
                             f'<tspan fill="{CYAN}">{esc(key)}</tspan><tspan fill="{TEXT}"> {esc(v)}</tspan></text>')
        self.t += len(rows) * 0.15
        self.y += (len(rows) - 1) * LH + 22

    def repr_line(self, text, note):
        """Out[n]: <Object ...>   # note"""
        self.out_label()
        self.body.append(f'<text class="ln" style="animation-delay:{self.t:.2f}s" x="{GX}" y="{self.y}" xml:space="preserve">'
                         f'<tspan fill="{PURPLE}">{esc(text)}</tspan><tspan fill="{MUTED}">   {esc(note)}</tspan></text>')
        self.y += 22

    def render(self, path, extra_h=0):
        H = self.y + extra_h
        top = ""
        if self.toolbar:
            top = (f'<path d="M.5 44H{CW_W-.5}" stroke="{BORDER}"/>'
                   f'<circle cx="24" cy="22" r="6" fill="{RED}"/><circle cx="44" cy="22" r="6" fill="{YELLOW}"/><circle cx="64" cy="22" r="6" fill="{GREEN}"/>'
                   f'<text x="96" y="27" fill="{TEXT}" font-family="{MONO}" font-size="14">profile.ipynb</text>'
                   f'<text x="{CW_W-24}" y="27" text-anchor="end" fill="{MUTED}" font-family="{MONO}" font-size="13">Python 3 (ipykernel)  <tspan fill="{GREEN}">●</tspan></text>')
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW_W} {H}" width="{CW_W}" height="{H}" role="img" aria-label="Notebook cell {self.n}">
<title>{esc(NAME)} — In [{self.n}]</title>
<defs>{"".join(self.defs)}</defs>
<style>{BASE_CSS}{self.css}{REDUCED}</style>
<rect x=".5" y=".5" width="{CW_W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
{top}
<g font-family="{MONO}" font-size="{FS}">
{chr(10).join(self.body)}
</g>
</svg>
'''
        with open(f"{OUT}/{path}", "w", encoding="utf-8") as fh:
            fh.write(svg)


# ---- cell 1: summary ------------------------------------------------
def cell_summary():
    c = Cell(1, ["from profile import Gonzalo", "Gonzalo.summary()"], toolbar=True)
    c.input()
    c.kv(SUMMARY)
    c.render("cell-1-summary.svg", extra_h=6)


# ---- cell 2: focus areas (animated cards) ---------------------------
def viz_ml(ox, oy, w, h, rng):
    s = []
    def f(u):
        return 0.95 - u + 0.12 * math.sin(u * 5)
    for cls in (0, 1):
        n = 0
        cu, cv = (0.28, 0.3) if cls == 0 else (0.72, 0.7)
        while n < 11:
            u, v = rng.gauss(cu, 0.14), rng.gauss(cv, 0.14)
            if not (0.06 < u < 0.94 and 0.08 < v < 0.92):
                continue
            if (cls == 0) == (v > f(u) - 0.04):
                continue
            x, y = ox + u * w, oy + h - v * h
            d = 1.0 + rng.random() * 0.6
            if cls == 0:
                s.append(f'<circle class="pop" style="animation-delay:{d:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{BLUE}"/>')
            else:
                s.append(f'<polygon class="pop" style="animation-delay:{d:.2f}s" points="{x:.1f},{y-4.5:.1f} {x+4.5:.1f},{y:.1f} {x:.1f},{y+4.5:.1f} {x-4.5:.1f},{y:.1f}" fill="{ORANGE}"/>')
            n += 1
    pts = []
    for i in range(41):
        u = i / 40
        v = f(u)
        if 0 <= v <= 1:
            pts.append(f"{ox + u*w:.1f},{oy + h - v*h:.1f}")
    s.append(f'<path class="loopdraw" pathLength="1" d="M{" L".join(pts)}" fill="none" stroke="{TEXT}" stroke-width="2" stroke-linecap="round"/>')
    return s


def viz_dl(ox, oy, w, h, rng):
    s = []
    layers = [3, 5, 5, 2]
    pos = []
    for li, n in enumerate(layers):
        x = ox + 14 + li * (w - 28) / (len(layers) - 1)
        col = [(x, oy + h / 2 + (i - (n - 1) / 2) * (h / 5.4)) for i in range(n)]
        pos.append(col)
    k = 0
    for li in range(len(layers) - 1):
        for a in pos[li]:
            for b in pos[li + 1]:
                s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{DIM}" stroke-width="1"/>')
                if rng.random() < 0.45:
                    d = li * 0.5 + rng.random() * 0.4
                    s.append(f'<line class="flow" style="animation-delay:{d:.2f}s" pathLength="1" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{TEAL}" stroke-width="1.6" stroke-linecap="round"/>')
                k += 1
    cols = [PURPLE, BLUE, CYAN, TEAL]
    for li, col in enumerate(pos):
        for (x, y) in col:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{BG}" stroke="{cols[li]}" stroke-width="2"/>')
            s.append(f'<circle class="fire" style="animation-delay:{li*0.5:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{cols[li]}"/>')
    return s


def viz_cv(ox, oy, w, h, rng):
    s = []
    cols, rows = 14, 8
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            o = 0.10 + rng.random() * 0.16
            s.append(f'<rect x="{ox + c*cw:.1f}" y="{oy + r*ch:.1f}" width="{cw-1:.1f}" height="{ch-1:.1f}" fill="{BLUE}" fill-opacity="{o:.2f}"/>')
    # two "objects"
    ax, ay = ox + w * 0.28, oy + h * 0.55
    bx, by = ox + w * 0.72, oy + h * 0.45
    s.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{h*0.2:.1f}" fill="{PURPLE}" fill-opacity=".85"/>')
    tri = f"{bx:.1f},{by - h*0.24:.1f} {bx + h*0.24:.1f},{by + h*0.18:.1f} {bx - h*0.24:.1f},{by + h*0.18:.1f}"
    s.append(f'<polygon points="{tri}" fill="{ORANGE}" fill-opacity=".85"/>')
    # scan line
    s.append(f'<rect class="scan" x="{ox}" y="{oy}" width="{w}" height="2" fill="{TEAL}" fill-opacity=".7"/>')
    # detections (alternate)
    for i, (cx, cy, lab, sc) in enumerate([(ax, ay, "obj", "0.97"), (bx, by, "obj", "0.93")]):
        bw, bh = h * 0.56, h * 0.56
        s.append(f'<g class="det{i}"><rect x="{cx-bw/2:.1f}" y="{cy-bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="none" stroke="{GREEN}" stroke-width="2" rx="2"/>'
                 f'<rect x="{cx-bw/2:.1f}" y="{cy-bh/2-14:.1f}" width="{bw:.1f}" height="14" fill="{GREEN}"/>'
                 f'<text x="{cx-bw/2+4:.1f}" y="{cy-bh/2-3:.1f}" fill="{BG}" font-size="10" font-weight="700">{lab} {sc}</text></g>')
    return s


def viz_opt(ox, oy, w, h, rng):
    s = []
    cx, cy = ox + w * 0.64, oy + h * 0.56
    for i, r in enumerate([0.18, 0.34, 0.52, 0.72, 0.95]):
        s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{w*0.46*r:.1f}" ry="{h*0.5*r:.1f}" fill="none" stroke="{PURPLE}" stroke-opacity="{0.75 - i*0.12:.2f}" stroke-width="1.2" transform="rotate(-18 {cx:.1f} {cy:.1f})"/>')
    # zig-zag descent path
    pts = [(ox + w * 0.08, oy + h * 0.12), (ox + w * 0.30, oy + h * 0.62), (ox + w * 0.40, oy + h * 0.22),
           (ox + w * 0.52, oy + h * 0.72), (ox + w * 0.58, oy + h * 0.40), (ox + w * 0.63, oy + h * 0.60), (cx, cy)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s.append(f'<path class="trail" pathLength="1" d="{d}" fill="none" stroke="{YELLOW}" stroke-width="1.6" stroke-dasharray="1" stroke-linejoin="round"/>')
    s.append(f'<circle r="4.5" fill="{YELLOW}"><animateMotion dur="5s" begin="1.2s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.6;1" calcMode="linear" path="{d}"/></circle>')
    s.append(f'<circle class="minpulse" cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="none" stroke="{GREEN}" stroke-width="1.6"/>')
    s.append(f'<text x="{cx+8:.1f}" y="{cy+18:.1f}" fill="{GREEN}" font-size="10">x*</text>')
    return s


def viz_web(ox, oy, w, h, rng):
    """mini browser whose layout builds itself, block by block"""
    s = []
    s.append(f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5" fill="{PANEL}" stroke="{BORDER}"/>')
    s.append(f'<path d="M{ox:.1f} {oy+13:.1f}H{ox+w:.1f}" stroke="{BORDER}"/>')
    for i, col in enumerate([RED, YELLOW, GREEN]):
        s.append(f'<circle cx="{ox + 7 + i*7:.1f}" cy="{oy+6.5:.1f}" r="2.2" fill="{col}"/>')
    s.append(f'<rect x="{ox+30:.1f}" y="{oy+3.5:.1f}" width="{w-38:.1f}" height="6" rx="3" fill="{BG}"/>')
    iy, ix, iw = oy + 19, ox + 6, w - 12
    blocks = [  # (x, y, w, h, color, opacity)
        (ix, iy, iw, 8, BLUE, .9),                                   # navbar
        (ix, iy + 13, iw * 0.62, 22, PURPLE, .75),                   # hero
        (ix + iw * 0.66, iy + 13, iw * 0.34, 22, TEAL, .6),          # hero image
        (ix, iy + 40, iw * 0.31, 20, CYAN, .45),                     # cards
        (ix + iw * 0.345, iy + 40, iw * 0.31, 20, CYAN, .45),
        (ix + iw * 0.69, iy + 40, iw * 0.31, 20, CYAN, .45),
        (ix, iy + 65, iw * 0.8, 4, MUTED, .5),                       # text lines
        (ix, iy + 72, iw * 0.55, 4, MUTED, .5),
    ]
    for i, (x, y, bw, bh, col, op) in enumerate(blocks):
        s.append(f'<rect class="bld" style="animation-delay:{1.0 + i*0.22:.2f}s" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="2" fill="{col}" fill-opacity="{op}"/>')
    s.append(f'<text class="tag" x="{ox + w - 6:.1f}" y="{oy + h - 5:.1f}" text-anchor="end" fill="{ORANGE}" font-size="11" font-weight="700">&lt;/&gt;</text>')
    return s

def viz_stats(ox, oy, w, h, rng):
    """histogram whose bars grow, then a normal curve is drawn over it (mu and ±sigma)"""
    s = []
    bins = 13
    mu, sigma = 0.5, 0.17
    base = oy + h - 8                      # x axis
    top = oy + 10                          # highest point of the curve
    bw = w / bins
    pdf = lambda u: math.exp(-0.5 * ((u - mu) / sigma) ** 2)
    # axis
    s.append(f'<path d="M{ox:.1f} {base:.1f}H{ox + w:.1f}" stroke="{MUTED}" stroke-width="1"/>')
    # bars (empirical histogram = pdf + noise)
    for i in range(bins):
        u = (i + 0.5) / bins
        hh = max(3, (base - top) * pdf(u) * rng.uniform(0.78, 1.08))
        x = ox + i * bw
        d = 1.0 + abs(i - bins // 2) * 0.07   # grows from the center outwards
        s.append(f'<rect class="bar" style="animation-delay:{d:.2f}s" x="{x + 1:.1f}" y="{base - hh:.1f}" width="{bw - 2:.1f}" height="{hh:.1f}" rx="1.5" fill="{BLUE}" fill-opacity=".55"/>')
    # normal curve
    pts = []
    for k in range(61):
        u = k / 60
        pts.append(f"{ox + u * w:.1f},{base - (base - top) * pdf(u):.1f}")
    s.append(f'<path class="gauss" pathLength="1" d="M{" L".join(pts)}" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-linecap="round"/>')
    # mu and ±sigma markers
    mx = ox + mu * w
    s.append(f'<g class="mu"><path d="M{mx:.1f} {top - 4:.1f}V{base:.1f}" stroke="{TEAL}" stroke-width="1.4" stroke-dasharray="3 3"/>'
             f'<text x="{mx + 4:.1f}" y="{top + 4:.1f}" fill="{TEAL}" font-size="11" font-weight="700">μ</text></g>')
    for sgn, lab in ((-1, "-σ"), (1, "+σ")):
        sx = ox + (mu + sgn * sigma) * w
        s.append(f'<g class="mu"><path d="M{sx:.1f} {base - 4:.1f}V{base + 4:.1f}" stroke="{PURPLE}" stroke-width="1.6"/>'
                 f'<text x="{sx:.1f}" y="{base + 13:.1f}" text-anchor="middle" fill="{PURPLE}" font-size="10">{lab}</text></g>')
    return s

VIZ = {"ml": viz_ml, "dl": viz_dl, "cv": viz_cv, "opt": viz_opt, "web": viz_web, "stats": viz_stats}


def cell_focus():
    c = Cell(2, ["Gonzalo.focus_areas()"])
    c.input()
    c.out_label()
    rng = random.Random(11)
    n = len(FOCUS)
    gap = 16 if n <= 4 else 12
    TITLE_FS = 15 if n <= 4 else 13
    x0 = GX - 14
    total_w = CW_W - x0 - 24
    card_w = (total_w - gap * (n - 1)) / n
    card_h = 206
    top = c.y - 16
    for i, (title, kind) in enumerate(FOCUS):
        x = x0 + i * (card_w + gap)
        d = c.t + i * 0.18
        c.body.append(f'<g class="up" style="animation-delay:{d:.2f}s">')
        c.body.append(f'<rect x="{x:.1f}" y="{top}" width="{card_w:.1f}" height="{card_h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>')
        c.body.append(f'<clipPath id="v{i}"><rect x="{x+12:.1f}" y="{top+12}" width="{card_w-24:.1f}" height="112" rx="6"/></clipPath>')
        c.body.append(f'<rect x="{x+12:.1f}" y="{top+12}" width="{card_w-24:.1f}" height="112" rx="6" fill="{BG}"/>')
        c.body.append(f'<g clip-path="url(#v{i})">')
        c.body.extend(VIZ[kind](x + 20, top + 20, card_w - 40, 96, rng))
        c.body.append('</g>')
        c.body.append(f'<text x="{x+14:.1f}" y="{top+146}" fill="{MUTED}" font-size="12">{i+1:02d}</text>')
        # wrap the title to the card width
        max_chars = int((card_w - 26) / (TITLE_FS * 0.62))
        lines, cur = [], ""
        for word in title.split(" "):
            if cur and len(cur) + 1 + len(word) > max_chars:
                lines.append(cur); cur = word
            else:
                cur = f"{cur} {word}".strip()
        lines.append(cur)
        for li, ln in enumerate(lines):
            c.body.append(f'<text x="{x+14:.1f}" y="{top+168 + li*19}" fill="{TEXT}" font-size="{TITLE_FS}" font-weight="700">{esc(ln)}</text>')
        c.body.append('</g>')
    c.css = f"""
  .pop {{ opacity:0; transform-box: fill-box; transform-origin:center; animation: pop .4s cubic-bezier(.3,1.6,.5,1) forwards; }}
  @keyframes pop {{ from {{ opacity:0; transform: scale(0); }} to {{ opacity:1; transform: scale(1); }} }}
  .loopdraw {{ stroke-dasharray:1; stroke-dashoffset:1; animation: loopdraw 6s ease-in-out 1.6s infinite; }}
  @keyframes loopdraw {{ 0% {{ stroke-dashoffset:1; }} 35%,85% {{ stroke-dashoffset:0; opacity:1; }} 100% {{ stroke-dashoffset:0; opacity:0; }} }}
  .flow {{ stroke-dasharray:.18 1; stroke-dashoffset:.18; opacity:0; animation: flow 2s linear infinite; }}
  @keyframes flow {{ 0% {{ stroke-dashoffset:.18; opacity:0; }} 10% {{ opacity:.9; }} 80% {{ opacity:.9; }} 100% {{ stroke-dashoffset:-1; opacity:0; }} }}
  .fire {{ opacity:.25; animation: fire 2s ease-in-out infinite; }}
  @keyframes fire {{ 0%,100% {{ opacity:.25; }} 20% {{ opacity:1; }} 50% {{ opacity:.25; }} }}
  .scan {{ animation: scan 3s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(0); }} to {{ transform: translateY(94px); }} }}
  .det0 {{ opacity:0; animation: det 6s steps(1) 1.5s infinite; }}
  .det1 {{ opacity:0; animation: det 6s steps(1) 4.5s infinite; }}
  @keyframes det {{ 0% {{ opacity:1; }} 45% {{ opacity:0; }} 100% {{ opacity:0; }} }}
  .trail {{ stroke-dasharray:1; stroke-dashoffset:1; animation: trail 5s linear 1.2s infinite; }}
  @keyframes trail {{ 0% {{ stroke-dashoffset:1; opacity:1; }} 60% {{ stroke-dashoffset:0; opacity:1; }} 90% {{ opacity:1; }} 100% {{ stroke-dashoffset:0; opacity:0; }} }}
  .bld {{ opacity:0; transform-box: fill-box; transform-origin: left center; animation: bld 7s ease-out infinite; }}
  @keyframes bld {{ 0% {{ opacity:0; transform: scaleX(0); }} 8% {{ opacity:1; transform: scaleX(1); }} 80% {{ opacity:1; transform: scaleX(1); }} 90%,100% {{ opacity:0; transform: scaleX(1); }} }}
  .tag {{ animation: tag 1.6s ease-in-out infinite; }}
  @keyframes tag {{ 0%,100% {{ opacity:.35; }} 50% {{ opacity:1; }} }}
  .bar {{ transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); animation: bar 7s cubic-bezier(.2,.7,.2,1) infinite; }}
  @keyframes bar {{ 0% {{ transform: scaleY(0); opacity:1; }} 12%,85% {{ transform: scaleY(1); opacity:1; }} 95%,100% {{ transform: scaleY(1); opacity:0; }} }}
  .gauss {{ stroke-dasharray:1; stroke-dashoffset:1; animation: gauss 7s ease-in-out 1.9s infinite; }}
  @keyframes gauss {{ 0% {{ stroke-dashoffset:1; opacity:1; }} 18%,70% {{ stroke-dashoffset:0; opacity:1; }} 80%,100% {{ stroke-dashoffset:0; opacity:0; }} }}
  .mu {{ opacity:0; animation: mu 7s ease-out 3.2s infinite; }}
  @keyframes mu {{ 0% {{ opacity:0; }} 6%,55% {{ opacity:1; }} 65%,100% {{ opacity:0; }} }}
  .minpulse {{ transform-box: fill-box; transform-origin:center; animation: minpulse 2s ease-out infinite; }}
  @keyframes minpulse {{ from {{ transform: scale(.6); opacity:1; }} to {{ transform: scale(2.6); opacity:0; }} }}
"""
    c.y = top + card_h + 22
    c.render("cell-2-focus.svg")


# ---- cells 3 & 4: stack / contact (output rendered natively below) ---
def cell_stack():
    c = Cell(3, ["Gonzalo.stack()"])
    c.input()
    items = sum(len(g[2].split(" · ")) for g in STACK)
    c.repr_line(f"<Stack groups={len(STACK)} tools={items}>", "# rendered below ↓")
    c.render("cell-3-stack.svg", extra_h=4)


def cell_contact():
    c = Cell(4, ["Gonzalo.contact()"])
    c.input()
    c.repr_line(f"<Contact links={len(CONTACT)}>", "# click a badge below ↓")
    c.render("cell-4-contact.svg", extra_h=4)


# ---- footer: empty cell + status bar ---------------------------------
def footer():
    W, H = CW_W, 104
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Empty notebook cell">
<title>{esc(NAME)} — In [ ]</title>
<style>{BASE_CSS}{REDUCED}</style>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
<g font-family="{MONO}" font-size="{FS}">
  <text x="{GX-26}" y="40" text-anchor="end" fill="{BLUE}">In [ ]:</text>
  <rect x="{GX-14}" y="18" width="{W-GX-10}" height="{LH+14}" rx="7" fill="{PANEL}" stroke="{BORDER}"/>
  <rect x="{GX-14}" y="18" width="3" height="{LH+14}" rx="1.5" fill="{GREEN}"/>
  <rect class="cur" x="{GX}" y="25" width="10" height="20" fill="{TEAL}"/>
</g>
<path d="M.5 {H-30}H{W-.5}" stroke="{BORDER}"/>
<g font-family="{MONO}" font-size="12" fill="{MUTED}">
  <text x="20" y="{H-11}"><tspan fill="{GREEN}">●</tspan> Python 3 (ipykernel) | Idle</text>
  <text x="{W/2}" y="{H-11}" text-anchor="middle">Mode: Edit</text>
  <text x="{W-20}" y="{H-11}" text-anchor="end">{esc(GITHUB_USER)} · profile.ipynb</text>
</g>
</svg>
'''
    with open(f"{OUT}/cell-5-footer.svg", "w", encoding="utf-8") as fh:
        fh.write(svg)


# ---------------------------------------------------------------- ICONOS LOCALES
# Los íconos se descargan UNA sola vez (necesita internet solo esa vez) y se
# guardan en assets/icons/. Si el archivo ya existe, no se vuelve a descargar,
# así que después todo funciona sin internet. Para forzar una nueva descarga,
# borra el archivo correspondiente de assets/icons/.
ICON_DIR = f"{OUT}/icons"
BADGE_DIR = f"{OUT}/badges"
SKILL_RAW = "https://raw.githubusercontent.com/tandpfun/skill-icons/main"
SIMPLE_RAW = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons"
_skill_index = None


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-readme-gen"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def _skill_files():
    """id -> file name, read from the skill-icons README table (cached in assets/icons)."""
    global _skill_index
    if _skill_index is not None:
        return _skill_index
    cache = f"{ICON_DIR}/_skill-index.json"
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as fh:
            _skill_index = json.load(fh)
        return _skill_index
    md = _get(f"{SKILL_RAW}/readme.md")
    _skill_index = dict(re.findall(r"\|\s*`([^`]+)`\s*\|.*?/icons/([^)\s#]+\.svg)", md))
    with open(cache, "w", encoding="utf-8") as fh:
        json.dump(_skill_index, fh, indent=1, sort_keys=True)
    return _skill_index


def skill_icon(icon_id):
    """Returns local path of a skill icon, downloading it the first time."""
    path = f"{ICON_DIR}/{icon_id}.svg"
    if os.path.exists(path):
        return path
    try:
        fname = _skill_files().get(icon_id)
        if not fname:
            print(f"  ! '{icon_id}' no existe en skillicons.dev; se omite")
            return None
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(_get(f"{SKILL_RAW}/icons/{fname}"))
        print(f"  ↓ {path}")
        return path
    except Exception as e:  # sin internet, etc.
        print(f"  ! no se pudo descargar '{icon_id}': {e}")
        return None


def simple_icon_path(slug):
    """Returns the SVG path data (24x24) of a simpleicons.org logo, cached locally."""
    path = f"{ICON_DIR}/si-{slug}.svg"
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(_get(f"{SIMPLE_RAW}/{slug}.svg"))
            print(f"  ↓ {path}")
        except Exception as e:
            print(f"  ! no se pudo descargar el logo '{slug}': {e}")
            if os.path.exists(path):
                os.remove(path)
            return None
    with open(path, encoding="utf-8") as fh:
        m = re.search(r'<path[^>]*\sd="([^"]+)"', fh.read())
    return m.group(1) if m else None


SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
# logos that simpleicons.org no longer ships -> drawn as a monogram
MONOGRAM = {"linkedin": "in"}
ENVELOPE = "M2 5.5A1.5 1.5 0 0 1 3.5 4h17A1.5 1.5 0 0 1 22 5.5v13a1.5 1.5 0 0 1-1.5 1.5h-17A1.5 1.5 0 0 1 2 18.5zm2.2.5L12 11.6 19.8 6zM4 8.2V18h16V8.2l-8 5.7z"


def badge(text, color, logo):
    """Draws a local badge SVG (same look as shields 'for-the-badge')."""
    label = text.upper()
    fs, cw = 12, 12 * 0.62
    d = ENVELOPE if not logo else (None if logo in MONOGRAM else simple_icon_path(logo))
    lw = 38
    W, H = int(lw + len(label) * (cw + 1.2) + 16), 30
    if d:
        icon = f'<g transform="translate(13 7) scale(.667)"><path d="{d}" fill="#{color}"/></g>'
    else:  # logo not available -> small monogram box (e.g. "in" for LinkedIn)
        mono = MONOGRAM.get(logo, (logo or text)[:1].upper())
        icon = (f'<rect x="13" y="7" width="16" height="16" rx="3" fill="#{color}"/>'
                f'<text x="21" y="19.5" text-anchor="middle" fill="{BG}" font-family="{SANS}" font-size="11" font-weight="700">{esc(mono)}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(text)}">
<title>{esc(text)}</title>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="{BG}" stroke="#{color}" stroke-opacity=".7"/>
{icon}
<text x="{lw}" y="19.5" fill="#{color}" font-family="{MONO}" font-size="{fs}" font-weight="700" letter-spacing="1.2">{esc(label)}</text>
</svg>
'''
    path = f"{BADGE_DIR}/{re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')}.svg"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return path


# ---------------------------------------------------------------- README
def readme():
    img = lambda f, alt: f'<img src="assets/{f}" width="100%" alt="{esc(alt)}"/>'
    rows = []
    for group, icons, label in STACK:
        imgs = []
        for icon_id in icons:
            p = skill_icon(icon_id)
            if p:
                imgs.append(f'<img src="{p}" height="40" alt="{esc(icon_id)}"/>')
        rows.append(f'''  <tr>
    <td><b>{esc(group)}</b></td>
    <td>{"&nbsp;".join(imgs)}</td>
    <td><sub>{esc(label)}</sub></td>
  </tr>''')
    badges = []
    for text, color, logo, link in CONTACT:
        badges.append(f'  <a href="{link}"><img src="{badge(text, color, logo)}" height="30" alt="{esc(text)}"/></a>')
    summary_alt = "; ".join(f"{k}: {v}" if k else v for k, v in SUMMARY)
    md = f'''<div align="center">
  {img("header.svg", f"{NAME} — " + " · ".join(ROLES))}
</div>

<br/>

{img("cell-1-summary.svg", "In [1]: Gonzalo.summary() — " + summary_alt)}

{img("cell-2-focus.svg", "In [2]: Gonzalo.focus_areas() — " + ", ".join(t for t, _ in FOCUS))}

{img("cell-3-stack.svg", "In [3]: Gonzalo.stack()")}

<div align="center">
<table>
{chr(10).join(rows)}
</table>
</div>

{img("cell-4-contact.svg", "In [4]: Gonzalo.contact()")}

<p align="center">
{chr(10).join(badges)}
</p>

{img("cell-5-footer.svg", "In [ ]:")}
'''
    with open("README.md", "w", encoding="utf-8") as fh:
        fh.write(md)


if __name__ == "__main__":
    for d in (OUT, ICON_DIR, BADGE_DIR):
        os.makedirs(d, exist_ok=True)
    header()
    cell_summary()
    cell_focus()
    cell_stack()
    cell_contact()
    footer()
    readme()
    print("ok — README.md and assets/ generated")
