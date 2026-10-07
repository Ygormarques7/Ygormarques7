"""Gera os SVGs 8-bit do README do perfil. Rodar: python build.py"""
import random
from pathlib import Path

OUT = Path(__file__).parent / "assets"

# ---------- paleta ----------
BG = "#0d0b1e"
PANEL = "#14122b"
WHITE = "#f4f4f4"
YEL = "#feae34"
RED = "#e43b44"
CYAN = "#2ce8f5"
GREEN = "#63c74d"
DGREEN = "#265c42"
BLUE = "#3b5dc9"
DBLUE = "#29366f"
PURPLE = "#b55088"
ORANGE = "#f77622"
GREY = "#8b9bb4"
DGREY = "#3a4466"
MONO = "font-family:'Courier New',Courier,monospace"

# ---------- fonte pixel 5x7 ----------
G = {
    "A": "01110 10001 10001 11111 10001 10001 10001",
    "B": "11110 10001 10001 11110 10001 10001 11110",
    "C": "01110 10001 10000 10000 10000 10001 01110",
    "D": "11110 10001 10001 10001 10001 10001 11110",
    "E": "11111 10000 10000 11110 10000 10000 11111",
    "F": "11111 10000 10000 11110 10000 10000 10000",
    "G": "01110 10001 10000 10111 10001 10001 01111",
    "H": "10001 10001 10001 11111 10001 10001 10001",
    "I": "01110 00100 00100 00100 00100 00100 01110",
    "J": "00111 00010 00010 00010 00010 10010 01100",
    "K": "10001 10010 10100 11000 10100 10010 10001",
    "L": "10000 10000 10000 10000 10000 10000 11111",
    "M": "10001 11011 10101 10101 10001 10001 10001",
    "N": "10001 10001 11001 10101 10011 10001 10001",
    "O": "01110 10001 10001 10001 10001 10001 01110",
    "P": "11110 10001 10001 11110 10000 10000 10000",
    "Q": "01110 10001 10001 10001 10101 10010 01101",
    "R": "11110 10001 10001 11110 10100 10010 10001",
    "S": "01111 10000 10000 01110 00001 00001 11110",
    "T": "11111 00100 00100 00100 00100 00100 00100",
    "U": "10001 10001 10001 10001 10001 10001 01110",
    "V": "10001 10001 10001 10001 10001 01010 00100",
    "W": "10001 10001 10001 10101 10101 10101 01010",
    "X": "10001 10001 01010 00100 01010 10001 10001",
    "Y": "10001 10001 01010 00100 00100 00100 00100",
    "Z": "11111 00001 00010 00100 01000 10000 11111",
    "0": "01110 10001 10011 10101 11001 10001 01110",
    "1": "00100 01100 00100 00100 00100 00100 01110",
    "2": "01110 10001 00001 00010 00100 01000 11111",
    "3": "11111 00010 00100 00010 00001 10001 01110",
    "4": "00010 00110 01010 10010 11111 00010 00010",
    "5": "11111 10000 11110 00001 00001 10001 01110",
    "6": "00110 01000 10000 11110 10001 10001 01110",
    "7": "11111 00001 00010 00100 01000 01000 01000",
    "8": "01110 10001 10001 01110 10001 10001 01110",
    "9": "01110 10001 10001 01111 00001 00010 01100",
    " ": "00000 00000 00000 00000 00000 00000 00000",
    ".": "00000 00000 00000 00000 00000 01100 01100",
    ",": "00000 00000 00000 00000 01100 00100 01000",
    ":": "00000 01100 01100 00000 01100 01100 00000",
    "-": "00000 00000 00000 11111 00000 00000 00000",
    "!": "00100 00100 00100 00100 00100 00000 00100",
    "?": "01110 10001 00001 00010 00100 00000 00100",
    "/": "00001 00001 00010 00100 01000 10000 10000",
    "&": "01100 10010 10100 01000 10101 10010 01101",
    ">": "01000 00100 00010 00001 00010 00100 01000",
    "<": "00010 00100 01000 10000 01000 00100 00010",
    "#": "01010 01010 11111 01010 11111 01010 01010",
    "+": "00000 00100 00100 11111 00100 00100 00000",
    "'": "00100 00100 01000 00000 00000 00000 00000",
    "*": "00000 00000 00000 00100 00000 00000 00000",
    "(": "00010 00100 01000 01000 01000 00100 00010",
    ")": "01000 00100 00010 00010 00010 00100 01000",
    "{": "00110 00100 00100 01000 00100 00100 00110",
    "}": "01100 00100 00100 00010 00100 00100 01100",
    "@": "01110 10001 10111 10101 10111 10000 01111",
    "=": "00000 00000 11111 00000 11111 00000 00000",
    "^": "00100 01010 10001 00000 00000 00000 00000",
    "~": "00000 00000 01000 10101 00010 00000 00000",
    "$": "00100 01111 10100 01110 00101 11110 00100",
    "%": "11001 11010 00010 00100 01000 01011 10011",
}
G = {k: v.split() for k, v in G.items()}
ACCENTS = str.maketrans("ÁÀÃÂÉÊÍÓÔÕÚÇ", "AAAAEEIOOOUC")


def text_w(s, sc):
    return len(s) * 6 * sc - sc


def ptext(s, x, y, sc, fill, cls="", extra=""):
    """Texto em fonte pixel: um <path> com as linhas de pixels agrupadas."""
    d = []
    for i, ch in enumerate(s.upper().translate(ACCENTS)):
        rows = G.get(ch, G["?"])
        ox = x + i * 6 * sc
        for r, row in enumerate(rows):
            c = 0
            while c < 5:
                if row[c] == "1":
                    start = c
                    while c < 5 and row[c] == "1":
                        c += 1
                    d.append(f"M{ox + start * sc} {y + r * sc}h{(c - start) * sc}v{sc}h-{(c - start) * sc}z")
                else:
                    c += 1
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} fill="{fill}" {extra} d="{"".join(d)}"/>'


def ptext_c(s, cx, y, sc, fill, cls="", shadow=None):
    x = cx - text_w(s, sc) // 2
    out = ""
    if shadow:
        out += ptext(s, x + sc, y + sc, sc, shadow, cls)
    return out + ptext(s, x, y, sc, fill, cls)


# ---------- sprites ----------
PAL = {
    "k": "#1a1c2c", "h": "#3e2731", "s": "#f5cfa8", "S": "#d9967a", "e": "#1a1c2c",
    "w": WHITE, "b": BLUE, "B": DBLUE, "p": "#262b44", "d": "#5a6988", "y": YEL,
    "r": RED, "g": "#566c86", "o": ORANGE, "c": CYAN, "G": GREEN, "l": "#c0cbdc",
}

HERO = [
    "...kkkkkk...",
    "..khhhhhhk..",
    ".khhhhhhhhk.",
    ".khhhhhhhhk.",
    ".khsssssshk.",
    ".kssesssesk.",
    ".kssssssssk.",
    "..kssSSssk..",
    "...kkssk....",
    "..kbbwwbbk..",
    ".kbbbwwbbbk.",
    ".kbbbbbbbbk.",
    "ksbbbbbbbbsk",
    ".kkppppppkk.",
    "..kppk.kppk.",
    "..kddk.kddk.",
]

# Galo: mascote pixel preto e branco
GALO = [
    "........rr..",
    ".......rrr..",
    ".......gwwg.",
    "......gwwekyy",
    "......gwwwgr.",
    "g.....gwwwg..",
    "gg...gwkwkg..",
    "gwg.gwkwkwkg.",
    ".gwgwkwkwkg..",
    "..gwkwkwkg...",
    "....y..y.....",
    "...yy..yy....",
]

BLOCK = [
    "kkkkkkkkkkkk",
    "kyyyyyyyyyyk",
    "kyoyyyyyyoyk",
    "kyyyykkkyyyk",
    "kyyykyyykyyk",
    "kyyyyyyykyyk",
    "kyyyyyykyyyk",
    "kyyyyykyyyyk",
    "kyyyyyyyyyyk",
    "kyoyyykyyoyk",
    "kyyyyyyyyyyk",
    "kkkkkkkkkkkk",
]

HEART = [
    ".rr.rr.",
    "rwrrrrr",
    "rrrrrrr",
    ".rrrrr.",
    "..rrr..",
    "...r...",
]


def sprite(rows, x, y, sc, extra=""):
    by = {}
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            start = c
            while c < len(row) and row[c] == ch:
                c += 1
            by.setdefault(PAL[ch], []).append(
                f"M{x + start * sc} {y + r * sc}h{(c - start) * sc}v{sc}h-{(c - start) * sc}z")
    paths = "".join(f'<path fill="{col}" d="{"".join(d)}"/>' for col, d in by.items())
    return f"<g {extra}>{paths}</g>" if extra else paths


# ---------- peças comuns ----------
def svg(w, h, body, style="", title=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">{t}<style>{style}</style>{body}</svg>')


def stars(w, h, n, seed, top=0):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.randrange(0, w, 4), rnd.randrange(top, h, 4)
        s = rnd.choice([2, 2, 2, 4])
        col = rnd.choice([WHITE, WHITE, CYAN, YEL, GREY])
        out.append(f'<rect class="tw" style="animation-delay:-{rnd.random() * 3:.2f}s" '
                   f'x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}"/>')
    return "".join(out)


TWINKLE = ".tw{animation:tw 3s steps(2,end) infinite}@keyframes tw{50%{opacity:.15}}"
BLINK = ".bl{animation:bl 1.2s steps(1,end) infinite}@keyframes bl{50%{opacity:0}}"


def ground(w, y, h):
    """Faixa de grama + tijolos."""
    out = [f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="#5d2c28"/>',
           f'<rect x="0" y="{y}" width="{w}" height="8" fill="{GREEN}"/>',
           f'<rect x="0" y="{y + 8}" width="{w}" height="4" fill="{DGREEN}"/>']
    tile = 24
    for row, ty in enumerate(range(y + 12, y + h, tile // 2)):
        off = (tile // 2) if row % 2 else 0
        out.append(f'<rect x="0" y="{ty}" width="{w}" height="2" fill="#3b1a1a"/>')
        for tx in range(-off, w, tile):
            out.append(f'<rect x="{tx}" y="{ty}" width="2" height="{tile // 2}" fill="#3b1a1a"/>')
            out.append(f'<rect x="{tx + 2}" y="{ty + 2}" width="{tile - 6}" height="2" fill="#8a4836"/>')
    return "".join(out)


def window(x, y, w, h, title=None, tcol=YEL):
    """Janela estilo RPG: borda dupla com cantos em degrau."""
    o = [f'<rect x="{x + 4}" y="{y}" width="{w - 8}" height="{h}" fill="{WHITE}"/>',
         f'<rect x="{x}" y="{y + 4}" width="{w}" height="{h - 8}" fill="{WHITE}"/>',
         f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" fill="{PANEL}"/>',
         f'<rect x="{x + 10}" y="{y + 10}" width="{w - 20}" height="{h - 20}" fill="none" '
         f'stroke="{DBLUE}" stroke-width="2"/>']
    if title:
        tw = text_w(title, 2) + 28
        o.append(f'<rect x="{x + 28}" y="{y - 10}" width="{tw}" height="24" fill="{PANEL}"/>')
        o.append(f'<rect x="{x + 28}" y="{y - 10}" width="{tw}" height="24" fill="none" '
                 f'stroke="{WHITE}" stroke-width="4"/>')
        o.append(ptext(title, x + 42, y - 5, 2, tcol))
    return "".join(o)


def bar(x, y, segs, filled, col, sz=12, gap=3):
    o = []
    for i in range(segs):
        c = col if i < filled else DGREY
        o.append(f'<rect x="{x + i * (sz + gap)}" y="{y}" width="{sz}" height="{sz}" fill="{c}"/>')
    return "".join(o)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- 1. header ----------
def header():
    W, H = 1000, 320
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', stars(W, 250, 70, 7)]
    # lua
    b.append(sprite(["..llll..", ".llllll.", "lllllwl.", "llllll..", "lllll...", "llllll..",
                     ".llllll.", "..llll.."], 880, 60, 5))
    # HUD
    b.append(ptext("1P", 30, 20, 2, RED) + ptext("YGOR", 30, 40, 2, WHITE))
    b.append(ptext_c("RECORDE", 500, 20, 2, RED) + ptext_c("0002026", 500, 40, 2, WHITE))
    b.append(ptext("FASE", 970 - text_w("FASE", 2), 20, 2, RED)
             + ptext("8-8", 970 - text_w("8-8", 2), 40, 2, WHITE))
    # título
    b.append(ptext_c("YGOR MARQUES", 500, 92, 7, YEL, shadow=RED))
    b.append(ptext_c("IMPLEMENTAÇÃO & AUTOMAÇÃO DE CRM * GOHIGHLEVEL", 500, 160, 2, CYAN))
    b.append(ptext_c("APERTE START", 500, 196, 3, WHITE, cls="bl"))
    # chão + personagens
    b.append(ground(W, 268, 52))
    b.append(sprite(BLOCK, 120, 120, 4, 'class="bump"'))
    b.append(sprite(HERO, 126, 204, 4, 'class="bob"'))
    b.append(sprite(GALO, 0, 232, 3, 'class="walk"'))
    st = (TWINKLE + BLINK +
          ".bob{animation:bob 1s steps(2,end) infinite}@keyframes bob{50%{transform:translateY(-4px)}}"
          ".bump{animation:bump 2.4s steps(1,end) infinite}@keyframes bump{0%,90%{transform:none}95%{transform:translateY(-8px)}}"
          ".walk{animation:walk 14s steps(140,end) infinite}"
          "@keyframes walk{from{transform:translateX(260px)}to{transform:translateX(1000px)}}")
    return svg(W, H, "".join(b), st, "Ygor Marques - Implementação & Automação de CRM")


# ---------- 2. botões ----------
def button(label, col):
    w = text_w(label, 2) + 70
    h = 52
    b = [f'<rect x="6" y="6" width="{w - 6}" height="{h - 6}" fill="#000"/>',  # sombra
         f'<rect x="4" y="0" width="{w - 14}" height="{h - 6}" fill="{WHITE}"/>',
         f'<rect x="0" y="4" width="{w - 6}" height="{h - 14}" fill="{WHITE}"/>',
         f'<rect x="4" y="4" width="{w - 14}" height="{h - 14}" fill="{col}"/>',
         f'<rect x="4" y="{h - 16}" width="{w - 14}" height="6" fill="#000" opacity=".25"/>',
         ptext(">", 18, 16, 2, WHITE, cls="bl"),
         ptext(label, 40, 16, 2, WHITE)]
    return svg(w, h, "".join(b), BLINK, label)


# ---------- 3. diálogo ----------
def dialog():
    W, H = 1000, 190
    lines = [
        "Oi! Eu sou o Ygor. Implemento e automatizo CRMs no GoHighLevel:",
        "pipelines, workflows, Conversation AI, Voice AI, WhatsApp e",
        "integrações via API para clientes reais. Também estou na reta",
        "final de Ciência da Computação na Univértix.",
    ]
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "JOGADOR 1")]
    b.append(sprite(HERO, 40, 60, 5))
    for i, ln in enumerate(lines):
        y = 66 + i * 28
        # largura base 860 = texto visível mesmo se o navegador não rodar a animação
        t0, t1 = (0.3 + i * 1.6) / 7, (1.9 + i * 1.6) / 7
        b.append(f'<clipPath id="c{i}"><rect x="120" y="{y - 20}" height="28" width="860">'
                 f'<animate attributeName="width" values="0;0;860" keyTimes="0;{t0:.3f};{t1:.3f}" '
                 f'dur="7s" begin="0s" fill="freeze"/></rect></clipPath>')
        b.append(f'<text x="124" y="{y}" clip-path="url(#c{i})" fill="{WHITE}" '
                 f'style="{MONO};font-size:19px;font-weight:bold">{esc(ln)}</text>')
    b.append(f'<g class="bl">{ptext("V", 940, 150, 2, YEL)}</g>')
    return svg(W, H, "".join(b), BLINK, "Intro")


# ---------- 4. status ----------
def status():
    W, H = 1000, 330
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "STATUS")]
    # retrato
    b.append(f'<rect x="40" y="50" width="170" height="240" fill="{DBLUE}"/>')
    b.append(f'<rect x="40" y="50" width="170" height="240" fill="none" stroke="{WHITE}" stroke-width="4"/>')
    b.append(sprite(HERO, 65, 70, 10, 'class="bob"'))
    b.append(ptext_c("LV 08", 125, 262, 2, YEL))
    rows = [
        ("NOME", "Ygor Marques"),
        ("CLASSE", "CRM & Automação"),
        ("GUILDA", "AVA Partners  (GoHighLevel)"),
        ("FACUL", "Univértix - Computação"),
        ("FASE", "8º período de 8"),
        ("BASE", "Minas Gerais, Brasil"),
        ("ALIADO", "Galo  (Atlético-MG)"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 70 + i * 26
        b.append(ptext(k, 240, y - 13, 2, YEL))
        b.append(ptext("." * (7 - len(k) + 2), 240 + text_w(k, 2) + 8, y - 13, 2, DGREY))
        b.append(f'<text x="370" y="{y}" fill="{WHITE}" style="{MONO};font-size:18px;font-weight:bold">'
                 f'{esc(v)}</text>')
    b.append(sprite(GALO, 600, 210, 3))
    # barras
    bars = [("HP", "CAFÉ", 13, 16, RED), ("MP", "FOCO", 11, 16, BLUE), ("XP", "DIPLOMA", 15, 16, GREEN)]
    for i, (k, lab, f, n, col) in enumerate(bars):
        y = 66 + i * 44
        x = 700
        b.append(ptext(k, x, y, 2, col) + ptext(lab, x + 34, y, 2, GREY))
        b.append(bar(x, y + 20, n, f, col, 12, 3))
    b.append(f'<g class="bl">{ptext("+1 COMMIT", 720, 262, 2, YEL)}</g>')
    st = BLINK + ".bob{animation:bob 1s steps(2,end) infinite}@keyframes bob{50%{transform:translateY(-6px)}}"
    return svg(W, H, "".join(b), st, "Status")


# ---------- 5. quest log ----------
QUESTS = [
    ("PRINCIPAL", RED, "IMPLEMENTAÇÕES GOHIGHLEVEL",
     "CRMs para clientes reais: pipelines, workflows, formulários, calendários.", "ATIVA", GREEN),
    ("PRINCIPAL", RED, "AGENTES DE IA",
     "Conversation AI e Voice AI que atendem, qualificam e agendam.", "ATIVA", GREEN),
    ("EXTRA", BLUE, "INTEGRAÇÕES",
     "WhatsApp, webhooks e APIs conectando o CRM ao resto da operação.", "LVL UP", YEL),
]


def quests():
    W = 1000
    H = 60 + len(QUESTS) * 74 + 20
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "MISSÕES")]
    for i, (tag, tcol, title, desc, stt, scol) in enumerate(QUESTS):
        y = 50 + i * 74
        if i:
            b.append(f'<rect x="40" y="{y - 10}" width="{W - 80}" height="2" fill="{DGREY}"/>')
        b.append(f'<rect x="40" y="{y + 4}" width="124" height="26" fill="{tcol}"/>')
        b.append(ptext_c(tag, 102, y + 10, 2, WHITE))
        b.append(ptext("!", 180, y + 10, 2, YEL, cls="bl"))
        b.append(ptext(title, 202, y + 10, 2, WHITE))
        b.append(f'<text x="202" y="{y + 52}" fill="{GREY}" style="{MONO};font-size:16px;font-weight:bold">'
                 f'{esc(desc)}</text>')
        b.append(ptext(stt, W - 44 - text_w(stt, 2), y + 10, 2, scol))
    return svg(W, H, "".join(b), BLINK, "Missões")


# ---------- 6. inventário ----------
ITEMS = [
    ("JS", "JavaScript", "#f7df1e"), ("RCT", "React", "#61dafb"), ("RN", "React Native", "#61dafb"),
    ("JAV", "Java", ORANGE), ("PY", "Python", "#4b8bbe"), ("</>", "HTML", "#e34f26"),
    ("{}", "CSS", "#2965f1"), ("GIT", "Git & GitHub", "#f05032"), ("AWS", "AWS", "#ff9900"),
    ("GHL", "GoHighLevel", CYAN), ("API", "APIs & Webhooks", GREEN), ("IA", "Claude & IA", "#d97757"),
]


def inventory():
    W, cols = 1000, 6
    rows = (len(ITEMS) + cols - 1) // cols
    sw, sh, gap = 142, 118, 12
    gx = (W - (cols * sw + (cols - 1) * gap)) // 2
    H = 60 + rows * (sh + gap) + 22
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "INVENTÁRIO")]
    for i, (ab, name, col) in enumerate(ITEMS):
        x = gx + (i % cols) * (sw + gap)
        y = 48 + (i // cols) * (sh + gap)
        b.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" fill="{BG}"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" fill="none" stroke="{DGREY}" stroke-width="4"/>')
        b.append(f'<rect x="{x + 4}" y="{y + 4}" width="{sw - 8}" height="4" fill="{DBLUE}"/>')
        b.append(ptext_c(ab, x + sw // 2, y + 26, 5, col))
        b.append(f'<text x="{x + sw // 2}" y="{y + sh - 16}" text-anchor="middle" fill="{WHITE}" '
                 f'style="{MONO};font-size:15px;font-weight:bold">{esc(name)}</text>')
    # cursor piscando no primeiro slot
    b.append(f'<rect class="bl" x="{gx - 2}" y="46" width="{sw + 4}" height="{sh + 4}" fill="none" '
             f'stroke="{YEL}" stroke-width="4"/>')
    return svg(W, H, "".join(b), BLINK, "Inventário - tecnologias")


# ---------- 7. rodapé ----------
def footer():
    W, H = 1000, 230
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', stars(W, 170, 40, 11)]
    b.append(ptext_c("OBRIGADO POR JOGAR!", 500, 34, 4, YEL, shadow=RED))
    b.append(ptext_c("CONTINUAR?", 470, 92, 3, WHITE))
    cx = 470 + text_w("CONTINUAR?", 3) // 2 + 30
    for k in range(10):
        d = 9 - k
        delay = 0 if k == 0 else -(10 - k)
        b.append(f'<g class="cd" style="animation-delay:{delay}s">{ptext(str(d), cx, 92, 3, YEL)}</g>')
    b.append(ptext_c("INSIRA UMA FICHA", 500, 136, 2, CYAN, cls="bl"))
    b.append(ground(W, 200, 30))
    b.append(sprite(HERO, 430, 152, 3, 'class="bob"'))
    for i in range(3):
        b.append(sprite(HEART, 30 + i * 30, 30, 3))
    b.append(sprite(GALO, 530, 164, 3))
    st = (TWINKLE + BLINK +
          ".cd{opacity:0;animation:cd 10s steps(1,end) infinite}@keyframes cd{0%{opacity:1}10%,100%{opacity:0}}"
          ".bob{animation:bob 1s steps(2,end) infinite}@keyframes bob{50%{transform:translateY(-4px)}}")
    return svg(W, H, "".join(b), st, "Thanks for playing")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "btn-email.svg": button("EMAIL", RED),
        "btn-repos.svg": button("REPOSITÓRIOS", BLUE),
        "btn-linkedin.svg": button("LINKEDIN", "#0a66c2"),
        "dialog.svg": dialog(),
        "status.svg": status(),
        "quests.svg": quests(),
        "inventory.svg": inventory(),
        "footer.svg": footer(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content) // 1024} KB")
