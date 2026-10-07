"""Gera o jogo do Galo: o Galo percorre o gráfico de contribuições comendo os
quadradinhos, perseguido por três bichinhos. Roda na Action todo dia.

Uso: GITHUB_TOKEN=... python galo.py [usuario]  ->  dist/galo-contribuicoes.svg
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

from build import (BG, BLUE, DGREY, GREY, ORANGE, PAL, PURPLE, GALO, WHITE,
                   ptext, sprite, svg, text_w, window)

USER = sys.argv[1] if len(sys.argv) > 1 else "Ygormarques7"
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{contributionCount contributionLevel date weekday}}}}}}"""

NIVEL = {"NONE": None, "FIRST_QUARTILE": "#265c42", "SECOND_QUARTILE": "#3e8948",
         "THIRD_QUARTILE": "#63c74d", "FOURTH_QUARTILE": "#b6f05a"}

BICHO = [
    "...cccc...",
    ".cccccccc.",
    "cccccccccc",
    "ccwwccwwcc",
    "ccwkccwkcc",
    "cccccccccc",
    "cccccccccc",
    "cc.cc.cc.c",
]
PAL.update({"1": PURPLE, "2": ORANGE, "3": "#e43b8f"})

CELL, GAP = 14, 3
STEP = CELL + GAP
TC = 0.12  # segundos por quadradinho
ATRASOS = [4, 7, 10]  # quantos quadradinhos cada bicho vem atrás do Galo


def calendario():
    token = os.environ["GITHUB_TOKEN"]
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={"Authorization": f"bearer {token}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def gerar(cal):
    W = 1000
    weeks = cal["weeks"]
    gx = (W - (len(weeks) * STEP - GAP)) // 2
    gy = 88
    H = gy + 7 * STEP + 34

    # caminho estilo Pac-Man: linha por linha, ida e volta (esquerda->direita, direita->esquerda...)
    por_dia = {}
    for c, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            por_dia[(d["weekday"], c)] = d
    pts, sentido = [], []
    for r in range(7):
        cols = range(len(weeks)) if r % 2 == 0 else range(len(weeks) - 1, -1, -1)
        for c in cols:
            if (r, c) in por_dia:
                pts.append((gx + c * STEP + CELL // 2, gy + r * STEP + CELL // 2, por_dia[(r, c)]))
                sentido.append(1 if r % 2 == 0 else -1)
    # distância acumulada: o movimento é pela distância, então o "comer" usa a mesma fração
    dist = [0.0]
    for (x0, y0, _), (x1, y1, _) in zip(pts, pts[1:]):
        dist.append(dist[-1] + ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5)
    D = dist[-1]
    frac = [d / D for d in dist]
    dur = D / STEP * TC
    lider = max(ATRASOS) * TC  # Galo começa à frente dos bichos

    total = cal["totalContributions"]
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', window(8, 18, W - 16, H - 26, "CONTRIBUIÇÕES")]
    info = f"{total} NO ÚLTIMO ANO"
    b.append(ptext(info, W - 44 - text_w(info, 2), 50, 2, GREY))

    # grade vazia + quadradinhos que o Galo come
    for x, y, d in pts:
        b.append(f'<rect x="{x - CELL // 2}" y="{y - CELL // 2}" width="{CELL}" height="{CELL}" fill="#1c2238"/>')
    for i, (x, y, d) in enumerate(pts):
        cor = NIVEL.get(d["contributionLevel"])
        if not cor:
            continue
        f = frac[i]
        b.append(f'<rect x="{x - CELL // 2}" y="{y - CELL // 2}" width="{CELL}" height="{CELL}" fill="{cor}">'
                 f'<animate attributeName="opacity" values="1;0" keyTimes="0;{f:.4f}" calcMode="discrete" '
                 f'dur="{dur:.1f}s" begin="-{lider:.1f}s" repeatCount="indefinite"/></rect>')

    caminho = "M" + " L".join(f"{x} {y}" for x, y, _ in pts)

    def mov(begin):
        return (f'<animateMotion path="{caminho}" dur="{dur:.2f}s" begin="{begin:.2f}s" '
                f'repeatCount="indefinite" calcMode="paced"/>')

    def sp(rows, sc):
        w, h = len(rows[0]) * sc, len(rows) * sc
        return sprite(rows, -w // 2, -h // 2, sc)

    for j, atraso in enumerate(ATRASOS):
        rows = [r.replace("c", str(j + 1)) for r in BICHO]
        b.append(f'<g><g class="flu">{sp(rows, 2)}</g>{mov(-(max(ATRASOS) - atraso) * TC)}</g>')

    # Galo virado para o lado em que anda: duas versões trocadas na virada de cada linha
    trocas = [0.0] + [frac[i] for i in range(1, len(pts)) if sentido[i] != sentido[i - 1]]
    vals_d = ";".join("1" if k % 2 == 0 else "0" for k in range(len(trocas)))
    vals_e = ";".join("0" if k % 2 == 0 else "1" for k in range(len(trocas)))
    kt = ";".join(f"{t:.4f}" for t in trocas)

    def lado(vals):
        return (f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" calcMode="discrete" '
                f'dur="{dur:.2f}s" begin="-{lider:.2f}s" repeatCount="indefinite"/>')

    galo = sp(GALO, 2)
    b.append(f'<g><g class="pula"><g>{galo}{lado(vals_d)}</g>'
             f'<g transform="scale(-1,1)" opacity="0">{galo}{lado(vals_e)}</g></g>{mov(-lider)}</g>')

    st = (".pula{animation:pula .3s steps(2,end) infinite}@keyframes pula{50%{transform:translateY(-2px)}}"
          ".flu{animation:flu .5s steps(2,end) infinite}@keyframes flu{50%{transform:translateY(1px)}}")
    return svg(W, H, "".join(b), st, f"Galo comendo {total} contribuições do último ano")


if __name__ == "__main__":
    out = Path("dist")
    out.mkdir(exist_ok=True)
    conteudo = gerar(calendario())
    (out / "galo-contribuicoes.svg").write_text(conteudo, encoding="utf-8")
    print(f"dist/galo-contribuicoes.svg: {len(conteudo) // 1024} KB")
