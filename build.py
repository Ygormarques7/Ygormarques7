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


# Galo grande do título: corpo + dois quadros de pernas (caminhada)
GALO_CORPO = [
    "...............r.r....",
    "..............rrrrr...",
    "..gg..........rrrrr...",
    ".gkkg........lwwwwwl..",
    "gkwkkg......lwwwwkwl..",
    "gkkwkkg.....lwwwwwwyyy",
    ".gkkwkkg....lwwwwwwyy.",
    "..gkkwkkg...lwwwwwrl..",
    "...gkkkkg..lwkwwwwrr..",
    "....gkkkkggwkwkwwwl...",
    "....gkkkkkkkkwkwkwg...",
    "...gkkkkkkkkkkwkwkg...",
    "...gkkkwwwwwwkkkkkg...",
    "...gkkkkwwwwwwkkkg....",
    "....gkkkkkkkkkkkg.....",
    ".....gggkkkkkggg......",
]
GALO_PERNAS = [
    ["........o...o.........",
     "........o...o.........",
     ".......oo..oo.........",
     "......ooo.ooo........."],
    [".........o.o..........",
     "........o...o.........",
     ".......o.....o........",
     "......oo.....oo......."],
]


def png(nome, x, y):
    """Embute um PNG de assets/ no SVG (SVG em <img> não carrega arquivo externo)."""
    import base64
    from PIL import Image
    p = Path(__file__).parent / "assets" / nome
    w, h = Image.open(p).size
    data = base64.b64encode(p.read_bytes()).decode()
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h}" style="image-rendering:pixelated" '
            f'href="data:image/png;base64,{data}"/>'), w, h


def escudo(x, y, h):
    """Escudo do Atlético (PNG enviado pelo Ygor), redimensionado para a altura h."""
    img, w0, h0 = png("escudo-cam.png", x, y)
    w = round(h * w0 / h0)
    return img.replace(f'width="{w0}" height="{h0}"', f'width="{w}" height="{h}"')


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


def stars(w, h, n, seed, top=0, calm=False):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.randrange(0, w, 4), rnd.randrange(top, h, 4)
        s = rnd.choice([2, 2, 2, 4])
        col = rnd.choice([GREY, DGREY, WHITE] if calm else [WHITE, WHITE, CYAN, YEL, GREY])
        out.append(f'<rect class="tw" style="animation-delay:-{rnd.random() * 3:.2f}s" '
                   f'x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}"/>')
    return "".join(out)


TWINKLE = ".tw{animation:tw 3s steps(2,end) infinite}@keyframes tw{50%{opacity:.15}}"
BLINK = ".bl{animation:bl 1.2s steps(1,end) infinite}@keyframes bl{50%{opacity:0}}"


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


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- 1. header ----------
def floor(w, y, h):
    """Piso discreto em azul-ardósia (substitui a grama/tijolo)."""
    out = [f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="#151a33"/>',
           f'<rect x="0" y="{y}" width="{w}" height="4" fill="{BLUE}"/>',
           f'<rect x="0" y="{y + 4}" width="{w}" height="2" fill="{DBLUE}"/>']
    for ty in range(y + 6, y + h, 16):
        out.append(f'<rect x="0" y="{ty + 14}" width="{w}" height="2" fill="#0f1226"/>')
        off = 16 if (ty - y) // 16 % 2 else 0
        for tx in range(-off, w, 32):
            out.append(f'<rect x="{tx}" y="{ty}" width="2" height="16" fill="#0f1226"/>')
    return "".join(out)


def header():
    W, H = 1000, 320
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', stars(W, 230, 40, 7, calm=True)]
    b.append(ptext("YGORMARQUES7", 30, 24, 2, GREY))
    b.append(ptext("MINAS GERAIS * BR", 970 - text_w("MINAS GERAIS * BR", 2), 24, 2, GREY))
    b.append(ptext_c("YGOR MARQUES", 500, 66, 7, WHITE, shadow=BLUE))
    b.append(f'<rect x="{500 - 60}" y="134" width="120" height="4" fill="{CYAN}"/>')
    b.append(ptext_c("IMPLEMENTAÇÃO & AUTOMAÇÃO DE CRM", 500, 152, 2, CYAN))
    b.append(ptext_c("GOHIGHLEVEL * AGENTES DE IA * INTEGRAÇÕES", 500, 176, 2, GREY))
    chao = 284
    b.append(floor(W, chao, 36))
    sc = 3
    alt = (len(GALO_CORPO) + 4) * sc
    quadros = "".join(f'<g class="q{i}">{sprite(GALO_CORPO + pernas, 0, chao - alt, sc)}</g>'
                      for i, pernas in enumerate(GALO_PERNAS))
    tro, x = [], 22 * sc + 40
    for i in range(4):
        img, w, h = png(f"trofeu-{i + 1}.png", x, 0)
        img = img.replace(' y="0"', f' y="{chao - h}"')
        tro.append(f'<g class="hop" style="animation-delay:-{i * .3:.1f}s">{img}</g>')
        x += w + 26
    b.append(f'<g class="walk">{quadros}{"".join(tro)}</g>')
    st = (TWINKLE +
          ".walk{animation:walk 26s steps(260,end) infinite}"
          f"@keyframes walk{{from{{transform:translateX(-{x + 20}px)}}to{{transform:translateX(1000px)}}}}"
          ".q0{animation:q0 .5s steps(1,end) infinite}@keyframes q0{50%{opacity:0}}"
          ".q1{opacity:0;animation:q1 .5s steps(1,end) infinite}@keyframes q1{50%{opacity:1}}"
          ".hop{animation:hop .8s steps(4,end) infinite}"
          "@keyframes hop{0%,100%{transform:none}50%{transform:translateY(-8px)}}")
    return svg(W, H, "".join(b), st, "Ygor Marques - Implementação & Automação de CRM")


# ---------- 2. botões ----------
ICONES = {
    "linkedin": [  # símbolo "in" do LinkedIn em pixel
        ".wwwwwwwwww.",
        "wwwwwwwwwwww",
        "wLLwwwwwwwww",
        "wLLwwwwwwwww",
        "wwwwwwwwwwww",
        "wLLwLLLLLLww",
        "wLLwLLwwLLww",
        "wLLwLLwwLLww",
        "wLLwLLwwLLww",
        "wLLwLLwwLLww",
        "wwwwwwwwwwww",
        ".wwwwwwwwww.",
    ],
    "email": [  # envelope
        "wwwwwwwwwwww",
        "wkwwwwwwwwkw",
        "wwkwwwwwwkww",
        "wwwkwwwwkwww",
        "wwwwkwwkwwww",
        "wwwwwkkwwwww",
        "wwwwwwwwwwww",
        "wwwwwwwwwwww",
        "wwwwwwwwwwww",
    ],
    "repos": [  # pasta
        "oooo........",
        "oooooooooooo",
        "oooooooooooo",
        "yyyyyyyyyyyy",
        "yyyyyyyyyyyy",
        "yyyyyyyyyyyy",
        "yyyyyyyyyyyy",
        "yyyyyyyyyyyy",
        "yyyyyyyyyyyy",
    ],
}
PAL["L"] = "#0a66c2"


def button(label, col, icone):
    w = text_w(label, 2) + 86
    h = 52
    ic = ICONES[icone]
    b = [f'<rect x="6" y="6" width="{w - 6}" height="{h - 6}" fill="#000"/>',  # sombra
         f'<rect x="4" y="0" width="{w - 14}" height="{h - 6}" fill="{WHITE}"/>',
         f'<rect x="0" y="4" width="{w - 6}" height="{h - 14}" fill="{WHITE}"/>',
         f'<rect x="4" y="4" width="{w - 14}" height="{h - 14}" fill="{col}"/>',
         f'<rect x="4" y="{h - 16}" width="{w - 14}" height="6" fill="#000" opacity=".25"/>',
         sprite(ic, 16, 23 - len(ic), 2),
         ptext(label, 52, 16, 2, WHITE)]
    return svg(w, h, "".join(b), "", label)


# ---------- 3. sobre ----------
# código do "Sobre": cada linha é uma lista de (texto, cor)
KW, CLS, STR, COM, PUN = "#e06c9f", YEL, GREEN, GREY, WHITE
CODIGO = [
    [("# sobre.py: quem sou eu", COM)],
    [("class ", KW), ("Ygor", CLS), ("(", PUN), ("Dev", CYAN), ("):", PUN)],
    [("    cargo   = ", PUN), ('"Implementação & Automação de CRM"', STR)],
    [("    empresa = ", PUN), ('"AVA Partners"', STR)],
    [],
    [("    def ", KW), ("trabalho", CYAN), ("(", PUN), ("self", ORANGE), ("):", PUN)],
    [("        return ", KW), ("[", PUN), ('"GoHighLevel"', STR), (", ", PUN), ('"pipelines"', STR),
     (", ", PUN), ('"workflows"', STR), (",", PUN)],
    [("                ", PUN), ('"agentes de IA"', STR), (", ", PUN), ('"Conversation AI"', STR),
     (", ", PUN), ('"Voice AI"', STR), (",", PUN)],
    [("                ", PUN), ('"WhatsApp"', STR), (", ", PUN), ('"integrações via API"', STR), ("]", PUN)],
    [],
    [("    def ", KW), ("formacao", CYAN), ("(", PUN), ("self", ORANGE), ("):", PUN)],
    [("        return ", KW), ('"Ciência da Computação @ Univértix · 8º período"', STR)],
]


def dialog():
    W = 1000
    LH, FS, CW = 24, 16, 9.6  # altura da linha, fonte, largura de um caractere (monospace 0,6em)
    top = 96
    H = top + len(CODIGO) * LH + 66
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "SOBRE")]
    # barra de abas do editor
    b.append(f'<rect x="22" y="32" width="{W - 44}" height="36" fill="#151a33"/>')
    b.append(f'<rect x="22" y="32" width="170" height="36" fill="{PANEL}"/>')
    b.append(f'<rect x="22" y="32" width="170" height="4" fill="{CYAN}"/>')
    b.append(ptext("SOBRE.PY", 44, 44, 2, WHITE))
    b.append(ptext("X", 168, 44, 2, GREY))
    # números das linhas
    x0 = 92
    for i in range(len(CODIGO)):
        y = top + i * LH
        b.append(f'<text x="70" y="{y}" text-anchor="end" fill="{DGREY}" '
                 f'style="{MONO};font-size:{FS}px;font-weight:bold">{i + 1}</text>')
    b.append(f'<rect x="80" y="{top - 18}" width="2" height="{len(CODIGO) * LH}" fill="{DGREY}"/>')

    # linha do tempo da digitação: um caractere por passo
    dt, espera = 0.03, 6.0
    t, passos = 0.4, []  # (tempo, x do cursor, y da linha)
    inicio = []
    for i, partes in enumerate(CODIGO):
        n = sum(len(tx) for tx, _ in partes)
        inicio.append((t, n))
        for k in range(n + 1):
            passos.append((t + k * dt, x0 + k * CW, top + i * LH))
        t += n * dt + 0.25
    dur = t + espera

    for i, partes in enumerate(CODIGO):
        if not partes:
            continue
        y = top + i * LH
        t0, n = inicio[i]
        vals = ["0"] + [f"{k * CW:.1f}" for k in range(n + 1)]
        kts = ["0"] + [f"{(t0 + k * dt) / dur:.4f}" for k in range(n + 1)]
        spans = "".join(f'<tspan fill="{c}">{esc(tx)}</tspan>' for tx, c in partes)
        b.append(f'<clipPath id="c{i}"><rect x="{x0}" y="{y - 18}" height="{LH}" width="{n * CW + 10:.1f}">'
                 f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{";".join(kts)}" '
                 f'calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite"/></rect></clipPath>')
        b.append(f'<text x="{x0}" y="{y}" clip-path="url(#c{i})" xml:space="preserve" '
                 f'style="{MONO};font-size:{FS}px;font-weight:bold">{spans}</text>')

    # cursor que acompanha a digitação
    kt = ";".join(["0"] + [f"{p[0] / dur:.4f}" for p in passos])
    xs = ";".join([str(x0)] + [f"{p[1]:.1f}" for p in passos])
    ys = ";".join([str(top - 15)] + [str(p[2] - 15) for p in passos])
    b.append(f'<g><rect x="{passos[-1][1]:.1f}" y="{passos[-1][2] - 15}" width="{CW:.1f}" height="18" fill="{CYAN}">'
             f'<animate attributeName="x" values="{xs}" keyTimes="{kt}" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{ys}" keyTimes="{kt}" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite"/>'
             f'</rect></g>')

    # barra de status
    sy = H - 44
    b.append(f'<rect x="22" y="{sy}" width="{W - 44}" height="24" fill="{BLUE}"/>')
    b.append(ptext("PYTHON  *  UTF-8  *  MAIN", 36, sy + 5, 2, WHITE))
    b.append(sprite(GALO, W - 64, sy - 14, 2))
    return svg(W, H, "".join(b), BLINK, "Sobre: class Ygor")


# ---------- 4. perfil ----------
def status():
    W, H = 1000, 270
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "PERFIL")]
    rows = [
        ("NOME", "Ygor Marques"),
        ("FUNÇÃO", "Implementação & Automação de CRM"),
        ("EMPRESA", "AVA Partners"),
        ("FORMAÇÃO", "Ciência da Computação · Univértix"),
        ("PERÍODO", "8º de 8"),
        ("BASE", "Minas Gerais, Brasil"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 72 + i * 30
        b.append(ptext(k, 44, y - 13, 2, CYAN))
        b.append(f'<text x="210" y="{y}" fill="{WHITE}" style="{MONO};font-size:18px;font-weight:bold">'
                 f'{esc(v)}</text>')
    # emblema do Galo
    fx, fy, fw, fh = 740, 48, 210, 196
    b.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{BG}"/>')
    b.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="{DGREY}" stroke-width="4"/>')
    b.append(escudo(fx + (fw - 105) // 2, fy + 10, 150))
    b.append(ptext_c("ATLÉTICO-MG", fx + fw // 2, fy + fh - 28, 2, GREY))
    return svg(W, H, "".join(b), "", "Perfil")


# ---------- 5. atuação ----------
QUESTS = [
    ("IMPLEMENTAÇÕES GOHIGHLEVEL",
     "CRMs para clientes reais: pipelines, workflows, formulários e calendários."),
    ("AGENTES DE IA",
     "Conversation AI e Voice AI que atendem, qualificam e agendam."),
    ("INTEGRAÇÕES",
     "WhatsApp, webhooks e APIs conectando o CRM ao resto da operação."),
]


def quests():
    W = 1000
    H = 60 + len(QUESTS) * 74 + 20
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "ATUAÇÃO")]
    for i, (title, desc) in enumerate(QUESTS):
        y = 50 + i * 74
        if i:
            b.append(f'<rect x="40" y="{y - 10}" width="{W - 80}" height="2" fill="{DGREY}"/>')
        b.append(f'<rect x="40" y="{y + 4}" width="56" height="26" fill="{BLUE}"/>')
        b.append(ptext_c(f"{i + 1:02d}", 68, y + 10, 2, WHITE))
        b.append(ptext(title, 120, y + 10, 2, WHITE))
        b.append(f'<text x="120" y="{y + 52}" fill="{GREY}" style="{MONO};font-size:16px;font-weight:bold">'
                 f'{esc(desc)}</text>')
    return svg(W, H, "".join(b), "", "Atuação")


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


# ---------- 6b. jogo: Galo atrás dos títulos no labirinto ----------
# Percurso fechado (coluna, linha) pelos corredores; o resto do labirinto é parede.
PERCURSO = [(1, 1), (11, 1), (11, 3), (22, 3), (22, 1), (33, 1), (33, 9), (26, 9), (26, 5),
            (18, 5), (18, 9), (7, 9), (7, 5), (4, 5), (4, 9), (1, 9), (1, 1)]
MZ_COLS, MZ_ROWS, MZ_CELL = 35, 11, 26
MZ_TC = 0.18  # segundos por casa


def jogo():
    W = 1000
    ox, oy = (W - MZ_COLS * MZ_CELL) // 2, 48
    H = oy + MZ_ROWS * MZ_CELL + 30

    # casas do percurso, na ordem
    casas = [PERCURSO[0]]
    for (c0, r0), (c1, r1) in zip(PERCURSO, PERCURSO[1:]):
        dc, dr = (c1 > c0) - (c1 < c0), (r1 > r0) - (r1 < r0)
        c, r = c0, r0
        while (c, r) != (c1, r1):
            c, r = c + dc, r + dr
            casas.append((c, r))
    casas = casas[:-1]  # o último repete o primeiro
    corredor = set(casas)
    n = len(casas)
    dur = n * MZ_TC

    def centro(c, r):
        return ox + c * MZ_CELL + MZ_CELL // 2, oy + r * MZ_CELL + MZ_CELL // 2

    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "CAÇA AOS TÍTULOS")]
    # paredes: contorno azul em volta dos corredores (estilo Pac-Man)
    PAREDE, t = "#2f4fe0", 3
    for c, r in corredor:
        x, y = ox + c * MZ_CELL, oy + r * MZ_CELL
        if (c, r - 1) not in corredor:
            b.append(f'<rect x="{x}" y="{y}" width="{MZ_CELL}" height="{t}" fill="{PAREDE}"/>')
        if (c, r + 1) not in corredor:
            b.append(f'<rect x="{x}" y="{y + MZ_CELL - t}" width="{MZ_CELL}" height="{t}" fill="{PAREDE}"/>')
        if (c - 1, r) not in corredor:
            b.append(f'<rect x="{x}" y="{y}" width="{t}" height="{MZ_CELL}" fill="{PAREDE}"/>')
        if (c + 1, r) not in corredor:
            b.append(f'<rect x="{x + MZ_CELL - t}" y="{y}" width="{t}" height="{MZ_CELL}" fill="{PAREDE}"/>')
    # barras internas (como os blocos do Pac-Man), em linhas alternadas
    def livre(c, r):
        return (0 < c < MZ_COLS - 1 and 0 < r < MZ_ROWS - 1 and (c, r) not in corredor and
                not any((c + dc, r + dr) in corredor for dc in (-1, 0, 1) for dr in (-1, 0, 1)))
    for r in range(1, MZ_ROWS - 1):
        c = 1
        while c < MZ_COLS - 1:
            if not livre(c, r):
                c += 1
                continue
            ini = c
            while c < MZ_COLS - 1 and livre(c, r) and c - ini < 5:
                c += 1
            x, y = ox + ini * MZ_CELL, oy + r * MZ_CELL
            larg = (c - ini) * MZ_CELL
            b.append(f'<rect x="{x + 5}" y="{y + 6}" width="{larg - 10}" height="{MZ_CELL - 12}" '
                     f'fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            c += 1  # espaço entre barras

    lider = 12 * MZ_TC  # o Galo começa 12 casas à frente do ponto de partida
    cantos = {(1, 1), (33, 1), (33, 9), (1, 9)}
    for i, (c, r) in enumerate(casas):
        x, y = centro(c, r)
        f = i / n
        anim = (f'<animate attributeName="opacity" values="1;0" keyTimes="0;{f:.4f}" calcMode="discrete" '
                f'dur="{dur:.2f}s" begin="-{lider:.2f}s" repeatCount="indefinite"/>')
        if (c, r) in cantos:
            b.append(f'<g class="bl"><rect x="{x - 6}" y="{y - 6}" width="12" height="12" fill="#ffd8a8">{anim}</rect></g>')
        else:
            b.append(f'<rect x="{x - 2}" y="{y - 2}" width="4" height="4" fill="#ffd8a8">{anim}</rect>')

    caminho = "M" + " L".join("{} {}".format(*centro(c, r)) for c, r in casas + [casas[0]])

    def mov(adiant):
        return (f'<animateMotion path="{caminho}" dur="{dur:.2f}s" begin="-{adiant:.2f}s" '
                f'repeatCount="indefinite" calcMode="linear"/>')

    # troféus fugindo na frente do Galo
    for i in range(4):
        img, w0, h0 = png(f"trofeu-{i + 1}.png", 0, 0)
        h = round(h0 * 0.62)
        w = round(w0 * 0.62)
        img = (img.replace(f'width="{w0}" height="{h0}"', f'width="{w}" height="{h}"')
                  .replace('x="0" y="0"', f'x="{-w // 2}" y="{MZ_CELL // 2 - h}"'))
        adiant = lider + (3 + i * 2.5) * MZ_TC
        b.append(f'<g><g class="hop" style="animation-delay:-{i * .3:.1f}s">{img}</g>{mov(adiant)}</g>')

    # Galo virado para o lado em que anda
    sentido, trocas, atual = [], [], None
    for i, ((c0, r0), (c1, r1)) in enumerate(zip(casas, casas[1:] + casas[:1])):
        if c1 != c0:
            d = 1 if c1 > c0 else -1
            if d != atual:
                trocas.append((i / n, d))
                atual = d
    if trocas[0][0] > 0:
        trocas.insert(0, (0.0, trocas[-1][1]))
    kt = ";".join(f"{t:.4f}" for t, _ in trocas)

    def lado(d):
        vals = ";".join("1" if s == d else "0" for _, s in trocas)
        return (f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" calcMode="discrete" '
                f'dur="{dur:.2f}s" begin="-{lider:.2f}s" repeatCount="indefinite"/>')

    sc = 1.5
    gw, gh = 22 * sc, (len(GALO_CORPO) + 4) * sc
    quadros = "".join(f'<g class="q{i}">{sprite(GALO_CORPO + p, -gw // 2, MZ_CELL // 2 - gh, sc)}</g>'
                      for i, p in enumerate(GALO_PERNAS))
    b.append(f'<g><g>{quadros}{lado(1)}</g><g transform="scale(-1,1)">{quadros}{lado(-1)}</g>{mov(lider)}</g>')

    st = (BLINK +
          ".q0{animation:q0 .4s steps(1,end) infinite}@keyframes q0{50%{opacity:0}}"
          ".q1{opacity:0;animation:q1 .4s steps(1,end) infinite}@keyframes q1{50%{opacity:1}}"
          ".hop{animation:hop .6s steps(3,end) infinite}"
          "@keyframes hop{0%,100%{transform:none}50%{transform:translateY(-5px)}}")
    return svg(W, H, "".join(b), st, "Caça aos títulos: o Galo atrás dos troféus no labirinto")


# ---------- 7. rodapé ----------
def footer():
    W, H = 1000, 210
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', stars(W, 160, 25, 11, calm=True)]
    b.append(ptext_c("VAMOS CONVERSAR?", 500, 36, 4, WHITE, shadow=BLUE))
    b.append(f'<text x="500" y="118" text-anchor="middle" fill="{GREY}" '
             f'style="{MONO};font-size:17px;font-weight:bold">'
             f'linkedin.com/in/ygor-freire-374940291  ·  ygorfreire.dev@gmail.com</text>')
    b.append(floor(W, 174, 36))
    return svg(W, H, "".join(b), TWINKLE, "Vamos conversar?")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "btn-email.svg": button("EMAIL", RED, "email"),
        "btn-repos.svg": button("REPOSITÓRIOS", BLUE, "repos"),
        "btn-linkedin.svg": button("LINKEDIN", "#0a66c2", "linkedin"),
        "dialog.svg": dialog(),
        "status.svg": status(),
        "quests.svg": quests(),
        "inventory.svg": inventory(),
        "jogo.svg": jogo(),
        "footer.svg": footer(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content) // 1024} KB")
