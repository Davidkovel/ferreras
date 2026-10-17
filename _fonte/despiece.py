# O relógio em peças (para a vitrina): fundo da caixa, rotor, calibre com rodas e balanço, caixa, esfera verdadeira,
# agulhas e cristal. Cada peça é uma camada do mesmo tamanho; o js/92-alcoba.js separa-as em profundidade e monta-as
# com o scroll. Tudo em SVG gerado aqui, com geometria determinista (nada aleatório entre builds).
import math


def _f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def roda(cx, cy, r, dentes, raios=5, cor="url(#dzOuro)", cls="gira", vel=8, rev=False):
    """Uma roda dentada: coroa com dentes trapezoidais, aro interior vazado em raios e eixo com rubi."""
    pts = []
    passo = 2 * math.pi / dentes
    for i in range(dentes):
        a = i * passo
        for da, rr in ((-0.32, r - r * 0.09), (-0.18, r), (0.18, r), (0.32, r - r * 0.09)):
            t = a + da * passo
            pts.append(f"{_f(cx + rr * math.cos(t))},{_f(cy + rr * math.sin(t))}")
    coroa = f'<polygon points="{" ".join(pts)}" fill="{cor}" stroke="#6b5222" stroke-width=".6"/>'
    ri = r * 0.72
    furo = f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(ri)}" fill="#2a2620"/>'
    rs = "".join(
        f'<rect x="{_f(cx - r * 0.06)}" y="{_f(cy - ri)}" width="{_f(r * 0.12)}" height="{_f(ri)}" fill="{cor}" transform="rotate({_f(i * 360 / raios)} {_f(cx)} {_f(cy)})"/>'
        for i in range(raios))
    eixo = f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r * 0.2)}" fill="{cor}"/><circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(max(2.2, r * 0.08))}" fill="#b3122e"/>'
    d = " dz-rev" if rev else ""
    return f'<g class="{cls}{d}" style="--v:{vel}s">{coroa}{furo}{rs}{eixo}</g>'


def calibre():
    """O movimento visto de frente: platina com perlage, pontes com Côtes de Genève, rodas, balanço e rubis."""
    perl = "".join(f'<circle cx="{_f(200 + 150 * math.cos(i * 0.618 * 6.283) * math.sqrt(i / 90))}" cy="{_f(200 + 150 * math.sin(i * 0.618 * 6.283) * math.sqrt(i / 90))}" r="13" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1"/>' for i in range(90))
    pontes = ('<path d="M120 80 L300 70 Q330 120 300 170 L210 190 Q160 200 120 160 Z" fill="url(#dzCotes)" stroke="#5f6468" stroke-width="1.2"/>'
              '<path d="M90 230 Q150 210 220 250 L250 330 Q190 350 120 320 Z" fill="url(#dzCotes)" stroke="#5f6468" stroke-width="1.2"/>')
    rubis = "".join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#b3122e" stroke="#e8c9a0" stroke-width="1.4"/><circle cx="{x - 1.2}" cy="{y - 1.4}" r="1.2" fill="#ff8aa0"/>'
                    for x, y in ((150, 110), (270, 100), (285, 150), (160, 280), (215, 300), (240, 205)))
    balanco = ('<g transform="translate(0 -64)"><g class="dz-balanco"><circle cx="200" cy="200" r="46" fill="none" stroke="url(#dzOuro)" stroke-width="7"/>'
               + "".join(f'<rect x="197" y="156" width="6" height="44" fill="url(#dzOuro)" transform="rotate({a} 200 200)"/>' for a in (0, 120, 240))
               + '<path d="M200 200 m0 -4 a4 4 0 1 1 -4 4 a8 8 0 1 1 8 -8 a12 12 0 1 1 -12 12 a16 16 0 1 1 16 -16 a20 20 0 1 1 -20 20" fill="none" stroke="#3a3d40" stroke-width="1"/>'
               + '<circle cx="200" cy="200" r="5" fill="#b3122e"/></g></g>')
    return ('<svg viewBox="0 0 400 400" aria-hidden="true"><defs>'
            '<radialGradient id="dzPlatina" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#e3e6e8"/><stop offset=".6" stop-color="#aeb4b9"/><stop offset="1" stop-color="#6f767c"/></radialGradient>'
            '<linearGradient id="dzOuro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1dca7"/><stop offset=".5" stop-color="#c49a52"/><stop offset="1" stop-color="#e5c68c"/></linearGradient>'
            '<pattern id="dzCotes" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-24)"><rect width="14" height="14" fill="#c3c8cc"/><rect width="7" height="14" fill="#d9dde0"/></pattern>'
            '</defs><circle cx="200" cy="200" r="188" fill="url(#dzPlatina)"/>' + perl
            + '<circle cx="200" cy="200" r="188" fill="none" stroke="#5f6468" stroke-width="2"/>' + pontes
            + roda(250, 130, 44, 40, vel=14) + roda(150, 150, 30, 28, vel=9, rev=True) + roda(185, 285, 36, 34, vel=11) + roda(280, 255, 22, 20, vel=6, rev=True)
            + balanco + rubis + '</svg>')


def rotor():
    return ('<svg viewBox="0 0 400 400" aria-hidden="true"><defs><linearGradient id="dzRotor" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#efd9a4"/><stop offset=".55" stop-color="#b8904a"/><stop offset="1" stop-color="#e2c486"/></linearGradient></defs>'
            '<path d="M20 200 A180 180 0 0 1 380 200 L250 200 A50 50 0 0 0 150 200 Z" fill="url(#dzRotor)" stroke="#6b5222" stroke-width="1.5"/>'
            '<circle cx="200" cy="200" r="22" fill="url(#dzRotor)" stroke="#6b5222"/><circle cx="200" cy="200" r="6" fill="#b3122e"/>'
            '<text x="200" y="120" text-anchor="middle" font-family="Bodoni Moda, Didot, serif" font-size="30" letter-spacing="6" fill="#6b5222">FERRERAS</text></svg>')


def fondo():
    txt = "AUTOMÁTICO · MECANISMO SUIZO · ENSAMBLADO EN BARCELONA · "
    return ('<svg viewBox="0 0 400 400" aria-hidden="true"><defs><radialGradient id="dzAcero" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#eef0f1"/><stop offset=".55" stop-color="#9aa1a6"/><stop offset="1" stop-color="#5b6166"/></radialGradient>'
            '<path id="dzAro" d="M200 200 m-150 0 a150 150 0 1 1 300 0 a150 150 0 1 1 -300 0"/></defs>'
            '<circle cx="200" cy="200" r="198" fill="url(#dzAcero)" stroke="#4a4f53" stroke-width="2"/>'
            '<circle cx="200" cy="200" r="120" fill="rgba(20,24,28,.55)" stroke="#c49a52" stroke-width="2"/>'
            f'<text font-family="Jost, Futura, sans-serif" font-size="15" letter-spacing="3" fill="#41464a"><textPath href="#dzAro">{txt}</textPath></text></svg>')


def caixa():
    return ('<svg viewBox="0 0 400 400" aria-hidden="true"><defs><linearGradient id="dzCaixa" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ead39f"/><stop offset=".5" stop-color="#b8975a"/><stop offset="1" stop-color="#d9bf88"/></linearGradient></defs>'
            '<circle cx="200" cy="200" r="194" fill="none" stroke="url(#dzCaixa)" stroke-width="10"/><circle cx="200" cy="200" r="187" fill="none" stroke="#0d0b09" stroke-width="5"/></svg>')


def agulhas():
    return ('<svg viewBox="0 0 400 400" aria-hidden="true"><defs><linearGradient id="dzAg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f1dca7"/><stop offset=".5" stop-color="#b8904a"/><stop offset="1" stop-color="#e2c486"/></linearGradient></defs>'
            '<g transform="rotate(-55 200 200)"><polygon points="200,98 207,200 200,216 193,200" fill="url(#dzAg)" stroke="#6b5222" stroke-width=".7"/></g>'
            '<g transform="rotate(60 200 200)"><polygon points="200,40 205,200 200,219 195,200" fill="url(#dzAg)" stroke="#6b5222" stroke-width=".7"/></g>'
            '<g transform="rotate(180 200 200)"><line x1="200" y1="244" x2="200" y2="54" stroke="#001a39" stroke-width="1.6"/><rect x="195" y="44" width="10" height="10" fill="#0022f1"/></g>'
            '<circle cx="200" cy="200" r="8.5" fill="url(#dzAg)" stroke="#6b5222" stroke-width=".6"/></svg>')


PECAS = [  # (classe, profundidade separada em px, nome na lista; None = não aparece na lista)
    ("dz-fondo", -230, "El fondo de la caja"),
    ("dz-rotor", -150, None),
    ("dz-calibre", -70, "El calibre: suizo y automático"),
    ("dz-caixa", 10, None),
    ("dz-esfera", 90, "La esfera, con el corazón abierto"),
    ("dz-agujas", 170, "Las agujas, con baño de oro de 18 quilates"),
    ("dz-cristal", 250, "El cristal, de zafiro"),
]


def despiece_html(R):
    corpo = {"dz-fondo": fondo(), "dz-rotor": rotor(), "dz-calibre": calibre(), "dz-caixa": caixa(),
             "dz-esfera": f'<img src="{R}img/dial-ferreras.webp" width="832" height="832" alt="" decoding="async">',
             "dz-agujas": agulhas(), "dz-cristal": ""}
    capas = "".join(f'<div class="dz-capa {c}" data-dz-capa data-z="{z}">{corpo[c]}</div>' for c, z, _ in PECAS)
    return f'<div class="dz" data-dz aria-hidden="true"><div class="dz-pila" data-dz-pila>{capas}</div></div>'


def lista_html():
    li = "".join(f'<li data-dz-paso><i></i>{n}</li>' for _, _, n in PECAS if n)
    return (f'<div class="dz-lista" data-dz-lista><p class="etiqueta"><span class="hora">16:30</span>Montaje</p>'
            f'<p class="dz-tit">Pieza a pieza.</p><ol>{li}</ol><p class="dz-pe" data-dz-pe>Montado en Barcelona.</p></div>')
