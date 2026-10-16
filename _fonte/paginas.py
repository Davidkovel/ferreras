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
    preguica = " data-lazy" if "lazy" in cls.split() else ""
    carga = ' loading="lazy"' if preguica else ' fetchpriority="high"'
    """Vídeo de fundo: horizontal no computador, vertical no telemóvel ao alto. O cartaz é um <picture> por baixo,
    o vídeo aparece por cima quando há fotogramas a sério (js/20-comuns.js)."""
    return (f'<div class="filme {cls}" aria-hidden="true"><picture><source media="(max-width: 899px) and (orientation: portrait)" srcset="{R}video/{nome}-v-poster.webp">'
            f'<img src="{R}video/{nome}-h-poster.webp" alt=""{carga}></picture>'
            f'<video muted playsinline loop preload="{"none" if preguica else "auto"}" data-filme{preguica} data-src-h="{R}video/{nome}-h.mp4" data-src-v="{R}video/{nome}-v.mp4"></video></div>')


def ph_media(R, eti, h1, lead, botoes, media, migas=None):
    """Hero de página interior: imagem ou vídeo de margem a margem, título por cima."""
    m = ""
    if migas:
        partes = [f'<a href="{R}{h}">{e(t)}</a>' if h is not None else e(t) for h, t in migas]
        m = '<p class="migas">' + ' <span aria-hidden="true">/</span> '.join(partes) + "</p>"
    ac = f'<div class="acoes" data-sube>{botoes}</div>' if botoes else ""
    return (f'<section class="pag-hero pag-media"><div class="pm-fundo">{media}</div><div class="pm-velo" aria-hidden="true"></div>'
            f'<div class="ph-txt">{m}{etq("", eti, "n")}<h1 class="titulo t-xl" data-linhas>{h1}</h1><p class="lead" data-sube>{lead}</p>{ac}</div></section>')


def fundo_img(R, base, alt):
    return img(R, base, alt, "100vw", lazy=False)


def faq_cab(num, titulo, link=""):
    return f'<div class="faq-cab">{etq(num, "Preguntas frecuentes", "n")}<h2 class="titulo t-l" data-linhas>{titulo}</h2>{link}</div>'


FAQ_INICIO = [
    ("¿Ferreras trabaja solo con marcas de lujo?", "No. Trabajamos habitualmente en entornos de lujo —automoción, joyería, relojería, hotelería y náutica— porque son sectores donde cada detalle se nota. Ese estándar lo aplicamos a cualquier empresa consolidada con margen y reputación que defender."),
    ("¿Tengo que elegir entre marketing e inteligencia artificial?", "No. Son las dos mitades del mismo departamento y entran juntas. En el diagnóstico decidimos por dónde empezar, según dónde se esté perdiendo hoy el dinero."),
    ("¿Cómo se controla lo que hace un agente de IA?", "Con alcance definido, permisos mínimos, registro de actividad, confirmación para acciones sensibles, entorno de pruebas y transferencia a una persona cuando la gestión lo requiere. Un agente hace lo que se le ha autorizado a hacer, y queda constancia."),
    ("¿Existe permanencia?", "En marketing recomendamos un mínimo de seis meses, porque la autoridad no se construye en menos. En proyectos web y de IA no hay permanencia: hay alcance, hitos y, si se desea, mantenimiento."),
    ("¿Cuándo recibiré respuesta?", "Una persona del equipo revisa cada solicitud y responde en un día laborable. Nunca con un mensaje automático haciéndose pasar por una persona."),
]

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
    ms = "".join(f'<p class="msg {c}">{se(bool(q), "<small>" + q + "</small>")}{e(t)}</p>' for c, q, t in CHAT)
    return (f'<div class="chat" role="log" aria-live="polite" aria-label="Simulación de una conversación con un agente de atención">'
            f'<div class="chat-cab"><b><i aria-hidden="true"></i>Agente de atención · Hotel</b><span>Simulación ilustrativa</span></div>'
            f'<div class="chat-lista">{ms}<p class="chat-vazio">Pulse «Probar la demostración».</p></div>'
            f'<div class="chat-pe"><span class="escribe" data-escribe hidden aria-hidden="true"><i></i><i></i><i></i></span><span>Permisos: solo lectura · registro activo</span></div></div>')


FASES = [("Diagnóstico", "Entender el negocio antes que el canal."), ("Diseño", "Definir el sistema y lo que queda fuera."),
         ("Implantación", "Construir, conectar y probar antes de encender."), ("Optimización", "Aprender de los datos y ajustar.")]


def fases_html():
    fs = "".join(f'<div class="fase" data-fase data-sube style="--i:{i}"><span class="num">0{i + 1}</span><h3>{n}</h3><p>{h}</p></div>' for i, (n, h) in enumerate(FASES))
    return f'<div class="grelha fases" data-linha-alvo><div class="linha-viva" data-linha-viva></div>{fs}</div>'


MKT_LISTA = ["Estrategia a 12 meses", "Podcast y entrevistas", "Vídeo y fotografía", "Redes y publicidad", "Imagen profesional", "Equipo y desplazamientos"]
IA_LISTA = ["Sistemas para su día a día", "Análisis de su empresa", "Agentes y automatizaciones", "Mejoras continuas", "Formación a su equipo"]


def sect_html(R, compacto=False):
    S = [("sectores/hoteles/", "hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado", "Hotelería", "Hoteles", "Más reservas y una marca que se recomienda."),
         ("sectores/automocion-lujo/", "tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario de automoción", "Automoción", "Automoción de lujo", "Contenido que enamora y vende coches."),
         ("sectores/nautica/", "yate-vistas", "Zona exterior de un yate con mesa, asientos y vistas a la costa", "Náutica", "Náutica, yates y puertos", "El mar, vivido antes de zarpar."),
         ("sectores/joyeria-relojeria/", "diamantes-anillos", "Dos anillos de diamantes sobre terciopelo azul oscuro", "Joyería", "Joyería y relojería", "Lujo que se desea y se recuerda.")]
    out = []
    for i, (h, b, alt, eti, t, p) in enumerate(S):
        out.append(f'<a href="{R}{h}">{img(R, b, alt, "(min-width: 900px) 45vw, 50vw")}<span class="etiqueta"><span class="n">0{i + 1}</span>{eti}</span><h3>{t}</h3><p>{p}</p><span class="fl" aria-hidden="true">→</span></a>')
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


# ================================================================= INICIO
# Composição à maneira do De Antonio, adaptada aos blocos da Ferreras: âncoras alternadas à esquerda e à direita,
# título e frase lado a lado, media fora do eixo ou a sair da margem, ar entre blocos, dois momentos de ecrã inteiro,
# números enormes só em contorno por trás das imagens. Os percentuais são guia de ritmo, não regra.
def inicio(R):
    ctl, pista = carril(R, TRABAJO, "Trabajos de producción propia")
    cifras = [("4", "sectores"), ("20+", "idiomas"), ("24 h", "de atención"), ("1 día", "laborable para responder")]
    cifras_h = "".join(f'<div data-sube style="--i:{i}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(cifras))
    return f'''
<section class="hero" data-hero data-hora="07:30" data-momento="Abre su empresa">
  {filme(R, 'showreel', 'hero-filme')}
  <div class="hero-velo" aria-hidden="true"></div>
  <div class="hero-grid">
    <div class="hero-tit"><p class="etiqueta" style="--i:0"><span class="hora">07:30</span>Barcelona · Marketing de lujo e inteligencia artificial</p>
      <h1 class="titulo t-xxl" data-linhas>{L('Su departamento', 'de marketing e IA.', '<em>Todo incluido.</em>')}</h1></div>
    <div class="hero-lado"><p class="lead" style="--i:1">De la agencia que crea marcas de lujo y tiene la suya propia.</p>
      <div class="acoes" style="--i:2">{btn(R + DIAG, CTA)}{btn('#trabajo', 'Ver el trabajo', 'btn-linha btn-vidro', False)}</div></div>
  </div>
  <p class="hero-pista" aria-hidden="true"><i></i>El reloj avanza con usted</p>
</section>

<section class="sec prod p-prod" id="trabajo" data-hora="10:30" data-momento="Rodaje en el puerto">
  <div class="grelha p-cab">
    <div class="p-tit">{etq('10:30', 'Así se ve nuestro trabajo')}<h2 class="titulo t-l" data-linhas>{L('Contenido que se ve,', 'se comparte <em>y se recuerda.</em>')}</h2></div>
    <p class="lead p-lead" data-sube>Producción propia: dron, cámaras, sonido e iluminación. El equipo y los desplazamientos van incluidos.</p>
  </div>
  {pista}
  <div class="grelha p-pe"><div class="prod-dado" data-sube><b><span data-conta="20000">20.000</span>–<span data-conta="300000">300.000</span></b><span>visitas de media por pieza en la línea editorial de un negocio de automoción deportiva</span></div>{ctl}</div>
</section>

<section class="interludio" data-hora="12:00" data-momento="Lo que no se puede repetir">
  {filme(R, 'interludio', 'lazy')}
  <div class="int-velo" aria-hidden="true"></div>
  <h2 class="titulo t-xl int-h" data-linhas>{L('Lo que no se puede repetir', '<em>se prepara antes.</em>')}</h2>
</section>

<section class="sec mitades p-mit" data-hora="13:00" data-momento="Dos departamentos, un solo plan">
  <div class="grelha p-mit-cab">
    <p class="contorno mit-24" aria-hidden="true">24 h</p>
    <div class="p-mit-tit">{etq('13:00', 'Las dos mitades')}<h2 class="titulo t-xl" data-linhas>{L('Marketing que atrae.', '<em>IA que atiende.</em>')}</h2><p class="lead" data-sube>Deslice la línea: el mismo barco, de día y de noche.</p></div>
  </div>
  <div class="rx rx-total" data-rx role="slider" tabindex="0" aria-label="Del día a la noche: marketing e inteligencia artificial" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
    <div class="rx-capa rx-dia">{img(R, 'yate-completo', 'Yate de lujo fondeado en una cala de aguas turquesa, de día')}</div>
    <div class="rx-capa rx-noche">{img(R, 'yate-noche', 'El mismo yate de noche, con las luces del salón encendidas')}</div>
    <div class="rx-linha" aria-hidden="true"></div><div class="rx-pega" aria-hidden="true">↔</div>
    <a class="rx-rot d" href="{R}marketing/"><b>De día · Marketing</b><span>Que le vean como merece</span></a>
    <a class="rx-rot n" href="{R}inteligencia-artificial/"><b>De noche · IA</b><span>Que nadie se quede sin respuesta</span></a>
  </div>
</section>

<section class="sec p-sect" data-hora="15:30" data-momento="Cuatro sectores">
  <div class="cab p-sect-cab">{etq('15:30', 'Sectores')}<h2 class="titulo t-l" data-linhas>{L('Cuatro sectores que conocemos <em>por dentro.</em>')}</h2></div>
  {sect_html(R)}
</section>

<section class="sec claro p-marca" data-claro data-hora="17:30" data-momento="Relojes Ferreras, nuestra marca">
  <div class="grelha p-marca-cab"><div class="p-marca-tit">{etq('17:30', 'Marca propia')}<h2 class="titulo t-xl" data-linhas>{L('Sabemos crear una marca.', '<em>Por eso tenemos la nuestra.</em>')}</h2></div></div>
  <div class="grelha trofeus">
    <figure class="trofeu t1"><span class="contorno" aria-hidden="true">100</span><div class="ventana" data-janela>{video(R, 'hero-ferreras-lifestyle', 'Campaña de Relojes Ferreras: un Aston Martin en una carretera de montaña nevada', 720, 1280)}</div><figcaption class="pie"><b>Edición limitada</b>A 100 piezas</figcaption></figure>
    <figure class="trofeu t2"><span class="contorno" aria-hidden="true">BCN</span><div class="tr-reloj">{reloj_html(R, '-m')}</div><figcaption class="pie"><b>Ensamblaje en Barcelona</b>Diseño propio y mecanismo suizo</figcaption></figure>
  </div>
  <div class="grelha p-marca-pe"><p data-sube>{enlace('https://relojes-ferreras.com/', 'Conocer Relojes Ferreras', True)}</p><p class="marca-nota" data-sube>{mini_reloj()}El reloj que le acompaña en esta página es el nuestro.</p></div>
</section>

<section class="sec p-dep" data-hora="20:00" data-momento="Todo incluido">
  <div class="grelha p-dep-cab">
    <div class="p-dep-tit">{etq('20:00', 'El departamento')}<h2 class="titulo t-l" data-linhas>{L('Un departamento', 'dentro de su empresa.', '<em>Todo incluido.</em>')}</h2></div>
    <p class="lead p-dep-lead" data-sube>Marketing e inteligencia artificial: dos equipos de especialistas con un solo plan.</p>
  </div>
  <figure class="p-dep-card"><div class="ventana" data-janela>{img(R, 'fernando-ferreras-ceo', 'Fernando Ferreras en un puerto deportivo, junto a dos vehículos de alta gama con estuches de reloj expuestos y embarcaciones al fondo', '(min-width: 900px) 72vw, 100vw')}</div><figcaption class="pie"><b>Fernando Ferreras</b>Dirección</figcaption></figure>
  <ul class="p-dep-tres"><li data-sube>Sin contratar, formar ni coordinar a nadie</li><li data-sube style="--i:1">Un solo equipo, un solo plan</li><li data-sube style="--i:2">Trato uno a uno con quien dirige su proyecto</li></ul>
  <dl class="cifras">{cifras_h}</dl>
</section>

<section class="sec noche p-noche" data-hora="23:40" data-momento="La consulta que entra de noche">
  <div class="grelha noche-g">
    <figure class="dia24" data-dia24>{dia24_svg()}<figcaption class="dia24-ley"><span><i class="eq"></i>Su equipo</span><span><i class="ag"></i>El agente, con la recepción cerrada</span><small>Ilustración: consultas de un día cualquiera.</small></figcaption></figure>
    <div class="noche-txt">
      {etq('23:40', 'Departamento de IA')}
      <h2 class="titulo t-l" data-linhas>{L('La consulta de las 23:40', '<em>no es una consulta perdida.</em>')}</h2>
      <p class="lead" data-sube>El agente responde en su idioma y, en el punto que usted decide, pasa el caso a una persona.</p>
      <p data-sube>{enlace(R + 'inteligencia-artificial/#demo', 'Ver una conversación de ejemplo')}</p>
    </div>
  </div>
</section>

<section class="sec p-faq" data-hora="07:00" data-momento="Antes de empezar">
  <div class="grelha">{faq_cab('07:00', L('Lo que suelen', 'preguntarnos', '<em>antes de empezar.</em>'), '<p>' + enlace(R + 'contacto/', 'Hacer otra pregunta') + '</p>')}{faq(FAQ_INICIO, 'fi')}</div>
</section>

<section class="sec claro final p-final" data-claro data-hora="07:30" data-momento="Veinticuatro horas después">
  <div class="grelha final-grid">
    <div class="final-txt">
      {etq('07:30', 'Veinticuatro horas después')}
      <h2 class="titulo t-xl" data-linhas>{L('Ha llegado hasta aquí', 'porque nunca se ha conformado.', '<em>Su empresa tampoco debería.</em>')}</h2>
      <div class="acoes" data-sube>{btn(R + DIAG, CTA, 'btn-oscuro')}{btn(R + 'contacto/', 'Escribir directamente', 'btn-linha', False)}</div>
    </div>
    <div class="final-dados" data-sube><div><b>8</b><span>preguntas</span></div><div><b>2 min</b><span>para completarlo</span></div><div><b>0 €</b><span>sin compromiso</span></div><div><b>3</b><span>primeras acciones</span></div></div>
  </div>
</section>
'''


pagina("", "IA & Marketing Ferreras · Su departamento de marketing e IA. Todo incluido.",
       "Un departamento de marketing y otro de inteligencia artificial montados dentro de su empresa, con un solo plan. Agencia de marketing de lujo en Barcelona: hotelería, automoción, náutica y joyería.",
       inicio, inicio=True)


# ================================================================= CASOS (dados partilhados)
CASOS = [
    dict(id="auto-voz", sector="automocion-lujo", sl="Automoción de lujo", prob="percepcion demanda", foto=("tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario de automoción"),
         t="De publicar coches a ser la voz de referencia del sector", s="Contenido de alto alcance y un podcast propio.",
         p="Una cuenta consolidada cuya presencia digital no reflejaba la autoridad real del negocio ni la calidad de su inventario.",
         i="Una línea editorial reconocible: piezas pensadas para alcance y un formato de podcast propio.",
         r="La cuenta pasó de acompañar al negocio a liderar la conversación de su categoría.",
         ev=["Contenidos con millones de visitas y una media de entre 20.000 y 300.000 visitas por pieza", "La comunidad se multiplicó durante el periodo de trabajo continuado"]),
    dict(id="joya-marca", sector="joyeria-relojeria", sl="Joyería y relojería", prob="percepcion", foto=("diamantes-riviere", "Macro de una pulsera rivière de diamantes sobre terciopelo azul oscuro"),
         t="Una pieza excepcional necesitaba una marca a su altura", s="Identidad, herramientas comerciales y contenido experto.",
         p="Producto de primer nivel y una identidad que no comunicaba ni su solvencia ni el ceremonial de una compra así.",
         i="Construir la marca y sus materiales: no solo un logotipo, también con qué se presenta y se cierra una venta.",
         r="Un estándar coherente con el valor del producto, con materiales que sostienen la venta.", ev=[]),
    dict(id="hotel-agente", sector="hoteles", sl="Hoteles", prob="consultas saturacion", foto=("hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado"),
         t="Un agente diseñado alrededor de la operativa real de un hotel", s="Más de veinte idiomas y derivación a recepción.",
         p="Consultas a cualquier hora, en varios idiomas y por varios canales, y una recepción que no puede estar en todo.",
         i="Un agente a medida, no un chatbot genérico: qué responde, qué consulta y cuándo avisa a una persona.",
         r="Atención continuada en más de veinte idiomas, con derivación a recepción cuando hace falta.", ev=[]),
    dict(id="auto-producto", sector="automocion-lujo", sl="Automoción de lujo", prob="demanda percepcion", foto=("sm-cardress-funda", "Coupé deportivo cubierto con una funda textil a medida con diseño personalizado"),
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
CASO_FERRERAS = dict(id="ferreras", sector="joyeria-relojeria", sl="Marca propia", prob="", foto=("reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche"),
                     t="Relojes Ferreras: nuestra propia casa", s="Diseño propio, mecanismo suizo y ensamblaje en Barcelona.",
                     p="Crear una marca de relojería obliga a resolver en casa lo mismo que un cliente encarga a una agencia.",
                     i="Construirla con el mismo método que proponemos, sin atajos ni decisiones delegadas.",
                     r="Un banco de pruebas permanente: lo que recomendamos lo hemos aplicado antes en casa.", ev=[])


def caso_html(R, c, filtro=False):
    foto = img(R, c["foto"][0], c["foto"][1], "(min-width: 900px) 30vw, 100vw") if c["foto"] else f'<div class="caso-marca"><svg viewBox="0 0 235 256" aria-hidden="true">{marca_paths()}</svg></div>'
    ev = ""
    if c["ev"]:
        ev = '<div class="evid">' + "<br>".join(e(x) for x in c["ev"]) + "<small>Trabajo dirigido por Ferreras. Las cifras se publican una vez verificadas con el cliente.</small></div>"
    atr = f' data-caso data-sector="{c["sector"]}" data-problema="{c["prob"]}"' if filtro else ""
    return (f'<details class="caso"{atr}><summary><div class="caso-foto ventana">{foto}</div><div class="caso-cab"><p class="etiqueta">{e(c["sl"])}</p>'
            f'<h3>{e(c["t"])}</h3><p>{e(c["s"])}</p><span class="caso-abre">Ver el caso<i aria-hidden="true"></i></span></div></summary>'
            f'<dl><dt>Problema</dt><dd>{e(c["p"])}</dd><dt>Intervención</dt><dd>{e(c["i"])}</dd><dt>Resultado</dt><dd>{e(c["r"])}</dd>{ev}</dl></details>')


def casos_de(sector):
    return [c for c in CASOS if c["sector"] == sector]


def pequenas(items, cols=4):
    """Cartões curtos: título e uma linha. Sem parágrafos."""
    return cards(items, cols, True)


# ================================================================= QUIÉN SOMOS
def quien(R):
    marcas = [("reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche", "Relojería · Marca propia", "Relojes Ferreras"),
              ("tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario de automoción", "Automoción", "TN Autosport"),
              ("hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado", "Hotelería", "Hotel Boltaña Ordesa"),
              ("puerto-club-vela-blanes", "Vista aérea de un puerto deportivo, su dique y la playa contigua", "Náutica", "Club náutico · Costa Brava"),
              ("diamantes-anillos", "Dos anillos de diamantes sobre terciopelo azul oscuro", "Joyería", "Joyería de diamantes · España"),
              ("sm-cardress-funda", "Coupé deportivo cubierto con una funda textil a medida con diseño personalizado", "Automoción", "Producto premium para automoción")]
    mh = "".join(f'<div class="marca-c"><div class="ventana">{img(R, b, alt, "(min-width: 900px) 30vw, 70vw")}</div><p class="etiqueta">{s}</p><h3>{t}</h3></div>' for b, alt, s, t in marcas)
    pruebas = [("Construimos nuestras propias marcas", "Lo que proponemos, lo hemos decidido antes en casa."),
               ("Transformamos la percepción de clientes", "Marcas cuya imagen pasó a estar a su altura."),
               ("Trabajamos donde no se repite la toma", "Hoteles, yates, puertos y regatas.")]
    return (ph(R, "Quién somos", L("Llevamos el marketing", "de marcas de referencia", "<em>en su sector.</em>"),
               "El departamento de marketing de TN Autosport y los creadores de Relojes Ferreras.",
               btn(R + DIAG, CTA), img(R, "fernando-ferreras-ceo", "Fernando Ferreras en un puerto deportivo, junto a dos vehículos de alta gama con estuches de reloj expuestos y embarcaciones al fondo", "(min-width: 900px) 40vw, 100vw", lazy=False))
            + sec(cab("01", "Marcas que llevamos", "Detrás de marcas que su sector <em>ya reconoce.</em>") + f'<div class="marcas">{mh}</div>')
            + sec(f'{etq("02", "Estándar", "n")}<p class="titulo promessa" data-duas-tintas>El lujo no es una etiqueta. <em>Es un estándar de ejecución.</em></p><p class="lead" data-sube>Pocas empresas, muy de cerca. La dirección entra en cada proyecto y no se delega.</p>')
            + sec(cab("03", "Autoridad", "Tres pruebas, <em>no tres adjetivos.</em>") + cards(pruebas, 3))
            + sec(cab("04", "Método", "Cada fase tiene <em>un responsable.</em>") + fases_html())
            + banda("¿Qué sistema encaja <em>con su empresa?</em>", "Dos minutos y sabrá por dónde empezar.", btn(R + DIAG, CTA)))


pagina("quien-somos/", "Quién somos", "Llevamos el marketing de marcas de referencia en su sector, como TN Autosport en automoción, y somos los creadores de Relojes Ferreras. Departamento de marketing e IA en Barcelona.", quien)


# ================================================================= MARKETING
MKT_TABS = [
    ("Estrategia a doce meses", "Qué tiene que cambiar en la percepción de su empresa, y en qué orden. Por escrito y revisado cada mes.", ["Análisis del negocio y de su cliente", "Posicionamiento y mensajes", "Calendario editorial a doce meses", "Panel de seguimiento mensual"]),
    ("Producción audiovisual", "Equipo propio y desplazamientos incluidos. Un producto de alto valor se juzga por cómo se ve.", ["Dron para exteriores y embarcaciones", "Vídeo y fotografía de producto y marca", "Eventos, regatas y entregas", "Postproducción y versiones por canal"]),
    ("Podcast y entrevistas", "Que se le vea explicando su criterio, no vendiendo su producto.", ["Formato propio de podcast o entrevista", "Guion, grabación, edición y distribución", "Ponencias y apariciones", "Imagen profesional"]),
    ("Redes y comunidad", "Una línea editorial reconocible, publicada con constancia.", ["Los canales que le convienen", "Contenido para alcance y preferencia", "Conversación y comunidad"]),
    ("Publicidad", "Objetivo declarado y medición honesta. La inversión se decide con usted.", ["Alcance, captación y recuperación", "Segmentación por público", "Lectura mensual de resultados"]),
    ("Email y canales de venta", "Recuperar a quien ya le conoce cuesta menos que convencer a quien no.", ["Recuperación y fidelización", "Venta directa frente a comisión", "Presencia donde su cliente decide"]),
    ("Web, ecommerce y SEO", "Desarrollada por nuestro equipo informático: una web que cualifica.", ["Arquitectura, mensaje y prueba", "Desarrollo a medida", "Ecommerce y catálogo", "SEO técnico y medición"]),
]


def marketing(R):
    problemas = [("Le comparan con quien no debería", "Cuando el cliente no distingue, decide por precio."),
                 ("Publica, pero no acumula", "Mucha actividad y ninguna autoridad que se quede."),
                 ("Depende de usted estar delante", "Lo que no está contado no vende por usted."),
                 ("Las métricas no hablan de dinero", "Sube el alcance; nadie sabe cuántas ventas trae.")]
    orden = [("Diagnóstico", "Cómo gana dinero y cómo decide su cliente."), ("Estrategia", "Qué cambiamos y en qué orden."), ("Producción", "Rodajes con equipo propio."), ("Distribución", "Constancia en los canales que convienen."), ("Lectura", "Revisión mensual de resultados.")]
    faqs = [("¿Cuánto tardan en verse resultados?", "Depende del punto de partida, del sector y del alcance. Fijamos objetivos y calendario en el diagnóstico y revisamos contra ellos."),
            ("¿Quién aparece en los vídeos?", "Quien mejor represente el criterio de la empresa. Existen formatos sin rostro, aunque construyen autoridad más despacio."),
            ("¿La inversión publicitaria está incluida?", "La gestión sí; el dinero que se entrega a las plataformas, no. Se decide con usted y se paga desde su cuenta.")]
    ctl, pista = carril(R, TRABAJO[:6], "Trabajos de producción propia")
    return (ph_media(R, "Departamento de Marketing", L("Que su empresa", "se perciba", "<em>como lo que es.</em>"),
                     "Estrategia, producción audiovisual propia y distribución, dentro de su empresa.",
                     btn(R + DIAG, CTA) + btn("#produccion", "Ver la producción", "btn-linha btn-vidro", False), filme(R, "showreel"))
            + sec(f'<div class="prod-cab"><div class="cab">{etq("01", "Producción propia", "n")}<h2 class="titulo t-l" data-linhas>No subcontratamos <em>la cámara.</em></h2></div></div>{pista}<div class="prod-pe">{ctl}<p class="mini">Dron, cámaras, sonido e iluminación. Equipo y desplazamientos incluidos.</p></div>', "prod", ' id="produccion"')
            + sec(cab("02", "El problema", "El producto está a la altura. <em>La percepción, casi nunca.</em>") + pequenas(problemas))
            + sec(cab("03", "Qué incluye", "Todo lo que haría <em>un departamento propio.</em>") + tabs("mk", MKT_TABS))
            + sec(cab("04", "El orden", "Cinco fases. <em>Ninguna se salta.</em>") + passos(orden))
            + sec(f'<div class="grelha">{faq_cab("05", "Lo que suelen <em>preguntarnos.</em>")}{faq(faqs, "fm")}</div>')
            + banda("¿Cómo se ve hoy su empresa <em>desde fuera?</em>", "Lo analizamos sin compromiso.", btn(R + DIAG, CTA), chips(CONDICIONES, "chips chips-cond")))


pagina("marketing/", "Departamento de Marketing", "Un departamento de marketing completo dentro de su empresa: estrategia a doce meses, producción audiovisual propia con dron y equipo, podcast, redes, publicidad, email marketing y web.", marketing)


# ================================================================= IA
IA_TABS = [
    ("Primero, usted", "Sistemas que le quitan horas a usted antes de tocar la empresa.", ["Asistentes privados con el contexto de su negocio", "Preparación y resumen de reuniones", "Análisis de documentación", "Formación uno a uno"]),
    ("Agentes de atención", "Teléfono, chat, WhatsApp o email. Responden, consultan y avisan a una persona.", ["Más de veinte idiomas", "Transferencia con el contexto recogido", "Conocimiento de su casa"]),
    ("Análisis de la empresa", "Dónde se pierde tiempo y dinero, y qué conviene automatizar.", ["Mapa de procesos", "Qué se automatiza y qué no", "Prioridades por retorno"]),
    ("Integraciones", "Conectado a lo que ya usa, con datos actualizados.", ["CRM, agenda, reservas, PMS y correo", "Solo lectura por defecto", "Entorno de pruebas"]),
    ("Control y mejora", "Revisamos conversaciones reales y corregimos lo que no responde bien.", ["Permisos, confirmaciones y registro", "Revisión periódica", "Ampliaciones de alcance"]),
]


def ia(R):
    problemas = [("La consulta fuera de hora", "Cuando alguien la lee, el cliente ya ha resuelto en otro sitio."),
                 ("Dos cosas a la vez", "Se atiende deprisa al teléfono y mal a quien tiene delante."),
                 ("El criterio en dos cabezas", "Si no están, la empresa responde peor."),
                 ("Una tecnología que cambia cada mes", "Estar al día es un trabajo, y no es el suyo.")]
    pasos = [("Analizamos", "Qué entra por cada canal."), ("Decidimos", "Qué automatizar y qué no."), ("Diseñamos", "Idiomas, permisos y transferencia."), ("Probamos", "Antes de hablar con ningún cliente."), ("Arrancamos", "Con su equipo formado."), ("Optimizamos", "Con conversaciones reales.")]
    faqs = [("¿Esto es un chatbot?", "No. Un chatbot se contrata; nosotros implantamos un sistema: conocimiento de su empresa, conexiones, permisos, pruebas, supervisión y mejora."),
            ("¿El agente puede equivocarse?", "Puede. Por eso se define qué está autorizado a hacer, qué requiere confirmación y cuándo avisa a una persona."),
            ("¿Qué pasa con los datos de nuestros clientes?", "Permisos mínimos y el menor volumen de datos necesario, todo definido por escrito antes de conectar nada."),
            ("¿Sustituye a una persona del equipo?", "No es el objetivo: las personas dejan lo repetitivo y dedican su tiempo a cerrar, resolver y cuidar al cliente.")]
    demo = (f'<div class="demo" data-demo><div class="cab" style="margin:0">{etq("02", "Demostración", "n")}<h2 class="titulo t-l" data-linhas>Pruébelo <em>usted mismo.</em></h2>'
            f'<p class="lead" data-sube>Fíjese menos en lo que responde y más en lo que se niega a responder.</p>'
            f'<div class="acoes" data-sube><button type="button" class="btn btn-claro" data-demo-play><span>Probar la demostración</span> <span class="fl">→</span></button></div>'
            f'<p class="mini">{AVISO_DEMO}</p></div>{chat_html()}</div>')
    return (ph_media(R, "Departamento de IA", L("Que su empresa", "atienda siempre.", "<em>También de noche.</em>"),
                     "Agentes de atención en más de veinte idiomas, con supervisión humana.",
                     btn(R + DIAG, CTA) + btn("#demo", "Ver la demostración", "btn-linha btn-vidro", False), fundo_img(R, "yate-noche", "Un yate de noche con las luces del salón encendidas"))
            + sec(f'<div class="grelha noche-g"><figure class="dia24" data-dia24>{dia24_svg()}<figcaption class="dia24-ley"><span><i class="eq"></i>Su equipo</span><span><i class="ag"></i>El agente, con la recepción cerrada</span><small>Ilustración: consultas de un día cualquiera.</small></figcaption></figure><div class="noche-txt">{etq("01", "Cómo funciona", "n")}<h2 class="titulo t-l" data-linhas>Dónde responde, <em>y dónde deja de hacerlo.</em></h2><p class="lead" data-sube>Lo importante no es que conteste: es el punto exacto en el que calla y avisa a una persona. Ese punto se decide con usted.</p></div></div>', "noche")
            + sec(demo, extra=' id="demo"')
            + sec(cab("03", "El problema", "Lo repetitivo se come <em>el tiempo de vender.</em>") + pequenas(problemas))
            + sec(cab("04", "Qué incluye", "Empezamos por usted. <em>Después, por la empresa.</em>") + tabs("ia", IA_TABS))
            + sec(cab("05", "El orden", "Seis pasos. <em>El primero no es instalar nada.</em>") + passos(pasos))
            + sec(f'<div class="grelha">{faq_cab("06", "Lo que suelen <em>preguntarnos.</em>")}{faq(faqs, "fa")}</div>')
            + banda("¿Qué atiende hoy su equipo <em>que no debería?</em>", "Lo analizamos sin compromiso.", btn(R + DIAG, CTA) + btn(R + "ia-hoteles/", "El caso de hotelería", "btn-linha"), chips(CONDICIONES, "chips chips-cond")))


pagina("inteligencia-artificial/", "Departamento de IA", "Un departamento de desarrollo de inteligencia artificial dentro de su empresa: agentes de atención en más de veinte idiomas, integraciones con sus sistemas, automatización de procesos y formación a su equipo.", ia)


# ================================================================= SECTORES
SECTORES = {
    "hoteles": dict(nome="Hoteles", titulo="Agentes de IA para hoteles", desc="Atienda 24/7, en varios idiomas y sin saturar recepción. Agentes de voz, chat y WhatsApp diseñados alrededor de la operativa real de su establecimiento.",
                    h1=("Atienda 24/7,", "en cualquier idioma,", "<em>sin saturar recepción.</em>"),
                    lead="Un agente que responde lo que sabe y avisa a recepción cuando hace falta una persona.",
                    media=("img", "ia-hotel-recepcion-equipo", "Recepcionista atendiendo en persona a una huésped mientras un sistema resuelve consultas en paralelo"),
                    margen=[("La consulta de las 23:40", "No es una consulta perdida: es una habitación vacía."), ("Dos cosas a la vez", "El teléfono suena con un huésped delante."),
                            ("Las mismas quince preguntas", "Horarios, parking, mascotas, cancelaciones."), ("El canal gana a la reserva directa", "Y la comisión pasa a ser la norma.")],
                    promessa="Que ninguna consulta se quede sin respuesta, <em>y que recepción recupere su tiempo.</em>",
                    entrada=("Asistente IA 24/7 para hoteles", "La integración con PMS depende de la API, los permisos y las pruebas. Los consumos de voz y mensajería se facturan aparte."),
                    extra_link=("ia-hoteles/", "Cómo trabajamos la atención de un hotel"),
                    faq=[("¿Se integra con nuestro PMS o Channel Manager?", "Depende de la API, de los permisos y de las pruebas. Se evalúa en el diagnóstico, no se da por hecha."),
                         ("¿El agente puede confirmar una reserva?", "Solo si se autoriza expresamente, con confirmación y registro. Por defecto, consulta y derivación a recepción."),
                         ("¿Qué pasa fuera del horario de recepción?", "El agente responde y deja la consulta lista para que recepción la resuelva a primera hora.")]),
    "automocion-lujo": dict(nome="Automoción de lujo", titulo="Marketing para automoción de lujo", desc="Eleve la percepción de su inventario y convierta atención en consultas cualificadas con contenido audiovisual y formatos de autoridad.",
                    h1=("Su inventario merece", "más que una ficha", "<em>con doce fotos.</em>"),
                    lead="Vídeo y formatos de autoridad que convierten atención en consultas cualificadas.",
                    media=("vid", "loop-gt3", ""),
                    margen=[("Se ve, pero no se desea", "Fotos correctas y ningún relato."), ("Alcance sin consultas", "Gusta, se comparte y no vende."),
                            ("La autoridad se la lleva otro", "Quien habla con criterio es la referencia."), ("El producto asociado no se explica", "Se vende en movimiento, no en estático.")],
                    promessa="Elevar la percepción del inventario <em>y convertir la atención en consultas.</em>",
                    entrada=("Autoridad & Demanda", "Estrategia, producción, distribución y panel de KPIs. La inversión publicitaria, aparte."),
                    extra_link=None,
                    faq=[("¿Graban en nuestras instalaciones?", "Sí: en su exposición o donde mejor se represente el vehículo."),
                         ("¿Sirve para vehículo de ocasión premium?", "Sí. Es donde más se nota la diferencia entre una ficha y una pieza bien contada."),
                         ("¿Necesitamos aparecer en cámara?", "Ayuda mucho en los formatos de autoridad. Hay alternativas sin rostro, más lentas.")]),
    "nautica": dict(nome="Náutica, yates y puertos", titulo="Marketing náutico: clubs, astilleros, yates y chárter", desc="Clubs náuticos, astilleros, compraventa de yates y alquiler de barcos. Identidad, producción audiovisual, cobertura de regatas y eventos, y comercialización.",
                    h1=("El mar se vende", "<em>enseñándolo.</em>"),
                    lead="Clubs, astilleros, compraventa y chárter: producción, regatas y comercialización.",
                    media=("img", "yate-completo", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire"),
                    margen=[("La experiencia no se transmite", "El cliente solo ve un barco blanco más."), ("Un club vive de que le vean", "Socios, escuela y patrocinadores."),
                            ("La regata se evapora", "El mejor material del año, sin uso posterior."), ("La consulta internacional se enfría", "Idioma, horario y respuesta deciden.")],
                    promessa="Que una embarcación se perciba como se vive <em>y llegar a quien aún no le conoce.</em>",
                    entrada=("Producción y comercialización", "Identidad e infraestructura digital por alcance. Viajes y dietas aparte."),
                    extra_link=None,
                    faq=[("¿Trabajan la comercialización internacional?", "La producción y la distribución, sí. La operación la mantiene usted o su bróker."),
                         ("¿Producen con dron?", "Sí, cuando la localización y la normativa lo permiten."),
                         ("¿Pueden cubrir una regata completa?", "Sí, incluida cobertura en vivo, con la historia decidida antes.")]),
    "joyeria-relojeria": dict(nome="Joyería y relojería", titulo="Autoridad de marca para joyería y relojería", desc="La autoridad es lo que sostiene el precio. Construimos la de su casa: criterio reconocido, contenido experto y materiales que venden cuando usted no está delante.",
                    h1=("En joyería no gana el que más enseña.", "<em>Gana el que más autoridad tiene.</em>"),
                    lead="La referencia de su plaza no negocia el precio. Esa autoridad se construye.",
                    media=("img", "diamantes-pulsera-zafiros", "Pulsera de zafiros azules y diamantes sobre terciopelo azul oscuro"),
                    margen=[("El producto supera a la marca", "Y el precio pasa a parecer alto."), ("Todo depende del mostrador", "Cada venta empieza de cero."),
                            ("La confianza está en el ceremonial", "Cómo se entrega pesa como la pieza."), ("Distribuir sin relato propio", "Un artículo más en la vitrina.")],
                    promessa="Que su casa sea la referencia <em>antes de que el cliente decida.</em>",
                    entrada=("Marketing estratégico", "Identidad, book comercial y ceremonial, presupuestados por alcance."),
                    extra_link=None,
                    faq=[("¿Trabajan con marcas sin identidad?", "Sí, es el punto de partida más frecuente."),
                         ("¿Producen fotografía de producto?", "Sí: una pieza mal fotografiada se percibe como de menos valor."),
                         ("¿Ayudan con la distribución en otras joyerías?", "Construimos los materiales y la estrategia; la relación comercial es suya.")]),
}


def sector_pagina(chave, d):
    def corpo(R):
        casos = casos_de(chave) + ([CASO_FERRERAS] if chave == "joyeria-relojeria" else [])
        casos_h = "".join(caso_html(R, c) for c in casos)
        extra = f'<p class="plano-link">{enlace(R + d["extra_link"][0], d["extra_link"][1])}</p>' if d["extra_link"] else ""
        tipo, base, alt = d["media"]
        media = filme(R, base) if tipo == "vid" else fundo_img(R, base, alt)
        return (ph_media(R, d["nome"], L(*d["h1"]), d["lead"], btn(R + DIAG + "?sector=" + chave, CTA) + btn("#casos", "Ver casos reales", "btn-linha btn-vidro", False), media,
                         migas=[("", "Inicio"), ("sectores/", "Sectores"), (None, d["nome"])])
                + sec(cab("01", "Lo que cuesta dinero", "Dónde se pierde el margen <em>en su sector.</em>") + pequenas(d["margen"]))
                + sec(f'{etq("02", "La promesa", "n")}<p class="titulo promessa" data-duas-tintas>{d["promessa"]}</p>')
                + sec(cab("03", "Experiencia", "Qué hemos hecho ya <em>en este terreno.</em>") + f'<div class="casos">{casos_h}</div>', extra=' id="casos"')
                + sec(f'<div class="grelha entrada"><div class="entrada-cab">{etq("04", "Punto de entrada", "n")}<h2 class="titulo t-l" data-linhas>Por dónde <em>se empieza.</em></h2></div><div class="plano dest" data-sube><span class="selo">Punto de entrada</span><h3>{d["entrada"][0]}</h3><p class="texto">{d["entrada"][1]}</p><p class="nota">Alcance e importe, por escrito tras el diagnóstico.</p>{extra}</div></div>')
                + sec(f'<div class="grelha">{faq_cab("05", "Lo que suelen preguntarnos <em>en su sector.</em>")}{faq(d["faq"], "fs")}</div>')
                + banda("Pida su <em>diagnóstico.</em>", "Con su sector ya seleccionado. Dos minutos.", btn(R + DIAG + "?sector=" + chave, "Empezar el diagnóstico")))
    pagina(f"sectores/{chave}/", d["titulo"], d["desc"], corpo)


for k, v in SECTORES.items():
    sector_pagina(k, v)


def sectores_idx(R):
    return (ph(R, "Sectores", L("Cuatro sectores", "que conocemos", "<em>por dentro.</em>"), "Donde cada detalle se nota. El mismo estándar, para cualquier empresa con reputación que defender.")
            + sec(sect_html(R)) + banda("¿Su sector <em>no está aquí?</em>", "Inmobiliaria premium, servicios profesionales o B2B: el diagnóstico le dice por dónde empezar.", btn(R + DIAG, CTA)))


pagina("sectores/", "Sectores", "Hotelería, automoción de lujo, náutica y joyería: cuatro sectores que conocemos por dentro.", sectores_idx)


# ================================================================= RESULTADOS
def resultados(R):
    sectores_f = [("todos", "Todos"), ("automocion-lujo", "Automoción"), ("joyeria-relojeria", "Joyería"), ("hoteles", "Hoteles"), ("nautica", "Náutica"), ("b2b", "B2B")]
    problemas_f = [("todos", "Todos"), ("percepcion", "Percepción"), ("demanda", "Demanda"), ("conversion", "Conversión"), ("consultas", "Consultas perdidas"), ("saturacion", "Saturación")]

    def bs(tipo, lista):
        return "".join(f'<button type="button" data-f="{tipo}" data-v="{v}" aria-pressed="{str(v == "todos").lower()}">{e(t)}</button>' for v, t in lista)
    casos_h = "".join(caso_html(R, c, True) for c in CASOS)
    return (ph_media(R, "Resultados", L("Lo que hicimos", "<em>y qué lo respalda.</em>"), "Problema, intervención, resultado y evidencia. Cifras solo verificadas y autorizadas.",
                     btn("#casos", "Ver los casos"), fundo_img(R, "regata-jovenes", "Jóvenes navegando en pequeños veleros durante una jornada de vela"))
            + sec(cab("01", "Todos los casos", "Filtre por sector <em>o por problema.</em>")
                  + f'<div data-filtros><div class="filtro-linha"><p class="filtro-rot">Sector</p><div class="filtros">{bs("sector", sectores_f)}</div></div><div class="filtro-linha"><p class="filtro-rot">Problema</p><div class="filtros">{bs("problema", problemas_f)}</div></div><p class="conteo" data-conteo>{len(CASOS)} casos</p></div>'
                  + f'<div class="casos">{casos_h}</div>', extra=' id="casos"')
            + sec(f'<div class="grelha marca-grid"><div class="marca-fotos"><figure class="f1 ventana" data-janela>{video(R, "reel-ferreras-lifestyle", "Campaña de Relojes Ferreras")}</figure><div class="f2 marca-reloj">{reloj_html(R, "-r")}</div></div><div class="marca-txt">{etq("02", "Nuestra propia marca", "n")}<h2 class="titulo t-l" data-linhas>Tan seguros, que <em>creamos la nuestra.</em></h2><p class="lead" data-sube>Si algo no funciona en Relojes Ferreras, lo pagamos nosotros.</p><p data-sube>{enlace("https://relojes-ferreras.com/", "Ver Relojes Ferreras", True)}</p></div></div>', "claro marca", " data-claro")
            + banda("¿Un resultado parecido <em>en su sector?</em>", "El diagnóstico lo compara con trabajos equivalentes.", btn(R + DIAG, CTA)))


pagina("resultados/", "Resultados y casos", "Casos con problema, intervención, resultado y tipo de evidencia. Publicamos cifras solo cuando están verificadas y autorizadas.", resultados)


def casos_p(R):
    return (ph(R, "Casos", L("Lo que cambia cuando", "los dos departamentos", "<em>trabajan juntos.</em>"), "Un caso completo, con cifras de antes y después.")
            + sec(f'<div class="via" style="max-width:52rem"><p class="etiqueta"><span class="n">●</span>En preparación</p><h2>Cerrando la medición del primer caso completo con el cliente.</h2><p class="texto">Se publicará con cifras verificadas y autorización por escrito, no antes.</p><div class="acoes">{btn(R + "resultados/", "Ver resultados")}{btn(R + DIAG, CTA, "btn-linha")}</div></div>'))


pagina("casos/", "Casos", "Marketing e inteligencia artificial trabajando juntos dentro de una misma empresa, con cifras de antes y después.", casos_p)


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
    faqs = [("¿Quién escribe los textos?", "Nosotros. Una web sin argumento es una plantilla bonita. Usted valida."),
            ("¿La web es nuestra?", "Sí: proyecto, accesos y dominio, a su nombre desde el primer día."),
            ("¿Cuánto dura un proyecto?", "Depende de páginas, contenido e integraciones. Se cierra con hitos en el diseño.")]
    return (ph_media(R, "Web y ecommerce", L("Una web no debería", "explicar su empresa.", "<em>Debería venderla.</em>"), "Ordena su propuesta, demuestra valor y cualifica al cliente.",
                     btn(R + DIAG, CTA) + btn("#planes", "Ver los planes", "btn-linha btn-vidro", False), fundo_img(R, "reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche"))
            + sec(cab("01", "La diferencia", "Web informativa frente a <em>infraestructura comercial.</em>") + f'<div class="compara"><div data-sube><h3>Web informativa</h3>{ul(inf)}</div><div class="bom" data-sube style="--i:1"><h3>Infraestructura comercial</h3>{ul(com)}</div></div>')
            + sec(cab("02", "Ruta del visitante", "De la visita <em>al seguimiento.</em>") + passos(ruta))
            + sec(cab("03", "Planes", "Tres alcances y uno <em>a medida.</em>", "Desarrollo propio. Alcance y precio por escrito antes de empezar.") + f'<div class="planos">{ph_}</div><p class="nota plano-flag"><b>Digital Flagship.</b> Multidioma, vídeo, motion, configuradores o áreas privadas: no es un paquete, es un proyecto.</p><div class="pagos">{pg}</div>', extra=' id="planes"')
            + sec(f'<div class="grelha">{faq_cab("04", "Antes de encargar <em>una web.</em>")}{faq(faqs, "fw")}</div>')
            + banda("¿Qué necesita realmente <em>su web?</em>", "Mensaje, prueba o conversión: el diagnóstico lo distingue.", btn(R + DIAG, CTA)))


pagina("web/", "Web y ecommerce con arquitectura comercial", "Diseñamos webs que ordenan su propuesta, demuestran valor, cualifican al cliente y convierten la atención en una siguiente acción medible.", web)


# ================================================================= IA PARA HOTELES
def ia_hoteles(R):
    preg = ["Horarios", "Disponibilidad", "Servicios", "Restaurante", "Parking", "Mascotas", "Check-in", "Cómo llegar", "Cancelaciones", "Otros idiomas", "Fuera de horario"]
    cap = [("Atender llamadas", "Una conversación real, no un menú."), ("Responder lo de siempre", "Con los datos de su casa."), ("Hablar su idioma", "El mismo criterio en cada idioma."),
           ("Pasar a una persona", "Con el contexto ya recogido."), ("Conectarse a sus sistemas", "Según API y permisos."), ("Seguir sus protocolos", "Definidos con usted.")]
    mk = [("Imagen audiovisual", "Un hotel se vende por cómo se ve."), ("Email marketing", "La reserva directa más barata."), ("Redes sociales", "Lo que el huésped comparte."), ("Canales de venta", "Directa frente a comisión.")]
    hab = ["Menos de 20 habitaciones", "Entre 20 y 50", "Entre 50 y 100", "Entre 100 y 200", "Más de 200", "Varios establecimientos"]
    opt = "".join(f"<option>{e(x)}</option>" for x in hab)
    caso = dict(CASOS[2], t="Hotel Boltaña Ordesa", s="Un agente alrededor de la operativa real de un hotel de montaña.", ev=[])
    form = f'''<form class="form" data-mail="Estudio de hotel" novalidate>
<div class="campo-duo"><div class="campo"><label for="h-nome">Nombre</label><input id="h-nome" name="nombre" autocomplete="name" data-campo="Nombre" data-req="Indique su nombre."><span class="erro" id="h-nome-erro"></span></div>
<div class="campo"><label for="h-emp">Hotel o empresa</label><input id="h-emp" name="empresa" autocomplete="organization" data-campo="Hotel o empresa" data-req="Indique el nombre del hotel."><span class="erro" id="h-emp-erro"></span></div></div>
<div class="campo-duo"><div class="campo"><label for="h-mail">Email</label><input id="h-mail" name="email" type="email" autocomplete="email" data-campo="Email" data-req="Indique su email."><span class="erro" id="h-mail-erro"></span></div>
<div class="campo"><label for="h-hab">Habitaciones</label><select id="h-hab" name="habitaciones" data-campo="Habitaciones">{opt}</select></div></div>
<input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
<div class="acoes"><button class="btn btn-claro" type="submit">Quiero estudiar mi caso <span class="fl">→</span></button></div>
<p class="form-nota">Se abre su correo con el mensaje ya escrito para {EMAIL}.</p>
</form><div class="form-ok" data-ok hidden><b>Su correo ya tiene el mensaje preparado.</b><p class="texto">Si no se ha abierto: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    return (ph_media(R, "Agentes de IA para hoteles", L("Su hotel puede atender", "24 horas, en cualquier idioma,", "<em>sin ampliar recepción.</em>"), "Un agente diseñado alrededor de la operativa real de su establecimiento.",
                     btn("#estudio", "Estudiar mi hotel") + btn("#como", "Ver cómo funciona", "btn-linha btn-vidro", False), fundo_img(R, "ia-hotel-atencion-atardecer", "Recepción de un hotel al atardecer, con una huésped atendida en el mostrador"))
            + sec(f'<div class="grelha noche-g"><figure class="dia24" data-dia24>{dia24_svg()}<figcaption class="dia24-ley"><span><i class="eq"></i>Recepción</span><span><i class="ag"></i>El agente, con la recepción cerrada</span><small>Ilustración: consultas de un día cualquiera.</small></figcaption></figure><div class="noche-txt">{etq("01", "El día a día", "n")}<h2 class="titulo t-l" data-linhas>El teléfono no suena <em>cuando recepción está libre.</em></h2><div data-sube>{chips(preg)}</div></div></div>', "noche", ' id="como"')
            + sec(cab("02", "Qué puede hacer", "Lo que puede llegar <em>a resolver.</em>") + pequenas(cap, 3))
            + sec(cab("03", "Caso real", "Diseñado alrededor <em>de un hotel de verdad.</em>") + f'<div class="casos">{caso_html(R, caso)}</div>')
            + sec(cab("04", "La otra mitad", "El agente atiende. <em>El marketing llena.</em>") + pequenas(mk))
            + sec(f'<div class="vias"><div class="cab" style="margin:0">{etq("05", "Solicitar estudio", "n")}<h2 class="titulo t-l" data-linhas>Cuéntenos <em>cómo es su caso.</em></h2><p class="lead" data-sube>Estudiamos su establecimiento antes de proponer nada.</p></div><div class="via">{form}</div></div>', extra=' id="estudio"'))


pagina("ia-hoteles/", "Agentes de IA para hoteles", "Agentes de IA y marketing para hoteles: atención 24 horas en cualquier idioma, imagen audiovisual premium, email marketing y redes.", ia_hoteles)


# ================================================================= CONTACTO
def contacto(R):
    sectores = ["Hotelería", "Automoción", "Náutica", "Joyería", "Otro"]
    plazos = ["Inmediato", "En 30–90 días", "El próximo trimestre", "Solo estoy explorando"]

    def rad(nome, campo, lista, pre):
        return "".join(f'<label><input type="radio" name="{nome}" value="{e(x)}" data-campo="{campo}"{se(x == pre, " checked")}><span>{e(x)}</span></label>' for x in lista)
    form = f'''<form class="form" data-mail="Solicitud desde la web" novalidate>
<div class="campo-duo"><div class="campo"><label for="c-nome">Nombre</label><input id="c-nome" name="nombre" autocomplete="name" data-campo="Nombre" data-req="Indique su nombre."><span class="erro" id="c-nome-erro"></span></div>
<div class="campo"><label for="c-emp">Empresa</label><input id="c-emp" name="empresa" autocomplete="organization" data-campo="Empresa" data-req="Indique el nombre de su empresa."><span class="erro" id="c-emp-erro"></span></div></div>
<div class="campo-duo"><div class="campo"><label for="c-mail">Email</label><input id="c-mail" name="email" type="email" autocomplete="email" data-campo="Email" data-req="Indique su email."><span class="erro" id="c-mail-erro"></span></div>
<div class="campo"><label for="c-tel">Teléfono <small>(opcional)</small></label><input id="c-tel" name="telefono" type="tel" autocomplete="tel" data-campo="Teléfono"></div></div>
<fieldset class="campo"><legend>Sector</legend><div class="radios">{rad("sector", "Sector", sectores, "")}</div></fieldset>
<fieldset class="campo"><legend>Plazo</legend><div class="radios">{rad("plazo", "Plazo", plazos, "")}</div></fieldset>
<div class="campo"><label for="c-msg">Objetivo</label><textarea id="c-msg" name="mensaje" data-campo="Objetivo" data-req="Cuéntenos en dos líneas qué quiere conseguir." placeholder="Dos líneas bastan: qué quiere conseguir y qué le frena."></textarea><span class="erro" id="c-msg-erro"></span></div>
<input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
<div class="acoes"><button class="btn btn-claro" type="submit">Enviar solicitud <span class="fl">→</span></button></div>
<p class="form-nota">Se abre su correo con la solicitud ya escrita para {EMAIL}. Respuesta personal en un día laborable.</p>
</form><div class="form-ok" data-ok hidden><b>Su correo ya tiene la solicitud preparada.</b><p class="texto">Si no se ha abierto: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    pasos3 = [("Leemos su caso", "Una persona, no un mensaje automático."), ("Respondemos en un día", "Con una primera lectura de su caso."), ("Asesoría privada", "Media hora. El presupuesto, después.")]
    return (ph(R, "Contacto", L("Dos formas de empezar.", "<em>Elija la que le ahorre tiempo.</em>"), "Si no sabe qué necesita, el diagnóstico. Si ya lo sabe, escríbanos.").replace('class="pag-hero"', 'class="pag-hero compacto"')
            + sec(f'<div class="vias"><div class="via" data-sube><p class="etiqueta"><span class="n">A</span>No sé qué necesito</p><h2>Diagnóstico de dos minutos</h2><p class="texto">Ocho preguntas y una recomendación concreta.</p><div class="acoes">{btn(R + DIAG, CTA)}</div><address class="nota direccion">IA &amp; Marketing Ferreras<br>Passeig de Gràcia 95, 5º 1ª · 08008 Barcelona<br><a class="enlace" href="mailto:{EMAIL}">{EMAIL}</a></address></div><div class="via" data-sube style="--i:1"><p class="etiqueta"><span class="n">B</span>Ya sé qué necesito</p><h2>Escríbanos</h2>{form}</div></div>')
            + sec(cab("01", "Qué pasa después", "Tres pasos, ninguno <em>le compromete.</em>") + passos(pasos3)))


pagina("contacto/", "Contacto", "Dos vías: si ya sabe lo que necesita, un formulario corto. Si no lo tiene claro, un diagnóstico de dos minutos.", contacto)


# ================================================================= DIAGNÓSTICO
def diagnostico(R):
    form = f'''<form class="form" novalidate>
<div class="campo-duo"><div class="campo"><label for="d-nome">Nombre</label><input id="d-nome" name="nombre" autocomplete="name" data-req="Indique su nombre."><span class="erro" id="d-nome-erro"></span></div>
<div class="campo"><label for="d-emp">Empresa</label><input id="d-emp" name="empresa" autocomplete="organization" data-req="Indique el nombre de su empresa."><span class="erro" id="d-emp-erro"></span></div></div>
<div class="campo-duo"><div class="campo"><label for="d-mail">Email</label><input id="d-mail" name="email" type="email" autocomplete="email" data-req="Revise la dirección de email."><span class="erro" id="d-mail-erro"></span></div>
<div class="campo"><label for="d-tel">Teléfono <small>(opcional)</small></label><input id="d-tel" name="telefono" type="tel" autocomplete="tel"></div></div>
<div class="acoes"><button class="btn btn-claro" type="submit">Enviar a Ferreras <span class="fl">→</span></button></div>
<p class="form-nota">Se abre su correo con sus respuestas y la recomendación ya escritas para {EMAIL}.</p>
</form><div class="form-ok" data-ok hidden><b>Su correo ya tiene el diagnóstico preparado.</b><p class="texto">Si no se ha abierto: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    reco = f'''<div class="reco" data-reco hidden>
<p class="etiqueta"><span class="n">✓</span>Su recomendación</p>
<h2 class="titulo t-l" tabindex="-1" data-r="prioridad"></h2>
<p class="lead" data-r="porque"></p>
<div class="reco-grid"><div><span class="etiqueta">Punto de partida</span><b data-r="plano"></b><p class="texto"><a class="enlace" data-r="ruta-a" href="#"><span data-r="ruta"></span> <span class="fl">→</span></a></p></div><div><span class="etiqueta">Su presupuesto</span><b>Tras la asesoría</b><p class="texto">Sin tarifas cerradas: primero entendemos su caso.</p></div></div>
<div><h3 class="titulo t-s" style="margin-bottom:1.2rem">Sus tres primeras acciones</h3><ol data-r="acoes"></ol></div>
<div class="deps" data-r="deps"></div>
<p class="texto"><b>Siguiente paso:</b> <span data-r="prox"></span></p>
<div class="via">{form}</div>
<p><button type="button" class="enlace" data-recomeca><span class="fl">↺</span> Empezar de nuevo</button></p>
</div>'''
    return (ph(R, "Diagnóstico comercial", L("Ocho preguntas.", "Dos minutos.", "<em>Una recomendación concreta.</em>"), "Sin puntuaciones ni presión. Al terminar sabrá por dónde empezar.").replace('class="pag-hero"', 'class="pag-hero compacto"')
            + sec(f'<div class="diag" data-diag><div class="diag-lado"><div class="diag-prog" data-diag-prog aria-hidden="true"></div><div class="diag-placa" data-diag-placa aria-label="Sus respuestas"></div><p class="mini">Sus respuestas se guardan en este navegador para que pueda retomarlo. Los datos de contacto solo se envían cuando usted decide.</p></div><div><div class="diag-paso" data-diag-paso aria-live="polite"></div>{reco}</div></div>', "diag-sec"))


pagina("diagnostico/", "Diagnóstico de 2 minutos", "Ocho preguntas, dos minutos y una recomendación concreta: qué priorizar, por dónde empezar y cuáles son sus tres primeras acciones. Sin precios y sin compromiso.", diagnostico)


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
