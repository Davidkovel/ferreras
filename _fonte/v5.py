# Ferreras v5 «Hoja de contactos». Gera o site inteiro: python -I _fonte/v5.py
# Uma arquitectura nova, sem nada da web antiga: cinco salas (Inicio, Trabajo, Servicios, La casa, Hablemos), papel
# de alumínio frio, só a Archivo (eixo de largura: condensada nos títulos, normal no texto), a tinta preta e o
# quadrado azul do logótipo como único acento. A assinatura: uma folha de contactos de fotógrafo; o lápis azul marca
# um fotograma e, com o scroll, esse fotograma cresce até ser o filme. Factos só do site antigo, em «usted».
import json
from html import escape
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
URL = "https://davidkovel.github.io/ferreras/"
EMAIL = "administracion@marketingferreras.com"
MORADA = "Passeig de Gràcia 95, 5º 1ª, 08008 Barcelona"
VERSAO = "9"


def e(s):
    return escape(str(s), quote=True)


# ----------------------------------------------------------------- logótipo, recolorido para papel claro
def _cor(svg, mapa):
    for a, b in mapa.items():
        svg = svg.replace(f'fill="{a}"', f'fill="{b}"')
    return svg


def _corpo(svg):
    return svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]


MARCA = _corpo(_cor((RAIZ / "img/logo-mark-light.svg").read_text(), {"#f6ebe1": "currentColor", "#a19990": "currentColor\" fill-opacity=\".45", "#001dfb": "#001DFB"}))
PALAVRA = _corpo(_cor((RAIZ / "img/logo-wordmark-light.svg").read_text(), {"#e9dcd3": "currentColor"}))


def logo():
    return (f'<svg class="lg-m" viewBox="0 0 235 256" aria-hidden="true">{MARCA}</svg>'
            f'<svg class="lg-w" viewBox="0 0 929 96" aria-hidden="true">{PALAVRA}</svg>')


# ----------------------------------------------------------------- imagens e vídeo
_DIM = {}


def dim(base):
    if base not in _DIM:
        _DIM[base] = Image.open(RAIZ / f"img/{base}-1600.webp").size
    return _DIM[base]


def img(R, base, alt, sizes="100vw", lazy=True, cls=""):
    w, h = dim(base)
    w9 = min(900, w)
    c = f' class="{cls}"' if cls else ""
    lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return (f'<img{c} src="{R}img/{base}-1600.webp" srcset="{R}img/{base}-900.webp {w9}w, {R}img/{base}-1600.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}"{lz}>')


def reel(R, nome, alt):
    """Vídeo vertical do Instagram deles: só descarrega e toca à vista (js)."""
    return (f'<video class="vd" data-vd muted loop playsinline preload="none" poster="{R}video/{nome}-poster.webp" aria-label="{e(alt)}">'
            f'<source data-src="{R}video/{nome}.mp4" type="video/mp4"></video>')


def filme(R, nome, alt, cls="vd"):
    """Filme 16:9 com versão vertical para o telemóvel; o js escolhe 720/1080 pela largura real."""
    return (f'<video class="{cls}" data-vd data-filme="{R}video/{nome}" muted loop playsinline preload="none" '
            f'poster="{R}video/{nome}-720-poster.webp" aria-label="{e(alt)}"></video>')


# ----------------------------------------------------------------- conteúdo (do site antigo, encurtado)
CASOS = [
    dict(id="automocion-voz", sector="automocion", sl="Automoción deportiva", foto=("tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario"),
         t="De publicar coches a ser la voz de referencia del sector",
         p="Una cuenta consolidada cuya presencia digital no reflejaba la autoridad real del negocio ni la calidad de su inventario.",
         i="Una línea editorial reconocible: piezas pensadas para alcance y un formato de podcast propio.",
         r="La cuenta pasó de acompañar al negocio a liderar la conversación de su categoría.",
         ev=["Contenidos con millones de visitas y una media de entre 20.000 y 300.000 visitas por pieza.", "La comunidad se multiplicó durante el periodo de trabajo continuado."]),
    dict(id="hotel-agente", sector="hoteles", sl="Hotel Boltaña Ordesa", foto=("hotel-boltana", "Fachada y terraza de un hotel de montaña rodeado de arbolado"),
         t="Un agente diseñado alrededor de la operativa real de un hotel",
         p="Consultas a cualquier hora, en varios idiomas y por varios canales, y una recepción que no puede estar en todo.",
         i="Un agente a medida, no un chatbot genérico: qué responde, qué consulta y cuándo avisa a una persona.",
         r="Atención continuada en más de veinte idiomas, con derivación a recepción cuando hace falta.", ev=[]),
    dict(id="joyeria-marca", sector="joyeria", sl="Joyería de diamantes", foto=("diamantes-riviere", "Pulsera rivière de diamantes sobre terciopelo azul oscuro"),
         t="Una pieza excepcional necesitaba una marca a su altura",
         p="Producto de primer nivel y una identidad que no comunicaba ni su solvencia ni el ceremonial de una compra así.",
         i="Construir la marca y sus materiales: no solo un logotipo, también con qué se presenta y se cierra una venta.",
         r="Un estándar coherente con el valor del producto, con materiales que sostienen la venta.", ev=[]),
    dict(id="automocion-producto", sector="automocion", sl="Fundas a medida para automoción", foto=("sm-cardress-funda", "Coupé deportivo cubierto con una funda textil a medida"),
         t="Un producto que se entiende en tres segundos",
         p="Un producto premium muy visual, fácil de admirar y difícil de explicar en un catálogo estático.",
         i="El producto como protagonista audiovisual, con entrevistas que aportan contexto y comunidad.",
         r="Se explica solo en el primer visionado: la marca tiene un catálogo audiovisual para vender cada día.",
         ev=["El cliente comunica un impacto comercial directo tras la pieza de mayor alcance."]),
    dict(id="nautica-identidad", sector="nautica", sl="Alquiler de yates, Costa Brava", foto=("yate-completo", "Yate fondeado en una cala de aguas turquesa, visto desde el aire"),
         t="Identidad e infraestructura digital para el alquiler de yates",
         p="Un activo de altísimo valor comercializado con materiales que no transmitían la calidad del barco ni del servicio.",
         i="Primero la identidad y la infraestructura digital, para que cada consulta llegue a un entorno a su altura.",
         r="Una presencia coherente con el producto y con la experiencia a bordo.", ev=[]),
    dict(id="nautica-regatas", sector="nautica", sl="Club náutico, Costa Brava", foto=("regata-dron", "Velero navegando frente a una localidad costera, visto desde el aire"),
         t="Producción y cobertura en vivo en puertos y regatas",
         p="Los eventos náuticos concentran en unas horas el material de un año, y suelen quedar sin dirección ni uso posterior.",
         i="Tratar la cobertura como producción: decidir antes qué historia se cuenta.",
         r="Un archivo audiovisual utilizable durante toda la temporada.", ev=[]),
    dict(id="nautica-compradores", sector="nautica", sl="Venta de una embarcación", foto=("yate-vistas", "Zona exterior de un yate con mesa, asientos y vistas a la costa"),
         t="Compradores de yate sin una cartera previa",
         p="Vender una embarcación de alto valor suele depender de una cartera de contactos de años.",
         i="Alcance dirigido: material a la altura del activo, distribuido donde está el comprador.",
         r="Se alcanzó a compradores cualificados sin cartera propia.", ev=[]),
    dict(id="b2b-vinoteca", sector="b2b", sl="Vinoteca de lujo", foto=None,
         t="Automatización interna en una vinoteca de lujo",
         p="Procesos necesarios, repetitivos y muy consumidores de tiempo.",
         i="Separar lo que podía automatizarse con control de lo que debía seguir en manos de una persona.",
         r="Una reducción sustancial del tiempo dedicado a los procesos incluidos en el alcance.", ev=[]),
]
SECTORES = [("hoteles", "Hotelería", "ia-hotel-atencion-atardecer", "Recepción de un hotel al atardecer"),
            ("automocion", "Automoción", "nissan-gtr", "Nissan GT-R en un estudio"),
            ("nautica", "Náutica", "puerto-club-vela-blanes", "Puerto deportivo de la Costa Brava visto desde el aire"),
            ("joyeria", "Joyería y relojería", "diamantes-anillos", "Dos anillos de diamantes sobre terciopelo")]

MKT = [("Estrategia a doce meses", "Qué tiene que cambiar en la percepción de su empresa, y en qué orden.", "img", "reloj-detalle-f", "Agujas doradas de un reloj Ferreras"),
       ("Producción audiovisual", "Dron, cámaras, sonido e iluminación. Equipo y desplazamientos incluidos.", "reel", "reel-tn-porsche", "Porsche 911 GT3 RS en el estudio de TN Autosport"),
       ("Podcast y entrevistas", "Que se le vea explicando su criterio, no vendiendo su producto.", "reel", "reel-diamantes", "Un joyero explica una pieza ante la cámara"),
       ("Redes y comunidad", "Una línea editorial reconocible, publicada con constancia.", "reel", "reel-ferreras-lifestyle", "Campaña de Relojes Ferreras"),
       ("Publicidad", "Objetivo declarado y medición honesta. La inversión se decide con usted.", "reel", "reel-cardress", "Funda a medida retirándose de un Porsche azul"),
       ("Email y canales de venta", "Recuperar a quien ya le conoce cuesta menos que convencer a quien no.", "img", "diamantes-pulsera-zafiros", "Pulsera de diamantes y zafiros"),
       ("Web, ecommerce y SEO", "Desarrollada por nuestro equipo: una web que cualifica antes de pedir datos.", "img", "reloj-ferreras-almirante", "Reloj Ferreras Almirante en su estuche")]
IA = [("Primero, usted", "Sistemas que le quitan horas a usted antes de tocar la empresa.", "img", "ia-portada-esfera", "Esfera de cristal con gráficos de datos"),
      ("Agentes de atención", "Teléfono, chat, WhatsApp o email, en más de veinte idiomas.", "img", "ia-hotel-multiidioma", "Recepción de hotel atendiendo a un grupo de huéspedes"),
      ("Análisis de la empresa", "Dónde se pierde tiempo y dinero, y qué conviene automatizar.", "img", "ia-hotel-estudio-establecimiento", "Mesa de trabajo con planos y paneles de datos"),
      ("Integraciones", "Conectado a lo que ya usa. Solo lectura por defecto.", "img", "ia-hotel-capacidades", "Vestíbulo de hotel con paneles de información"),
      ("Control y mejora", "Permisos, registro y revisión de conversaciones reales.", "img", "ia-hotel-recepcion-equipo", "Recepcionista atendiendo a una huésped"),
      ("Formación a su equipo", "Para que lo que se implanta se use, y se use bien.", "img", "rodaje-hotel-salon", "Rodaje en el salón de un hotel")]

NAV = [("trabajo/", "Trabajo"), ("servicios/", "Servicios"), ("casa/", "La casa")]


# ----------------------------------------------------------------- casca
def head(R, rota, titulo, desc):
    t = titulo if not rota else f"{titulo} | IA & Marketing Ferreras"
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "IA & Marketing Ferreras", "legalName": "FERRERAS LUXURY GROUP, S.L.",
           "url": "https://www.marketingferreras.com/", "email": EMAIL,
           "address": {"@type": "PostalAddress", "streetAddress": "Passeig de Gràcia 95, 5º 1ª", "postalCode": "08008", "addressLocality": "Barcelona", "addressCountry": "ES"}}
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{URL}{rota}">
<meta name="theme-color" content="#E4E4DF">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{URL}{rota}"><meta property="og:image" content="{URL}og/inicio.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{R}fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}estilo.css?v={VERSAO}">
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>'''


def cabecera(R, rota):
    li = "".join(f'<li><a href="{R}{h}"{" aria-current=" + chr(34) + "page" + chr(34) if rota.startswith(h) else ""}>{t}</a></li>' for h, t in NAV)
    grande = "".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in NAV + [("hablemos/", "Hablemos")])
    return f'''<a class="salta" href="#conteudo">Saltar al contenido</a>
<header class="cab" data-cab>
  <a class="cab-logo" href="{R}" aria-label="IA &amp; Marketing Ferreras, inicio">{logo()}</a>
  <nav class="cab-nav" aria-label="Principal"><ul>{li}</ul></nav>
  <a class="pilula cab-cta" href="{R}hablemos/">Hablemos</a>
  <button class="cab-menu" type="button" aria-expanded="false" aria-controls="menu" data-menu-abre>Menú</button>
</header>
<div class="menu" id="menu" data-menu hidden>
  <button class="cab-menu menu-fecha" type="button" data-menu-fecha>Cerrar</button>
  <ul class="menu-l">{grande}</ul>
  <p class="menu-pe"><a href="mailto:{EMAIL}">{EMAIL}</a><br>{MORADA}</p>
</div>'''


def rodape(R):
    return f'''<footer class="rod" data-escuro>
  <div class="rod-g">
    <div><p class="rod-t">IA &amp; Marketing Ferreras</p><address>Passeig de Gràcia 95, 5º 1ª<br>08008 Barcelona<br><a href="mailto:{EMAIL}">{EMAIL}</a></address></div>
    <ul class="rod-l">{"".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in NAV + [("hablemos/", "Hablemos")])}</ul>
    <ul class="rod-l"><li><a href="{R}legal/aviso-legal/">Aviso legal</a></li><li><a href="{R}legal/privacidad/">Privacidad</a></li><li><a href="{R}legal/cookies/">Cookies</a></li></ul>
  </div>
  <div class="rod-marca" aria-hidden="true"><svg viewBox="0 0 929 96">{PALAVRA}</svg></div>
  <p class="rod-pe">© 2026 FERRERAS LUXURY GROUP, S.L., NIF B25958869. Propuesta de rediseño, no es la web oficial.</p>
</footer>'''


FEITAS = []


def pagina(rota, titulo, desc, corpo, classe=""):
    R = "../" * rota.count("/")
    html = (head(R, rota, titulo, desc) + f'\n<body class="{classe}">\n' + cabecera(R, rota)
            + f'\n<main id="conteudo">\n{corpo(R)}\n</main>\n' + rodape(R)
            + f'\n<script>window.FERRERAS={{raiz:"{R}",email:"{EMAIL}"}}</script>\n<script src="{R}js/sitio.js?v={VERSAO}" defer></script>\n</body>\n</html>\n')
    destino = RAIZ / rota / "index.html" if rota else RAIZ / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")
    FEITAS.append(rota)


def pilula(href, txt, cls=""):
    return f'<a class="pilula {cls}" href="{href}">{txt}</a>'


def cierre(R, titulo="¿Hablamos de su marca?"):
    """O fecho de cada sala: preto, a pergunta e as duas vias. Ao fundo continua o rodapé."""
    return f'''<section class="cierre" data-escuro>
  <h2 class="t-xxl">{titulo}</h2>
  <div class="cierre-vias">
    <div><p class="t-m">Ocho preguntas y una recomendación concreta en el acto.</p>{pilula(R + "hablemos/#conversacion", "Responder las preguntas", "clara")}</div>
    <div><p class="t-m">O escríbanos directamente. Responde una persona en un día laborable.</p><a class="enl" href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
</section>'''


# ----------------------------------------------------------------- INICIO
HOJA = [("tn-autosport-deportivos", "Coches deportivos en un concesionario"), ("diamantes-riviere", "Pulsera de diamantes"), ("yate-completo", "Yate en una cala"),
        ("reloj-ferreras-almirante", "Reloj Ferreras Almirante"), None, ("hotel-boltana", "Hotel de montaña"),
        ("regata-dron", "Regata desde el aire"), ("sm-cardress-funda", "Funda a medida sobre un coupé"), ("ia-hotel-atencion-atardecer", "Recepción de hotel al atardecer")]


def lapiz():
    # o traço do lápis azul de quem escolhe o fotograma: um rectângulo à mão, que fecha a passar do início
    return ('<svg class="lapiz" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
            '<path pathLength="1" d="M4 7 C30 3.5 70 5 97 6.5 C96 35 97.5 68 95.5 94 C66 96.5 32 95 4.5 93.5 C3 66 5 33 3.5 9 C4 6 9 4.5 16 5"/></svg>')


def inicio(R):
    fr = []
    for k in HOJA:
        if k is None:
            fr.append(f'<figure class="fr fr-marcado" data-marcado>{filme(R, "hero", "Fragmentos de rodajes propios: coches, relojes y estilo de vida")}{lapiz()}</figure>')
        else:
            fr.append(f'<figure class="fr">{img(R, k[0], k[1], "(min-width: 900px) 20vw, 34vw", lazy=False)}</figure>')
    hoja = f'''<section class="hoja" data-hoja>
  <div class="hoja-palco" data-palco>
    <div class="hoja-txt" data-hoja-txt>
      <h1 class="t-xl">Rodamos su marca. Atendemos a sus clientes.</h1>
      <p class="t-m">Marketing e inteligencia artificial para marcas de lujo, desde Barcelona.</p>
      {pilula(R + "hablemos/", "Hablemos de su marca")}
    </div>
    <div class="folha" data-folha>{"".join(fr)}</div>
    <p class="hoja-pie" data-hoja-pie>Planos de nuestros rodajes para TN Autosport, Relojes Ferreras y SM CarDress.</p>
  </div>
</section>'''

    oficio = lambda href, nome, media, txt: (f'<a class="oficio" href="{href}"><span class="of-nome t-xxl">{nome}</span>'
                                              f'<span class="of-media">{media}</span><span class="of-txt t-m">{txt}</span></a>')
    oficios = f'''<section class="oficios">
  <h2 class="t-l sec-t">Dos oficios y un solo equipo, dentro de su empresa.</h2>
  {oficio(R + "servicios/#marketing", "Marketing", reel(R, "reel-tn-porsche", "Porsche 911 GT3 RS en el estudio de TN Autosport"),
          "Estrategia a doce meses, producción propia con dron y equipo, podcast, redes, publicidad, email y web.")}
  {oficio(R + "servicios/#ia", "Inteligencia artificial", img(R, "ia-hotel-atencion-atardecer", "Recepción de un hotel al atardecer", "(min-width: 900px) 30vw, 100vw"),
          "Agentes que atienden en más de veinte idiomas, integraciones con sus sistemas y automatización de procesos.")}
</section>'''

    filas = "".join(
        f'<li><a href="{R}trabajo/#{c["id"]}" data-prev="{R}img/{c["foto"][0]}-900.webp"><span class="tl-s">{e(c["sl"])}</span>'
        f'<span class="tl-t">{e(c["t"])}</span><span class="tl-img">{img(R, c["foto"][0], c["foto"][1], "40vw")}</span></a></li>'
        for c in CASOS if c["foto"])
    trabajo = f'''<section class="trab">
  <div class="sec-cab"><h2 class="t-l">Trabajo reciente</h2><a class="enl" href="{R}trabajo/">Ver todos los casos</a></div>
  <ul class="tl" data-tl>{filas}</ul>
  <figure class="tl-cursor" data-cursor aria-hidden="true"><img alt="" width="900" height="600"></figure>
</section>'''

    relojes = f'''<section class="relojes" data-escuro>
  <picture class="rl-foto">
    <source media="(max-width: 700px)" srcset="{R}img/reloj-detalle-firma-900.webp 900w, {R}img/reloj-detalle-firma-1600.webp 1038w" sizes="100vw">
    {img(R, "reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche", "(min-width: 701px) 1600px, 100vw")}
  </picture>
  <div class="rl-txt">
    <h2 class="t-xxl">Relojes Ferreras</h2>
    <p class="t-m">Antes de proponerle nada, lo hicimos con lo nuestro: una marca de relojes con diseño propio, mecanismo suizo y ensamblaje en Barcelona.</p>
    <a class="enl" href="{R}casa/">Conocer la casa</a>
  </div>
</section>'''

    cifras = f'''<section class="cifras">
  <div class="cf"><b class="t-xxl">20+</b><p>idiomas en los que atiende un agente, por teléfono, chat, WhatsApp o email.</p></div>
  <div class="cf"><b class="t-xxl">24 h</b><p>de atención, también cuando la recepción está cerrada.</p></div>
  <div class="cf cf-larga"><b class="t-xl">20.000–300.000</b><p>visitas de media por pieza en la línea editorial de un cliente de automoción deportiva.</p></div>
</section>'''
    return hoja + oficios + trabajo + relojes + cifras + cierre(R)


pagina("", "IA & Marketing Ferreras, marketing e inteligencia artificial para marcas de lujo",
       "Rodamos su marca y atendemos a sus clientes. Marketing e inteligencia artificial para marcas de lujo desde Barcelona: hotelería, automoción, náutica y joyería.",
       inicio, "inicio")


# ----------------------------------------------------------------- TRABAJO
def caso(R, c, i):
    if c["foto"]:
        foto = img(R, c["foto"][0], c["foto"][1], "(min-width: 900px) 58vw, 100vw")
    else:
        foto = f'<div class="cs-sin"><svg viewBox="0 0 235 256" aria-hidden="true">{MARCA}</svg><span>Sin imagen pública por confidencialidad</span></div>'
    ev = "".join(f"<li>{e(x)}</li>" for x in c["ev"])
    ev = f'<ul class="cs-ev">{ev}</ul>' if ev else ""
    return f'''<article class="cs{" cs-inv" if i % 2 else ""}" id="{c["id"]}" data-sector="{c["sector"]}">
  <figure class="cs-foto">{foto}</figure>
  <div class="cs-txt">
    <p class="cs-s">{e(c["sl"])}</p>
    <h2 class="t-l">{e(c["t"])}</h2>
    <dl><div><dt>El punto de partida</dt><dd>{e(c["p"])}</dd></div><div><dt>Lo que hicimos</dt><dd>{e(c["i"])}</dd></div><div><dt>El resultado</dt><dd>{e(c["r"])}</dd></div></dl>
    {ev}
  </div>
</article>'''


def trabajo(R):
    filtros = [("", "Todo")] + [(k, t) for k, t, _, _ in SECTORES] + [("b2b", "B2B y servicios")]
    fb = "".join(f'<button type="button" data-filtro="{k}" aria-pressed="{"true" if not k else "false"}">{t}</button>' for k, t in filtros)
    return f'''<section class="ph">
  <h1 class="t-xxl">Trabajo</h1>
  <p class="t-m ph-l">Cada caso con su punto de partida, lo que hicimos y el resultado. Publicamos cifras solo cuando están verificadas y el cliente lo autoriza.</p>
</section>
<div class="filtros" role="group" aria-label="Filtrar por sector">{fb}</div>
<section class="casos" data-casos>{"".join(caso(R, c, i) for i, c in enumerate(CASOS))}</section>
<section class="propia">
  <figure>{img(R, "reloj-detalle-firma", "Esfera de un reloj Ferreras con el logotipo de la casa", "(min-width: 900px) 40vw, 100vw")}</figure>
  <div><p class="cs-s">Marca propia</p><h2 class="t-l">Relojes Ferreras, nuestro banco de pruebas</h2>
  <p class="t-m">Crear una marca de relojería obliga a resolver en casa lo mismo que un cliente encarga a una agencia. Lo que le recomendamos, lo hemos aplicado antes con lo nuestro.</p>
  <a class="enl" href="{R}casa/">Conocer la casa</a></div>
</section>''' + cierre(R)


pagina("trabajo/", "Trabajo", "Casos de marketing e inteligencia artificial en hotelería, automoción, náutica y joyería, con punto de partida, intervención y resultado.", trabajo)


# ----------------------------------------------------------------- SERVICIOS
def campo(id_, nome, rot, tipo="text", req="", auto="", opc=False, extra=""):
    lab = rot + (" <small>(opcional)</small>" if opc else "")
    r = f' data-req="{req}"' if req else ""
    a = f' autocomplete="{auto}"' if auto else ""
    return f'<div class="campo"><label for="{id_}">{lab}</label><input id="{id_}" name="{nome}" type="{tipo}"{a}{r}{extra}><span class="erro" id="{id_}-erro"></span></div>'


def area(id_, nome, rot, req="", ph="", opc=False):
    lab = rot + (" <small>(opcional)</small>" if opc else "")
    r = f' data-req="{req}" data-min="10"' if req else ""
    return f'<div class="campo largo"><label for="{id_}">{lab}</label><textarea id="{id_}" name="{nome}" rows="3" placeholder="{e(ph)}"{r}></textarea><span class="erro" id="{id_}-erro"></span></div>'


def opcoes(nome, legenda, ops, pre=0):
    ls = "".join(f'<label><input type="radio" name="{nome}" value="{e(v)}"{" checked" if j == pre else ""}><span>{e(v)}</span></label>' for j, v in enumerate(ops))
    return f'<fieldset class="campo largo opcoes"><legend>{legenda}</legend><div>{ls}</div></fieldset>'


def consentimento(R, pref):
    return (f'<div class="campo largo consent"><label class="check"><input type="checkbox" id="{pref}-ok" name="consentimiento" data-req="Necesitamos su consentimiento para poder responderle.">'
            f'<span>He leído la <a href="{R}legal/privacidad/">política de privacidad</a> y acepto que Ferreras me contacte sobre esta solicitud.</span></label><span class="erro" id="{pref}-ok-erro"></span></div>')


TRAMPA = '<input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">'


def envio(ok):
    return (f'<div class="envio" data-envio aria-live="polite"><p data-e="a" hidden>Enviando…</p>'
            f'<div data-e="ok" hidden><b>{ok}</b><p>Una persona del equipo la revisa y le responde en un día laborable.</p></div>'
            f'<div data-e="ko" hidden><b>No hemos podido conectar.</b><p>Sus datos siguen escritos. Puede reintentarlo o escribirnos a <a data-mailto href="mailto:{EMAIL}">{EMAIL}</a>.</p></div></div>')


def linhas_servico(R, itens):
    out = []
    for t, d, tipo, base, alt in itens:
        m = reel(R, base, alt) if tipo == "reel" else img(R, base, alt, "(min-width: 900px) 22vw, 40vw")
        out.append(f'<li class="sv"><h3 class="t-l">{t}</h3><p>{d}</p><figure class="sv-m{" sv-v" if tipo == "reel" else ""}">{m}</figure></li>')
    return f'<ul class="svs">{"".join(out)}</ul>'


def servicios(R):
    hab = ["Menos de 20 habitaciones", "Entre 20 y 50", "Entre 50 y 100", "Entre 100 y 200", "Más de 200", "Varios establecimientos"]
    form_hotel = (f'<form class="form" data-lead="hotel" novalidate><div class="campos">'
                  + campo("h-nome", "nombre", "Nombre", req="Indique su nombre.", auto="name")
                  + campo("h-emp", "hotel", "Hotel o establecimiento", req="Indique el nombre del establecimiento.", auto="organization")
                  + campo("h-tel", "telefono", "Teléfono", "tel", req="Necesitamos un teléfono para poder llamarle.", auto="tel", extra=' data-min-dig="6"')
                  + campo("h-mail", "email", "Email", "email", req="Revise la dirección de email.", auto="email")
                  + opcoes("habitaciones", "Habitaciones", hab, 1)
                  + area("h-mej", "mejora", "Qué quiere mejorar o automatizar", ph="Por ejemplo: reservas fuera de horario, preguntas repetidas, idiomas.", opc=True)
                  + consentimento(R, "h") + TRAMPA
                  + f'</div><button class="pilula" type="submit">Pedir el estudio de mi hotel</button>{envio("Solicitud recibida")}</form>')
    cap = ["Atender llamadas con una conversación real, no un menú.", "Responder lo de siempre con los datos de su casa.", "Hablar el idioma del huésped con el mismo criterio.",
           "Pasar a una persona con el contexto ya recogido.", "Conectarse a sus sistemas, según API y permisos.", "Seguir los protocolos que definimos con usted."]
    planos = [("Web Signature", "Sobria y a la altura del negocio.", ["Diseño personalizado", "Hasta 5 páginas", "Copy, responsive y SEO básico"]),
              ("Web de Captación", "Cualifica y produce oportunidades.", ["Hasta 10–12 páginas", "Casos y sistema de prueba", "Cualificación del visitante", "CRM y medición"]),
              ("Ecommerce", "Catálogo y venta conectada.", ["Arquitectura de conversión", "Pagos, envíos y analítica", "SEO base y lanzamiento"])]
    pl = "".join(f'<div class="pl"><h3 class="t-l">{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></div>' for t, d, xs in planos)
    sect = "".join(f'<a class="st" href="{R}trabajo/?sector={k}"><figure>{img(R, b, a, "(min-width: 900px) 25vw, 50vw")}</figure><span>{t}</span></a>' for k, t, b, a in SECTORES)
    return f'''<section class="ph">
  <h1 class="t-xxl">Servicios</h1>
  <p class="t-m ph-l">Un departamento de marketing y otro de inteligencia artificial, montados dentro de su empresa con un solo plan. Sin contratar, formar ni coordinar a nadie.</p>
</section>
<section class="sv-bloco" id="marketing">
  <div class="sv-cab"><h2 class="t-xxl">Marketing</h2><p class="t-m">Que se le vea como lo que es: el referente de su sector.</p></div>
  <figure class="sv-filme">{filme(R, "mkt", "Producción propia: rodajes de automoción, relojería y estilo de vida")}</figure>
  {linhas_servico(R, MKT)}
</section>
<section class="sv-bloco" id="ia">
  <div class="sv-cab"><h2 class="t-xxl">Inteligencia artificial</h2><p class="t-m">Que nadie se quede sin respuesta, y que su equipo recupere las horas que hoy se van en lo repetitivo.</p></div>
  {linhas_servico(R, IA)}
</section>
<section class="hoteles" id="hoteles" data-escuro>
  <div class="ht-txt">
    <h2 class="t-xl">Su hotel puede atender 24 horas, en cualquier idioma, sin ampliar recepción.</h2>
    <ul class="ht-cap">{"".join(f"<li>{x}</li>" for x in cap)}</ul>
    <p class="ht-nota">Caso real: un agente diseñado alrededor de la operativa del Hotel Boltaña Ordesa. <a class="enl" href="{R}trabajo/#hotel-agente">Ver el caso</a></p>
  </div>
  <div class="ht-form"><p class="t-m">Estudiamos su establecimiento antes de proponer nada.</p>{form_hotel}</div>
</section>
<section class="web" id="web">
  <div class="sv-cab"><h2 class="t-xl">Una web no debería explicar su empresa. Debería venderla.</h2>
  <p class="t-m">Desarrollo propio. Alcance y precio por escrito antes de empezar.</p></div>
  <div class="pls">{pl}</div>
  <p class="web-pe">Pago en tres partes: 50 % al inicio, 30 % con el diseño aprobado y 20 % antes de publicar. Multidioma, vídeo, configuradores o áreas privadas se presupuestan como proyecto aparte.</p>
</section>
<section class="sects">
  <h2 class="t-l sec-t">Cuatro sectores que conocemos por dentro</h2>
  <div class="sts">{sect}</div>
</section>''' + cierre(R)


pagina("servicios/", "Servicios", "Marketing e inteligencia artificial dentro de su empresa: estrategia, producción audiovisual propia, redes, publicidad, web, agentes de atención en más de veinte idiomas y automatización.", servicios)


# ----------------------------------------------------------------- LA CASA
def casa(R):
    marcas = [("reloj-ferreras-almirante", "Reloj Ferreras Almirante en su estuche", "Relojes Ferreras", "Relojería, marca propia"),
              ("tn-autosport-deportivos", "Coches deportivos en un concesionario", "TN Autosport", "Automoción"),
              ("hotel-boltana", "Hotel de montaña rodeado de arbolado", "Hotel Boltaña Ordesa", "Hotelería"),
              ("puerto-club-vela-blanes", "Puerto deportivo visto desde el aire", "Club náutico", "Náutica, Costa Brava"),
              ("diamantes-anillos", "Anillos de diamantes sobre terciopelo", "Joyería de diamantes", "Joyería, España"),
              ("sm-cardress-funda", "Coupé cubierto con una funda a medida", "SM CarDress", "Producto para automoción")]
    mh = "".join(f'<figure class="mc">{img(R, b, a, "(min-width: 900px) 30vw, 50vw")}<figcaption><b>{t}</b><span>{s}</span></figcaption></figure>' for b, a, t, s in marcas)
    return f'''<section class="ph ph-casa">
  <h1 class="t-xxl">La casa</h1>
  <p class="t-m ph-l">Llevamos el marketing de marcas de referencia en su sector, como TN Autosport en automoción, y somos los creadores de Relojes Ferreras.</p>
</section>
<section class="marcas"><h2 class="t-l sec-t">Marcas que llevamos</h2><div class="mcs">{mh}</div></section>
<section class="estandar">
  <figure>{img(R, "fernando-ferreras-ceo", "Fernando Ferreras en un puerto deportivo, junto a dos vehículos de alta gama", "(min-width: 900px) 40vw, 100vw")}<figcaption>Fernando Ferreras, dirección</figcaption></figure>
  <div>
    <p class="t-xl">El lujo no es una etiqueta. Es un estándar de ejecución.</p>
    <p class="t-m">Pocas empresas, muy de cerca. La dirección entra en cada proyecto y no se delega.</p>
  </div>
</section>
<section class="relojes relojes-casa" data-escuro>
  <picture class="rl-foto">{img(R, "reloj-detalle-f", "Detalle de las agujas doradas de un reloj Ferreras", "100vw")}</picture>
  <div class="rl-txt">
    <h2 class="t-xxl">Relojes Ferreras</h2>
    <p class="t-m">Una marca de relojes automáticos de autor: diseño propio, mecanismo suizo y ensamblaje en Barcelona. Nació dentro de esta agencia para demostrar que nuestras estrategias funcionan cuando somos nosotros quienes asumimos las consecuencias.</p>
  </div>
</section>
<section class="dir">
  <h2 class="t-l">Dónde estamos</h2>
  <p class="t-m">{MORADA}</p>
  <p><a class="enl" href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>''' + cierre(R)


pagina("casa/", "La casa", "Llevamos el marketing de marcas de referencia en su sector, como TN Autosport, y somos los creadores de Relojes Ferreras. Barcelona.", casa)


# ----------------------------------------------------------------- HABLEMOS
def hablemos(R):
    form = (f'<form class="form" data-lead="contacto" novalidate><div class="campos">'
            + campo("c-nome", "nombre", "Nombre", req="Indique su nombre.", auto="name")
            + campo("c-emp", "empresa", "Empresa", req="Indique el nombre de su empresa.", auto="organization")
            + campo("c-mail", "email", "Email", "email", req="Revise la dirección de email.", auto="email")
            + campo("c-tel", "telefono", "Teléfono", "tel", auto="tel", opc=True)
            + campo("c-cargo", "cargo", "Cargo", auto="organization-title", opc=True)
            + opcoes("sector", "Sector", ["Hotelería", "Automoción", "Náutica", "Joyería", "Otro"])
            + opcoes("plazo", "Plazo", ["Inmediato", "En 30–90 días", "El próximo trimestre", "Solo estoy explorando"])
            + area("c-msg", "objetivo", "Qué quiere conseguir", req="Cuéntenos brevemente qué necesita.", ph="Dos líneas bastan: qué quiere conseguir y qué le frena.")
            + opcoes("preferencia", "Prefiero que me contacten por", ["email", "telefono", "whatsapp"]).replace(">email<", ">Email<").replace(">telefono<", ">Teléfono<").replace(">whatsapp<", ">WhatsApp<")
            + consentimento(R, "c") + TRAMPA
            + f'</div><button class="pilula" type="submit">Enviar mensaje</button>{envio("Mensaje recibido")}</form>')
    return f'''<section class="ph">
  <h1 class="t-xxl">Hablemos</h1>
  <p class="t-m ph-l">Ocho preguntas con una recomendación en el acto, o un mensaje directo. En los dos casos le responde una persona en un día laborable.</p>
</section>
<section class="hab">
  <div class="conv" id="conversacion" data-conv aria-live="polite">
    <h2 class="t-l">Ocho preguntas, dos minutos</h2>
    <ol class="conv-l" data-conv-l></ol>
    <div class="conv-ops" data-conv-ops></div>
  </div>
  <aside class="msg">
    <h2 class="t-l">Un mensaje directo</h2>
    {form}
    <p class="msg-pe">{MORADA}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </aside>
</section>'''


pagina("hablemos/", "Hablemos", "Ocho preguntas y una recomendación concreta en el acto, o un mensaje directo. Le responde una persona en un día laborable.", hablemos)


# ----------------------------------------------------------------- legal, 404 e endereços antigos
LEGAL = json.loads((RAIZ / "_fonte/legal.json").read_text(encoding="utf-8"))


def legal(slug):
    def corpo(R):
        out = []
        for x in LEGAL[slug]:
            if x.startswith("[h1] "):
                out.append(f'<h1 class="t-xl">{e(x[5:])}</h1>')
            elif x.startswith("[h2] "):
                out.append(f'<h2>{e(x[5:])}</h2>')
            else:
                out.append(f"<p>{e(x)}</p>")
        return f'<article class="legal">{"".join(out)}</article>'
    titulo = LEGAL[slug][0][5:]
    pagina(f"legal/{slug}/", titulo, f"{titulo} de IA & Marketing Ferreras.", corpo)


for s in LEGAL:
    legal(s)


def p404(R):
    return f'<section class="ph p404"><h1 class="t-xxl">Esta página no existe</h1><p class="t-m ph-l">Puede que la dirección haya cambiado.</p>{pilula(R, "Volver al inicio")}</section>'


pagina("404/", "Página no encontrada", "La página que busca no existe.", p404)
(RAIZ / "404.html").write_text((RAIZ / "404/index.html").read_text(encoding="utf-8").replace('="../', '="/ferreras/'), encoding="utf-8")

ANTIGAS = {"marketing/": "servicios/#marketing", "inteligencia-artificial/": "servicios/#ia", "web/": "servicios/#web", "ia-hoteles/": "servicios/#hoteles",
           "sectores/": "trabajo/", "sectores/hoteles/": "trabajo/?sector=hoteles", "sectores/automocion-lujo/": "trabajo/?sector=automocion",
           "sectores/nautica/": "trabajo/?sector=nautica", "sectores/joyeria-relojeria/": "trabajo/?sector=joyeria",
           "resultados/": "trabajo/", "casos/": "trabajo/", "quien-somos/": "casa/", "contacto/": "hablemos/", "diagnostico/": "hablemos/#conversacion"}
for velha, nova in ANTIGAS.items():
    R = "../" * velha.count("/")
    d = RAIZ / velha
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Ferreras</title>'
                                  f'<meta http-equiv="refresh" content="0; url={R}{nova}"><link rel="canonical" href="{URL}{nova}"><a href="{R}{nova}">Continuar</a>\n', encoding="utf-8")

(RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                  + "".join(f"  <url><loc>{URL}{r}</loc></url>\n" for r in FEITAS if r != "404/") + "</urlset>\n", encoding="utf-8")
print("paginas:", len(FEITAS), FEITAS)
