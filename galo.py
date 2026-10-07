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
TC = 0.1  # segundos por quadradinho
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

    # caminho em zigue-zague, coluna por coluna (desce, sobe, desce...)
    pts = []
    for c, wk in enumerate(weeks):
        dias = sorted(wk["contributionDays"], key=lambda d: d["weekday"])
        if c % 2:
            dias = dias[::-1]
        for d in dias:
            pts.append((gx + c * STEP + CELL // 2, gy + d["weekday"] * STEP + CELL // 2, d))
    n = len(pts)
    dur = n * TC
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
        f = i / n
        b.append(f'<rect x="{x - CELL // 2}" y="{y - CELL // 2}" width="{CELL}" height="{CELL}" fill="{cor}">'
                 f'<animate attributeName="opacity" values="1;0" keyTimes="0;{f:.4f}" calcMode="discrete" '
                 f'dur="{dur:.1f}s" begin="-{lider:.1f}s" repeatCount="indefinite"/></rect>')

    caminho = "M" + " L".join(f"{x} {y}" for x, y, _ in pts)

    def ator(rows, sc, begin, cls):
        w, h = len(rows[0]) * sc, len(rows) * sc
        return (f'<g><g class="{cls}">{sprite(rows, -w // 2, -h // 2, sc)}</g>'
                f'<animateMotion path="{caminho}" dur="{dur:.1f}s" begin="{begin:.1f}s" '
                f'repeatCount="indefinite" calcMode="linear"/></g>')

    for j, atraso in enumerate(ATRASOS):
        cor = str(j + 1)
        rows = [r.replace("c", cor) for r in BICHO]
        b.append(ator(rows, 2, -(max(ATRASOS) - atraso) * TC, "flu"))
    b.append(ator(GALO, 2, -lider, "pula"))

    st = (".pula{animation:pula .3s steps(2,end) infinite}@keyframes pula{50%{transform:translateY(-2px)}}"
          ".flu{animation:flu .5s steps(2,end) infinite}@keyframes flu{50%{transform:translateY(1px)}}")
    return svg(W, H, "".join(b), st, f"Galo comendo {total} contribuições do último ano")


if __name__ == "__main__":
    out = Path("dist")
    out.mkdir(exist_ok=True)
    conteudo = gerar(calendario())
    (out / "galo-contribuicoes.svg").write_text(conteudo, encoding="utf-8")
    print(f"dist/galo-contribuicoes.svg: {len(conteudo) // 1024} KB")
