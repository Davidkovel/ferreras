# Conteúdo das páginas. Corre dentro do build.py (exec), por isso usa as funções de lá.
# Regra da casa: três segundos de atenção por ecrã. Cada secção é uma imagem ou um vídeo que se vê antes de se ler,
# um título curto e, no máximo, uma linha. O detalhe vive nas páginas interiores, também com imagem primeiro.
# Nada inventado: os textos vêm do site antigo, em «usted» e encurtados. Expressões das f-strings com aspas do outro tipo.

DIAG = "diagnostico/"


def enlace(href, txt, ext=False):
    alvo = ' target="_blank" rel="noopener"' if ext else ""
    seta = "↗" if ext else "→"
    return f'<a class="enlace" href="{href}"{alvo}>{txt} <span class="fl">{seta}</span></a>'


def figura(R, base, alt, cap_b="", cap="", cls="", sizes="(min-width: 900px) 40vw, 100vw", janela=True):
    jan = " data-janela" if janela else ""
    fc = f'<figcaption class="pie"><b>{cap_b}</b>{cap}</figcaption>' if (cap_b or cap) else ""
    return f'<figure class="{cls}"><div class="ventana"{jan}>{img(R, base, alt, sizes)}</div>{fc}</figure>'


def filme(R, nome, cls=""):
    """Vídeo de fundo: horizontal no computador, vertical no telemóvel ao alto. O cartaz é um <picture> por baixo,
    o vídeo aparece por cima quando há fotogramas a sério (js/20-comuns.js). As montagens nítidas (showreel2.py)
    têm duas resoluções de cada lado e o JS escolhe pelo ecrã; as outras são um par -h/-v simples."""
    preguica = " data-lazy" if "lazy" in cls.split() else ""
    carga = ' loading="lazy"' if preguica else ' fetchpriority="high"'
    v = f"{R}video/{nome}"
    mv = '<source media="(max-width: 899px) and (orientation: portrait)"'
    if (RAIZ / "video" / f"{nome}-1080.mp4").exists():
        pic = (f'{mv} srcset="{v}-v720-poster.webp 720w, {v}-v1080-poster.webp 1080w" sizes="100vw">'
               f'<img src="{v}-1080-poster.webp" srcset="{v}-720-poster.webp 1280w, {v}-1080-poster.webp 1920w" sizes="100vw" alt=""{carga}>')
        fontes = f'data-src-h="{v}-720.mp4?v={VERSAO}" data-src-hd="{v}-1080.mp4?v={VERSAO}" data-src-v="{v}-v720.mp4?v={VERSAO}" data-src-vd="{v}-v1080.mp4?v={VERSAO}"'
    else:
        pic = f'{mv} srcset="{v}-v-poster.webp"><img src="{v}-h-poster.webp" alt=""{carga}>'
        fontes = f'data-src-h="{v}-h.mp4?v={VERSAO}" data-src-v="{v}-v.mp4?v={VERSAO}"'
    return (f'<div class="filme {cls}" aria-hidden="true"><picture>{pic}</picture>'
            f'<video muted playsinline loop preload="{"none" if preguica else "auto"}" data-filme{preguica} {fontes}></video></div>')


def ph_media(R, eti, h1, lead, botoes, media, migas=None, sobre=""):
    """Hero de página interior com imagem ou filme: o mesmo arco que ph()."""
    return arco(R, eti, h1, lead, botoes, media, None, migas, "", sobre)


def fundo_img(R, base, alt):
    return img(R, base, alt, "100vw", lazy=False)


# el guion de la demostración de la web original (página del Departamento de IA)
CHAT = [
    ("cliente", "Cliente", "Guten Abend, haben Sie am Wochenende noch ein Doppelzimmer frei?"),
    ("agente", "Agente", "Guten Abend. Ich prüfe die verfügbaren Informationen für das Wochenende. Einen Moment, bitte."),
    ("sistema", "", "Consulta a fuente conectada · solo lectura"),
    ("agente", "Agente", "Para ese fin de semana figura disponibilidad en habitación doble. El check-in es a partir de las 15:00 y el parking es gratuito."),
    ("cliente", "Cliente", "¿Pueden aplicarme la tarifa de grupo? Somos catorce personas."),
    ("sistema corte", "", "Fuera de alcance autorizado · transferencia a recepción"),
    ("agente", "Agente", "Una reserva de grupo la valora directamente recepción para ofrecerle la mejor condición. Le paso el contacto ahora con todo lo que hemos hablado, para que no tenga que repetir nada."),
]
AVISO_DEMO = "Guion fijo con fines ilustrativos. No es una conversación en vivo ni refleja disponibilidad, tarifas ni datos reales de ningún establecimiento."


def chat_html():
    ms = "".join(f'<p class="msg {c}">{se(bool(q), "<small>" + q + "</small>")}{e(t)}</p>' for c, q, t in [CHAT[i] for i in (0, 3, 4, 5, 6)])
    return (f'<div class="chat" role="log" aria-live="polite" aria-label="Simulación de una conversación con un agente de atención">'
            f'<p class="chat-ej">Ejemplo · así respondería su agente</p><div class="chat-cab"><b><i aria-hidden="true"></i>Agente de atención · Hotel</b><span>Simulación ilustrativa</span></div>'
            f'<div class="chat-lista">{ms}</div>'
            f'<div class="chat-pe"><span class="escribe" data-escribe hidden aria-hidden="true"><i></i><i></i><i></i></span><span>Permisos: solo lectura · registro activo</span></div></div>')


MKT_LISTA = ["Estrategia a 12 meses", "Podcast y entrevistas", "Vídeo y fotografía", "Redes y publicidad", "Imagen profesional", "Equipo y desplazamientos"]
IA_LISTA = ["Sistemas para su día a día", "Análisis de su empresa", "Agentes y automatizaciones", "Mejoras continuas", "Formación a su equipo"]


def sect_html(R, compacto=False):
    S = [("sectores/hoteles/", "sector-hotel-servicio", "Cava servido en la terraza de un evento, con la sala del restaurante al fondo", "Hotelería", "Hoteles", "Más reservas y una marca que se recomienda."),
         ("sectores/automocion-lujo/", "sector-auto-gt3", "Porsche 911 GT3 verde trazando una curva en circuito", "Automoción", "Automoción de lujo", "Contenido que enamora y vende coches."),
         ("sectores/nautica/", "sector-mar-puerto", "Puerto deportivo de la Costa Brava visto desde el aire", "Náutica", "Náutica, yates y puertos", "El mar, vivido antes de zarpar."),
         ("sectores/joyeria-relojeria/", "sector-joya-esmeralda", "Anillo de esmeralda y diamantes sobre terciopelo negro", "Joyería", "Joyería y relojería", "Lujo que se desea y se recuerda.")]
    out = []
    for i, (h, b, alt, eti, t, p) in enumerate(S):
        out.append(f'<a href="{R}{h}">{img(R, b, alt, "(min-width: 900px) 1600px, 100vw")}<span class="etiqueta">{eti}</span><h3>{t}</h3><p>{p}</p><span class="fl" aria-hidden="true">→</span></a>')
    return f'<div class="sect{se(compacto, " baixo")}">{"".join(out)}</div>'


def carril(R, itens, rotulo):
    fig = []
    for b, o, alt, s, c in itens:
        m = video(R, b[4:], alt) if b.startswith("vid:") else img(R, b, alt, "(min-width: 900px) 26vw, 72vw")
        fig.append(f'<figure class="carril-item {o}"><div class="ventana">{m}</div><figcaption class="pie"><b>{s}</b>{c}</figcaption></figure>')
    n = len(itens)
    ctl = (f'<div class="carril-ctl"><button type="button" class="carril-b" data-carril-ant aria-label="Anterior">←</button>'
           f'<span class="carril-n" data-carril-n>01 / {n:02d}</span><button type="button" class="carril-b" data-carril-prox aria-label="Siguiente">→</button></div>')
    return ctl, (f'<div class="carril" data-carril tabindex="0" role="region" aria-label="{e(rotulo)}">{"".join(fig)}</div>'
                 f'<div class="carril-barra" aria-hidden="true"><i data-carril-barra></i></div>')


TRABAJO = [("vid:reel-tn-porsche", "v", "Porsche 911 GT3 RS negro en el estudio de TN Autosport", "Automoción", "TN Autosport"),
           ("vid:reel-ferreras-lifestyle", "v", "Campaña de Relojes Ferreras: coche, gastronomía, música y el reloj", "Relojes Ferreras", "Campaña de marca"),
           ("vid:reel-cardress", "v", "Funda textil a medida retirándose de un Porsche azul", "Automoción", "Fundas a medida, hechas en Barcelona"),
           ("vid:reel-diamantes", "v", "Un joyero explica una pieza ante la cámara", "Joyería", "Podcast de una casa de diamantes"),
           ("regata-dron", "v", "Velero navegando frente a una localidad costera, fotografiado desde el aire", "Náutica", "Cobertura aérea de una regata"),
           ("vid:reel-tn-track", "v", "Porsche GT3 en circuito, rodado desde un coche en paralelo", "Automoción", "TN Autosport en circuito"),
           ("vid:reel-ferreras-lamborghini", "v", "Presentación de Relojes Ferreras en un concesionario de superdeportivos", "Relojes Ferreras", "Presentación en una gala"),
           ("yate-completo-vertical", "v", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire", "Náutica", "Alquiler de yates, Costa Brava")]


def campo(id_, nome, rot, tipo="text", req="", auto="", opc=False, extra=""):
    lab = rot + (" <small>(opcional)</small>" if opc else "")
    r = f' data-req="{req}"' if req else ""
    a = f' autocomplete="{auto}"' if auto else ""
    return f'<div class="campo"><label for="{id_}">{lab}</label><input id="{id_}" name="{nome}" type="{tipo}"{a}{r}{extra}><span class="erro" id="{id_}-erro"></span></div>'


def area(id_, nome, rot, req="", ph="", opc=False):
    lab = rot + (" <small>(opcional)</small>" if opc else "")
    r = f' data-req="{req}" data-min="10"' if req else ""
    return f'<div class="campo largo"><label for="{id_}">{lab}</label><textarea id="{id_}" name="{nome}" rows="3" placeholder="{ph}"{r}></textarea><span class="erro" id="{id_}-erro"></span></div>'


def pills(nome, legenda, ops, pre=None):
    """Escolha única em pílulas (rádios nativos por baixo)."""
    pre = pre if pre is not None else ops[0][0]
    ls = "".join(f'<label><input type="radio" name="{nome}" value="{e(v)}"{se(v == pre, " checked")}><span>{e(t)}</span></label>' for v, t in ops)
    return f'<fieldset class="campo largo pills"><legend>{legenda}</legend><div>{ls}</div></fieldset>'


def consentimento(R, pref):
    return (f'<div class="campo largo consent"><label class="check"><input type="checkbox" id="{pref}-ok" name="consentimiento" data-req="Necesitamos su consentimiento para poder responderle.">'
            f'<i aria-hidden="true"></i><span>He leído la <a href="{R}legal/privacidad/">política de privacidad</a> y acepto que Ferreras me contacte sobre esta solicitud.</span></label><span class="erro" id="{pref}-ok-erro"></span></div>')


TRAMPA = '<input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">'
PREF = [("email", "Email"), ("telefono", "Teléfono"), ("whatsapp", "WhatsApp")]


def estado_envio(titulo_ok):
    """Os três estados do envio, como no site antigo: a enviar, recebido, falhou (com o correio como saída)."""
    return (f'<div class="envio" data-envio aria-live="polite"><p class="envio-a" data-e="a" hidden>Enviando…</p>'
            f'<div class="envio-ok" data-e="ok" hidden><b>{titulo_ok}</b><p>Una persona del equipo la revisa y le responde en un día laborable.</p></div>'
            f'<div class="envio-ko" data-e="ko" hidden><b>No hemos podido conectar.</b><p>Sus datos siguen escritos: puede reintentarlo o escribirnos a <a data-mailto href="mailto:{EMAIL}">{EMAIL}</a>.</p></div></div>')


def placa_html(R, linhas, pe="Passeig de Gràcia 95, 5º 1ª · 08008 Barcelona"):
    """A placa da casa: fotografia, marca e as linhas que o formulário vai preenchendo."""
    ls = "".join(f'<div data-pl-l="{k}"><dt>{t}</dt><dd class="vazio" data-pl="{k}">Elegir</dd></div>' for k, t in linhas)
    return (f'<aside class="placa" data-placa><div class="placa-foto">{img(R, "reloj-terciopelo", "Reloj Ferreras de corazón abierto sobre terciopelo rojo", "(min-width: 900px) 30vw, 90vw")}'
            f'<div class="placa-marca"><svg viewBox="0 0 235 256" aria-hidden="true">{marca_paths()}</svg><span>Barcelona</span></div></div>'
            f'<dl class="placa-l">{ls}</dl><p class="placa-pe">{pe}</p><div class="selo" data-selo hidden><b>Recibido</b><span data-selo-t></span></div></aside>')


def diag_html(R):
    """O diagnóstico como uma viagem: a estrada com as quatro etapas e o coche como marcador; as opções em cartões
    sobre um painel escuro; a placa à direita regista cada resposta. Lógica e envio em js/70-paginas.js."""
    linhas = [("sector", "Sector"), ("objetivo", "Objetivo"), ("friccion", "Fricción"), ("activos", "Activos"), ("volumen", "Volumen"),
              ("plazo", "Plazo"), ("inversion", "Inversión"), ("rol", "Su papel")]
    etapas = "".join(f'<li style="--p:{p}">{t}</li>' for p, t in [(0, "Su empresa"), (0.25, "Su objetivo"), (0.5, "Su momento"), (1, "Contacto")])
    return (f'<div class="dj" data-diag data-raiz="{R}"><div class="dj-estrada" data-estrada><div class="dj-linha"><i data-estrada-viva></i></div>'
            f'<ol class="dj-etapas">{etapas}</ol><span class="dj-coche" data-coche-diag data-ruta-fim>{coche_svg("-d")}</span></div>'
            f'<div class="dj-corpo"><div class="dj-passo" data-diag-paso></div><div class="dj-reco" data-reco hidden tabindex="-1"></div></div>'
            f'{placa_html(R, linhas)}</div>')


# ================================================================= INICIO
# Composição à maneira do De Antonio, adaptada aos blocos da Ferreras: âncoras alternadas à esquerda e à direita,
# título e frase lado a lado, media fora do eixo ou a sair da margem, ar entre blocos, dois momentos de ecrã inteiro,
# números enormes só em contorno por trás das imagens. Os percentuais são guia de ritmo, não regra.
exec((RAIZ / "_fonte/despiece.py").read_text(encoding="utf-8"))


def inicio(R):
    ctl, pista = carril(R, TRABAJO, "Trabajos de producción propia")
    return f'''
<section class="hero hero-reloj" data-hero data-hero-3d data-hora="07:30" data-momento="Abre su empresa">
  <figure class="hero-foto" aria-hidden="true">{img(R, 'reloj-terciopelo', '', '(min-width: 900px) 40vw, 80vw', lazy=False)}</figure>
  <div class="hero-velo" aria-hidden="true"></div>
  <div class="hero-grid">
    <div class="hero-tit"><p class="etiqueta" style="--i:0"><span class="hora">07:30</span>Desde Barcelona</p>
      <h1 class="titulo t-xxl" data-linhas>{L('Veinticuatro horas', 'a la altura', '<em>de su marca.</em>')}</h1></div>
    <div class="hero-lado"><p class="lead" style="--i:1">Marketing de lujo mientras le miran. Inteligencia artificial mientras le escriben.</p>
      <div class="acoes" style="--i:2">{btn('#diagnostico', CTA, extra=' data-vai')}{btn('#que-hacemos', 'Ver el día', 'btn-linha btn-vidro', False)}</div></div>
  </div>
  <p class="hero-pista" aria-hidden="true"><i></i>Arrastre el reloj para girarlo</p>
</section>

<section class="sec p-que" id="que-hacemos" data-hora="08:30" data-momento="Qué hacemos">
  <div class="grelha p-que-cab">
    <div class="p-que-tit" data-ruta-ini>{etq('08:30', 'El día empieza')}<h2 class="titulo t-l" data-linhas>{L('Dos equipos.', '<em>Un mismo reloj.</em>')}</h2></div>
    <p class="lead p-que-lead" data-sube>Uno trabaja para que su marca se vea; el otro, para que ninguna consulta se quede sin contestar. Los dos, dentro de su empresa y con un solo plan.</p>
  </div>
  <div class="puertas">
    <a class="puerta" href="{R}marketing/" data-sube><div class="ventana pu-media">{video(R, 'reel-tn-porsche', 'Porsche 911 GT3 RS negro en el estudio de TN Autosport')}</div>
      <div class="pu-txt"><p class="etiqueta">Marketing</p><h3>Rodaje, redes <em>y estrategia.</em></h3>
      <ul><li>Un plan de doce meses, por escrito</li><li>Equipo de rodaje propio: dron, cámaras y sonido</li><li>Redes, publicidad y email</li></ul><span class="enlace">Ver el departamento <span class="fl">→</span></span></div></a>
    <a class="puerta" href="{R}inteligencia-artificial/" data-sube style="--i:1"><div class="ventana pu-media pu-dia"><figure class="dia24" data-dia24 aria-label="Las consultas de un día, hora a hora">{dia24_svg()}</figure></div>
      <div class="pu-txt"><p class="etiqueta">Inteligencia artificial</p><h3>Respuesta <em>a cualquier hora.</em></h3>
      <ul><li>Teléfono, WhatsApp, chat y email</li><li>Más de veinte idiomas</li><li>Una persona entra cuando hace falta</li></ul><span class="enlace">Ver el departamento <span class="fl">→</span></span></div></a>
  </div>
</section>

<section class="sec prod p-prod" id="trabajo" data-hora="10:30" data-momento="Rodaje en el puerto">
  <div class="grelha p-cab">
    <div class="p-tit">{etq('10:30', 'Rodaje')}<h2 class="titulo t-l" data-linhas>{L('Lo rodamos nosotros.', '<em>Y se nota.</em>')}</h2></div>
    <p class="lead p-lead" data-sube>Dron, cámaras, sonido e iluminación propios. El equipo viaja con cada proyecto.</p>
  </div>
  {pista}
  <div class="grelha p-pe"><div class="prod-dado" data-sube><b><span data-conta="20000">20.000</span>–<span data-conta="300000">300.000</span></b><span>visitas de media por pieza en la línea editorial de un negocio de automoción deportiva</span></div>{ctl}</div>
</section>

<section class="interludio" data-ruta-tunel data-hora="12:00" data-momento="Lo que no se puede repetir">
  {filme(R, 'interludio', 'lazy')}
  <div class="int-velo" aria-hidden="true"></div>
  <h2 class="titulo t-xl int-h" data-linhas>{L('Un buen plano', '<em>no se improvisa.</em>')}</h2>
</section>

<section class="sec mitades p-mit" data-hora="13:00" data-momento="El mismo barco, de día y de noche">
  <div class="grelha p-mit-cab">
    <p class="contorno mit-24" aria-hidden="true">24 h</p>
    <div class="p-mit-tit">{etq('13:00', 'Mediodía')}<h2 class="titulo t-xl" data-linhas>{L('Cuando le miran, marketing.', '<em>Cuando le escriben, IA.</em>')}</h2><p class="lead" data-sube>Mueva la línea: el mismo barco, a pleno sol y de noche.</p></div>
  </div>
  <div class="rx rx-total" data-rx data-ruta-tunel role="slider" tabindex="0" aria-label="Del día a la noche: marketing e inteligencia artificial" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
    <div class="rx-capa rx-dia">{img(R, 'yate-completo', 'Yate de lujo fondeado en una cala de aguas turquesa, de día')}</div>
    <div class="rx-capa rx-noche">{img(R, 'yate-noche', 'El mismo yate de noche, con las luces del salón encendidas')}</div>
    <div class="rx-linha" aria-hidden="true"></div><div class="rx-pega" aria-hidden="true">↔</div>
    <a class="rx-rot d" href="{R}marketing/"><b>Sol · Marketing</b><span>Que se le vea como es</span></a>
    <a class="rx-rot n" href="{R}inteligencia-artificial/"><b>Noche · IA</b><span>Que siempre haya respuesta</span></a>
  </div>
</section>

<section class="sec p-sect" data-hora="15:30" data-momento="Cuatro sectores">
  <div class="cab p-sect-cab">{etq('15:30', 'Sectores')}<h2 class="titulo t-l" data-linhas>{L('Hoteles, motor, mar <em>y joyas.</em>')}</h2></div>
  {sect_html(R)}
</section>

<section class="alcoba" data-alcoba data-ruta-tunel data-hora="16:45" data-momento="El reloj, en su vitrina" aria-label="Relojes Ferreras en su vitrina">
  <div class="al-palco">
    <div class="al-fondo" aria-hidden="true"></div>
    <div class="al-nicho" data-al-nicho aria-hidden="true"><i></i></div>
    <div class="al-cono" data-al-cono aria-hidden="true"></div>
    <p class="al-grande" aria-hidden="true"><span data-al-grande>Ferreras</span></p>
    <div class="al-reloj" data-al-reloj><div class="al-tilt" data-al-tilt>{despiece_html(R)}{reloj_html(R, "-a")}</div><div class="al-sombra" aria-hidden="true"></div></div>
    <div class="al-polvo" data-al-polvo aria-hidden="true">{"".join(f"<i style='--x:{(i * 37) % 100}%;--y:{(i * 53 + 11) % 100}%;--s:{4 + (i * 7) % 9}px;--d:{(i % 5) * 0.12 + 0.45:.2f}'></i>" for i in range(16))}</div>
    {lista_html()}
    <div class="al-txt" data-al-txt>
      <p class="etiqueta"><span class="hora">16:45</span>Relojes Ferreras</p>
      <h2 class="titulo t-xl"><span class="al-l"><span>Diseño propio.</span></span><span class="al-l"><span>Mecanismo suizo.</span></span><span class="al-l"><span><em>Ensamblado en Barcelona.</em></span></span></h2>
      <p class="lead al-l"><span>Una edición limitada a 100 piezas, nacida dentro de esta agencia.</span></p>
    </div>
    <div class="al-vela" data-al-vela aria-hidden="true"></div>
  </div>
</section>

<section class="sec claro p-marca" data-claro data-hora="17:30" data-momento="Relojes Ferreras, nuestra marca">
  <div class="grelha p-marca-cab"><div class="p-marca-tit">{etq('17:30', 'Marca propia')}<h2 class="titulo t-xl" data-linhas>{L('Una marca de relojes', '<em>nacida en esta agencia.</em>')}</h2></div></div>
  <div class="grelha trofeus">
    <figure class="trofeu t1"><span class="contorno" aria-hidden="true">100</span><div class="ventana" data-janela>{video(R, 'hero-ferreras-lifestyle', 'Campaña de Relojes Ferreras: un Aston Martin en una carretera de montaña nevada', 720, 1280)}</div><figcaption class="pie"><b>Edición limitada</b>A 100 piezas</figcaption></figure>
    <figure class="trofeu t2"><span class="contorno" aria-hidden="true">BCN</span><div class="tr-reloj">{reloj_html(R, '-m')}</div><figcaption class="pie"><b>Ensamblaje en Barcelona</b>Diseño propio y mecanismo suizo</figcaption></figure>
  </div>
  <div class="grelha p-marca-pe"><p data-sube>{enlace('https://relojes-ferreras.com/', 'Conocer Relojes Ferreras', True)}</p><p class="marca-nota" data-sube>{mini_reloj()}El reloj que le acompaña en esta página es el nuestro.</p></div>
</section>

<section class="sec claro final p-final" id="diagnostico" data-claro data-hora="07:30" data-momento="Veinticuatro horas después">
  <div class="grelha final-cab">
    <div class="final-txt">{etq('07:30', 'Al día siguiente')}<h2 class="titulo t-xl" data-linhas>{L('Ocho preguntas.', '<em>Una recomendación.</em>')}</h2></div>
    <p class="lead final-lead" data-sube>Dos minutos para saber por dónde empezar y qué dejar para después. Sin compromiso.</p>
  </div>
  {diag_html(R)}
</section>
'''

pagina("", "IA & Marketing Ferreras · Veinticuatro horas a la altura de su marca",
       "Un departamento de marketing y otro de inteligencia artificial montados dentro de su empresa, con un solo plan. Agencia de marketing de lujo en Barcelona: hotelería, automoción, náutica y joyería.",
       inicio, inicio=True)



# ================================================================= VISUAIS DA IA
# A web antiga ilustrava a IA com imagens geradas de recepções de hotel. Aqui a IA mostra-se com o que faz: idiomas,
# uma pergunta e a sua resposta (do guião de demonstração da própria web antiga), o aviso a uma pessoa, as horas que
# se perdem, as ligações aos sistemas e o registo. Desenho em HTML e CSS, nítido a qualquer tamanho.
SAUDOS = ["Buenas noches", "Good evening", "Bonsoir", "Guten Abend", "Buonasera", "Boa noite", "Goedenavond", "Добрый вечер", "こんばんは", "晚上好", "مساء الخير", "Dobry wieczór"]


def vis(kind):
    if kind == "idiomas":
        ouro = ' class="ouro"'
        ls = "".join(f'<li style="--i:{i}"{ouro if i == 3 else ""}>{x}</li>' for i, x in enumerate(SAUDOS))
        return f'<div class="vis vis-idiomas" aria-hidden="true"><ul>{ls}{ls}</ul></div>'
    if kind == "consulta":
        return ('<div class="vis vis-consulta" aria-hidden="true"><p class="vq">Guten Abend, haben Sie am Wochenende noch ein Doppelzimmer frei?</p>'
                '<p class="vs">Consulta a fuente conectada · solo lectura</p>'
                '<p class="va">Para ese fin de semana figura disponibilidad en habitación doble. El check-in es a partir de las 15:00.</p></div>')
    if kind == "avisa":
        return ('<div class="vis vis-avisa" aria-hidden="true"><span class="va-anel"><i></i><i></i><b>Recepción</b></span>'
                '<p>Fuera de alcance autorizado<br><em>pasa a una persona, con el contexto</em></p></div>')
    if kind == "horas":
        bars = "".join(f'<i style="--h:{h}"></i>' for h in (12, 8, 6, 5, 6, 14, 30, 52, 70, 64, 58, 61, 66, 60, 55, 57, 63, 72, 80, 74, 62, 44, 30, 20))
        return f'<div class="vis vis-horas" aria-hidden="true"><div class="vh-b">{bars}</div><p><span>00:00</span><span>12:00</span><span>24:00</span></p></div>'
    if kind == "integra":
        nos = "".join(f'<li style="--a:{a}deg">{t}</li>' for a, t in ((0, "Reservas"), (60, "CRM"), (120, "WhatsApp"), (180, "Email"), (240, "Teléfono"), (300, "Web")))
        return f'<div class="vis vis-integra" aria-hidden="true"><ul>{nos}</ul><span class="vi-c">F</span></div>'
    if kind == "control":
        ls = "".join(f"<li><i></i>{t}</li>" for t in ("Permiso: solo lectura", "Conversación revisada", "Respuesta corregida", "Protocolo de recepción", "Registro completo"))
        return f'<div class="vis vis-control" aria-hidden="true"><ul>{ls}</ul></div>'
    if kind == "usted":
        ls = "".join(f'<li><b>{h}</b><span>{t}</span></li>' for h, t in (("08:00", "Correo ordenado"), ("09:30", "Informe del día, ya escrito"), ("12:00", "Propuesta en borrador"), ("18:00", "Agenda de mañana")))
        return f'<div class="vis vis-usted" aria-hidden="true"><ul>{ls}</ul></div>'
    raise KeyError(kind)


# ================================================================= CASOS (dados partilhados)
CASOS = [
    dict(id="auto-voz", sector="automocion-lujo", sl="Automoción de lujo", prob="percepcion demanda", foto=("tn-gt3rs-frente", "Porsche 911 GT3 RS negro en el estudio de TN Autosport"),
         t="De publicar coches a ser la voz de referencia del sector", s="Contenido de alto alcance y un podcast propio.",
         p="Una cuenta consolidada cuya presencia digital no reflejaba la autoridad real del negocio ni la calidad de su inventario.",
         i="Una línea editorial reconocible: piezas pensadas para alcance y un formato de podcast propio.",
         r="La cuenta pasó de acompañar al negocio a liderar la conversación de su categoría.",
         ev=["Contenidos con millones de visitas y una media de entre 20.000 y 300.000 visitas por pieza", "La comunidad se multiplicó durante el periodo de trabajo continuado"]),
    dict(id="joya-marca", sector="joyeria-relojeria", sl="Joyería y relojería", prob="percepcion", foto=("joya-morganita", "Pendientes y anillo de morganita sobre terciopelo negro"),
         t="Una pieza excepcional necesitaba una marca a su altura", s="Identidad, herramientas comerciales y contenido experto.",
         p="Producto de primer nivel y una identidad que no comunicaba ni su solvencia ni el ceremonial de una compra así.",
         i="Construir la marca y sus materiales: no solo un logotipo, también con qué se presenta y se cierra una venta.",
         r="Un estándar coherente con el valor del producto, con materiales que sostienen la venta.", ev=[]),
    dict(id="hotel-agente", sector="hoteles", sl="Hoteles", prob="consultas saturacion", foto=("hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado"),
         t="Un agente diseñado alrededor de la operativa real de un hotel", s="Más de veinte idiomas y derivación a recepción.",
         p="Consultas a cualquier hora, en varios idiomas y por varios canales, y una recepción que no puede estar en todo.",
         i="Un agente a medida, no un chatbot genérico: qué responde, qué consulta y cuándo avisa a una persona.",
         r="Atención continuada en más de veinte idiomas, con derivación a recepción cuando hace falta.", ev=[]),
    dict(id="auto-producto", sector="automocion-lujo", sl="Automoción de lujo", prob="demanda percepcion", foto=("cardress-audi", "Audi con funda a medida de SM CarDress, rodando por carretera"),
         t="Un producto que se entiende en tres segundos", s="Vídeo de producto y entrevistas.",
         p="Un producto premium muy visual, fácil de admirar y difícil de explicar en un catálogo estático.",
         i="El producto como protagonista audiovisual, con entrevistas que aportan contexto y comunidad.",
         r="Se explica solo en el primer visionado; la marca tiene un catálogo audiovisual para vender cada día.",
         ev=["El cliente comunica un impacto comercial directo tras la pieza de mayor alcance"]),
    dict(id="nautica-identidad", sector="nautica", sl="Náutica, yates y puertos", prob="percepcion conversion", foto=("yate-completo", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire"),
         t="Identidad e infraestructura digital para el alquiler de yates", s="Una agencia de alquiler de yates de lujo, Costa Brava.",
         p="Un activo de altísimo valor comercializado con materiales que no transmitían la calidad del barco ni del servicio.",
         i="Primero la identidad y la infraestructura digital, para que cada consulta llegue a un entorno a su altura.",
         r="Una presencia coherente con el producto y con la experiencia a bordo.", ev=[]),
    dict(id="b2b-vinoteca", sector="b2b", sl="B2B y servicios", prob="saturacion", foto=None,
         t="Automatización interna en una vinoteca de lujo", s="IA y automatización en la operativa diaria.",
         p="Procesos necesarios, repetitivos y muy consumidores de tiempo.",
         i="Separar lo que podía automatizarse con control de lo que debía seguir en manos de una persona.",
         r="Una reducción sustancial del tiempo dedicado a los procesos incluidos en el alcance.", ev=[]),
    dict(id="nautica-regatas", sector="nautica", sl="Náutica, yates y puertos", prob="percepcion", foto=("regata-dron", "Velero navegando frente a una localidad costera, fotografiado desde el aire"),
         t="Producción y cobertura en vivo en puertos y regatas", s="Competición y puerto, con criterio editorial.",
         p="Los eventos náuticos concentran en unas horas el material de un año, y suelen quedar sin dirección ni uso posterior.",
         i="Tratar la cobertura como producción: decidir antes qué historia se cuenta.",
         r="Un archivo audiovisual utilizable durante toda la temporada.", ev=[]),
    dict(id="nautica-compradores", sector="nautica", sl="Náutica, yates y puertos", prob="demanda", foto=("yate-vistas", "Zona exterior de un yate con mesa, asientos y vistas a la costa"),
         t="Compradores de yate sin una cartera previa", s="Fotografía, canales especializados y redes.",
         p="Vender una embarcación de alto valor suele depender de una cartera de contactos de años.",
         i="Alcance dirigido: material a la altura del activo, distribuido donde está el comprador.",
         r="Se alcanzó a compradores cualificados sin cartera propia.", ev=[]),
]
CASO_FERRERAS = dict(id="ferreras", sector="joyeria-relojeria", sl="Marca propia", prob="", foto=("reloj-terciopelo", "Reloj Ferreras de corazón abierto sobre terciopelo rojo"),
                     t="Relojes Ferreras: nuestra propia casa", s="Diseño propio, mecanismo suizo y ensamblaje en Barcelona.",
                     p="Crear una marca de relojería obliga a resolver en casa lo mismo que un cliente encarga a una agencia.",
                     i="Construirla con el mismo método que proponemos, sin atajos ni decisiones delegadas.",
                     r="Un banco de pruebas permanente: lo que recomendamos lo hemos aplicado antes en casa.", ev=[])


def caso_card(R, c, filtro=False):
    """Um caso num cartão de fotografia: sector, título e o resultado numa linha. Nada se abre nem se expande."""
    foto = img(R, c["foto"][0], c["foto"][1], "(min-width: 900px) 56vw, 120vw") if c["foto"] else f'<div class="caso-marca"><svg viewBox="0 0 235 256" aria-hidden="true">{marca_paths()}</svg></div>'
    ev = f'<p class="cc-ev">{e(c["ev"][0])}</p>' if c["ev"] else ""
    atr = f' data-caso data-sector="{c["sector"]}" data-problema="{c["prob"]}"' if filtro else ""
    return (f'<article class="cc"{atr}><div class="cc-foto">{foto}</div><div class="cc-txt"><p class="etiqueta">{e(c["sl"])}</p>'
            f'<h3>{e(c["t"])}</h3><p class="cc-r">{e(c["r"])}</p>{ev}</div></article>')


def casos_grid(R, casos, filtro=False):
    return f'<div class="ccs" style="--n:{len(casos)}">{"".join(caso_card(R, c, filtro) for c in casos)}</div>'


def casos_de(sector):
    return [c for c in CASOS if c["sector"] == sector]


def indice(R, items, rotulo):
    """O que inclui: uma linha por serviço e, ao lado, a imagem ou o vídeo do que está activo (substitui os separadores).
    No telemóvel a pré-visualização some e cada linha leva a sua miniatura."""
    vistas, linhas = [], []
    for i, it in enumerate(items):
        t, p, (tipo, base, alt) = it[:3]
        href = it[3] if len(it) > 3 else None
        if tipo == "vis":
            mv = vis(base)
            mini = '<span class="vis-mini"></span>'
        elif tipo == "vid":
            mv = f'<video muted playsinline loop preload="none" poster="{R}video/{base}-poster.webp" data-src="{R}video/{base}.mp4"></video>'
            mini = f'<img src="{R}video/{base}-poster.webp" alt="" loading="lazy" decoding="async">'
        else:
            mv = img(R, base, alt, "(min-width: 900px) 1600px, 1px")
            mini = img(R, base, "", "120px")
        vistas.append(f'<div class="iv{se(i == 0, " on")}" data-iv>{mv}</div>')
        h3 = f'<a href="{R}{href}">{e(t)} <span class="fl">→</span></a>' if href else e(t)
        linhas.append(f'<li class="ix{se(i == 0, " on")}" data-ix><span class="ix-mini ventana" aria-hidden="true">{mini}</span><h3>{h3}</h3><p>{e(p)}</p></li>')
    return (f'<div class="indice" data-indice><ul class="indice-lista" aria-label="{e(rotulo)}">{"".join(linhas)}</ul>'
            f'<div class="indice-vista ventana" aria-hidden="true">{"".join(vistas)}</div></div>')


def tachado(items):
    """Onde se perde o dinheiro: uma linha cada, riscada a ouro quando entra no ecrã."""
    return '<ul class="tachado">' + "".join(f'<li data-tacha style="--i:{i}"><span>{e(t)}</span></li>' for i, t in enumerate(items)) + "</ul>"


def flujo(items):
    """O método numa só linha: palavras ligadas por um traço que se desenha (substitui os cartões 01–05)."""
    return '<ol class="flujo" data-sube>' + "".join(f'<li style="--i:{i}">{e(t)}</li>' for i, t in enumerate(items)) + "</ol>"


def lineas(items):
    """Capacidades: título grande e meia linha, sem números nem cartões."""
    return '<ul class="lineas">' + "".join(f'<li data-sube style="--i:{i % 2}"><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(items)) + "</ul>"


# ================================================================= QUIÉN SOMOS
def quien(R):
    marcas = [("reloj-muneca", "Un reloj Ferreras en la muñeca", "Relojería · Marca propia", "Relojes Ferreras"),
              ("tn-gt3rs-asientos", "Asientos de competición con cinturones amarillos de un GT3 RS de TN Autosport", "Automoción", "TN Autosport"),
              ("hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado", "Hotelería", "Hotel Boltaña Ordesa"),
              ("sector-mar-puerto", "Puerto deportivo de la Costa Brava visto desde el aire", "Náutica", "Club náutico · Costa Brava"),
              ("sector-joya-esmeralda", "Anillo de esmeralda y diamantes sobre terciopelo negro", "Joyería", "Joyería de diamantes · España"),
              ("cardress-audi", "Audi con funda a medida de SM CarDress, rodando por carretera", "Automoción", "SM CarDress")]
    mh = "".join(f'<figure class="marca-c" data-sube style="--i:{i % 3}"><div class="ventana">{img(R, b, alt, "(min-width: 900px) 34vw, 90vw")}</div><figcaption><p class="etiqueta">{s}</p><h3>{t}</h3></figcaption></figure>' for i, (b, alt, s, t) in enumerate(marcas))
    nomes = "".join(f"<li>{t}</li>" for t in ["Relojes Ferreras", "TN Autosport", "Hotel Boltaña Ordesa", "SM CarDress", "Club náutico · Costa Brava", "Joyería de diamantes"])
    return (ph(R, "La casa", L("Pocas marcas,", "<em>muy de cerca.</em>"),
               "El departamento de marketing de TN Autosport y los creadores de Relojes Ferreras.",
               btn(R + DIAG, CTA) + btn(R + "casos/", "Ver los casos", "btn-linha", False), img(R, "stand-ferreras", "Expositor de Relojes Ferreras con el lema Diseñado para dominar el tiempo, en una presentación con estuches de reloj expuestos y embarcaciones al fondo", "(min-width: 900px) 46vw, 100vw", lazy=False), extra=f'<div class="ph-nomes"><p class="etiqueta">Trabajamos con</p><ul>{nomes}</ul></div>')
            + sec(cab("", "Marcas que llevamos", "Nombres que su sector <em>ya conoce.</em>") + f'<div class="marcas">{mh}</div>')
            + sec(f'<div class="grelha estandar"><figure class="est-foto ventana" data-janela>{img(R, "relojero-lupa", "Un relojero revisa una pieza con la lupa", "(min-width: 900px) 40vw, 100vw")}</figure>'
                  f'<div class="est-txt"><p class="titulo promessa" data-duas-tintas>El lujo no es una etiqueta. <em>Es un estándar de ejecución.</em></p><p class="lead" data-sube>Pocas empresas, muy de cerca. La dirección entra en cada proyecto y no se delega.</p></div></div>')
            + banda("¿Por dónde <em>empezaría usted?</em>", "Ocho preguntas, dos minutos y una respuesta concreta.", btn(R + DIAG, CTA)))

pagina("la-casa/", "La casa", "Pocas marcas, muy de cerca: TN Autosport en automoción, Relojes Ferreras como marca propia. Marketing de lujo e inteligencia artificial desde Barcelona.", quien)


# ================================================================= MARKETING
MKT = [("Estrategia a doce meses", "Qué tiene que cambiar en la percepción de su empresa, y en qué orden.", ("img", "mecanismo-macro", "El corazón abierto de un reloj Ferreras, con el volante a la vista")),
       ("Producción audiovisual", "Dron, cámaras, sonido e iluminación. Equipo y desplazamientos incluidos.", ("vid", "reel-tn-porsche", "Porsche 911 GT3 RS negro en el estudio de TN Autosport")),
       ("Podcast y entrevistas", "Que se le vea explicando su criterio, no vendiendo su producto.", ("vid", "reel-diamantes", "Un joyero explica una pieza ante la cámara")),
       ("Redes y comunidad", "Una línea editorial reconocible, publicada con constancia.", ("vid", "reel-ferreras-lifestyle", "Campaña de Relojes Ferreras: coche, gastronomía, música y el reloj")),
       ("Publicidad", "Objetivo declarado y medición honesta. La inversión se decide con usted.", ("vid", "reel-cardress", "Funda textil a medida retirándose de un Porsche azul")),
       ("Email y canales de venta", "Recuperar a quien ya le conoce cuesta menos que convencer a quien no.", ("img", "joya-morganita", "Pendientes y anillo de morganita sobre terciopelo negro")),
       ("Web, ecommerce y SEO", "Desarrollada por nuestro equipo: una web que cualifica.", ("img", "reloj-terciopelo", "Reloj Ferreras de corazón abierto sobre terciopelo rojo"), "web/")]

def marketing(R):
    pilares = [("reel-tn-porsche", "Porsche 911 GT3 RS negro en el estudio de TN Autosport", "Rodamos.", "Equipo propio: dron, cámaras, sonido e iluminación. Desplazamientos incluidos."),
               ("reel-ferreras-lifestyle", "Campaña de Relojes Ferreras: coche, gastronomía, música y el reloj", "Publicamos.", "Redes, publicidad y email, con una línea editorial que se reconoce."),
               ("reel-diamantes", "Un joyero explica una pieza ante la cámara", "Le ponemos delante.", "Podcast y entrevistas: que se le vea explicando su criterio.")]
    ph_ = "".join(f'<figure class="pilar" data-sube style="--i:{i}"><div class="ventana">{video(R, b, alt)}</div><figcaption><h3>{t}</h3><p>{p}</p></figcaption></figure>' for i, (b, alt, t, p) in enumerate(pilares))
    rx = (f'<div class="rx rx-ad" data-rx role="slider" tabindex="0" aria-label="Antes y después: una ficha de inventario frente a una pieza de vídeo" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">'
          f'<div class="rx-capa rx-dia">{img(R, "tn-autosport-deportivos", "Dos coches deportivos expuestos en un concesionario, en una fotografía de catálogo", "(min-width: 900px) 40vw, 100vw")}'
          f'<div class="ficha"><p class="etiqueta">Ficha de inventario</p><b>Deportivo de ocasión</b><span>12 fotos · Precio a consultar</span></div></div>'
          f'<div class="rx-capa rx-noche">{video(R, "reel-tn-track", "Porsche GT3 en circuito, rodado desde un coche en paralelo")}'
          f'<div class="ad-dado"><b>20.000–300.000</b><span>visitas de media por pieza</span></div></div>'
          f'<div class="rx-linha" aria-hidden="true"></div><div class="rx-pega" aria-hidden="true">↔</div>'
          f'<span class="rx-rot d"><b>Antes</b><span>Una ficha más</span></span><span class="rx-rot n"><b>Con Ferreras</b><span>Una pieza que se comparte</span></span></div>')
    cifras = [("20.000–300.000", "visitas de media por pieza, en la línea editorial de un negocio de automoción deportiva"),
              ("12 meses", "de estrategia por escrito, revisada cada mes"), ("Sin extras", "equipo, producción y desplazamientos van en el plan")]
    ch = "".join(f'<div data-sube style="--i:{i}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(cifras))
    return (ph_media(R, "Marketing", L("Rodamos, publicamos", "<em>y medimos.</em>"),
                     "Estrategia, producción audiovisual propia y distribución, dentro de su empresa.",
                     btn(R + DIAG, CTA) + btn("#hacemos", "Qué hacemos", "btn-linha btn-vidro", False), filme(R, "mkt"))
            + sec(cab("", "Qué hacemos", "Del plan <em>al plano.</em>") + f'<div class="pilares">{ph_}</div>', "p-pilares", ' id="hacemos"')
            + sec(f'<div class="grelha antes"><div class="antes-txt">{etq("", "La diferencia", "n")}<h2 class="titulo t-l" data-linhas>El mismo coche. <em>Contado por nosotros.</em></h2>'
                  f'<p class="lead" data-sube>Deslice la línea: de una ficha con doce fotos a una pieza que la gente comparte.</p><dl class="cifras-m">{ch}</dl></div>{rx}</div>')
            + banda("¿Cómo se ve su marca <em>desde fuera?</em>", "Lo vemos con usted en dos minutos, sin compromiso.", btn(R + DIAG, CTA), chips(CONDICIONES, "chips chips-cond")))

pagina("marketing/", "Marketing", "Marketing de lujo dentro de su empresa: estrategia a doce meses, producción audiovisual propia con dron y equipo, podcast, redes, publicidad, email marketing y web.", marketing)


# ================================================================= IA
IA = [("Primero, usted", "Sistemas que le quitan horas a usted antes de tocar la empresa.", ("vis", "usted", "")),
      ("Agentes de atención", "Teléfono, chat, WhatsApp o email, en más de veinte idiomas.", ("vis", "idiomas", ""), "ia-hoteles/"),
      ("Análisis de la empresa", "Dónde se pierde tiempo y dinero, y qué conviene automatizar.", ("vis", "horas", "")),
      ("Integraciones", "Conectado a lo que ya usa. Solo lectura por defecto.", ("vis", "integra", "")),
      ("Control y mejora", "Permisos, registro y revisión de conversaciones reales.", ("vis", "control", ""))]

def ia(R):
    feed = [("23:40", "DE", "Guten Abend, haben Sie am Wochenende noch ein Doppelzimmer frei?"), ("00:12", "EN", "Is breakfast included?"),
            ("01:05", "FR", "Le parking est-il gratuit ?"), ("06:48", "ES", "¿A qué hora es el check-in?")]
    fd = "".join(f'<li style="--i:{i}"><span class="fd-h">{h} · {l}</span><span class="fd-t">{e(t)}</span><span class="fd-ok">Respondido en su idioma</span></li>' for i, (h, l, t) in enumerate(feed))
    hace = [("idiomas", "", "Atiende.", "Teléfono, WhatsApp, chat y email. En más de veinte idiomas, a cualquier hora."),
            ("consulta", "", "Consulta.", "Disponibilidad, horarios y datos de su casa, conectado a sus sistemas. Solo lectura por defecto."),
            ("avisa", "", "Avisa a una persona.", "Cuando algo sale de lo autorizado, pasa el caso con todo el contexto.")]
    hh = "".join(f'<figure class="pilar" data-sube style="--i:{i}"><div class="ventana">{vis(b)}</div><figcaption><h3>{t}</h3><p>{p}</p></figcaption></figure>' for i, (b, alt, t, p) in enumerate(hace))
    demo = (f'<div class="grelha conversa" data-demo><div class="conv-txt">{etq("", "Así responde", "n")}<h2 class="titulo t-l" data-linhas>Lo importante <em>es dónde calla.</em></h2>'
            f'<p class="lead" data-sube>Responde lo que sabe, consulta lo autorizado y, en el punto que usted decide, pasa el caso a recepción.</p>'
            f'<p class="mini">{AVISO_DEMO}</p><p><button type="button" class="enlace" data-demo-play><span>Repetir</span> <span class="fl">↺</span></button></p></div>'
            f'<div class="conv-lado"><span class="contorno conv-c" aria-hidden="true">23:40</span><div class="movil">{chat_html()}</div></div></div>')
    return (ph_media(R, "Inteligencia artificial", L("Ninguna consulta", "<em>sin respuesta.</em>"),
                     "Agentes de atención en más de veinte idiomas, con supervisión humana.",
                     btn(R + DIAG, CTA) + btn("#hace", "Qué hace", "btn-linha btn-vidro", False), fundo_img(R, "yate-noche", "Un yate de noche con las luces del salón encendidas"),
                     sobre=f'<ul class="feed" data-feed aria-label="Ilustración: consultas que entran de noche">{fd}</ul>')
            + sec(cab("", "Qué hace", "Responde, consulta <em>y avisa.</em>") + f'<div class="pilares">{hh}</div>', "p-pilares", ' id="hace"')
            + sec(f'<div class="grelha noche-g"><figure class="dia24" data-dia24>{dia24_svg()}<figcaption class="dia24-ley"><span><i class="eq"></i>Su equipo</span><span><i class="ag"></i>El agente, con la recepción cerrada</span><small>Ilustración: consultas de un día cualquiera.</small></figcaption></figure><div class="noche-txt">{etq("", "Las 24 horas", "n")}<h2 class="titulo t-l" data-linhas>La consulta de las 23:40 <em>no es una consulta perdida.</em></h2><p class="lead" data-sube>Su equipo atiende de día. El agente, cuando la recepción está cerrada.</p></div></div>', "noche")
            + sec(demo, extra=' id="demo"')
            + banda("¿Qué hace hoy su equipo <em>que podría hacer un agente?</em>", "Lo vemos con usted en dos minutos, sin compromiso.", btn(R + DIAG, CTA) + btn(R + "ia-hoteles/", "El caso de hotelería", "btn-linha")))

pagina("inteligencia-artificial/", "Inteligencia artificial", "Inteligencia artificial dentro de su empresa: agentes de atención en más de veinte idiomas, integraciones con sus sistemas, automatización de procesos y formación a su equipo.", ia)


# ================================================================= SECTORES
SECTORES = {
    "hoteles": dict(nome="Hoteles", titulo="Agentes de IA para hoteles", desc="Atienda 24/7, en varios idiomas y sin saturar recepción. Agentes de voz, chat y WhatsApp diseñados alrededor de la operativa real de su establecimiento.",
                    h1=("Su hotel, atendido", "a cualquier hora", "<em>y en cualquier idioma.</em>"),
                    lead="Un agente que responde lo que sabe y avisa a recepción cuando hace falta una persona.",
                    media=("img", "servicio-coffre", "Servicio de caviar en una concha dorada, con guante blanco"),
                    margen=[("La consulta de las 23:40", "No es una consulta perdida: es una habitación vacía."), ("Dos cosas a la vez", "El teléfono suena con un huésped delante."),
                            ("Las mismas quince preguntas", "Horarios, parking, mascotas, cancelaciones."), ("El canal gana a la reserva directa", "Y la comisión pasa a ser la norma.")],
                    promessa="Que ninguna consulta se quede sin respuesta, <em>y que recepción recupere su tiempo.</em>",
                    entrada=("Asistente IA 24/7 para hoteles", "La integración con PMS depende de la API, los permisos y las pruebas. Los consumos de voz y mensajería se facturan aparte."),
                    extra_link=("ia-hoteles/", "Cómo trabajamos la atención de un hotel")),
    "automocion-lujo": dict(nome="Automoción de lujo", titulo="Marketing para automoción de lujo", desc="Eleve la percepción de su inventario y convierta atención en consultas cualificadas con contenido audiovisual y formatos de autoridad.",
                    h1=("Un coche se vende", "<em>en movimiento.</em>"),
                    lead="Vídeo y formatos de autoridad que convierten atención en consultas cualificadas.",
                    media=("vid", "auto", ""),
                    margen=[("Se ve, pero no se desea", "Fotos correctas y ningún relato."), ("Alcance sin consultas", "Gusta, se comparte y no vende."),
                            ("La autoridad se la lleva otro", "Quien habla con criterio es la referencia."), ("El producto asociado no se explica", "Se vende en movimiento, no en estático.")],
                    promessa="Elevar la percepción del inventario <em>y convertir la atención en consultas.</em>",
                    entrada=("Autoridad & Demanda", "Estrategia, producción, distribución y panel de KPIs. La inversión publicitaria, aparte."),
                    extra_link=None),
    "nautica": dict(nome="Náutica, yates y puertos", titulo="Marketing náutico: clubs, astilleros, yates y chárter", desc="Clubs náuticos, astilleros, compraventa de yates y alquiler de barcos. Identidad, producción audiovisual, cobertura de regatas y eventos, y comercialización.",
                    h1=("El mar se vende", "<em>desde el agua.</em>"),
                    lead="Clubs, astilleros, compraventa y chárter: producción, regatas y comercialización.",
                    media=("img", "yate-completo", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire"),
                    margen=[("La experiencia no se transmite", "El cliente solo ve un barco blanco más."), ("Un club vive de que le vean", "Socios, escuela y patrocinadores."),
                            ("La regata se evapora", "El mejor material del año, sin uso posterior."), ("La consulta internacional se enfría", "Idioma, horario y respuesta deciden.")],
                    promessa="Que una embarcación se perciba como se vive <em>y llegar a quien aún no le conoce.</em>",
                    entrada=("Producción y comercialización", "Identidad e infraestructura digital por alcance. Viajes y dietas aparte."),
                    extra_link=None),
    "joyeria-relojeria": dict(nome="Joyería y relojería", titulo="Autoridad de marca para joyería y relojería", desc="La autoridad es lo que sostiene el precio. Construimos la de su casa: criterio reconocido, contenido experto y materiales que venden cuando usted no está delante.",
                    h1=("En joyería manda", "<em>la autoridad.</em>"),
                    lead="La referencia de su plaza no negocia el precio. Esa autoridad se construye.",
                    media=("img", "joya-morganita", "Pendientes y anillo de morganita sobre terciopelo negro"),
                    margen=[("El producto supera a la marca", "Y el precio pasa a parecer alto."), ("Todo depende del mostrador", "Cada venta empieza de cero."),
                            ("La confianza está en el ceremonial", "Cómo se entrega pesa como la pieza."), ("Distribuir sin relato propio", "Un artículo más en la vitrina.")],
                    promessa="Que su casa sea la referencia <em>antes de que el cliente decida.</em>",
                    entrada=("Marketing estratégico", "Identidad, book comercial y ceremonial, presupuestados por alcance."),
                    extra_link=None),
}


def sector_pagina(chave, d):
    def corpo(R):
        casos = casos_de(chave) + ([CASO_FERRERAS] if chave == "joyeria-relojeria" else [])
        extra = f'<p class="plano-link">{enlace(R + d["extra_link"][0], d["extra_link"][1])}</p>' if d["extra_link"] else ""
        tipo, base, alt = d["media"]
        media = filme(R, base) if tipo == "vid" else fundo_img(R, base, alt)
        return (ph_media(R, d["nome"], L(*d["h1"]), d["lead"], btn(R + DIAG + "?sector=" + chave, CTA) + btn("#casos", "Ver casos reales", "btn-linha btn-vidro", False), media,
                         migas=[("", "Inicio"), ("sectores/", "Sectores"), (None, d["nome"])])
                + sec(f'{etq("", "Dónde se pierde el margen", "n")}{tachado([t for t, _ in d["margen"]])}<p class="titulo promessa" data-duas-tintas>{d["promessa"]}</p>', "margem")
                + sec(cab("", "Experiencia", "Lo que ya hemos hecho <em>en su terreno.</em>") + casos_grid(R, casos), extra=' id="casos"')
                + banda(f'{d["entrada"][0]}. <em>Por aquí se empieza.</em>', "Alcance e importe, por escrito tras el diagnóstico.", btn(R + DIAG + "?sector=" + chave, "Empezar el diagnóstico"),
                        f'<p class="mini">{d["entrada"][1]}</p>{extra}'))
    pagina(f"sectores/{chave}/", d["titulo"], d["desc"], corpo)

for k, v in SECTORES.items():
    sector_pagina(k, v)


SECT_MEDIA = {"hoteles": ("img", "salon-violin", "Una violinista toca en el salón de un hotel de montaña", "Hotel"),
              "automocion-lujo": ("vid", "reel-tn-porsche", "Porsche 911 GT3 RS negro en el estudio de TN Autosport", "Motor"),
              "nautica": ("img", "sector-mar-puerto", "Puerto deportivo de la Costa Brava visto desde el aire", "Mar"),
              "joyeria-relojeria": ("img", "sector-joya-esmeralda", "Anillo de esmeralda y diamantes sobre terciopelo negro", "Joya")}


def sector_capitulo(R, i, chave, d):
    tipo, base, alt, palavra = SECT_MEDIA[chave]
    m = video(R, base, alt) if tipo == "vid" else img(R, base, alt, "(min-width: 900px) 60vw, 100vw")
    n = len(casos_de(chave)) + (1 if chave == "joyeria-relojeria" else 0)
    ch = "".join(f"<li>{e(t)}</li>" for t, _ in d["margen"][:3])
    return (f'<article class="sx{se(i % 2 == 1, " inv")}"><a class="sx-media ventana" href="{R}sectores/{chave}/" data-janela aria-label="{e(d["nome"])}">{m}</a>'
            f'<div class="sx-txt"><span class="contorno sx-c" aria-hidden="true">{palavra}</span><p class="etiqueta">{e(d["nome"])}</p>'
            f'<h2 class="titulo t-l" data-linhas>{" ".join(d["h1"])}</h2><p class="lead" data-sube>{d["lead"]}</p>'
            f'<p class="sx-rot">Dónde se pierde el margen</p><ul class="sx-chips" data-sube>{ch}</ul>'
            f'<div class="acoes" data-sube>{btn(R + "sectores/" + chave + "/", "Ver el sector")}'
            f'{btn(R + DIAG + "?sector=" + chave, f"{n} caso" + ("" if n == 1 else "s") + " · Diagnóstico", "btn-linha", False)}</div></div></article>')


def sectores_idx(R):
    caps = "".join(sector_capitulo(R, i, k, v) for i, (k, v) in enumerate(SECTORES.items()))
    return (ph_media(R, "Sectores", L("Cuatro sectores,", "<em>vistos por dentro.</em>"), "Donde cada detalle se nota: hoteles, automoción, náutica y joyería.",
                     btn("#capitulos", "Ver los sectores"), filme(R, "auto"))
            + sec(f'<div class="sxs">{caps}</div>', "sect-caps", ' id="capitulos"') + banda("¿Su sector <em>es otro?</em>", "Inmobiliaria premium, servicios profesionales o B2B: las ocho preguntas le dicen por dónde empezar.", btn(R + DIAG, CTA)))

pagina("sectores/", "Sectores", "Hotelería, automoción de lujo, náutica y joyería: cuatro sectores que conocemos por dentro.", sectores_idx)


# ================================================================= RESULTADOS
def resultados(R):
    sectores_f = [("todos", "Todos"), ("automocion-lujo", "Automoción"), ("joyeria-relojeria", "Joyería"), ("hoteles", "Hoteles"), ("nautica", "Náutica"), ("b2b", "B2B")]
    problemas_f = [("todos", "Todos"), ("percepcion", "Percepción"), ("demanda", "Demanda"), ("conversion", "Conversión"), ("consultas", "Consultas perdidas"), ("saturacion", "Saturación")]

    def bs(tipo, lista):
        return "".join(f'<button type="button" data-f="{tipo}" data-v="{v}" aria-pressed="{str(v == "todos").lower()}">{e(t)}</button>' for v, t in lista)
    return (ph_media(R, "Casos", L("Lo que hicimos,", "<em>caso a caso.</em>"), "Cifras solo verificadas y autorizadas.",
                     btn("#casos", "Ver los casos"), filme(R, "interludio"))
            + sec(f'<div data-filtros><div class="filtro-linha"><p class="filtro-rot">Sector</p><div class="filtros">{bs("sector", sectores_f)}</div></div><div class="filtro-linha"><p class="filtro-rot">Problema</p><div class="filtros">{bs("problema", problemas_f)}</div></div><p class="conteo" data-conteo>{len(CASOS)} casos</p></div>'
                  + casos_grid(R, CASOS, True) + '<p class="mini nota-casos">Trabajo dirigido por Ferreras. Las cifras se publican una vez verificadas con el cliente.</p>', extra=' id="casos"')
            + sec(f'<div class="grelha marca-grid"><div class="marca-fotos"><figure class="f1 ventana" data-janela>{video(R, "reel-ferreras-lifestyle", "Campaña de Relojes Ferreras")}</figure><div class="f2 marca-reloj">{reloj_html(R, "-r")}</div></div><div class="marca-txt">{etq("", "Nuestra propia marca", "n")}<h2 class="titulo t-l" data-linhas>Lo probamos primero <em>con lo nuestro.</em></h2><p class="lead" data-sube>Cada método que le proponemos lo hemos aplicado antes a nuestra propia marca de relojes.</p><p data-sube>{enlace("https://relojes-ferreras.com/", "Ver Relojes Ferreras", True)}</p></div></div>', "claro marca", " data-claro")
            + banda("¿Algo parecido <em>en su sector?</em>", "Las ocho preguntas lo comparan con trabajos equivalentes.", btn(R + DIAG, CTA)))

pagina("casos/", "Casos", "Casos con problema, intervención, resultado y tipo de evidencia. Publicamos cifras solo cuando están verificadas y autorizadas.", resultados)




# ================================================================= WEB
def web(R):
    inf = ["Explica quiénes son", "Catálogo de servicios", "El visitante decide solo", "Formulario genérico", "Mide visitas", "Se rehace cada tres años"]
    com = ["Ordena la decisión paso a paso", "Demuestra con evidencia", "Cualifica antes de pedir datos", "Conectada a CRM", "Mide negocio", "Evoluciona cada mes"]

    def ul(lista):
        return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in lista) + "</ul>"
    ruta = [("Visita", "Llega con una pregunta."), ("Mensaje", "Entiende qué hace."), ("Prueba", "Ve evidencia."), ("Recomendación", "Un paso a su medida."), ("Lead", "Datos con contexto."), ("Seguimiento", "Su equipo llama preparado.")]
    planos = [("Web Signature", "Sobria y a la altura del negocio.", ["Diseño personalizado", "Hasta 5 páginas", "Copy, responsive y SEO básico"], ""),
              ("Web de Captación", "Cualifica y produce oportunidades.", ["Hasta 10–12 páginas", "Casos y sistema de prueba", "Funnel de cualificación", "CRM y medición"], "Bestseller de su categoría"),
              ("Ecommerce", "Catálogo y venta conectada.", ["Arquitectura de conversión", "Pagos, envíos y analítica", "SEO base y lanzamiento"], "")]
    ph_ = "".join(f'<div class="plano{se(bool(s), " dest")}" data-sube style="--i:{i}">{se(bool(s), "<span class=" + Q + "selo" + Q + ">" + s + "</span>")}<h3>{t}</h3><p class="texto">{p}</p><ul>{"".join("<li>" + e(x) + "</li>" for x in lista)}</ul></div>' for i, (t, p, lista, s) in enumerate(planos))
    pagos = [("50 %", "Al inicio."), ("30 %", "Con el diseño aprobado."), ("20 %", "Antes de publicar.")]
    pg = "".join(f'<div data-sube style="--i:{i}"><b>{a}</b><p>{b}</p></div>' for i, (a, b) in enumerate(pagos))
    return (ph_media(R, "Web y ecommerce", L("Su web, su mejor", "<em>comercial.</em>"), "Ordena su propuesta, demuestra valor y cualifica al cliente.",
                     btn(R + DIAG, CTA) + btn("#planes", "Ver los planes", "btn-linha btn-vidro", False), fundo_img(R, "reloj-terciopelo", "Reloj Ferreras de corazón abierto sobre terciopelo rojo"))
            + sec(cab("", "La diferencia", "Folleto <em>o comercial.</em>") + f'<div class="compara"><div data-sube><h3>Web informativa</h3>{ul(inf)}</div><div class="bom" data-sube style="--i:1"><h3>Infraestructura comercial</h3>{ul(com)}</div></div>')
            + sec(cab("", "Ruta del visitante", "De la primera visita <em>a la llamada.</em>") + flujo([a for a, _ in ruta]))
            + sec(cab("", "Planes", "Tres alcances, <em>o uno a medida.</em>", "Desarrollo propio. Alcance y precio por escrito antes de empezar.") + f'<div class="planos">{ph_}</div><p class="nota plano-flag"><b>Digital Flagship.</b> Multidioma, vídeo, motion, configuradores o áreas privadas: no es un paquete, es un proyecto.</p><div class="pagos">{pg}</div>', extra=' id="planes"')
            + banda("¿Qué le falta <em>a su web?</em>", "Mensaje, prueba o conversión: las ocho preguntas lo distinguen.", btn(R + DIAG, CTA)))


pagina("web/", "Web y ecommerce con arquitectura comercial", "Diseñamos webs que ordenan su propuesta, demuestran valor, cualifican al cliente y convierten la atención en una siguiente acción medible.", web)


# ================================================================= IA PARA HOTELES
def ia_hoteles(R):
    preg = ["Horarios", "Disponibilidad", "Servicios", "Restaurante", "Parking", "Mascotas", "Check-in", "Cómo llegar", "Cancelaciones", "Otros idiomas", "Fuera de horario"]
    cap = [("Atender llamadas", "Una conversación real, no un menú."), ("Responder lo de siempre", "Con los datos de su casa."), ("Hablar su idioma", "El mismo criterio en cada idioma."),
           ("Pasar a una persona", "Con el contexto ya recogido."), ("Conectarse a sus sistemas", "Según API y permisos."), ("Seguir sus protocolos", "Definidos con usted.")]
    mk = [("Imagen audiovisual", "Un hotel se vende por cómo se ve."), ("Email marketing", "La reserva directa más barata."), ("Redes sociales", "Lo que el huésped comparte."), ("Canales de venta", "Directa frente a comisión.")]
    hab = ["Menos de 20 habitaciones", "Entre 20 y 50", "Entre 50 y 100", "Entre 100 y 200", "Más de 200", "Varios establecimientos"]
    caso = dict(CASOS[2], t="Hotel Boltaña Ordesa", s="Un agente alrededor de la operativa real de un hotel de montaña.", ev=[])
    habs = [(x, x) for x in hab]
    form = (f'<form class="form-l" data-lead="hotel" novalidate><div class="campos">'
            + campo("h-nome", "nombre", "Nombre", req="Indique su nombre.", auto="name")
            + campo("h-emp", "hotel", "Hotel o establecimiento", req="Indique el nombre del establecimiento.", auto="organization")
            + campo("h-tel", "telefono", "Teléfono", "tel", req="Necesitamos un teléfono para poder llamarle.", auto="tel", extra=' data-min-dig="6"')
            + campo("h-mail", "email", "Email", "email", req="Revise la dirección de email.", auto="email")
            + pills("habitaciones", "Habitaciones", habs, hab[1])
            + area("h-mej", "mejora", "Qué quiere mejorar o automatizar", ph="Por ejemplo: reservas fuera de horario, preguntas repetidas, idiomas.", opc=True)
            + consentimento(R, "h") + TRAMPA
            + f'</div><div class="acoes"><button class="btn btn-claro" type="submit">Quiero estudiar mi caso <span class="fl">→</span></button></div>{estado_envio("Solicitud recibida")}</form>')
    return (ph_media(R, "Agentes de IA para hoteles", L("Su recepción,", "abierta toda la noche,", "<em>en cualquier idioma.</em>"), "Un agente diseñado alrededor de la operativa real de su establecimiento.",
                     btn("#estudio", "Estudiar mi hotel") + btn("#como", "Ver cómo funciona", "btn-linha btn-vidro", False), fundo_img(R, "salon-violin", "Una violinista toca en el salón de un hotel de montaña"))
            + sec(f'<div class="grelha noche-g"><figure class="dia24" data-dia24>{dia24_svg()}<figcaption class="dia24-ley"><span><i class="eq"></i>Recepción</span><span><i class="ag"></i>El agente, con la recepción cerrada</span><small>Ilustración: consultas de un día cualquiera.</small></figcaption></figure><div class="noche-txt">{etq("", "El día a día", "n")}<h2 class="titulo t-l" data-linhas>El teléfono no suena <em>cuando recepción está libre.</em></h2><div data-sube>{chips(preg)}</div></div></div>', "noche", ' id="como"')
            + sec(cab("", "Qué puede hacer", "Lo que puede <em>resolver solo.</em>") + lineas(cap))
            + sec(cab("", "Caso real", "Diseñado alrededor <em>de un hotel de verdad.</em>") + casos_grid(R, [caso]))
            + sec(cab("", "La otra mitad", "El agente atiende. <em>El marketing llena.</em>") + lineas(mk))
            + sec(f'<div class="vias"><div class="cab" style="margin:0">{etq("", "Solicitar estudio", "n")}<h2 class="titulo t-l" data-linhas>Cuéntenos <em>cómo es su caso.</em></h2><p class="lead" data-sube>Estudiamos su establecimiento antes de proponer nada.</p></div><div class="via">{form}</div></div>', extra=' id="estudio"'))


pagina("ia-hoteles/", "Agentes de IA para hoteles", "Agentes de IA y marketing para hoteles: atención 24 horas en cualquier idioma, imagen audiovisual premium, email marketing y redes.", ia_hoteles)


# ================================================================= CONTACTO
def contacto(R):
    sectores = [("Hotelería", "Hotelería"), ("Automoción", "Automoción"), ("Náutica", "Náutica"), ("Joyería", "Joyería"), ("Otro", "Otro")]
    plazos = [("Inmediato", "Inmediato"), ("En 30–90 días", "En 30–90 días"), ("El próximo trimestre", "El próximo trimestre"), ("Solo estoy explorando", "Solo estoy explorando")]
    form = (f'<form class="form-l" data-lead="contacto" novalidate><div class="campos">'
            + campo("c-nome", "nombre", "Nombre", req="Indique su nombre.", auto="name")
            + campo("c-emp", "empresa", "Empresa", req="Indique el nombre de su empresa.", auto="organization")
            + campo("c-mail", "email", "Email", "email", req="Revise la dirección de email.", auto="email")
            + campo("c-tel", "telefono", "Teléfono", "tel", auto="tel", opc=True)
            + campo("c-cargo", "cargo", "Cargo", auto="organization-title", opc=True)
            + pills("sector", "Sector", sectores) + pills("plazo", "Plazo", plazos)
            + area("c-msg", "objetivo", "Qué quiere conseguir", req="Cuéntenos brevemente qué necesita.", ph="Dos líneas bastan: qué quiere conseguir y qué le frena.")
            + pills("preferencia", "Prefiero que me contacten por", PREF) + consentimento(R, "c") + TRAMPA
            + f'</div><div class="acoes"><button class="btn btn-oscuro" type="submit">Enviar solicitud <span class="fl">→</span></button></div>{estado_envio("Solicitud recibida")}</form>')
    lado = (f'<aside class="placa placa-c"><div class="placa-foto">{img(R, "evento-terraza", "Invitados en la terraza de una presentación de Relojes Ferreras", "(min-width: 900px) 30vw, 90vw")}'
            f'<div class="placa-marca"><svg viewBox="0 0 235 256" aria-hidden="true">{marca_paths()}</svg><span>Barcelona</span></div></div>'
            f'<dl class="placa-l"><div><dt>Dirección</dt><dd>Passeig de Gràcia 95, 5º 1ª</dd></div><div><dt>Ciudad</dt><dd>08008 Barcelona</dd></div>'
            f'<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div><div><dt>Respuesta</dt><dd>Una persona, en un día laborable</dd></div></dl>'
            f'<p class="placa-pe">¿No sabe qué necesita? {enlace(R + DIAG, "Diagnóstico de dos minutos")}</p></aside>')
    return (ph(R, "Contacto", L("Escríbanos.", "<em>Contesta una persona.</em>"), "Si ya sabe lo que necesita, aquí. Si no, el diagnóstico de dos minutos.")
            + sec(f'<div class="grelha contacto-g"><div class="contacto-form">{form}</div>{lado}</div>', "claro", " data-claro"))

pagina("contacto/", "Hablemos", "Dos vías: si ya sabe lo que necesita, un formulario corto. Si no lo tiene claro, un diagnóstico de dos minutos.", contacto)


# ================================================================= DIAGNÓSTICO
def diagnostico(R):
    return (ph(R, "Diagnóstico comercial", L("Antes de hablar,", "<em>ocho preguntas.</em>"), "Sin puntuaciones ni presión. Al terminar sabrá por dónde empezar.")
            + sec(diag_html(R), "claro diag-sec", " data-claro"))

pagina("diagnostico/", "Ocho preguntas", "Ocho preguntas, dos minutos y una recomendación concreta: qué priorizar, por dónde empezar y cuáles son sus tres primeras acciones. Sin precios y sin compromiso.", diagnostico)


# ================================================================= LEGAL (texto do site antigo)
LEGAL_TXT = RAIZ / "_fonte" / "legal.json"


def legal_pagina(slug, titulo):
    ls = json.loads(LEGAL_TXT.read_text(encoding="utf-8"))[slug]

    def corpo(R):
        h1 = ls[0][4:].strip()
        partes = []
        for linha in ls[1:]:
            if linha.startswith("[h2]"):
                partes.append(f"<h2>{e(linha[4:].strip())}</h2>")
            elif linha.startswith("[h3]"):
                partes.append(f"<h3>{e(linha[4:].strip())}</h3>")
            elif linha.strip():
                t = e(linha.strip()).replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
                partes.append(f"<p>{t}</p>")
        return (f'<section class="pag-hero legal-hero"><div class="ph-txt"><p class="migas"><a href="{R}">Inicio</a> <span aria-hidden="true">/</span> Legal</p><h1 class="titulo t-l">{e(h1)}</h1></div></section>'
                + sec(f'<div class="prosa">{"".join(partes)}</div>'))
    pagina(f"legal/{slug}/", titulo, f"{titulo} de IA & Marketing Ferreras.", corpo)


legal_pagina("aviso-legal", "Aviso legal")
legal_pagina("privacidad", "Política de privacidad")
legal_pagina("cookies", "Política de cookies")


# ================================================================= 404, robots, sitemap
def p404(R):
    return ph(R, "Error 404", L("Esta hora no existe", "<em>en nuestro reloj.</em>"), "La página que busca se ha movido o nunca existió.", btn(R or "./", "Volver al inicio") + btn(R + DIAG, CTA, "btn-linha"))


pagina("404/", "Página no encontrada", "La página que busca no existe.", p404)
(RAIZ / "404.html").write_text((RAIZ / "404" / "index.html").read_text(encoding="utf-8").replace('"../', '"/ferreras/'), encoding="utf-8")
(RAIZ / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
(RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{URL}{r}</loc></url>\n" for r in FEITAS if r != "404/") + "</urlset>\n", encoding="utf-8")
(RAIZ / ".nojekyll").write_text("", encoding="utf-8")
(RAIZ / "favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -30 315 316"><rect x="-40" y="-30" width="315" height="316" rx="60" fill="#00101f"/>{marca_paths()}</svg>', encoding="utf-8")
print(len(FEITAS), "páginas:", ", ".join(r or "/" for r in FEITAS))


# endereços da versão anterior: levam à sala nova
for _velha, _nova in {"quien-somos/": "la-casa/", "resultados/": "casos/"}.items():
    (RAIZ / _velha).mkdir(exist_ok=True)
    (RAIZ / _velha / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Ferreras</title><meta http-equiv="refresh" content="0; url=../{_nova}"><a href="../{_nova}">Continuar</a>', encoding="utf-8")
