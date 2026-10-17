"""Escreve o site estático da proposta Ferreras: o shell partilhado e o conteúdo de cada página.

    python -I _fonte/build.py

O site publicado é só HTML/CSS/JS; este script é a ferramenta que o escreve (não há build no servidor).
O conteúdo vem do site antigo (marketingferreras.com), em «usted», encurtado; nada inventado.
Python 3.11: nenhuma expressão de f-string leva barra invertida nem o mesmo tipo de aspas.
"""
import html as H
import json
import math
import random
import re
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parents[1]
URL = "https://davidkovel.github.io/ferreras/"
EMAIL = "administracion@marketingferreras.com"
VERSAO = "15"
Q = '"'
CTA = "Hablemos de su marca"


def e(s):
    return H.escape(s, quote=True)


def se(cond, s):
    return s if cond else ""


# ---------------------------------------------------------------- logotipo (vectorizado a partir dos PNG originais)
def _paths(svg):
    return re.findall(r'<path fill="([^"]+)" fill-rule="evenodd" d="([^"]+)"/>', svg)


def _sub(d):
    return [("M" + p).strip() for p in d.split("M") if p.strip()]


def _xs(d):
    xs = [float(a) for a in re.findall(r"(-?[\d.]+) -?[\d.]+", d)]
    return min(xs), max(xs)


MARK = (RAIZ / "img/logo-mark-light.svg").read_text()
WORD = (RAIZ / "img/logo-wordmark-light.svg").read_text()
_M = {c[:2]: d for c, d in _paths(MARK)}           # '#f' marfil, '#a' piedra, '#0' señal
MARFIL = sorted(_sub(_M["#f"]), key=lambda d: _xs(d)[1] - _xs(d)[0], reverse=True)   # [barra de arriba, vertical]
WORD_D = _paths(WORD)[0][1]


def _letras():
    subs = sorted(_sub(WORD_D), key=lambda d: _xs(d)[0])
    out = []
    for d in subs:
        a, b = _xs(d)
        if out and a < out[-1][1] - 2:
            out[-1][0].append(d)
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([[d], b])
    return [" ".join(ds) for ds, _ in out]


LETRAS = _letras()


def logo_svg(pecas=False):
    """F + FERRERAS na horizontal; com pecas=True cada peça leva classe e índice para a abertura."""
    def p(cls, d, i=None, senal=False):
        k = cls + (" pz" if pecas and i is not None else "") + (" pz-senal" if pecas and senal else "")
        st = f' style="--i:{i}"' if pecas and i is not None else ""
        return f'<path class="{k}"{st} fill-rule="evenodd" d="{d}"/>'
    partes = [p("lg-m", MARFIL[0], 0), p("lg-p", _M["#a"], 1), p("lg-m", MARFIL[1], 2), p("lg-s", _M["#0"], senal=True)]
    letras = "".join(f'<path{se(pecas, f" class={Q}letra{Q} style={Q}--i:{i}{Q}")} fill-rule="evenodd" d="{d}"/>' for i, d in enumerate(LETRAS))
    return f'<svg viewBox="0 0 1253 256" aria-hidden="true">{"".join(partes)}<g class="lg-w" transform="translate(305 79) scale(1.0208)">{letras}</g></svg>'


def marca_paths():
    return (f'<path fill="#f3e6dc" fill-rule="evenodd" d="{_M["#f"]}"/><path fill="#a1998f" fill-rule="evenodd" d="{_M["#a"]}"/>'
            f'<path fill="#0022f1" fill-rule="evenodd" d="{_M["#0"]}"/>')


def wordmark_svg(cls="wm"):
    return f'<svg class="{cls}" viewBox="0 0 929 96" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{WORD_D}"/></svg>'


# ---------------------------------------------------------------- o relógio
def reloj_html(R="", sfx=""):
    """A esfera verdadeira do Ferreras (foto endireitada, com o coração aberto recortado); por baixo, um céu que gira
    dentro da abertura (dia com sol, entardecer, noite com lua e estrelas); por cima, os ponteiros em SVG."""
    oro = (f'<linearGradient id="oroG{sfx}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ead39f"/>'
           '<stop offset=".5" stop-color="#b8975a"/><stop offset="1" stop-color="#d9bf88"/></linearGradient>')
    caixa = (f'<svg class="r-caixa" viewBox="0 0 400 400" aria-hidden="true"><defs>{oro}</defs>'
             '<circle cx="200" cy="200" r="199" fill="#081322"/>'
             f'<circle cx="200" cy="200" r="197.5" fill="none" stroke="url(#oroG{sfx})" stroke-width="3"/>'
             '<circle cx="200" cy="200" r="193" fill="none" stroke="#0b1622" stroke-width="5"/></svg>')
    ceu = '<div class="r-ceu ag-d"></div>'
    esfera = f'<img class="r-esfera" src="{R}img/dial-ferreras.webp" width="832" height="832" alt="">'
    agujas = f'''<svg class="r-agujas" viewBox="0 0 400 400" aria-hidden="true"><defs>{oro.replace('oroG', 'oroH')}
<filter id="sombraA{sfx}" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="1.5" dy="2.5" stdDeviation="1.6" flood-color="#2a1d08" flood-opacity=".45"/></filter></defs>
<g filter="url(#sombraA{sfx})">
<g class="ag ag-h"><polygon points="200,98 207,200 200,216 193,200" fill="url(#oroH{sfx})" stroke="#6b5222" stroke-width=".7"/><polygon points="200,98 200,216 193,200" fill="rgba(110,80,30,.45)"/></g>
<g class="ag ag-m"><polygon points="200,40 205,200 200,219 195,200" fill="url(#oroH{sfx})" stroke="#6b5222" stroke-width=".7"/><polygon points="200,40 200,219 195,200" fill="rgba(110,80,30,.45)"/></g>
<g class="ag ag-s"><line x1="200" y1="244" x2="200" y2="54" stroke="#001a39" stroke-width="1.6"/><circle cx="200" cy="230" r="5.5" fill="none" stroke="#001a39" stroke-width="1.6"/><rect x="195" y="44" width="10" height="10" fill="#0022f1"/></g>
<circle cx="200" cy="200" r="8.5" fill="url(#oroH{sfx})" stroke="#6b5222" stroke-width=".6"/><circle cx="200" cy="200" r="2.6" fill="#001a39"/></g></svg>'''
    return f'<div class="reloj">{caixa}{ceu}{esfera}{agujas}<div class="brillo"></div></div>'


def mini_reloj():
    return ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#f3e6dc" stroke="#c2a263" stroke-width="1.6"/>'
            '<line x1="20" y1="20" x2="20" y2="9" stroke="#a98b52" stroke-width="2" stroke-linecap="round"/><line x1="20" y1="20" x2="27" y2="24" stroke="#a98b52" stroke-width="2" stroke-linecap="round"/>'
            '<rect x="18.5" y="4.5" width="3" height="3" fill="#0022f1"/></svg>')


# ---------------------------------------------------------------- as 24 horas de uma recepção (ilustração)
def dia24_svg():
    """Consultas de um dia qualquer à volta de um mostrador de 24 h (00 em cima). Com a recepção fechada (23–08)
    cada consulta é um quadrado azul: o sinal do logótipo, o agente. Pontos fixos (semente), nada aleatório no browser."""
    rnd = random.Random(2340)
    peso = [3, 2, 1, 1, 1, 1, 1, 2, 4, 6, 6, 5, 4, 3, 3, 4, 5, 5, 4, 4, 4, 4, 4, 4]
    fechado = lambda hh: hh >= 23 or hh < 8
    pts = []
    for hh, n in enumerate(peso):
        for _ in range(n):
            pts.append((hh * 60 + rnd.uniform(4, 56), rnd.uniform(-22, 22)))
    alvo = 23 * 60 + 40
    pts = [p for p in pts if abs(p[0] - alvo) > 9]      # o lugar da consulta das 23:40 fica livre
    pts.append((alvo, 0))
    out = []
    pol = lambda m, r: (200 + r * math.sin(m / 1440 * 2 * math.pi), 200 - r * math.cos(m / 1440 * 2 * math.pi))
    for i in range(24):
        a, b = (162, 180) if i % 6 == 0 else (170, 177)
        x1, y1 = pol(i * 60, a)
        x2, y2 = pol(i * 60, b)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="tq{se(i % 6 == 0, " tq6")}"/>')
    for hh, lab in ((0, "00"), (6, "06"), (12, "12"), (18, "18")):
        x, y = pol(hh * 60, 197)
        out.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" class="lab">{lab}</text>')
    x0, y0 = pol(23 * 60, 150)
    x1, y1 = pol(32 * 60, 150)
    out.append(f'<path class="arco" d="M{x0:.1f} {y0:.1f} A150 150 0 0 1 {x1:.1f} {y1:.1f}"/>')
    for m, j in sorted(pts):
        x, y = pol(m, 150 + j)
        d = f"{m / 1440 * 3.2:.2f}s"
        if m == alvo:
            out.append(f'<g class="pt alvo" style="--d:{d}"><circle cx="{x:.1f}" cy="{y:.1f}" r="13" class="anel"/><rect x="{x - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" class="ag"/></g>')
            tx, ty = pol(m, 117)
            out.append(f'<text x="{tx + 6:.1f}" y="{ty + 6:.1f}" class="pt lab-alvo" style="--d:{d}">23:40 · DE</text>')
        elif fechado(int(m // 60)):
            out.append(f'<rect class="pt ag" style="--d:{d}" x="{x - 3.2:.1f}" y="{y - 3.2:.1f}" width="6.4" height="6.4"/>')
        else:
            out.append(f'<circle class="pt eq" style="--d:{d}" cx="{x:.1f}" cy="{y:.1f}" r="3.3"/>')
    centro = ('<text x="200" y="200" class="c1">24 h</text>'
              '<text x="200" y="228" class="c2">NINGUNA CONSULTA</text><text x="200" y="244" class="c2">SIN RESPUESTA</text>')
    varre = '<line class="varre" x1="200" y1="200" x2="200" y2="16"/>'
    return (f'<svg class="dia24-svg" viewBox="-34 -34 468 468" role="img" aria-label="Ilustración: las consultas de un día cualquiera; '
            f'de las 23:00 a las 8:00, con la recepción cerrada, las atiende el agente">{"".join(out)}{varre}{centro}</svg>')


# ---------------------------------------------------------------- imagens e vídeo
def _dim(base, w):
    p = RAIZ / "img" / f"{base}-{w}.webp"
    return Image.open(p).size if p.exists() else None


def img(R, base, alt, sizes="100vw", lazy=True, extra=""):
    d9, d16 = _dim(base, 900), _dim(base, 1600)
    src = [f"{R}img/{base}-900.webp {d9[0]}w"] + ([f"{R}img/{base}-1600.webp {d16[0]}w"] if d16 else [])
    w, h = d16 or d9
    carga = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="{R}img/{base}-{1600 if d16 else 900}.webp" srcset="{", ".join(src)}" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}"{carga}{extra}>'


def video(R, nome, alt, w=540, h=960):
    return (f'<video muted playsinline loop preload="none" width="{w}" height="{h}" poster="{R}video/{nome}-poster.webp" '
            f'data-src="{R}video/{nome}.mp4?v={VERSAO}" data-video-auto aria-label="{e(alt)}"></video>')


def coche_svg(sfx=""):
    """O coche visto de cima, de frente para baixo (+y): carroçaria negra brilhante, asa traseira e a barra de luz
    vermelha de um GT3 RS, faróis acesos. Serve à rota da home e de marcador no diagnóstico."""
    corpo = ("M24 3C34 1 46 1 56 3C70 5 78 16 78 38C78 60 74 78 74 96C74 112 77 128 77 146C77 162 70 172 58 174"
             "C48 175.5 32 175.5 22 174C10 172 3 162 3 146C3 128 6 112 6 96C6 78 2 60 2 38C2 16 10 5 24 3Z")
    return (f'<svg class="coche" viewBox="0 0 80 176" aria-hidden="true"><defs>'
            f'<linearGradient id="cc-c{sfx}" x1="0" x2="1"><stop offset="0" stop-color="#04070b"/><stop offset=".36" stop-color="#141b24"/>'
            f'<stop offset=".5" stop-color="#2a3542"/><stop offset=".64" stop-color="#141b24"/><stop offset="1" stop-color="#04070b"/></linearGradient>'
            f'<linearGradient id="cc-v{sfx}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22303f"/><stop offset="1" stop-color="#06090d"/></linearGradient>'
            f'<radialGradient id="cc-f{sfx}"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#e3edff"/><stop offset="1" stop-color="#e3edff" stop-opacity="0"/></radialGradient>'
            f'<filter id="cc-b{sfx}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter></defs>'
            f'<ellipse cx="40" cy="90" rx="39" ry="87" fill="#000" opacity=".4" filter="url(#cc-b{sfx})"/>'
            f'<path d="{corpo}" fill="url(#cc-c{sfx})" stroke="rgba(255,255,255,.24)" stroke-width=".8"/>'
            f'<rect x="15" y="4.4" width="50" height="3.2" rx="1.6" fill="#ff2b2b" opacity=".75" filter="url(#cc-b{sfx})"/>'
            f'<rect x="15" y="5.1" width="50" height="1.8" rx=".9" fill="#ff3b30"/>'
            f'<rect x="5" y="12" width="70" height="7" rx="2" fill="#0a0e13" stroke="rgba(255,255,255,.26)" stroke-width=".6"/>'
            f'<path d="M28 26h24M27 30h26M27 34h26M28 38h24" stroke="rgba(255,255,255,.12)" stroke-width="1"/>'
            f'<path d="M26 58H54L51 46H29Z" fill="url(#cc-v{sfx})" stroke="rgba(255,255,255,.15)" stroke-width=".5"/>'
            f'<rect x="22" y="58" width="36" height="40" rx="7" fill="#0e141b"/>'
            f'<path d="M22 98H58L64 121H16Z" fill="url(#cc-v{sfx})" stroke="rgba(255,255,255,.18)" stroke-width=".5"/>'
            f'<path d="M26 101H40L33 118H20Z" fill="#fff" opacity=".07"/>'
            f'<ellipse cx="5.5" cy="104" rx="4" ry="2.6" fill="#0a0e13" stroke="rgba(255,255,255,.22)" stroke-width=".5"/>'
            f'<ellipse cx="74.5" cy="104" rx="4" ry="2.6" fill="#0a0e13" stroke="rgba(255,255,255,.22)" stroke-width=".5"/>'
            f'<path d="M40 125V166M26 167H54" stroke="rgba(255,255,255,.1)" stroke-width="1.2"/>'
            f'<ellipse cx="17" cy="159" rx="6.5" ry="4.5" fill="url(#cc-f{sfx})"/><ellipse cx="63" cy="159" rx="6.5" ry="4.5" fill="url(#cc-f{sfx})"/></svg>')


# ---------------------------------------------------------------- shell
NAV = [("la-casa/", "La casa"), ("marketing/", "Marketing"), ("inteligencia-artificial/", "IA"), ("sectores/", "Sectores"), ("casos/", "Casos")]
SECT = [("sectores/hoteles/", "Hoteles"), ("sectores/automocion-lujo/", "Automoción de lujo"), ("sectores/nautica/", "Náutica, yates y puertos"), ("sectores/joyeria-relojeria/", "Joyería y relojería")]


def head(R, titulo, desc, rota):
    t = titulo if "Ferreras" in titulo else f"{titulo} · IA & Marketing Ferreras"
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "IA & Marketing Ferreras", "legalName": "FERRERAS LUXURY GROUP, S.L.",
           "url": URL, "email": EMAIL, "taxID": "B25958869",
           "address": {"@type": "PostalAddress", "streetAddress": "Passeig de Gràcia 95, 5º 1ª", "postalCode": "08008", "addressLocality": "Barcelona", "addressCountry": "ES"},
           "sameAs": ["https://relojes-ferreras.com/"]}
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{URL}{rota}">
<meta name="theme-color" content="#0d0b09">
<meta property="og:type" content="website">
<meta property="og:site_name" content="IA &amp; Marketing Ferreras">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(t)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{URL}{rota}">
<meta property="og:image" content="{URL}og/inicio.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Las manecillas doradas de un reloj Ferreras sobre negro, junto al logotipo y la frase Veinticuatro horas a la altura de su marca">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{URL}og/inicio.jpg">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{R}fonts/bodoni.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{R}fonts/jost.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}estilo.css?v={VERSAO}">
<script>document.documentElement.classList.add('js');try{{if(sessionStorage.getItem('ferreras.abertura')==='1'||matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('sem-abertura')}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>
'''


def cabecera(R, atual):
    nav = "".join(f'<a href="{R}{h}"{se(atual.startswith(h), " aria-current=" + Q + "page" + Q)}>{e(t)}</a>' for h, t in NAV)
    itens = NAV + [("contacto/", "Contacto")]
    menu = "".join(f'<li style="--i:{i}"><a href="{R}{h}"><small>0{i + 1}</small>{e(t)}</a></li>' for i, (h, t) in enumerate(itens))
    sub = "".join(f'<a href="{R}{h}">{e(t)}</a>' for h, t in SECT)
    inicio = R or "./"
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<div class="cielo" aria-hidden="true"><div class="cielo-dia"></div><div class="cielo-alba"></div><div class="cielo-tarde"></div><div class="cielo-noche"></div></div>
<header class="topo" data-topo>
  <nav class="topo-lado" aria-label="Principal">{nav}</nav>
  <a class="topo-marca" href="{inicio}" data-logo-alvo aria-label="IA &amp; Marketing Ferreras, inicio">{logo_svg()}</a>
  <div class="topo-dir">
    <div class="hud" data-hud aria-hidden="true"><div class="hud-txt"><b class="hud-hora" data-hud-hora>07:30<small>MKT</small></b><span class="hud-mom" data-hud-mom></span></div><div class="hud-dock" data-hud-dock><svg class="hud-anillo" data-hud-anillo viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" class="f"/><circle class="v" cx="50" cy="50" r="48" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 50 50)"/></svg></div></div>
    <a class="btn btn-claro topo-cta" href="{R}diagnostico/">{CTA} <span class="fl">→</span></a>
    <button class="menu-botao" type="button" data-menu-botao aria-expanded="false" aria-controls="menu"><span>Menú</span><i></i></button>
  </div>
</header>
<div class="menu" id="menu" data-menu hidden>
  <nav aria-label="Menú"><ul class="menu-lista">{menu}</ul><div class="menu-sub">{sub}</div></nav>
  <div class="menu-pe"><a class="btn btn-claro" href="{R}diagnostico/">{CTA} <span class="fl">→</span></a><p class="mini">{EMAIL}</p></div>
</div>
'''


def rodape(R):
    sis = [("marketing/", "Marketing"), ("inteligencia-artificial/", "Inteligencia artificial"), ("web/", "Web y ecommerce"), ("ia-hoteles/", "IA para hoteles")]
    fir = [("casos/", "Casos"), ("la-casa/", "La casa"), ("contacto/", "Hablemos"), ("diagnostico/", "Ocho preguntas")]

    def col(t, lista):
        li = "".join(f'<li><a href="{R}{h}">{e(x)}</a></li>' for h, x in lista)
        return f"<div><h3>{t}</h3><ul>{li}</ul></div>"
    return f'''<footer class="rodape" data-rodape>
  <div class="rodape-marca">{wordmark_svg()}<p class="rodape-lema">La innovación es lo que distingue a un líder de los demás.</p></div>
  <div class="rodape-cols">
    <div><h3>IA &amp; Marketing Ferreras</h3><address>Passeig de Gràcia 95, 5º 1ª<br>08008 Barcelona<br><a href="mailto:{EMAIL}">{EMAIL}</a></address></div>
    {col("Sistema", sis)}{col("Firma", fir)}{col("Sectores", SECT)}
  </div>
  <div class="rodape-legal"><p>© 2026 IA &amp; Marketing Ferreras · FERRERAS LUXURY GROUP, S.L. · NIF B25958869</p><nav aria-label="Legal"><a href="{R}legal/aviso-legal/">Aviso legal</a><a href="{R}legal/privacidad/">Privacidad</a><a href="{R}legal/cookies/">Cookies</a></nav><p class="concepto">Propuesta de rediseño · concepto</p></div>
</footer>
<div class="barra-dx" data-barra><a class="btn btn-claro" href="{R}diagnostico/">{CTA} <span class="fl">→</span></a></div>
<div class="reloj-voo" data-reloj-voo aria-hidden="true">{reloj_html(R)}</div>
'''


SCRIPTS = ["00-nucleo", "10-abertura", "20-comuns", "30-reloj", "40-escenas", "45-ruta", "70-paginas", "90-luz", "92-alcoba"]
VENDOR = ["gsap.min", "ScrollTrigger.min", "lenis.min"]
FEITAS = []


def pagina(rota, titulo, desc, corpo, inicio=False):
    R = "../" * rota.count("/")
    ab = (f'<div class="abertura" data-abertura aria-hidden="true"><div class="caja">{logo_svg(pecas=True)}</div>'
          '<div class="rasto-w"><i class="rasto"></i><i class="rasto-cab"></i></div></div>') if inicio else ""
    s = "".join(f'<script src="{R}vendor/{n}.js"></script>' for n in VENDOR) + "".join(f'<script src="{R}js/{n}.js?v={VERSAO}"></script>' for n in SCRIPTS)
    cls = ' class="a-abrir"' if inicio else ' class="interior"'
    # a rota do coche (home, computador): estrada em SVG, rasto de luz num canvas, o coche por cima (js/45-ruta.js)
    rt = ('<div class="ruta" data-ruta aria-hidden="true"><svg class="ruta-svg" data-ruta-svg><path class="ruta-p" data-ruta-p d=""/></svg>'
          f'<div class="coche-w" data-coche><span class="feixe"></span>{coche_svg("-r")}</div></div><canvas class="ruta-luz" data-ruta-luz aria-hidden="true"></canvas>') if inicio else ""
    # o reloj 3D da vitrina (só na portada): mapa de importação para o Three.js de vendor/ e o módulo, que carrega tarde
    m3 = (f'<script type="importmap">{{"imports":{{"three":"./{R}vendor/three/three.module.min.js","three/addons/":"./{R}vendor/three/addons/"}}}}</script>'
          f'<script type="module" src="{R}js/93-reloj3d.js?v={VERSAO}"></script>') if inicio else ""
    doc = head(R, titulo, desc, rota) + f"<body{cls}>\n{ab}{cabecera(R, rota)}<main id=\"contenido\">\n{rt}{corpo(R)}\n</main>\n{rodape(R)}{s}{m3}\n</body>\n</html>\n"
    if rota in ("diagnostico/", "contacto/"):
        doc = doc.replace('<div class="barra-dx" data-barra>', '<div class="barra-dx" data-barra hidden>')
    destino = RAIZ / rota / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")
    FEITAS.append(rota)


# ---------------------------------------------------------------- componentes
def etq(a, txt, cls="hora"):
    sp = f'<span class="{cls}">{a}</span>' if a else ""
    return f'<p class="etiqueta">{sp}{txt}</p>'


def L(*ls):
    return "".join(f'<span class="l" style="--i:{i}"><span>{x}</span></span>' for i, x in enumerate(ls))


def btn(href, txt, cls="btn-claro", seta=True, extra=""):
    return f'<a class="btn {cls}" href="{href}"{extra}>{txt}{se(seta, " <span class=" + Q + "fl" + Q + ">→</span>")}</a>'


def cab(num, eti, titulo, lead="", h="h2"):
    ld = f'<p class="lead" data-sube>{lead}</p>' if lead else ""
    return f'<div class="cab">{etq(num, eti, "n")}<{h} class="titulo t-l" data-linhas>{titulo}</{h}>{ld}</div>'


def sec(c, cls="", extra=""):
    return f'<section class="sec {cls}"{extra}>{c}</section>'


def banda(titulo, txt, botoes, extra=""):
    return sec(f'<div class="banda"><div class="cab" style="margin:0"><h2 class="titulo t-l" data-linhas>{titulo}</h2><p class="lead" data-sube>{txt}</p>{extra}</div><div class="acoes">{botoes}</div></div>')


def chips(items, cls="chips"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def arco(R, eti, h1, lead, botoes="", media=None, chips_=None, migas=None, extra="", sobre=""):
    """Cabeça das páginas interiores: título ao centro e, por baixo, a imagem dentro de um arco (o nicho da vitrina).
    Com o scroll o arco abre-se até à largura do ecrã (90-luz.js). Sem imagem fica só o título, mais compacto."""
    m = ""
    if migas:
        partes = [f'<a href="{R}{h}">{e(t)}</a>' if h is not None else e(t) for h, t in migas]
        m = '<p class="migas">' + ' <span aria-hidden="true">/</span> '.join(partes) + "</p>"
    ch = '<ul class="ph-chips">' + "".join(f"<li>{e(c)}</li>" for c in chips_) + "</ul>" if chips_ else ""
    ac = f'<div class="acoes" data-sube>{botoes}</div>' if botoes else ""
    et = etq("", eti, "n") if eti else ""
    med = f'<div class="ah-arco" data-arco><div class="ah-m">{media}</div>{sobre}</div>' if media else ""
    cls = "pag-hero arco-hero" + ("" if media else " sem-media")
    return (f'<section class="{cls}"><div class="ah-cab">{m}{et}<h1 class="titulo t-xl" data-linhas>{h1}</h1></div>{med}'
            f'<div class="ah-pe"><p class="lead" data-sube>{lead}</p>{ac}{ch}{extra}</div></section>')


def ph(R, eti, h1, lead, botoes="", foto=None, chips_=None, migas=None, extra="", sobre=""):
    return arco(R, eti, h1, lead, botoes, foto, chips_, migas, extra, sobre)


CONDICIONES = ["Alcance cerrado por escrito", "Sin permanencia obligatoria", "El proyecto y los accesos son suyos", "Trato uno a uno"]

exec((Path(__file__).parent / "paginas.py").read_text(encoding="utf-8"))
