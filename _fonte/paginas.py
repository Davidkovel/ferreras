# Conteúdo das páginas. Corre dentro do build.py (exec), por isso usa as funções de lá.
# Textos do site antigo, em «usted», encurtados onde repetiam. Expressões das f-strings só com aspas simples.

DIAG = "diagnostico/"


def enlace(href, txt, ext=False):
    alvo = ' target="_blank" rel="noopener"' if ext else ""
    seta = "↗" if ext else "→"
    return f'<a class="enlace" href="{href}"{alvo}>{txt} <span class="fl">{seta}</span></a>'


def figura(R, base, alt, cap_b="", cap="", cls="", sizes="(min-width: 900px) 40vw, 100vw", janela=True):
    jan = " data-janela" if janela else ""
    fc = f'<figcaption class="pie"><b>{cap_b}</b>{cap}</figcaption>' if (cap_b or cap) else ""
    return f'<figure class="{cls}"><div class="ventana"{jan}>{img(R, base, alt, sizes)}</div>{fc}</figure>'


FAQ_INICIO = [
    ("¿Ferreras trabaja solo con marcas de lujo?", "No. Trabajamos habitualmente en entornos de lujo —automoción, joyería, relojería, hotelería y náutica— porque son sectores donde cada detalle se nota. Ese estándar lo aplicamos a cualquier empresa consolidada con margen y reputación que defender, sea del sector que sea."),
    ("¿Tengo que elegir entre marketing e inteligencia artificial?", "No. Son las dos mitades del mismo departamento y entran juntas. Lo que decidimos en el diagnóstico es por dónde empezar y en qué orden, según dónde se esté perdiendo hoy el dinero: en que le conozcan poco, en que le visiten y no le contacten, o en que le contacten y no se llegue a atender bien ni a tiempo."),
    ("¿Qué costes externos pueden existir?", "Trabajamos como si formáramos parte interna de la empresa, por eso tratamos de minimizar esos costes: estrategias eficaces, retorno claro e invirtiendo lo necesario. Todo mediante aviso previo."),
    ("¿Cómo se controla lo que hace un agente de IA?", "Con alcance definido, permisos mínimos, registro de actividad, confirmación obligatoria para acciones sensibles, entorno de pruebas previo y transferencia a una persona cuando la gestión lo requiere. Un agente hace lo que se le ha autorizado a hacer, y queda constancia."),
    ("¿Cómo se miden los resultados?", "Acordamos en el diagnóstico qué indicadores importan, cuál es el punto de partida y con qué periodicidad se revisan. Distinguimos siempre entre alcance, interacción, oportunidades y ventas: no son lo mismo y no se suman."),
    ("¿Existe permanencia?", "En marketing recomendamos un mínimo de seis meses, porque construir autoridad por debajo de ese plazo suele ser tirar el dinero. En proyectos web y de IA no hay permanencia: hay alcance, hitos y, si se desea, mantenimiento posterior."),
    ("¿Cuándo recibiré respuesta?", "Una persona del equipo revisa cada solicitud y responde en un día laborable. No respondemos con un mensaje automático haciéndose pasar por una persona."),
]

CHAT = [
    ("cliente", "Cliente", "Guten Abend, haben Sie am Wochenende noch ein Doppelzimmer frei?"),
    ("agente", "Agente", "Guten Abend. Ich prüfe die verfügbaren Informationen für das Wochenende. Einen Moment, bitte."),
    ("sistema", "", "Consulta a fuente conectada · solo lectura"),
    ("agente", "Agente", "Para ese fin de semana figura disponibilidad en habitación doble. El check-in es a partir de las 15:00 y el parking es gratuito."),
    ("cliente", "Cliente", "¿Pueden aplicarme la tarifa de grupo? Somos catorce personas."),
    ("sistema corte", "", "Fuera de alcance autorizado · transferencia a recepción"),
    ("agente", "Agente", "Una reserva de grupo la valora directamente recepción para ofrecerle la mejor condición. Le paso el contacto ahora con todo lo que hemos hablado, para que no tenga que repetir nada."),
]


def chat_html(cab_dir="23:40 · DE"):
    ms = "".join(f'<p class="msg {c}">{se(bool(q), "<small>" + q + "</small>")}{e(t)}</p>' for c, q, t in CHAT)
    return (f'<div class="chat" role="log" aria-label="Simulación de una conversación con un agente de atención">'
            f'<div class="chat-cab"><b><i aria-hidden="true"></i>Agente de atención · Hotel</b><span>{cab_dir}</span></div>'
            f'<div class="chat-lista">{ms}</div>'
            f'<div class="chat-pe"><span class="escribe" data-escribe hidden aria-hidden="true"><i></i><i></i><i></i></span><span>Permisos: solo lectura · registro activo</span></div></div>')


AVISO_DEMO = "Guion fijo con fines ilustrativos. No es una conversación en vivo ni refleja disponibilidad, tarifas ni datos reales de ningún establecimiento."

FASES = [
    ("Diagnóstico", "Entender el negocio antes que el canal.", "Analizamos cómo gana dinero su empresa, dónde se pierde una oportunidad y qué activos ya existen. Sin esta fase, cualquier propuesta sería una suposición.", ["Negocio y modelo", "Cliente y decisión de compra", "Fricción real", "Activos disponibles", "Economía de la operación"]),
    ("Diseño", "Definir el sistema y lo que queda fuera.", "Decidimos qué se construye, en qué orden, con qué mensaje y cómo se medirá. El alcance se cierra por escrito para que nadie descubra sorpresas a mitad de proyecto.", ["Sistema y prioridades", "Mensaje y posicionamiento", "Procesos y permisos", "Alcance cerrado", "KPIs acordados"]),
    ("Implantación", "Construir, conectar y probar antes de encender.", "Producción, desarrollo e integraciones con un entorno de pruebas previo. Nada llega a producción sin haberse comportado correctamente antes.", ["Producción y desarrollo", "Integraciones", "Entorno de pruebas", "Formación del equipo", "Lanzamiento"]),
    ("Optimización", "Aprender de los datos y ajustar.", "Revisión periódica de lo que produce resultado y de lo que no. El sistema se corrige con datos, no con opiniones.", ["Datos y lectura", "Aprendizaje", "Soporte", "Mejora continua", "Revisión de alcance"]),
]


def fases_html():
    fs = []
    for i, (n, h, p, tg) in enumerate(FASES):
        tags = "".join(f"<li>{e(t)}</li>" for t in tg)
        fs.append(f'<div class="fase" data-fase data-sube style="--i:{i}"><span class="num">0{i + 1}</span><h3>{n}</h3><h4>{h}</h4><p>{p}</p><ul class="tags">{tags}</ul></div>')
    return f'<div class="grelha fases" data-linha-alvo><div class="linha-viva" data-linha-viva></div>{"".join(fs)}</div>'


MKT_LISTA = ["Estrategia a 12 meses", "Podcast y entrevistas", "Vídeo y fotografía", "Redes y publicidad", "Imagen profesional", "Equipo y desplazamientos"]
IA_LISTA = ["Sistemas para su día a día", "Análisis de su empresa", "Agentes y automatizaciones", "Mejoras continuas", "Formación a su equipo"]


def sect_html(R, baixo=False):
    S = [("sectores/hoteles/", "hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado", "Hotelería", "Hoteles", "Más reservas y una marca que se recomienda."),
         ("sectores/automocion-lujo/", "tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario de automoción", "Automoción", "Automoción de lujo", "Contenido que enamora y vende coches."),
         ("sectores/nautica/", "yate-vistas", "Zona exterior de un yate con mesa, asientos y vistas a la costa", "Náutica", "Náutica, yates y puertos", "El mar, vivido antes de zarpar."),
         ("sectores/joyeria-relojeria/", "diamantes-anillos", "Dos anillos de diamantes sobre terciopelo azul oscuro", "Joyería", "Joyería y relojería", "Lujo que se desea y se recuerda.")]
    out = []
    for i, (h, b, alt, eti, t, p) in enumerate(S):
        out.append(f'<a href="{R}{h}">{img(R, b, alt, "(min-width: 900px) 45vw, 100vw")}<span class="etiqueta"><span class="n">0{i + 1}</span>{eti}</span><h3>{t}</h3><p>{p}</p><span class="fl" aria-hidden="true">→</span></a>')
    return f'<div class="sect{se(baixo, " baixo")}">{"".join(out)}</div>'


# ================================================================= INICIO
def inicio(R):
    custos = [("Varios perfiles que contratar", "Estrategia, contenido, redes, desarrollo de IA… cada uno, un sueldo."),
              ("Meses antes de ver resultados", "Selección, formación y coordinación, mientras el mercado sigue avanzando."),
              ("Todo depende de usted", "Bajas, rotación y estar al día de una tecnología que cambia cada mes.")]
    custos_h = "".join(f'<div class="custo traco" data-traco data-sube style="--i:{i}"><span class="num">0{i + 1}</span><h3>{t}</h3><p class="texto">{p}</p></div>' for i, (t, p) in enumerate(custos))
    prod = [("vid:reel-tn-porsche", "v", "Porsche 911 GT3 RS negro en el estudio de TN Autosport", "Automoción", "TN Autosport · Porsche 911 GT3 RS"),
            ("yate-completo", "h", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire", "Náutica", "Alquiler de yates, Costa Brava"),
            ("regata-dron", "v", "Velero navegando frente a una localidad costera, fotografiado desde el aire", "Náutica", "Cobertura aérea de una regata"),
            ("vid:reel-cardress", "v", "Funda textil a medida retirándose de un Porsche azul", "Automoción", "Fundas a medida, hechas en Barcelona"),
            ("diamantes-riviere", "h", "Macro de una pulsera rivière de diamantes sobre terciopelo azul oscuro", "Joyería", "Fotografía de producto"),
            ("vid:reel-diamantes", "v", "Un joyero explica una pieza ante la cámara", "Joyería", "Contenido de autoridad"),
            ("rodaje-hotel-salon", "v", "Operador de cámara con estabilizador y luz grabando el salón de eventos de un hotel", "Hotelería", "Rodaje en un salón de eventos"),
            ("vid:reel-tn-track", "v", "Porsche GT3 en circuito, rodado desde un coche en paralelo", "Automoción", "TN Autosport en circuito"),
            ("puerto-club-vela-blanes", "h", "Vista aérea de un puerto deportivo, su dique y la playa contigua", "Náutica", "Club de vela, Costa Brava"),
            ("vid:reel-ferreras-lifestyle", "v", "Campaña de Relojes Ferreras: coche, gastronomía, música y el reloj", "Relojes Ferreras", "Campaña de nuestra marca")]

    def medio(b, alt):
        if b.startswith("vid:"):
            v = b[4:]
            return (f'<video muted playsinline loop preload="none" width="540" height="960" poster="{R}video/{v}-poster.webp" '
                    f'data-src="{R}video/{v}.mp4" data-video-auto aria-label="{e(alt)}"></video>')
        return img(R, b, alt, "(min-width: 900px) 34vw, 70vw")
    prod_h = "".join(f'<figure class="prod-item {o}"><div class="ventana">{medio(b, alt)}</div><figcaption class="pie"><b>{s}</b>{c}</figcaption></figure>' for b, o, alt, s, c in prod)
    factos = [("Diseño", "Propio"), ("Mecanismo", "Suizo"), ("Ensamblaje", "En Barcelona"), ("Distribución", "En joyerías de toda España")]
    factos_h = "".join(f"<li><span>{a}</span>{b}</li>" for a, b in factos)
    mk = "".join(f"<li>{t}<span>0{i + 1}</span></li>" for i, t in enumerate(MKT_LISTA))
    ia = "".join(f"<li>{t}<span>0{i + 1}</span></li>" for i, t in enumerate(IA_LISTA))
    control = [("Alcance definido", "Qué puede resolver y qué no, decidido con usted antes de que ningún cliente hable con el sistema."),
               ("Permisos mínimos", "Solo lectura por defecto y el menor volumen de datos necesario."),
               ("Registro de actividad", "Cada conversación y cada consulta a una fuente quedan registradas y se pueden revisar."),
               ("Confirmación obligatoria", "Las acciones sensibles, como confirmar una reserva, exigen confirmación expresa."),
               ("Entorno de pruebas", "Nada llega a sus clientes sin haberse comportado correctamente antes."),
               ("Transferencia a una persona", "Cuando la gestión lo requiere, el agente calla y pasa el caso con el contexto ya recogido.")]
    control_h = "".join(f'<li data-sube style="--i:{i % 2}"><b>{t}</b><p>{p}</p></li>' for i, (t, p) in enumerate(control))
    sin = "".join(f"<li>{t}</li>" for t in ["Sin procesos de selección", "Sin bajas ni vacaciones que cubrir", "Sin despidos ni indemnizaciones", "Sin formación a su cargo"])
    return f'''
<section class="hero" data-hero data-hora="07:30" data-momento="Abre su empresa">
  <div class="hero-txt">
    <p class="etiqueta" style="--i:0"><span class="hora">07:30</span>Barcelona · Marketing de lujo e inteligencia artificial</p>
    <h1 class="titulo t-xxl" data-linhas>{L('Su departamento', 'de marketing e IA.', '<em>Todo incluido.</em>')}</h1>
    <p class="lead" style="--i:1">De la agencia que crea marcas de lujo y tiene la suya propia.</p>
    <div class="acoes" style="--i:2">{btn(R + DIAG, 'Pide su diagnóstico')}{btn('#reto', 'Cómo trabajamos', 'btn-linha', False)}</div>
    <p class="hero-nota" style="--i:3">Analizamos cómo se ve su marca y cómo atiende hoy a sus clientes. Sin compromiso.</p>
  </div>
  <div class="hero-reloj" data-hero-reloj></div>
  <p class="hero-pista" aria-hidden="true"><i></i>El reloj avanza con usted</p>
</section>

<section class="sec reto" id="reto" data-hora="08:30" data-momento="Reunión de dirección">
  <div class="cab">{etq('08:30', 'El reto')}<p class="titulo reto-frase" data-duas-tintas>¿Se imagina su empresa con su propio departamento de marketing y otro de <em>inteligencia artificial?</em></p></div>
  <div class="grelha reto-custos"><p class="etiqueta">Montarlos por su cuenta significa</p>{custos_h}</div>
</section>

<section class="sec" data-hora="09:15" data-momento="Nos sentamos con usted">
  <div class="grelha">
    <div class="dep-txt">
      {etq('09:15', 'El departamento')}
      <h2 class="titulo t-l" data-linhas>{L('Un departamento', 'dentro de su empresa.', '<em>Sin montarlo.</em>')}</h2>
      <p class="texto" data-sube>Nos integramos como si fuéramos de la casa. Usted nos dice hacia dónde va y puede delegar el plan en nosotros, con un seguimiento uno a uno, como un departamento interno más.</p>
      <ul class="checks" data-sube><li>Sin contratar, formar ni coordinar a nadie</li><li>Un solo equipo, un solo plan</li><li>Trato uno a uno, con seguimiento continuo</li></ul>
      <p data-sube>{enlace(R + 'quien-somos/', 'Quién somos')}</p>
    </div>
    {figura(R, 'rodaje-hotel-salon', 'Operador de cámara con estabilizador y luz grabando el salón de eventos de un hotel, con la mesa montada en primer plano', 'Producción propia', 'Rodaje en el salón de eventos de un hotel', 'dep-foto')}
  </div>
</section>

<section class="sec mitades" data-hora="10:00" data-momento="Dos departamentos, un solo plan">
  <div class="cab">{etq('10:00', 'Las dos mitades')}<h2 class="titulo t-xl" data-linhas>{L('Marketing que atrae.', '<em>IA que atiende.</em>')}</h2><p class="lead" data-sube>Son las dos mitades del mismo departamento y entran juntas. En el diagnóstico decidimos por cuál empezar.</p></div>
  <div class="rx" data-rx role="slider" tabindex="0" aria-label="Del día a la noche: marketing e inteligencia artificial" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
    <div class="rx-capa rx-dia">{img(R, 'yate-completo', 'Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire')}</div>
    <div class="rx-capa rx-noche">{img(R, 'ia-hotel-atencion-atardecer', 'Recepción de un hotel al atardecer, con una huésped atendida en el mostrador')}</div>
    <div class="rx-linha" aria-hidden="true"></div><div class="rx-pega" aria-hidden="true">↔</div>
    <p class="rx-rot d"><b>De día · Marketing</b><span>Que le vean como merece</span></p>
    <p class="rx-rot n"><b>De noche · IA</b><span>Que nadie se quede sin respuesta</span></p>
  </div>
  <div class="grelha mitades-cards">
    <div class="mitad" data-sube><p class="etiqueta">Marketing</p><h3>Que le vean como merece</h3><p class="texto">Su empresa compite con marcas peores y mejor contadas. Trabajamos la percepción hasta que el mercado le sitúe donde le corresponde.</p><p>{enlace(R + 'marketing/', 'Departamento de Marketing')}</p></div>
    <div class="mitad n" data-sube style="--i:1"><p class="etiqueta">Inteligencia artificial</p><h3>Que nadie se quede sin respuesta</h3><p class="texto">La consulta que entra de noche, en otro idioma o mientras su equipo está ocupado deja de perderse por el camino.</p><p>{enlace(R + 'inteligencia-artificial/', 'Departamento de IA')}</p></div>
  </div>
</section>

<section class="prod" data-prod data-hora="11:30" data-momento="Rodaje con dron en el puerto">
  <div class="prod-fixo">
    <div class="prod-cab">{etq('11:30', 'Producción propia')}<h2 class="titulo t-l" data-linhas>{L('No subcontratamos', '<em>la cámara.</em>')}</h2><p class="texto">Rodamos con dron, cámaras, sonido e iluminación. El equipo y los desplazamientos van incluidos: por eso podemos decidir sobre la marcha y repetir lo que no ha salido.</p></div>
    <div class="prod-janela" data-prod-janela><div class="prod-pista" data-prod-pista>{prod_h}</div></div>
    <div class="prod-barra" data-prod-barra aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="sec marca" data-hora="13:00" data-momento="Relojes Ferreras, nuestra marca">
  <div class="grelha marca-grid">
    <div class="marca-fotos">
      <figure class="f1 ventana" data-janela><video muted playsinline loop preload="none" width="720" height="1280" poster="{R}video/hero-ferreras-lifestyle-poster.webp" data-src="{R}video/hero-ferreras-lifestyle.mp4" data-video-auto aria-label="Campaña de Relojes Ferreras: un Aston Martin en una carretera de montaña nevada"></video></figure>
      <figure class="f2 ventana" data-vivo>{img(R, 'reloj-detalle-firma', 'Macro de la firma Ferreras y del tiburón aplicados sobre la esfera guilloché del reloj', '(min-width: 900px) 24vw, 50vw')}</figure>
    </div>
    <div class="marca-txt">
      {etq('13:00', 'Marca propia')}
      <h2 class="titulo t-l" data-linhas>{L('Sabemos crear una marca', 'desde cero.', '<em>Por eso tenemos la nuestra.</em>')}</h2>
      <p class="texto" data-sube>Relojes Ferreras es nuestra firma de relojería automática de autor. Producto, relato, distribución y experiencia, resueltos en nuestra casa antes de proponérselos a nadie.</p>
      <ul class="factos" data-sube>{factos_h}</ul>
      <p data-sube>{enlace('https://relojes-ferreras.com/', 'Conocer Relojes Ferreras', True)}</p>
      <p class="marca-nota" data-sube>{mini_reloj()}El reloj que le acompaña en esta página está inspirado en el nuestro.</p>
    </div>
  </div>
</section>

<section class="sec" data-hora="16:00" data-momento="Cuatro sectores">
  <div class="cab">{etq('16:00', 'Sectores')}<h2 class="titulo t-l" data-linhas>{L('Cuatro sectores', 'que conocemos <em>por dentro.</em>')}</h2></div>
  {sect_html(R)}
</section>

<section class="sec" data-hora="19:30" data-momento="Se publica la pieza">
  <div class="cab">{etq('19:30', 'Alcance')}<h2 class="titulo t-l" data-linhas>{L('Contenido que se ve,', 'se comparte <em>y se recuerda.</em>')}</h2><p class="lead" data-sube>Contenido viral orgánico, con enfoque profesional y dirigido a su público objetivo.</p></div>
  <div class="grelha numeros">
    <div class="numero largo" data-sube><p class="v"><span data-conta="20000">20.000</span>–<span data-conta="300000">300.000</span></p><p>visitas de media por pieza en la línea editorial de un negocio de automoción deportiva, con contenidos de millones de visitas.</p></div>
    <div class="numero" data-sube style="--i:1"><p class="v">4</p><p>sectores con producción propia: hotelería, automoción, náutica y joyería.</p></div>
    <div class="numero" data-sube style="--i:2"><p class="v">20<small>+</small></p><p>idiomas en los que atiende un agente, con el mismo criterio de la casa.</p></div>
  </div>
  <p class="nota" style="margin-top:2.4rem">Trabajo dirigido por Ferreras. Las cifras se publican una vez verificadas con el cliente.</p>
</section>

<section class="sec" data-hora="20:30" data-momento="Todo incluido">
  <div class="cab">{etq('20:30', 'Alcance del servicio')}<h2 class="titulo t-xl" data-linhas>{L('Incluye <em>todo.</em>')}</h2><p class="lead" data-sube>Despreocúpese de la letra pequeña. Nos hacemos cargo de todo, como lo haría su propio departamento.</p></div>
  <div class="grelha">
    <div class="incluye-col" data-sube><p class="etiqueta">Marketing</p><ul class="lista-l">{mk}</ul></div>
    <div class="incluye-col n" data-sube style="--i:1"><p class="etiqueta">Inteligencia artificial</p><ul class="lista-l">{ia}</ul></div>
  </div>
  <p class="cierre-incluye" data-sube>…y todo lo que vaya surgiendo. Sin letra pequeña.</p>
</section>

<section class="sec anochece" data-hora="22:00" data-momento="Se marcha el último">
  {etq('22:00', 'Anochece')}
  <p class="titulo" data-duas-tintas>A las diez se marcha el último. <em>Su empresa sigue abierta.</em></p>
</section>

<section class="consulta" data-consulta data-hora="23:40" data-momento="Entra una consulta en alemán">
  <div class="consulta-fixo">
    <div class="consulta-txt">
      {etq('23:40', 'Departamento de IA · Simulación ilustrativa')}
      <h2 class="titulo t-xl"><b>23:40.</b> Entra una consulta en alemán.</h2>
      <p class="lead">Llega fuera de horario y en otro idioma. Lo importante de un agente bien acotado no es que conteste: es el punto exacto en el que calla y avisa a una persona.</p>
      <div class="traspaso" data-traspaso><span><b>Recepción</b> recibe la conversación completa: el cliente no tendrá que repetir nada.</span></div>
      <p class="aviso">{AVISO_DEMO}</p>
    </div>
    {chat_html()}
  </div>
  <div class="consulta-fim" data-hora="23:44" data-momento="La consulta pasa a recepción"></div>
</section>

<section class="sec" data-hora="03:00" data-momento="Todo queda registrado">
  <div class="grelha">
    <div class="control-cab">{etq('03:00', 'Control')}<h2 class="titulo t-l" data-linhas>{L('Mientras usted duerme,', '<em>todo queda registrado.</em>')}</h2><p class="texto" data-sube>Un agente hace lo que se le ha autorizado a hacer, y queda constancia.</p><p data-sube>{enlace(R + 'inteligencia-artificial/', 'Departamento de IA')}</p></div>
    <ul class="control-lista">{control_h}</ul>
  </div>
</section>

<section class="sec" data-hora="06:45" data-momento="Amanece">
  <div class="grelha">
    {figura(R, 'fernando-ferreras-ceo', 'Fernando Ferreras en un puerto deportivo, junto a dos vehículos de alta gama con estuches de reloj expuestos y embarcaciones al fondo', 'Fernando Ferreras', 'Dirección', 'equipo-foto')}
    <div class="equipo-txt">
      {etq('06:45', 'Equipo')}
      <h2 class="titulo t-l" data-linhas>{L('Solo lo bueno', 'de <em>tener equipo.</em>')}</h2>
      <p class="texto" data-sube>Dos equipos de especialistas trabajando para su empresa: marketing estratégico y desarrollo de IA. Un equipo corto y con nombres: sabrá siempre quién lleva su cuenta y a quién escribir cuando algo importe.</p>
      <blockquote class="cita" data-sube>La dirección entra en el diagnóstico, en la estrategia y en las conversaciones que deciden un proyecto, y no se delega.</blockquote>
      <ul class="sin" data-sube>{sin}</ul>
      <p data-sube>{enlace(R + 'quien-somos/', 'Quién somos')}</p>
    </div>
  </div>
</section>

<section class="sec" data-hora="07:00" data-momento="Primero, el diagnóstico">
  <div class="cab">{etq('07:00', 'Método')}<h2 class="titulo t-l" data-linhas>{L('Cada fase tiene', '<em>un responsable.</em>')}</h2><p class="lead" data-sube>Los dos departamentos trabajan con un solo plan: marketing estratégico lleva el diagnóstico, la estrategia y la producción; desarrollo de IA, el análisis, la implantación y la formación.</p></div>
  {fases_html()}
</section>

<section class="sec" data-hora="07:15" data-momento="Sus preguntas">
  <div class="grelha">
    <div class="faq-cab">{etq('07:15', 'Preguntas frecuentes')}<h2 class="titulo t-l" data-linhas>{L('Lo que suelen', 'preguntarnos', '<em>antes de empezar.</em>')}</h2><p>{enlace(R + 'contacto/', 'Hacer otra pregunta')}</p></div>
    {faq(FAQ_INICIO, 'fi')}
  </div>
</section>

<section class="sec final" data-claro data-hora="07:30" data-momento="Veinticuatro horas después">
  <div class="grelha final-grid">
    <div class="final-txt">
      {etq('07:30', 'Veinticuatro horas después')}
      <h2 class="titulo t-xl" data-linhas>{L('Ha llegado hasta aquí', 'porque nunca se ha conformado.', '<em>Su empresa tampoco debería.</em>')}</h2>
      <p class="lead" data-sube>Ocho preguntas, dos minutos y una recomendación concreta: qué priorizar, por dónde empezar y cuáles serían sus tres primeras acciones.</p>
      <div class="acoes" data-sube>{btn(R + DIAG, 'Pide su diagnóstico', 'btn-oscuro')}{btn(R + 'contacto/', 'Escribir directamente', 'btn-linha', False)}</div>
    </div>
    <div class="final-dados" data-sube><div><b>8</b><span>preguntas, ninguna sobre presupuesto cerrado</span></div><div><b>2 min</b><span>es lo que tarda en completarlo</span></div><div><b>0 €</b><span>sin coste y sin compromiso</span></div><div><b>3</b><span>primeras acciones concretas al terminar</span></div></div>
  </div>
</section>
'''


pagina("", "IA & Marketing Ferreras · Su departamento de marketing e IA. Todo incluido.",
       "Un departamento de marketing y otro de inteligencia artificial montados dentro de su empresa, con un solo plan. Agencia de marketing de lujo en Barcelona: hotelería, automoción, náutica y joyería.",
       inicio, inicio=True)


# ================================================================= QUIÉN SOMOS
def quien(R):
    marcas = [("reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche", "Relojería · Marca propia", "Relojes Ferreras", "La creamos desde cero: producto, identidad, web y distribución en joyerías de toda España."),
              ("tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario de automoción", "Automoción", "TN Autosport", "Llevamos su marketing: contenido, vídeo y redes de una referencia en coches de alta gama."),
              ("hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado", "Hotelería", "Hotel Boltaña Ordesa", "Marketing y un agente de IA que atiende a sus huéspedes a cualquier hora."),
              ("puerto-club-vela-blanes", "Vista aérea de un puerto deportivo, su dique y la playa contigua", "Náutica", "Club náutico · Costa Brava", "Contenido y comunicación de un club de vela de referencia en la Costa Brava."),
              ("diamantes-anillos", "Dos anillos de diamantes sobre terciopelo azul oscuro", "Joyería", "Joyería de diamantes · España", "Contenido de autoridad para una casa de diamantes con clientes en toda España."),
              ("sm-cardress-funda", "Coupé deportivo cubierto con una funda textil a medida con diseño personalizado", "Automoción", "Producto premium para automoción", "Imagen y contenido de un producto premium a medida para coches de alta gama.")]
    mh = "".join(f'<div class="marca-c" data-sube style="--i:{i % 3}"><div class="ventana">{img(R, b, alt, "(min-width: 900px) 30vw, 100vw")}</div><p class="etiqueta">{s}</p><h3>{t}</h3><p>{p}</p></div>' for i, (b, alt, s, t, p) in enumerate(marcas))
    pruebas = [("Construimos nuestras propias marcas", "Relojes Ferreras: diseño de producto, identidad, web y ecommerce, distribución en joyerías, presentaciones y el evento Luxury & Yachts. Cada decisión que proponemos a un cliente la hemos tomado antes en nuestra propia casa."),
               ("Transformamos la percepción de clientes", "TN Autosport en automoción, joyería de diamantes y producto premium para automoción: marcas cuya imagen pública pasó a estar a la altura de lo que ya eran, con línea editorial, herramientas comerciales y contenido de autoridad."),
               ("Trabajamos en entornos de alta exigencia", "Hotelería, yates, puertos, regatas y comercialización de activos de lujo. Entornos donde no se puede repetir la toma, donde la discreción forma parte del servicio y donde un detalle mal resuelto se paga en percepción.")]
    return (ph(R, "Quién somos", L("Llevamos el marketing", "de marcas de referencia", "<em>en su sector.</em>"),
               "Somos el departamento de marketing de TN Autosport en automoción y los creadores de Relojes Ferreras, entre otras marcas de hotelería, náutica y joyería. Ese mismo equipo, de marketing y de inteligencia artificial, es el que trabaja para su empresa.",
               btn(R + DIAG, "Pide su diagnóstico"), img(R, "fernando-ferreras-ceo", "Fernando Ferreras en un puerto deportivo, junto a dos vehículos de alta gama con estuches de reloj expuestos y embarcaciones al fondo", "(min-width: 900px) 40vw, 100vw", lazy=False))
            + sec(cab("01", "Marcas que llevamos", "Detrás de marcas que su sector <em>ya reconoce.</em>", "No hablamos de lujo: lo trabajamos cada semana, en cuatro sectores, y con una marca propia que hemos levantado desde cero.") + f'<div class="marcas">{mh}</div><p style="margin-top:3rem">{enlace("https://relojes-ferreras.com/", "Ver Relojes Ferreras, la marca que creamos", True)}</p>')
            + sec(f'<div class="grelha"><div style="grid-column:1/6">{etq("", "Dirección", "n")}<h2 class="titulo t-l" data-linhas style="margin-top:1.4rem">{L("Una sola dirección", "<em>en cada proyecto.</em>")}</h2></div><div style="grid-column:7/13" class="prosa" data-sube><p>Trabajamos con pocas empresas y muy de cerca. La dirección entra en el diagnóstico, en la estrategia y en las conversaciones que deciden un proyecto, y no se delega.</p><p>El criterio no viene solo de asesorar a otros: hemos creado Relojes Ferreras, una marca española de relojería automática de autor con diseño propio, mecanismo suizo y ensamblaje en Barcelona, hemos abierto su distribución en joyerías y hemos organizado eventos de lujo como Luxury &amp; Yachts. Producto, relato, deseo, distribución y seguimiento resueltos en nuestra casa antes de proponérselos a nadie.</p></div></div>')
            + sec(cab("02", "Equipo operativo", "Quién va <em>a responderle.</em>", "Un equipo corto y con nombres. Sabrá siempre quién lleva su cuenta y a quién escribir cuando algo importe.") + cards([("Departamento de marketing estratégico", "Estrategia, producción audiovisual, distribución y seguimiento comercial."), ("Departamento de desarrollo de IA", "Análisis, implantación de sistemas y agentes, integraciones y formación.")]))
            + sec(f'{etq("03", "Estándar", "n")}<p class="titulo promessa" data-duas-tintas style="margin:1.6rem 0 2.4rem">El lujo no es una etiqueta. <em>Es un estándar de ejecución.</em></p><div class="prosa" data-sube><p>Hemos aprendido a construir deseo trabajando donde cada detalle cuenta: automoción, joyería, relojería, hotelería y náutica.</p><p>Ese estándar no se queda en la imagen. Lo aplicamos al mensaje, a la captación, a la tecnología y a la forma en la que una empresa atiende a sus clientes: en el tiempo de respuesta, en la discreción con la que se trata una operación y en el cuidado con el que se cierra un detalle que casi nadie mirará.</p></div>')
            + sec(cab("04", "Autoridad", "Tres pruebas, <em>no tres adjetivos.</em>") + cards(pruebas, 3))
            + sec(cab("05", "Cómo trabajamos", "Un departamento dentro de su empresa. <em>Sin montarlo.</em>", "Nos integramos como si fuéramos de la casa. Usted nos dice hacia dónde va y puede delegar el plan en nosotros.") + f'<div class="grelha"><div class="incluye-col" data-sube><p class="etiqueta">Marketing</p>{chips(MKT_LISTA)}</div><div class="incluye-col n" data-sube><p class="etiqueta">Inteligencia artificial</p>{chips(IA_LISTA)}</div></div>')
            + sec(cab("06", "Método", "Cada fase tiene <em>un responsable.</em>", "Los dos departamentos trabajan con un solo plan.") + fases_html())
            + banda("¿Qué sistema encaja <em>con su empresa?</em>", "Dos minutos y sabrá qué priorizar, por dónde empezar y con quién trabajaría.", btn(R + DIAG, "Conocer qué sistema encaja")))


pagina("quien-somos/", "Quién somos", "Llevamos el marketing de marcas de referencia en su sector, como TN Autosport en automoción, y somos los creadores de Relojes Ferreras. Departamento de marketing e IA en Barcelona.", quien)


# ================================================================= MARKETING
MKT_TABS = [
    ("Estrategia a doce meses", "Antes de grabar nada, decidimos qué tiene que cambiar en la percepción de su empresa y en qué orden. El plan se cierra por escrito y se revisa cada mes.", ["Análisis del negocio y de cómo decide su cliente", "Posicionamiento y mensajes por público", "Calendario editorial a doce meses", "Panel de seguimiento con revisión mensual"]),
    ("Producción audiovisual premium", "Equipo propio y desplazamientos incluidos. Grabamos con dron, cámaras de cine, sonido e iluminación, porque un producto de alto valor se juzga por cómo se ve antes de que nadie pregunte el precio.", ["Dron para exteriores, instalaciones y embarcaciones", "Vídeo y fotografía de producto, marca y equipo", "Cobertura de eventos, regatas, presentaciones y entregas", "Postproducción, color y versiones para cada canal"]),
    ("Podcast, entrevistas y ponencias", "La forma más rápida de que a usted se le reconozca como la referencia de su sector es que se le vea explicando su criterio, no vendiendo su producto.", ["Formato propio de podcast o entrevista", "Guion, grabación, edición y distribución", "Preparación de ponencias y apariciones", "Imagen profesional y material de marca personal"]),
    ("Redes y comunidad", "Una línea editorial reconocible, publicada con constancia, y una comunidad que comparte. El contenido orgánico bien dirigido sigue siendo el metro cuadrado más barato que existe.", ["Gestión de los canales que le convienen, no de todos", "Contenido pensado para alcance y para preferencia", "Conversación y comunidad", "Adaptaciones por formato y plataforma"]),
    ("Publicidad", "Campañas con objetivo declarado y medición honesta. La inversión publicitaria se presupuesta aparte y se decide con usted antes de gastar un euro.", ["Campañas de alcance, captación y recuperación", "Segmentación por público y momento de compra", "Lectura mensual de qué funciona y qué se corta"]),
    ("Email marketing y canales de venta", "Su base de clientes es el activo más barato que tiene. Recuperar a quien ya le conoce cuesta mucho menos que convencer a quien no.", ["Secuencias de recuperación y fidelización", "Venta directa frente a comisión de terceros", "Presencia donde su cliente decide, no donde está de moda"]),
    ("Web, ecommerce y SEO", "Lo desarrolla nuestro propio equipo informático, en casa. La web deja de ser un folleto y pasa a cualificar: explica, demuestra y recoge la solicitud con la información que su equipo necesita para llamar.", ["Arquitectura, mensaje y prueba", "Desarrollo a medida, sin plantillas de catálogo", "Ecommerce, pasarelas y catálogo cuando el producto lo pide", "SEO técnico y de contenidos, y medición de oportunidades reales"]),
]


def marketing(R):
    problemas = [("Le comparan con quien no debería", "Marcas peores y mejor contadas ocupan el lugar que le corresponde. Cuando el cliente no distingue, decide por precio."),
                 ("Publica, pero no acumula", "Sin línea editorial cada pieza empieza de cero. Hay actividad constante y ninguna autoridad que se quede."),
                 ("Depende de usted estar delante", "La empresa vende cuando usted vende. Lo que no está contado no trabaja mientras usted hace otra cosa."),
                 ("Las métricas no hablan de dinero", "Suben el alcance y las interacciones, y nadie sabe cuántas conversaciones comerciales ha producido el trimestre.")]
    servicios = ["Estrategia a doce meses", "Rodaje con dron", "Podcast y entrevistas", "Fotografía de producto", "Redes y comunidad", "Publicidad medida", "Email marketing", "Web y ecommerce", "SEO técnico", "Cobertura de eventos", "Imagen de marca personal", "Analítica y paneles"]
    dev = ["Desarrollo web a medida y rendimiento", "Ecommerce, catálogo y pasarelas de pago", "SEO técnico, contenidos y datos estructurados", "Email marketing y automatizaciones", "Analítica, medición y paneles", "Integraciones con CRM, reservas y gestión", "Mantenimiento, seguridad y copias", "Accesibilidad y cumplimiento legal"]
    dev_c = [("Un cambio se hace, no se pide", "Cuando la estrategia cambia, la web cambia esa semana. Sin tickets a un proveedor externo ni presupuestos por cada ajuste."),
             ("Quien programa sabe qué vende", "El desarrollo lo hace quien ha estado en la reunión de estrategia. Por eso la web cualifica en lugar de limitarse a informar."),
             ("Todo conectado de verdad", "Web, ecommerce, email marketing, analítica y agentes de IA se conectan entre sí porque los construye el mismo equipo."),
             ("Los accesos son suyos", "Dominio, código, hosting y cuentas quedan a su nombre desde el primer día. Nadie le retiene el proyecto.")]
    orden = [("Diagnóstico", "Cómo gana dinero su empresa, cómo decide su cliente y qué activos ya existen."), ("Estrategia", "Qué cambiamos en la percepción, con qué mensajes y en qué orden."), ("Producción", "Rodajes, sesiones y formatos. Equipo y desplazamientos incluidos."), ("Distribución", "Publicación constante por los canales que le convienen."), ("Lectura", "Revisión mensual de lo que produce conversaciones y de lo que no.")]
    faqs = [("¿Cuánto tardan en verse resultados?", "Depende del punto de partida, del sector y del alcance contratado. No damos plazos universales porque serían falsos: fijamos objetivos, punto de partida y calendario en el diagnóstico y revisamos contra ellos."),
            ("¿Quién aparece en los vídeos?", "Habitualmente, quien mejor represente el criterio de la empresa: propiedad, dirección o un técnico con autoridad real. Si nadie quiere aparecer en cámara, existen formatos que funcionan sin rostro, aunque construyen autoridad más despacio."),
            ("¿Qué tenemos que aportar nosotros?", "Acceso a producto, disponibilidad para las sesiones de producción, validación de mensajes clave y una persona de contacto con capacidad de decisión. El resto lo dirigimos nosotros."),
            ("¿La inversión publicitaria está incluida?", "No. La gestión sí; el dinero que se entrega a las plataformas, no. Se decide con usted y se paga directamente desde su cuenta publicitaria.")]
    return (ph(R, "Departamento de Marketing", L("Que su empresa", "se perciba", "<em>como lo que es.</em>"),
               "Un departamento de marketing completo dentro de su empresa: estrategia, producción audiovisual propia, distribución y seguimiento. Sin contratar a nadie y sin coordinar a nadie.",
               btn(R + DIAG, "Pide su diagnóstico") + btn("#problema", "Descubra el departamento", "btn-linha", False),
               img(R, "marketing-portada-camara", "Cámara de cine en primer plano con escenas de producción de marca proyectadas al fondo", "(min-width: 900px) 40vw, 100vw", lazy=False),
               ["Producción audiovisual propia", "Estrategia a 12 meses", "Redes y publicidad"])
            + sec(cab("01", "El problema", "El producto está a la altura. <em>La percepción, casi nunca.</em>", "Las empresas con las que trabajamos no tienen un problema de calidad. Tienen un problema de cómo se las ve, y eso se paga en cada negociación.") + cards(problemas), extra=' id="problema"')
            + sec(cab("02", "Qué incluye", "Todo lo que haría <em>un departamento propio.</em>", "Elija cualquiera y vea exactamente qué recibe. No hay paquetes cerrados: el alcance se decide en el diagnóstico y se cierra por escrito.") + tabs("mk", MKT_TABS))
            + sec(cab("03", "Producción propia", "No subcontratamos <em>la cámara.</em>", "Grabamos nosotros, con nuestro equipo y nuestros desplazamientos. Por eso podemos decidir sobre la marcha y repetir lo que no ha salido.")
                  + f'<div class="duo-foto">{figura(R, "sm-cardress-funda", "Coupé deportivo cubierto con una funda textil a medida con diseño personalizado", "Automoción", "Producto premium a medida", "foto")}{figura(R, "regata-dron", "Velero navegando frente a una localidad costera, fotografiado desde el aire", "Náutica", "Cobertura aérea", "foto")}</div>'
                  + f'<div style="margin-top:3rem" data-sube><p class="nota" style="margin-bottom:1.2rem">Dron para exteriores, instalaciones y embarcaciones. Cámaras, sonido e iluminación para producto, marca y equipo. Cobertura de eventos, regatas, presentaciones y entregas.</p>{chips(servicios)}</div>')
            + sec(cab("04", "Equipo informático propio", "El desarrollo <em>también es nuestro.</em>", "Dentro del departamento hay equipo informático propio. No subcontratamos la web, ni el ecommerce, ni las integraciones: se desarrollan en casa, con la misma gente que conoce su estrategia.") + f'<div data-sube style="margin-bottom:3rem">{chips(dev)}</div>' + cards(dev_c) + '<p class="nota" style="margin-top:2rem">Dominio, código, alojamiento y cuentas quedan a nombre de su empresa desde el primer día. Licencias, pasarelas de pago y servicios de terceros se presupuestan aparte y se avisan antes.</p>')
            + sec(cab("05", "El orden", "Cinco fases. <em>Ninguna se salta.</em>", "Saltarse el diagnóstico es la forma más cara de empezar: se produce mucho y no cambia nada.") + passos(orden))
            + sec(f'<div class="grelha marca-grid"><div class="marca-fotos"><figure class="f1 ventana" data-janela>{img(R, "reloj-detalle-firma", "Macro de la firma Ferreras sobre la esfera guilloché del reloj", "(min-width: 900px) 34vw, 70vw")}</figure><figure class="f2 ventana" data-vivo>{img(R, "reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche", "(min-width: 900px) 24vw, 50vw")}</figure></div><div class="marca-txt">{etq("06", "Por qué nosotros", "n")}<h2 class="titulo t-l" data-linhas>{L("Sabemos crear una marca", "desde cero porque", "<em>tenemos la nuestra.</em>")}</h2><p class="texto" data-sube>Relojes Ferreras es nuestra firma de relojería automática: diseño propio, mecanismo suizo y ensamblaje en Barcelona. Cada recomendación que le hacemos la hemos aplicado antes a nuestra propia empresa.</p><p data-sube>{enlace(R + "quien-somos/", "Conocer quiénes somos")}</p></div></div>')
            + sec(cab("07", "Dónde tenemos más recorrido", "Cuatro sectores que conocemos <em>por dentro.</em>") + sect_html(R, True))
            + sec(cab("08", "Condiciones", "Lo que pasa <em>antes de empezar.</em>") + cards(CONDICIONES, 4, False))
            + sec(f'<div class="grelha"><div class="faq-cab">{etq("09", "Preguntas frecuentes", "n")}<h2 class="titulo t-l" data-linhas>Lo que suelen <em>preguntarnos.</em></h2></div>{faq(faqs, "fm")}</div>')
            + banda("¿Cómo se ve hoy su empresa <em>desde fuera?</em>", "Analizamos cómo se percibe su marca y qué cambiaríamos primero. Sin compromiso.", btn(R + DIAG, "Pide su diagnóstico")))


pagina("marketing/", "Departamento de Marketing", "Un departamento de marketing completo dentro de su empresa: estrategia a doce meses, producción audiovisual propia con dron y equipo, podcast, redes, publicidad, email marketing y web.", marketing)


# ================================================================= IA
IA_TABS = [
    ("Primero, usted", "Antes de tocar la empresa, montamos los sistemas que le quitan horas a usted: preparación de reuniones, redacción, análisis de documentos y seguimiento de lo que tiene abierto.", ["Asistentes privados con el contexto de su negocio", "Preparación y resumen de reuniones", "Análisis de documentación y propuestas", "Formación uno a uno para que lo use de verdad"]),
    ("Agentes de atención", "Atienden por teléfono, chat, WhatsApp o email. Responden lo que saben, consultan lo que deben consultar y avisan a una persona en el punto exacto que se define con usted.", ["Voz, chat, WhatsApp y email según alcance", "Más de veinte idiomas con el mismo criterio", "Transferencia a una persona con el contexto recogido", "Conocimiento de su casa, no generalidades del sector"]),
    ("Análisis de la empresa", "Miramos dónde se pierde tiempo y dónde se pierde dinero, y separamos lo que conviene automatizar de lo que debe seguir decidiendo una persona. No todo merece automatizarse.", ["Mapa de procesos y de cuellos de botella", "Qué se automatiza, qué no y por qué", "Prioridades por retorno, no por novedad"]),
    ("Integraciones", "Conectamos el sistema con lo que ya usa, para que responda con datos actualizados en lugar de con una copia congelada del mes pasado.", ["CRM, agenda, reservas, PMS, correo y hojas de cálculo", "Permisos mínimos y de solo lectura por defecto", "Entorno de pruebas antes de que hable con nadie"]),
    ("Automatización de procesos", "Confirmaciones, avisos, seguimientos y traspasos internos dejan de depender de que alguien se acuerde.", ["Flujos internos acotados y revisables", "Avisos y seguimientos automáticos", "Registro de actividad consultable"]),
    ("Control y mejora continua", "Un sistema que atiende clientes no se instala y se olvida. Revisamos conversaciones reales y corregimos lo que no responde como debería.", ["Permisos, confirmaciones y registro", "Revisión periódica de conversaciones", "Ajustes y ampliaciones de alcance", "Formación a su equipo"]),
]


def demo_html():
    return (f'<div class="demo"><div class="cab" style="margin:0"><p class="etiqueta"><span class="n">03</span>Demostración</p><h2 class="titulo t-l" data-linhas>Pruébelo <em>usted mismo.</em></h2>'
            f'<p class="lead" data-sube>Una simulación de un agente acotado. Fíjese menos en lo que responde y más en lo que se niega a responder.</p>'
            f'<p class="nota">Cuatro consultas fuera de horario, en cuatro idiomas. El agente responde en el idioma del cliente, su equipo lo lee en español y el paso delicado lo cierra siempre una persona.</p><p class="mini">{AVISO_DEMO}</p></div>'
            '<div data-ai-demo="hotel"></div></div>')


def ia(R):
    problemas = [("La consulta que entra fuera de hora", "Llega de noche o en otro idioma. Cuando alguien la lee, el cliente ya ha resuelto en otro sitio."),
                 ("Su equipo atiende dos cosas a la vez", "Y ninguna bien. Se responde deprisa al teléfono y se cuida mal a quien tiene delante."),
                 ("El criterio vive en la cabeza de dos personas", "Si no están, la empresa responde peor. Nada de eso está escrito ni es consultable."),
                 ("La tecnología cambia cada mes", "Estar al día es un trabajo en sí mismo, y no es el suyo.")]
    capac = ["Agentes de voz", "WhatsApp y chat", "Más de 20 idiomas", "Integración con su CRM", "Reservas y agenda", "Automatización de procesos", "Asistentes privados", "Entorno de pruebas", "Permisos mínimos", "Formación al equipo", "Revisión de conversaciones", "Análisis de procesos"]
    pasos = [("Analizamos", "Cómo trabaja hoy su equipo y qué entra por cada canal."), ("Decidimos", "Qué conviene automatizar y qué debe seguir siendo humano."), ("Diseñamos", "Conocimiento, canales, idiomas, permisos y punto de transferencia."), ("Probamos", "Entorno de pruebas antes de que ningún cliente hable con el sistema."), ("Arrancamos", "Puesta en marcha acompañada y formación al equipo."), ("Optimizamos", "Revisión de conversaciones reales y mejora continua.")]
    faqs = [("¿Esto es un chatbot?", "No. Un chatbot es una herramienta que se contrata. Nosotros implantamos un sistema: conocimiento de su empresa, conexiones con sus herramientas, permisos, pruebas, supervisión y mejora. La diferencia se nota el día que un cliente pregunta algo que no estaba en el guion."),
            ("¿El agente puede equivocarse?", "Puede. Por eso se define qué está autorizado a hacer, qué requiere confirmación y en qué punto deja de responder y avisa a una persona. Un sistema honesto asume el error y lo acota; no promete infalibilidad."),
            ("¿Se integra con nuestras herramientas actuales?", "Depende de que existan API, permisos y un entorno donde probar. Cuando una integración está en desarrollo lo decimos, no la presentamos como operativa."),
            ("¿Qué pasa con los datos de nuestros clientes?", "Se trabaja con permisos mínimos y con el menor volumen de datos necesario. Los accesos, la conservación y los encargados de tratamiento se definen por escrito antes de conectar nada."),
            ("¿Sustituye a una persona del equipo?", "No es el objetivo. El objetivo es que las personas dejen de hacer lo repetitivo y dediquen ese tiempo a lo que sí requiere criterio: cerrar, resolver y cuidar al cliente.")]
    return (ph(R, "Departamento de IA", L("Que su empresa atienda siempre,", "y que su equipo recupere", "<em>sus mejores horas.</em>"),
               "Un departamento de desarrollo de inteligencia artificial dentro de su empresa. Empezamos por los sistemas que le hacen más eficiente a usted y después analizamos la compañía para decidir qué automatizar.",
               btn(R + DIAG, "Pide su diagnóstico") + btn("#problema", "Descubra el departamento", "btn-linha", False),
               img(R, "ia-portada-esfera", "Esfera de luz dorada con interfaces de datos flotando en su interior", "(min-width: 900px) 40vw, 100vw", lazy=False),
               ["Atención 24/7 en más de 20 idiomas", "Sistemas para su día a día", "Supervisión humana"])
            + sec(cab("01", "El problema", "Lo repetitivo se come el tiempo <em>que debería dedicar a vender.</em>", "No es un problema de esfuerzo. Es que las mismas quince preguntas, todos los días, ocupan a las personas que deberían estar cerrando operaciones.") + cards(problemas) + '<p class="cierre-incluye">El sistema resuelve lo repetitivo en paralelo. La persona sigue atendiendo a quien tiene delante.</p>', extra=' id="problema"')
            + sec(cab("02", "Cómo funciona", "Dónde responde, <em>y dónde deja de hacerlo.</em>", "Lo importante de un agente bien acotado no es que conteste. Es el punto exacto en el que calla y avisa a una persona, y ese punto se decide con usted.") + f'<div data-sube>{chips(capac)}</div><p class="nota" style="margin-top:1.6rem">El punto de transferencia se define con usted: qué puede resolver el agente y qué no, decidido antes de que ningún cliente hable con el sistema.</p>')
            + sec(demo_html())
            + sec(cab("04", "Qué incluye", "Empezamos por usted. <em>Después, por la empresa.</em>", "Elija cualquiera y vea exactamente qué recibe. Qué se activa en su caso se decide después del análisis, no antes.") + tabs("ia", IA_TABS) + '<p class="nota" style="margin-top:2rem">Cada integración depende de que exista API, permisos y un entorno donde probar. Cuando una conexión está en desarrollo lo decimos: no la presentamos como operativa. Los consumos de voz, mensajería, modelos y APIs se presupuestan aparte y se avisan antes.</p>')
            + sec(cab("05", "El orden", "Seis pasos. <em>El primero no es instalar nada.</em>", "No todo merece automatizarse. Separar lo repetitivo de lo que exige criterio es la mitad del trabajo.") + passos(pasos)
                  + f'<div class="duo-foto" style="margin-top:4rem">{figura(R, "ia-hotel-estudio-establecimiento", "Mesa de trabajo con planos del establecimiento y una vista del hotel desplegada sobre una tableta", "", "Primero se estudia la casa. Después se decide qué automatizar.", "foto")}{figura(R, "ia-hotel-multiidioma", "Grupo de huéspedes internacionales en recepción con indicadores de varios idiomas atendidos a la vez", "", "Más de veinte idiomas con el mismo criterio de la casa.", "foto")}</div>')
            + sec(f'<div class="banda" style="border:0;padding:0"><div class="cab" style="margin:0">{etq("06", "Aplicado", "n")}<h2 class="titulo t-l" data-linhas>Verlo funcionando en <em>un sector concreto.</em></h2><p class="lead" data-sube>La atención hotelera es donde el problema se ve más claro: consultas a cualquier hora, en varios idiomas y con alguien esperando en el mostrador. El método es el mismo en un concesionario, una joyería o una empresa náutica.</p></div><div class="acoes">{btn(R + "ia-hoteles/", "Ver el caso de hotelería")}</div></div>')
            + sec(cab("07", "Condiciones", "Lo que pasa <em>antes de empezar.</em>") + cards(CONDICIONES, 4, False))
            + sec(f'<div class="grelha"><div class="faq-cab">{etq("08", "Preguntas frecuentes", "n")}<h2 class="titulo t-l" data-linhas>Lo que suelen <em>preguntarnos.</em></h2></div>{faq(faqs, "fa")}</div>')
            + banda("¿Qué está atendiendo hoy su equipo <em>que no debería?</em>", "Analizamos cómo atiende hoy a sus clientes y qué conviene automatizar primero. Sin compromiso.", btn(R + DIAG, "Pide su diagnóstico")))


pagina("inteligencia-artificial/", "Departamento de IA", "Un departamento de desarrollo de inteligencia artificial dentro de su empresa: agentes de atención en más de veinte idiomas, integraciones con sus sistemas, automatización de procesos y formación a su equipo.", ia)


# ================================================================= CASOS (dados partilhados)
CASOS = [
    dict(id="auto-voz", sector="automocion-lujo", sl="Automoción de lujo", prob="percepcion demanda", foto=("tn-autosport-deportivos", "Dos coches deportivos expuestos en el interior de un concesionario de automoción"),
         t="De publicar coches a construir la voz de referencia del sector", s="Una transformación editorial continuada: contenido audiovisual de alto alcance combinado con un formato de podcast propio para convertir producto y criterio en autoridad.",
         p="Una cuenta consolidada, con comunidad propia y baja interacción relativa, cuya presencia digital todavía no reflejaba la autoridad real del negocio ni la calidad del inventario que movía.",
         i="En lugar de aumentar la frecuencia de publicación, se diseñó una línea editorial reconocible: piezas audiovisuales pensadas para alcance y un formato de podcast propio que convirtiera la conversación del sector en un activo de marca.",
         r="La cuenta pasó de acompañar al negocio a liderar la conversación de su categoría, con piezas de alcance muy superior a su comunidad y un formato editorial que sostiene la autoridad mes a mes.",
         ev=["Contenidos con millones de visitas y una media de entre 20.000 y 300.000 visitas por pieza", "La comunidad se multiplicó durante el periodo de trabajo continuado"]),
    dict(id="joya-marca", sector="joyeria-relojeria", sl="Joyería y relojería", prob="percepcion", foto=("diamantes-riviere", "Macro de una pulsera rivière de diamantes sobre terciopelo azul oscuro"),
         t="Una pieza excepcional necesitaba una marca a su altura", s="Identidad, herramientas comerciales físicas y contenido experto para elevar el valor percibido de un producto de altísimo valor real.",
         p="Un negocio de diamantes con producto de primer nivel y una identidad que no comunicaba ni su solvencia ni el ceremonial que acompaña a una compra de este tipo.",
         i="Construir la marca desde el principio y dotarla de herramientas comerciales tangibles: no solo un logotipo, sino los materiales con los que se presenta y se cierra una venta.",
         r="La marca pasó a presentarse con un estándar coherente con el valor de su producto, con materiales propios que sostienen la conversación comercial en el punto de venta.", ev=[]),
    dict(id="hotel-agente", sector="hoteles", sl="Hoteles", prob="consultas saturacion", foto=("hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado"),
         t="Un agente diseñado alrededor de la operativa real de un hotel", s="Atención en más de veinte idiomas, consulta de fuentes conectadas y derivación a recepción cuando la gestión exige intervención humana.",
         p="Un establecimiento con consultas que entran a cualquier hora, en varios idiomas y por varios canales, y una recepción que no puede estar en todo sin dejar de atender bien a quien ya está alojado.",
         i="Diseñar un agente alrededor de la operativa concreta del hotel en lugar de instalar un chatbot genérico: qué puede responder, qué debe consultar y en qué momento exacto deja de hablar y avisa a una persona.",
         r="Un canal de atención disponible de forma continuada, capaz de responder en más de veinte idiomas y de derivar a recepción cuando la gestión lo requiere.", ev=[]),
    dict(id="auto-producto", sector="automocion-lujo", sl="Automoción de lujo", prob="demanda percepcion", foto=("sm-cardress-funda", "Coupé deportivo cubierto con una funda textil a medida con diseño personalizado"),
         t="Contenido de producto que se entiende en tres segundos", s="Estrategia audiovisual centrada en el producto y formatos de entrevista para construir comunidad alrededor de una pieza muy visual.",
         p="Un producto premium para automoción, muy visual y fácil de admirar, pero difícil de explicar en un catálogo estático.",
         i="Tratar el producto como protagonista audiovisual y complementarlo con entrevistas que aportaran contexto, criterio y comunidad alrededor de la marca.",
         r="El producto pasó a explicarse solo en el primer visionado y la marca construyó un catálogo audiovisual reutilizable en su venta diaria.",
         ev=["El cliente comunica un impacto comercial directo tras la pieza de mayor alcance"]),
    dict(id="nautica-identidad", sector="nautica", sl="Náutica, yates y puertos", prob="percepcion conversion", foto=("yate-completo", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire"),
         t="Identidad e infraestructura digital para el alquiler de yates", s="Creación de identidad integral e infraestructuras digitales para una agencia de alquiler de yates de lujo en la Costa Brava.",
         p="Un activo de altísimo valor por experiencia se comercializa, muchas veces, con materiales que no transmiten ni la calidad del barco ni la del servicio a bordo.",
         i="Construir primero la identidad y la infraestructura digital, para que cada consulta llegara a un entorno que sostuviera el nivel de la experiencia ofrecida.",
         r="Una presencia coherente con el producto, capaz de presentar la embarcación y la experiencia con el mismo estándar con el que se vive a bordo.", ev=[]),
    dict(id="b2b-vinoteca", sector="b2b", sl="B2B y servicios", prob="saturacion", foto=None,
         t="Automatización interna en una vinoteca de lujo", s="Sistemas internos de IA y automatización aplicados a procesos seleccionados de la operativa diaria.",
         p="Procesos internos necesarios, repetitivos y muy consumidores de tiempo dentro de una operación de producto de alto valor.",
         i="Identificar qué procesos concretos podían automatizarse con control y cuáles debían seguir dependiendo de una persona.",
         r="Una reducción sustancial del tiempo dedicado a los procesos incluidos en el alcance.", ev=["Reducción sustancial del tiempo dedicado a los procesos incluidos en el alcance"]),
    dict(id="nautica-regatas", sector="nautica", sl="Náutica, yates y puertos", prob="percepcion", foto=("regata-dron", "Velero navegando frente a una localidad costera, fotografiado desde el aire"),
         t="Producción y cobertura en vivo en puertos y regatas", s="Cobertura profesional de eventos náuticos: competición, comunidad y experiencia de puerto documentadas con criterio editorial.",
         p="Los eventos náuticos concentran en pocas horas todo lo que una marca necesita mostrar durante un año, y suelen quedar registrados sin dirección ni aprovechamiento posterior.",
         i="Tratar la cobertura como producción, no como reportaje: decidir antes qué historia se cuenta y qué se necesita capturar para poder contarla.",
         r="Un archivo audiovisual con criterio, utilizable durante toda la temporada y no solo el día del evento.", ev=[]),
    dict(id="nautica-compradores", sector="nautica", sl="Náutica, yates y puertos", prob="demanda", foto=("yate-vistas", "Zona exterior de un yate con mesa, asientos y vistas a la costa"),
         t="Llegar a compradores de yate sin una cartera previa", s="Fotografía profesional, distribución en canales especializados y estrategia de venta en redes aplicadas a la comercialización privada de embarcaciones.",
         p="La comercialización de una embarcación de alto valor depende, tradicionalmente, de una cartera de contactos que se construye durante años.",
         i="Sustituir la cartera por alcance dirigido: producir el material a la altura del activo y distribuirlo donde está el comprador, no donde está el vendedor.",
         r="Se alcanzó a compradores cualificados sin disponer previamente de una cartera propia.", ev=[]),
]


def caso_html(R, c, filtro=False):
    foto = f'<div class="ventana" style="aspect-ratio:4/3">{img(R, c["foto"][0], c["foto"][1], "(min-width: 900px) 36vw, 100vw")}</div>' if c["foto"] else ""
    ev = ""
    if c["ev"]:
        ev = '<div class="evid">' + "<br>".join(e(x) for x in c["ev"]) + "<small>Trabajo dirigido por Ferreras. Las cifras se publican una vez verificadas con el cliente.</small></div>"
    atr = f' data-caso data-sector="{c["sector"]}" data-problema="{c["prob"]}"' if filtro else ""
    return (f'<article class="caso"{atr} data-sube><div class="caso-cab">{foto}<p class="etiqueta">{e(c["sl"])}</p><h3>{e(c["t"])}</h3><p>{e(c["s"])}</p></div>'
            f'<dl><dt>Problema</dt><dd>{e(c["p"])}</dd><dt>Intervención</dt><dd>{e(c["i"])}</dd><dt>Resultado</dt><dd>{e(c["r"])}</dd>{ev}</dl></article>')


def casos_de(sector):
    return [c for c in CASOS if c["sector"] == sector]


# ================================================================= SECTORES
SECTORES = {
    "hoteles": dict(nome="Hoteles", titulo="Agentes de IA para hoteles", desc="Atienda 24/7, en varios idiomas y sin saturar recepción. Agentes de voz, chat y WhatsApp diseñados alrededor de la operativa real de su establecimiento.",
                    h1=("Atienda 24/7, en varios idiomas", "y sin saturar recepción", "<em>ni dejar reservas sin respuesta.</em>"),
                    lead="Un agente diseñado alrededor de su operativa real: responde lo que sabe, consulta lo que debe consultar y avisa a recepción cuando la gestión exige una persona.",
                    foto=("ia-hotel-recepcion-equipo", "Recepcionista atendiendo en persona a una huésped mientras un sistema resuelve consultas en paralelo"),
                    margen=[("La consulta que entra a las 23:40", "Llega fuera de horario, muchas veces en otro idioma. Cuando alguien la lee, el cliente ya ha reservado en otro establecimiento. No es una consulta perdida: es una habitación vacía."),
                            ("Recepción atiende dos cosas a la vez y ninguna bien", "El teléfono suena mientras hay un huésped delante del mostrador. Se atiende rápido a los dos y se cuida mal a ambos."),
                            ("Las mismas quince preguntas, todos los días", "Horarios, parking, mascotas, cancelaciones, servicios, cómo llegar. Un trabajo necesario que consume el tiempo que debería dedicarse a vender mejor."),
                            ("La reserva directa pierde contra el canal", "Cuando el canal responde antes y mejor que el establecimiento, la comisión deja de ser una opción y pasa a ser la norma.")],
                    promessa="Que ninguna consulta se quede sin respuesta por hora, idioma o carga de trabajo, <em>y que recepción recupere su tiempo.</em>",
                    sistema=[("Conocimiento del establecimiento", "El agente aprende su operativa concreta: servicios, horarios, políticas, entorno y particularidades. No responde con generalidades de sector."),
                             ("Canales de entrada", "Voz, web y WhatsApp según el alcance contratado. La consulta entra por donde el cliente prefiera y se trata con el mismo criterio."),
                             ("Fuentes conectadas", "Consulta de fuentes de información autorizadas para responder con datos actualizados en lugar de con una copia congelada del mes pasado."),
                             ("Cualificación y derivación", "Recoge lo necesario, resuelve lo que está autorizado a resolver y transfiere a recepción cuando la gestión requiere intervención humana."),
                             ("Permisos y registro", "Alcance definido, permisos mínimos, confirmación para acciones sensibles y registro de actividad revisable.")],
                    exp="Ferreras ha diseñado un agente de atención para un hotel de montaña, preparado para atender de forma continuada en más de veinte idiomas, consultar fuentes conectadas para responder con información actualizada y derivar a recepción cuando la gestión lo exige. Además, la firma cuenta con experiencia de marketing en el sector hotelero.",
                    entrada=("Asistente IA 24/7 para hoteles", "La integración con PMS o Channel Manager depende del alcance, de la API disponible, de los permisos y de las pruebas. Los consumos de voz, WhatsApp, modelos y APIs se facturan aparte."),
                    extra_link=("ia-hoteles/", "Ver cómo trabajamos la atención de un hotel"),
                    faq=[("¿Se integra con nuestro PMS o Channel Manager?", "Depende del alcance, de la existencia de API, de los permisos que nos concedan y de las pruebas. Es una posibilidad a evaluar en el diagnóstico, no una integración que demos por hecha."),
                         ("¿El agente puede confirmar una reserva?", "Solo si se autoriza expresamente esa acción, con confirmación y registro. Por defecto trabajamos en modo consulta y derivación a recepción."),
                         ("¿En cuántos idiomas atiende?", "La atención multidioma es una de las capacidades centrales. El número final de idiomas activos se fija en el alcance, según los mercados reales del establecimiento."),
                         ("¿Qué pasa fuera del horario de recepción?", "El agente responde y recoge la consulta con la información necesaria para que recepción la resuelva a primera hora, en lugar de perderla.")]),
    "automocion-lujo": dict(nome="Automoción de lujo", titulo="Marketing para automoción de lujo", desc="Eleve la percepción de su inventario y convierta atención en consultas cualificadas con contenido audiovisual y formatos de autoridad.",
                    h1=("Su inventario merece contarse", "mejor que en una ficha", "<em>con doce fotos.</em>"),
                    lead="Contenido audiovisual y formatos de autoridad que elevan la percepción del vehículo y convierten atención en consultas cualificadas.",
                    foto=("nissan-gtr", "Nissan GT-R preparado, con carrocería ensanchada y alerón trasero, en acabado camaleón violeta y rosa"),
                    margen=[("El coche se ve, pero no se desea", "Fotografías correctas y ningún relato. El comprador compara precio contra precio porque no le hemos dado otra cosa que comparar."),
                            ("Alcance sin consultas", "El contenido gusta, se comparte y no genera una sola conversación comercial porque nunca se diseñó para producirla."),
                            ("La autoridad se la lleva otro", "En un sector de opiniones fuertes, quien habla con criterio se convierte en referencia. El resto solo publica stock."),
                            ("El producto asociado no se explica", "Accesorios y productos premium para el vehículo son muy visuales y difíciles de explicar en estático: se venden mucho mejor en movimiento.")],
                    promessa="Elevar la percepción del inventario y de los productos asociados, <em>y convertir la atención en consultas cualificadas.</em>",
                    sistema=[("Línea editorial", "Una voz reconocible que distingue su cuenta de un tablón de anuncios."), ("Piezas de alcance", "Contenido audiovisual diseñado para salir de su comunidad actual."), ("Formato de autoridad", "Entrevistas y podcast que convierten criterio y conversación en marca."), ("Contenido de producto", "El producto explicado en los primeros tres segundos, sin necesidad de texto."), ("Captación", "Una ruta clara desde la pieza hasta la consulta cualificada.")],
                    exp="Ferreras ha dirigido la transformación editorial continuada de un negocio de automoción deportiva, creando un formato de podcast propio, y ha desarrollado la estrategia de contenido de un producto premium para automoción.",
                    entrada=("Autoridad & Demanda", "Incluye estrategia, producción, distribución y panel de KPIs. La inversión publicitaria se presupuesta aparte."),
                    extra_link=None,
                    faq=[("¿Graban en nuestras instalaciones?", "Sí. Las sesiones de producción se planifican en su exposición o en la localización que mejor represente el vehículo."),
                         ("¿Sirve para vehículo de ocasión premium?", "Sí. De hecho es donde más se nota la diferencia entre una ficha estándar y una pieza bien contada."),
                         ("¿Necesitamos aparecer en cámara?", "Ayuda mucho, sobre todo en los formatos de autoridad. Existen alternativas sin rostro, aunque construyen reputación más despacio.")]),
    "nautica": dict(nome="Náutica, yates y puertos", titulo="Marketing náutico: clubs, astilleros, yates y chárter", desc="Clubs náuticos, astilleros, compraventa de yates y alquiler de barcos. Identidad, producción audiovisual, cobertura de regatas y eventos, y comercialización.",
                    h1=("El mar se vende enseñándolo.", "Nadie reserva ni compra", "<em>por una ficha técnica.</em>"),
                    lead="Clubs náuticos, astilleros, compraventa de yates y alquiler de barcos: relato, producción audiovisual, cobertura de regatas y eventos, y seguimiento comercial.",
                    foto=("yate-completo", "Yate de lujo fondeado en una cala de aguas turquesa, fotografiado desde el aire"),
                    margen=[("La experiencia a bordo no se transmite", "Lo que se reserva o se compra no es la eslora: es un día concreto. Si no se produce bien, el cliente solo ve un barco blanco más."),
                            ("Un club vive de que le vean", "Socios, escuela, regatas y patrocinadores dependen de la misma cosa: que el club se perciba activo y con nivel. Sin contenido, esa percepción se apaga entre temporadas."),
                            ("La regata se celebra y se evapora", "Una regata, una botadura o una presentación concentran en unas horas el mejor material del año, y suelen quedar grabadas sin dirección ni uso posterior."),
                            ("La consulta internacional llega y se enfría", "Idioma, franja horaria y tiempo de respuesta deciden más operaciones de las que parece.")],
                    promessa="Que una embarcación, un club o una temporada se perciban con el mismo estándar con el que se viven, <em>y llegar a quien todavía no le conoce.</em>",
                    sistema=[("Identidad e infraestructura digital", "La base sobre la que se sostiene cualquier consulta cualificada."), ("Producción fotográfica y audiovisual", "Embarcación, experiencia a bordo y entorno, producidos con criterio editorial."), ("Distribución especializada", "Canales del sector y estrategia social orientada a alcanzar comprador, no a acumular seguidores."), ("Evento y cobertura", "Organización y producción en puerto, incluida cobertura en vivo de competición.")],
                    exp="Ferreras ha creado la identidad e infraestructura digital de una agencia de alquiler de yates de lujo, ha ejercido de bróker privado apoyándose en producción fotográfica y distribución multicanal para alcanzar compradores sin cartera previa, y produce y cubre eventos y regatas en puerto, incluido el evento propio Luxury & Yachts.",
                    entrada=("Producción y comercialización", "Los proyectos de identidad e infraestructura digital se presupuestan por alcance. Viajes y dietas aparte."),
                    extra_link=None,
                    faq=[("¿Trabajan la comercialización internacional?", "La producción y la distribución sí están pensadas para comprador internacional. La operación y su documentación las mantiene usted o su bróker."),
                         ("¿Producen con dron?", "Sí, cuando la localización y la normativa lo permiten. En náutica el plano aéreo es habitualmente el que mejor explica el activo."),
                         ("¿Pueden cubrir una regata completa?", "Sí, incluida cobertura en vivo. Se planifica antes qué historia se cuenta para que el material sirva durante toda la temporada.")]),
    "joyeria-relojeria": dict(nome="Joyería y relojería", titulo="Autoridad de marca para joyería y relojería", desc="La autoridad es lo que sostiene el precio. Construimos la de su casa: criterio reconocido, contenido experto y materiales que venden cuando usted no está delante.",
                    h1=("En joyería no gana", "el que más enseña.", "<em>Gana el que más autoridad tiene.</em>"),
                    lead="Quien es percibido como la referencia de su plaza no negocia el precio, no compite por descuento y recibe al cliente ya convencido. Esa autoridad se construye.",
                    foto=("diamantes-pulsera-zafiros", "Pulsera de zafiros azules y diamantes sobre terciopelo azul oscuro"),
                    margen=[("El producto supera a la marca", "La pieza es excepcional y la presentación no acompaña. El cliente compara con marcas peores y mejor contadas, y el precio pasa a parecer alto."),
                            ("La venta depende por completo del mostrador", "Sin materiales que sostengan la conversación fuera de la tienda, cada venta exige empezar de cero y estar presente."),
                            ("La confianza se juega en el ceremonial", "En una compra de alto valor, cómo se entrega la pieza y qué la acompaña pesa tanto como la pieza misma."),
                            ("Distribuir en terceros sin un relato propio", "Colocar producto en otras joyerías sin materiales de marca convierte la pieza en un artículo más de la vitrina.")],
                    promessa="Que su casa sea la referencia a la que se acude antes de decidir, <em>y que esa autoridad trabaje incluso cuando usted no está delante.</em>",
                    sistema=[("Identidad", "Logotipo, sistema visual y normas de uso coherentes con el nivel del producto."), ("Herramientas comerciales", "Book comercial para distribución en joyerías y elementos de ceremonial de entrega."), ("Contenido experto", "Formatos de autoridad que explican criterio, calidad y procedencia, no solo producto."), ("Infraestructura digital", "Una presencia que sostiene el nivel del producto y cualifica al comprador.")],
                    exp="Ferreras ha construido la identidad y las herramientas comerciales de un negocio de diamantes, y opera su propia marca española de relojes automáticos de autor, con diseño propio, mecanismo suizo, ensamblaje en Barcelona y distribución en joyerías.",
                    entrada=("Marketing estratégico", "Los proyectos de identidad, book comercial y elementos de ceremonial se presupuestan por alcance."),
                    extra_link=None,
                    faq=[("¿Trabajan con marcas que aún no tienen identidad?", "Sí. De hecho es el punto de partida más frecuente: primero se define la marca y sus materiales, y después se construye el contenido que la difunde."),
                         ("¿Producen fotografía de producto?", "Sí, y es una parte crítica en este sector. Una pieza de alto valor mal fotografiada se percibe como una pieza de menos valor."),
                         ("¿Pueden ayudar con la distribución en otras joyerías?", "Podemos construir los materiales que la hacen posible —book comercial, argumentario, elementos de ceremonial— y la estrategia de presentación. La relación comercial la mantiene usted.")]),
}


def sector_pagina(chave, d):
    def corpo(R):
        casos = casos_de(chave)
        if chave == "joyeria-relojeria":
            casos = casos + [dict(id="ferreras", sector="joyeria-relojeria", sl="Marca propia", prob="", foto=("reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche"),
                                  t="Producto, relato, distribución y experiencia, en nuestra propia casa", s="Una marca española de relojes automáticos de autor: diseño propio, mecanismo suizo, ensamblaje en Barcelona, distribución en joyerías y presentaciones en entornos de lujo.",
                                  p="Crear una marca de relojería de autor obliga a resolver, en la propia casa, exactamente los mismos problemas que un cliente encarga a una agencia: producto, relato, deseo, distribución y seguimiento.",
                                  i="Construir Relojes Ferreras aplicando el mismo método que se propone a los clientes, sin atajos y sin delegar las decisiones difíciles.",
                                  r="Una marca en funcionamiento que sirve de banco de pruebas permanente: cada recomendación que hacemos a un cliente la hemos aplicado antes a nuestra propia empresa.", ev=[])]
        casos_h = "".join(caso_html(R, c) for c in casos)
        extra = f'<p style="margin-top:2rem">{enlace(R + d["extra_link"][0], d["extra_link"][1])}</p>' if d["extra_link"] else ""
        sistema = cards(d["sistema"], 2)
        return (ph(R, d["nome"], L(*d["h1"]), d["lead"], btn(R + DIAG + "?sector=" + chave, "Pide su diagnóstico") + btn(R + "resultados/", "Ver resultados reales", "btn-linha", False),
                   img(R, d["foto"][0], d["foto"][1], "(min-width: 900px) 40vw, 100vw", lazy=False), migas=[("", "Inicio"), ("sectores/", "Sectores"), (None, d["nome"])])
                + sec(cab("01", "Lo que cuesta dinero", "Dónde se pierde el margen <em>en su sector.</em>") + cards(d["margen"]))
                + sec(f'{etq("02", "La promesa", "n")}<p class="titulo promessa" data-duas-tintas style="margin:1.6rem 0 4rem">{d["promessa"]}</p><p class="etiqueta" style="margin-bottom:1rem">Así se adapta el sistema a la operativa de su sector</p>{sistema}')
                + sec(cab("03", "Experiencia", "Qué hemos hecho ya <em>en este terreno.</em>", e(d["exp"])) + casos_h)
                + sec(f'<div class="grelha"><div style="grid-column:1/6">{etq("04", "Punto de entrada", "n")}<h2 class="titulo t-l" data-linhas style="margin-top:1.4rem">Por dónde <em>se empieza.</em></h2></div><div style="grid-column:7/13" class="plano dest" data-sube><span class="selo">Punto de entrada</span><h3>{d["entrada"][0]}</h3><p class="texto">{d["entrada"][1]}</p><p class="nota">El alcance y el importe se cierran por escrito tras el diagnóstico.</p>{extra}</div></div>')
                + sec(f'<div class="grelha"><div class="faq-cab">{etq("05", "Objeciones habituales", "n")}<h2 class="titulo t-l" data-linhas>Lo que suelen preguntarnos <em>en su sector.</em></h2></div>{faq(d["faq"], "fs")}</div>')
                + banda("Pide su <em>diagnóstico.</em>", "El diagnóstico ya viene con su sector seleccionado. Dos minutos y tendrá una recomendación concreta.", btn(R + DIAG + "?sector=" + chave, "Empezar el diagnóstico")))
    pagina(f"sectores/{chave}/", d["titulo"], d["desc"], corpo)


for k, v in SECTORES.items():
    sector_pagina(k, v)


def sectores_idx(R):
    return (ph(R, "Sectores", L("Cuatro sectores", "que conocemos", "<em>por dentro.</em>"), "Hotelería, automoción, náutica y joyería: sectores donde cada detalle se nota. El mismo estándar, aplicado a cualquier empresa consolidada con margen y reputación que defender.", btn(R + DIAG, "Pide su diagnóstico"))
            + sec(sect_html(R)) + banda("¿Su sector <em>no está aquí?</em>", "Trabajamos también con inmobiliaria premium, servicios profesionales y B2B. El diagnóstico le dice por dónde empezaríamos.", btn(R + DIAG, "Pide su diagnóstico")))


pagina("sectores/", "Sectores", "Hotelería, automoción de lujo, náutica y joyería: cuatro sectores que conocemos por dentro.", sectores_idx)


# ================================================================= RESULTADOS
def resultados(R):
    sectores_f = [("todos", "Todos"), ("automocion-lujo", "Automoción de lujo"), ("joyeria-relojeria", "Joyería y relojería"), ("hoteles", "Hoteles"), ("nautica", "Náutica, yates y puertos"), ("b2b", "B2B y servicios")]
    problemas_f = [("todos", "Todos"), ("percepcion", "Percepción por debajo del producto"), ("demanda", "Falta de demanda cualificada"), ("conversion", "Tráfico que no convierte"), ("consultas", "Consultas perdidas o desatendidas"), ("saturacion", "Saturación operativa")]
    bs = lambda tipo, l: "".join(f'<button type="button" data-f="{tipo}" data-v="{v}" aria-pressed="{str(v == "todos").lower()}">{e(t)}</button>' for v, t in l)
    casos_h = "".join(caso_html(R, c, True) for c in CASOS)
    return (ph(R, "Resultados", L("Lo que hicimos,", "por qué lo decidimos", "<em>y qué lo respalda.</em>"), "Cada caso se cuenta con la misma estructura: contexto, decisión, ejecución, resultado y evidencia. Las cifras se publican cuando están verificadas y el cliente autoriza su difusión, no antes.", btn(R + DIAG, "Pide su diagnóstico"))
            + sec(f'{etq("", "Cómo tratamos la evidencia", "n")}<p class="titulo promessa" data-duas-tintas style="margin:1.6rem 0 2rem">Preferimos un caso honesto <em>a una cifra impresionante.</em></p><p class="texto" data-sube style="max-width:60ch">No sumamos resultados de publicaciones, periodos o clientes distintos. Distinguimos siempre entre alcance, interacción, oportunidades y ventas. Y cuando un cliente no ha autorizado el uso de su marca, describimos el trabajo sin identificarlo en lugar de presentarlo como propio.</p>')
            + sec(f'<div class="grelha marca-grid"><div class="marca-fotos"><figure class="f1 ventana" data-janela>{img(R, "reloj-detalle-f", "Macro de la aguja en forma de F y del movimiento visto del reloj Ferreras Almirante", "(min-width: 900px) 34vw, 70vw")}</figure><figure class="f2 ventana" data-vivo>{img(R, "reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche", "(min-width: 900px) 24vw, 50vw")}</figure></div><div class="marca-txt">{etq("01", "Nuestra propia marca", "n")}<h2 class="titulo t-l" data-linhas>Estamos tan seguros de nuestros resultados que <em>creamos nuestra propia marca.</em></h2><p class="texto" data-sube>Relojes Ferreras nació dentro de esta agencia, desde cero, para demostrar que nuestras estrategias funcionan cuando somos nosotros quienes asumimos las consecuencias.</p><p class="texto" data-sube>Producto, identidad, web y ecommerce, distribución en joyerías y experiencia de cliente. Aquí no hay un informe detrás del que escondernos: si algo no funciona, lo pagamos nosotros.</p><p data-sube>{enlace("https://relojes-ferreras.com/", "Ver Relojes Ferreras", True)}</p></div></div>')
            + sec(cab("02", "Todos los casos", "Filtre por sector o por <em>el problema que quiere resolver.</em>")
                  + f'<div data-filtros><p class="filtro-rot">Filtrar por sector</p><div class="filtros">{bs("sector", sectores_f)}</div><p class="filtro-rot">Filtrar por problema</p><div class="filtros">{bs("problema", problemas_f)}</div><p class="conteo" data-conteo>{len(CASOS)} casos</p></div>'
                  + f'<div style="margin-top:2rem">{casos_h}</div>')
            + sec(cab("03", "Producción", "Eventos, puertos y entornos <em>de alta exigencia.</em>", "Producir donde no se puede repetir una toma enseña una disciplina que después se nota en todo lo demás.") + f'<figure class="foto-larga ventana" data-janela>{img(R, "puerto-club-vela-blanes", "Vista aérea de un puerto deportivo, su dique y la playa contigua")}</figure><p class="pie" style="margin-top:.8rem"><b>Náutica</b>Puertos, regatas y producto. Cobertura aérea y de agua con equipo propio.</p>')
            + banda("¿Quiere un resultado parecido <em>en su sector?</em>", "El diagnóstico compara su situación con trabajos equivalentes y le dice por dónde empezar.", btn(R + DIAG, "Pide su diagnóstico")))


pagina("resultados/", "Resultados y casos", "Casos con contexto, decisión, ejecución, resultado y tipo de evidencia. Publicamos cifras solo cuando están verificadas y autorizadas.", resultados)


def casos_p(R):
    return (ph(R, "Casos", L("Lo que cambia cuando", "los dos departamentos", "<em>trabajan juntos.</em>"), "Un caso completo, con la situación de partida, lo que se hizo y las cifras de antes y después.")
            + sec(f'<div class="via" style="max-width:52rem"><p class="etiqueta"><span class="n">●</span>En preparación</p><h2>Estamos cerrando la medición del primer caso completo con el cliente.</h2><p class="texto">Lo publicaremos con las cifras verificadas y su autorización por escrito, no antes. Si quiere ver trabajos concretos mientras tanto, la página de resultados recoge lo que ya está publicado.</p><div class="acoes">{btn(R + "resultados/", "Ver resultados")}{btn(R + DIAG, "Pide su diagnóstico", "btn-linha")}</div></div>'))


pagina("casos/", "Casos", "Marketing e inteligencia artificial trabajando juntos dentro de una misma empresa, con cifras de antes y después.", casos_p)


# ================================================================= WEB
def web(R):
    inf = ["Explica quiénes son y qué hacen", "Presenta servicios en forma de catálogo", "Deja al visitante decidir solo", "Un formulario genérico al final", "Métricas de visitas, no de negocio", "Se rehace entera cada tres años"]
    com = ["Ordena la decisión del visitante paso a paso", "Demuestra con evidencia, no con adjetivos", "Cualifica y recomienda antes de pedir datos", "Conversión conectada a CRM y seguimiento", "Eventos de negocio definidos y medidos", "Evoluciona con lo que aprende cada mes"]
    ul = lambda l: "<ul>" + "".join(f"<li>{e(x)}</li>" for x in l) + "</ul>"
    ruta = [("Visita", "Llega con una pregunta."), ("Mensaje", "Entiende en segundos qué hace y para quién."), ("Prueba", "Ve evidencia, no adjetivos."), ("Recomendación", "Recibe un siguiente paso a su medida."), ("Lead", "Deja sus datos con contexto."), ("Seguimiento", "Su equipo llama sabiendo qué necesita.")]
    averias = [("La web informa, pero no guía", "Explica quiénes son y qué hacen. No ordena la decisión del visitante ni le dice cuál es el siguiente paso que le conviene."),
               ("Entra tráfico y no sale nada", "Hay visitas, hay tiempo de permanencia y no hay solicitudes. Falta prueba, falta cualificación y falta una conversión creíble."),
               ("La evidencia está dispersa", "Los mejores trabajos viven en redes, en el móvil de alguien o en una carpeta. La web no los usa para construir confianza."),
               ("Nadie sabe qué está midiendo", "Sin eventos ni definición de oportunidad cualificada, cada decisión sobre la web se toma por intuición.")]
    planos = [("Web Signature", "Una presencia ordenada, sobria y coherente con el nivel real del negocio.", ["Estrategia, arquitectura y diseño personalizado", "Hasta 5 páginas o plantillas principales", "Copy comercial, responsive y SEO técnico básico", "Formularios, analítica y formación"], ""),
              ("Web de Captación", "Una infraestructura que cualifica al visitante y produce oportunidades medibles.", ["Investigación de público, oferta y competencia", "Hasta 10–12 páginas o plantillas estratégicas", "Casos de éxito y sistema de prueba", "Configurador o funnel de cualificación", "Integración con CRM, email y medición de conversión", "Una landing sectorial reutilizable"], "Bestseller de su categoría"),
              ("Ecommerce", "Catálogo, arquitectura de conversión y operativa de venta conectada.", ["Diseño, catálogo inicial y arquitectura de conversión", "Pagos, envíos, emails transaccionales y analítica", "SEO base, formación y lanzamiento", "Alcance final según productos, mercados e integraciones"], "")]
    ph_ = "".join(f'<div class="plano{se(bool(s), " dest")}" data-sube style="--i:{i}">{se(bool(s), "<span class=" + Q + "selo" + Q + ">" + s + "</span>")}<h3>{t}</h3><p class="texto">{p}</p><ul>{"".join("<li>" + e(x) + "</li>" for x in l)}</ul></div>' for i, (t, p, l, s) in enumerate(planos))
    care = [("Care Esencial", "Mantenimiento técnico, seguridad, copias de seguridad y analítica."), ("Care Evolución", "Todo lo anterior más una mejora mensual y trabajo continuado de CRO."), ("Care Prioritario", "Soporte ecommerce o evolución prioritaria con tiempos de respuesta acordados.")]
    pagos = [("50 %", "Al inicio del proyecto, con la fase de diagnóstico y arquitectura ya planificada."), ("30 %", "Con la aprobación del diseño, antes de entrar en desarrollo."), ("20 %", "Antes de la publicación, con la web revisada y probada.")]
    pg = "".join(f'<div data-sube style="--i:{i}"><b>{a}</b><p>{b}</p></div>' for i, (a, b) in enumerate(pagos))
    faqs = [("¿Cuánto dura un proyecto web?", "Depende del número de páginas, de la producción de contenido y de las integraciones. El calendario se cierra con hitos concretos en la fase de diseño, no antes."),
            ("¿Quién escribe los textos?", "Nosotros. El copy comercial forma parte del proyecto porque una web sin argumento es una plantilla bonita. Usted valida."),
            ("¿La web es nuestra?", "Sí. El proyecto, los accesos y el dominio quedan a su nombre. Ferreras Care es un servicio opcional, no una forma de retener el control."),
            ("¿Cómo son los pagos?", "De forma orientativa, 50 % al inicio, 30 % con la aprobación del diseño y 20 % antes de la publicación. Las condiciones definitivas son las del contrato.")]
    return (ph(R, "Web y ecommerce", L("Una web no debería limitarse", "a explicar su empresa.", "<em>Debería ayudarle a venderla.</em>"), "Diseñamos experiencias que ordenan su propuesta, demuestran valor, cualifican al cliente y convierten atención en una siguiente acción medible.",
               btn(R + DIAG, "Pide su diagnóstico") + btn("#planes", "Ver qué incluye cada plan", "btn-linha", False), chips_=["Alcance cerrado antes de producir", "Pagos por hitos", "El proyecto y los accesos son suyos"])
            + sec(cab("01", "La diferencia", "Web informativa frente a <em>infraestructura comercial.</em>", "Las dos se ven bien en una captura. Solo una de ellas produce oportunidades cuando usted no está delante.") + f'<div class="compara"><div data-sube><h3>Web informativa</h3>{ul(inf)}</div><div class="bom" data-sube style="--i:1"><h3>Infraestructura comercial</h3>{ul(com)}</div></div>')
            + sec(cab("02", "Ruta del visitante", "De la visita <em>al seguimiento.</em>", "Cada paso tiene una función y una medición. Cuando una web no convierte, casi siempre es porque uno de estos pasos no existe.") + passos(ruta) + f'<div style="margin-top:4rem">{cards(averias)}</div>')
            + sec(cab("03", "Portfolio", "Proyectos explicados por <em>objetivo y decisión.</em>", "Un portfolio de capturas bonitas no demuestra nada. Preferimos contar qué se decidió y por qué.")
                  + f'<article class="caso" data-sube><div class="caso-cab"><div class="ventana" style="aspect-ratio:4/3">{img(R, "reloj-ferreras-almirante", "Reloj automático Ferreras Almirante presentado en su estuche", "(min-width: 900px) 36vw, 100vw")}</div><p class="etiqueta">Caso propio</p><h3>Una marca que también vende online</h3></div><dl><dt>Proyecto</dt><dd>Relojes Ferreras es nuestra propia marca de relojería automática: producto, identidad, web y ecommerce, distribución en joyerías y experiencia de cliente.</dd><dt>Por qué importa</dt><dd>Es el proyecto donde no podemos escondernos detrás de un informe, porque las consecuencias de cada decisión las asumimos nosotros.</dd><dt>Ver</dt><dd>{enlace("https://relojes-ferreras.com/", "La web de Relojes Ferreras", True)}</dd></dl></article>'
                  + caso_html(R, CASOS[4]))
            + banda("¿Su problema está en el mensaje, <em>en la prueba o en la conversión?</em>", "Son tres averías distintas y se arreglan de forma distinta. El diagnóstico identifica cuál es la suya antes de presupuestar nada.", btn(R + DIAG, "Pide su diagnóstico"))
            + sec(cab("04", "Planes", "Tres alcances y un nivel <em>superior a medida.</em>", "El desarrollo lo hace nuestro propio equipo informático, no un proveedor externo.") + f'<div class="planos">{ph_}</div>'
                  + f'<div class="plano" style="margin-top:var(--g)" data-sube><span class="selo">Digital Flagship</span><h3>Cuando el proyecto no cabe en un paquete</h3><p class="texto">Proyectos de lujo con multidioma, vídeo, motion, configuradores, áreas privadas o integraciones complejas. Siempre con alcance definido caso por caso: no es un paquete, es un proyecto.</p></div>'
                  + '<p class="nota" style="margin-top:2rem">Cada proyecto se diseña y se presupuesta a medida: el alcance y el precio se cierran por escrito antes de empezar a producir. Dominios, alojamiento, licencias, bancos de imágenes, pasarelas de pago, traducciones profesionales, publicidad, desplazamientos, telefonía, APIs y consumos externos se presupuestan aparte.</p>', extra=' id="planes"')
            + sec(cab("05", "Ferreras Care", "Una web publicada <em>no es una web terminada.</em>", "El mantenimiento es opcional y no condiciona la propiedad del proyecto: los accesos y el dominio son suyos desde el primer día.") + cards(care, 3, False))
            + sec(cab("06", "Proceso y pagos", "Pagos por hitos, <em>no por confianza ciega.</em>") + f'<div class="pagos">{pg}</div><p class="nota" style="margin-top:2rem">Condiciones orientativas. Las definitivas son las que recoja el contrato del proyecto.</p>')
            + sec(f'<div class="grelha"><div class="faq-cab">{etq("07", "Preguntas frecuentes", "n")}<h2 class="titulo t-l" data-linhas>Antes de encargar <em>una web.</em></h2></div>{faq(faqs, "fw")}</div>')
            + banda("¿Qué necesita realmente <em>su web?</em>", "El diagnóstico distingue si el problema está en el mensaje, en la prueba o en la conversión.", btn(R + DIAG, "Pide su diagnóstico")))


pagina("web/", "Web y ecommerce con arquitectura comercial", "Diseñamos webs que ordenan su propuesta, demuestran valor, cualifican al cliente y convierten la atención en una siguiente acción medible.", web)


# ================================================================= IA PARA HOTELES
def ia_hoteles(R):
    preg = ["Horarios", "Disponibilidad de habitaciones", "Servicios del hotel", "Restaurante", "Parking", "Mascotas", "Check-in y check-out", "Cómo llegar", "Cancelaciones", "Consultas en otros idiomas", "Llamadas fuera de horario", "Llamadas repetidas a la misma hora"]
    estudia = ["Cómo funciona el establecimiento", "Horarios de cada servicio", "Departamentos y responsables", "Las preguntas que más se repiten", "Protocolos de recepción", "Idiomas que necesita atender", "Servicios e instalaciones", "Circunstancias particulares de la casa"]
    cap = [("Atender llamadas telefónicas", "Descuelga cuando recepción está ocupada o cerrada, y mantiene una conversación real en lugar de leer un menú de opciones."),
           ("Responder preguntas frecuentes", "Horarios, servicios, instalaciones, políticas y entorno, con la información concreta de su establecimiento y no con generalidades del sector."),
           ("Atender en varios idiomas", "La misma conversación, con el mismo criterio, en el idioma en el que llama el cliente."),
           ("Transferir al departamento adecuado", "Reconoce cuándo la gestión exige una persona y pasa la llamada a quien corresponde, con el contexto ya recogido."),
           ("Cubrir el fuera de horario", "La consulta de las 23:40 deja de ser una habitación vacía al día siguiente."),
           ("Integrarse con sus sistemas", "Consulta de fuentes autorizadas para responder con datos actualizados, según la API disponible y los permisos concedidos."),
           ("Automatizar por WhatsApp o email", "Confirmaciones, avisos y seguimientos por los canales que su cliente ya utiliza."),
           ("Adaptarse a sus protocolos", "Qué puede resolver, qué debe consultar y en qué momento exacto deja de hablar. Definido con usted, no por defecto.")]
    mk = [("Imagen audiovisual premium", "Rodamos con dron, cámaras y el equipo necesario. Un hotel se vende por cómo se ve antes de que nadie pise la recepción."),
          ("Email marketing", "La base de huéspedes que ya tiene es su canal más barato. Recuperar una reserva directa cuesta menos que captar una nueva."),
          ("Redes sociales", "Línea editorial propia y contenido que el huésped comparte, que es la mejor recomendación que existe."),
          ("Otros canales de venta", "Trabajamos la reserva directa frente a la comisión del canal, y la presencia donde su cliente decide.")]
    pasos6 = [("Analizamos el establecimiento", "Cómo trabaja hoy su recepción, qué entra por teléfono y qué se queda sin responder."), ("Detectamos qué automatizar", "No todo merece automatizarse. Separamos lo repetitivo de lo que exige criterio humano."), ("Diseñamos el agente", "Conocimiento del hotel, canales, idiomas, permisos y punto de transferencia a recepción."), ("Integramos y probamos", "Conexión con las fuentes autorizadas y pruebas antes de que ningún cliente hable con el sistema."), ("Puesta en funcionamiento", "Arranque acompañado, con su equipo sabiendo qué hace el agente y cómo intervenir."), ("Optimización", "Revisión de conversaciones reales para corregir lo que no responde como debería.")]
    hab = ["Menos de 20 habitaciones", "Entre 20 y 50", "Entre 50 y 100", "Entre 100 y 200", "Más de 200", "Varios establecimientos"]
    opt = "".join(f"<option>{e(x)}</option>" for x in hab)
    form = f'''<form class="form" data-mail="Estudio de hotel" novalidate>
<div class="campo-duo"><div class="campo"><label for="h-nome">Nombre</label><input id="h-nome" name="nombre" autocomplete="name" data-campo="Nombre" data-req="Indique su nombre."><span class="erro" id="h-nome-erro"></span></div>
<div class="campo"><label for="h-emp">Hotel o empresa</label><input id="h-emp" name="empresa" autocomplete="organization" data-campo="Hotel o empresa" data-req="Indique el nombre del hotel."><span class="erro" id="h-emp-erro"></span></div></div>
<div class="campo-duo"><div class="campo"><label for="h-tel">Teléfono</label><input id="h-tel" name="telefono" type="tel" autocomplete="tel" data-campo="Teléfono"></div>
<div class="campo"><label for="h-mail">Email</label><input id="h-mail" name="email" type="email" autocomplete="email" data-campo="Email" data-req="Indique su email."><span class="erro" id="h-mail-erro"></span></div></div>
<div class="campo"><label for="h-hab">Número aproximado de habitaciones</label><select id="h-hab" name="habitaciones" data-campo="Habitaciones">{opt}</select></div>
<div class="campo"><label for="h-msg">¿Qué le gustaría mejorar o automatizar? <small>(opcional)</small></label><textarea id="h-msg" name="mensaje" data-campo="Mejorar o automatizar"></textarea></div>
<input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
<div class="acoes"><button class="btn btn-claro" type="submit">Quiero estudiar mi caso <span class="fl">→</span></button></div>
<p class="form-nota">Al enviar se abre su correo con el mensaje ya escrito para {EMAIL}. Respuesta personal en un día laborable.</p>
</form><div class="form-ok" data-ok hidden><b>Su correo ya tiene el mensaje preparado.</b><p class="texto">Si no se ha abierto, escríbanos a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    return (ph(R, "Agentes de IA para hoteles", L("Su hotel puede atender llamadas", "24 horas al día, en cualquier idioma,", "<em>sin ampliar recepción.</em>"), "Diseñamos agentes de inteligencia artificial alrededor de la operativa real de su establecimiento: qué debe responder, qué debe consultar y en qué momento exacto avisa a una persona.",
               btn("#estudio", "Estudiar mi hotel") + btn("#como", "Ver cómo funciona", "btn-linha", False), img(R, "ia-hotel-atencion-atardecer-vertical", "Recepción de un hotel al atardecer, con una huésped atendida en el mostrador", "(min-width: 900px) 40vw, 100vw", lazy=False), ["Estudiamos cada establecimiento antes de proponer nada", "Sin compromiso"])
            + sec(cab("01", "El día a día de recepción", "El teléfono no suena <em>cuando recepción está libre.</em>", "Suena mientras hay un huésped delante del mostrador, mientras se prepara una salida o a las once y media de la noche. Y casi siempre para preguntar algo que ya se ha preguntado hoy.")
                  + f'<div class="grelha"><div style="grid-column:1/7" class="prosa" data-sube><p>Cada interrupción tiene un coste doble: la consulta que se atiende deprisa y el huésped que se atiende peor. La suma de las dos cosas no aparece en ningún informe, pero se nota en la reseña del lunes y en la reserva que se fue al canal.</p><h3>Esto no va de sustituir a su equipo</h3><p>Un agente de IA no hace el trabajo de su recepción: le quita de encima el que no requiere su criterio. Lo repetitivo deja de interrumpir, y las personas se concentran en lo que de verdad necesita una persona: el huésped delante, la incidencia, la venta que se cierra hablando.</p></div><div style="grid-column:8/13" data-sube>{chips(preg)}</div></div>', extra=' id="como"')
            + sec(cab("02", "Solución personalizada", "IA a medida <em>de su hotel.</em>", "No instalamos un agente estándar ni un chatbot con el logotipo cambiado. Antes de escribir una sola respuesta, estudiamos cómo funciona su casa.")
                  + f'<div class="duo-foto">{figura(R, "ia-hotel-estudio-establecimiento", "Mesa de trabajo con planos del establecimiento y una vista del hotel desplegada sobre una tableta", "", "Después diseñamos el agente alrededor del establecimiento. Nunca al revés.", "foto")}<div data-sube><p class="texto" style="margin-bottom:1.4rem">Un hotel de montaña con media pensión y un urbano de paso no tienen el mismo problema, ni las mismas preguntas, ni el mismo punto en el que conviene pasar la llamada a una persona.</p>{chips(estudia)}</div></div>')
            + sec(cab("03", "Qué puede hacer", "Lo que puede llegar a resolver, <em>según el proyecto.</em>", "Estas son las capacidades del sistema. Cuáles se activan en su hotel se decide después del estudio.") + cards(cap) + '<p class="nota" style="margin-top:2rem">Las funciones disponibles dependen del proyecto, de los sistemas del establecimiento, de las APIs disponibles y de los permisos concedidos. El alcance se cierra por escrito después del estudio y antes de empezar.</p>')
            + sec(cab("04", "Caso real", "Hotel Boltaña <em>Ordesa.</em>") + f'<article class="caso" data-sube><div class="caso-cab"><div class="ventana" style="aspect-ratio:4/3">{img(R, "hotel-boltana", "Fachada y terraza exterior de un hotel de montaña rodeado de arbolado", "(min-width: 900px) 36vw, 100vw")}</div><p class="etiqueta">Hoteles</p><h3>Un agente diseñado alrededor de la operativa real de un hotel</h3></div><dl><dt>Contexto</dt><dd>Un establecimiento con consultas que entran a cualquier hora, en varios idiomas y por varios canales, y una recepción que no puede estar en todo sin dejar de atender bien a quien ya está alojado.</dd><dt>Decisión</dt><dd>Diseñar un agente alrededor de la operativa concreta del hotel en lugar de instalar un chatbot genérico.</dd><dt>Implementación</dt><dd>Construcción del conocimiento del establecimiento, conexión a fuentes de información para responder con datos actualizados, permisos de solo lectura y diseño del punto de transferencia a recepción.</dd><dt>Resultado</dt><dd>Un canal de atención disponible de forma continuada, capaz de responder en más de veinte idiomas y de derivar a recepción cuando la gestión lo requiere.</dd><div class="evid">Demostración en preparación<small>Estamos registrando una grabación de una conversación real del agente. Hasta entonces no publicamos cifras de resultado: preferimos enseñarlo a contarlo.</small></div></dl></article>')
            + sec(cab("05", "La otra mitad", "El agente atiende. <em>El marketing llena.</em>", "Un agente que responde bien no sirve de nada si no entra nadie. Somos una agencia de marketing antes que nada: la inteligencia artificial es lo que añadimos cuando la atención se convierte en el cuello de botella.") + cards(mk))
            + sec(cab("06", "Cómo trabajamos", "Seis pasos. <em>El primero no es instalar nada.</em>", "El orden importa: saltarse el análisis es la forma más cara de automatizar lo que no había que automatizar.") + passos(pasos6))
            + sec(cab("07", "No solo hoteles", "Si su empresa recibe consultas, <em>esto le sirve igual.</em>", "Un concesionario con pruebas de vehículo que coordinar, una joyería que atiende encargos, una empresa náutica con reservas por temporada: cambian las preguntas y los sistemas a conectar; no cambia el método.") + f'<p>{enlace(R + "inteligencia-artificial/", "Ver cómo trabajamos en cualquier sector")}</p>')
            + sec(f'<div class="vias"><div class="cab" style="margin:0">{etq("08", "Solicitar estudio", "n")}<h2 class="titulo t-l" data-linhas>Cuéntenos <em>cómo es su caso.</em></h2><p class="lead" data-sube>Con estos datos ya podemos hacernos una idea de qué procesos tendría sentido automatizar y qué conviene trabajar antes.</p></div><div class="via">{form}</div></div>', extra=' id="estudio"')
            + banda("No necesita adaptar su hotel a la tecnología. <em>Diseñamos la tecnología alrededor de su hotel.</em>", "Estudiamos cada establecimiento antes de proponer nada. Sin compromiso.", btn("#estudio", "Estudiar mi hotel")))


pagina("ia-hoteles/", "Agentes de IA para hoteles", "Agentes de IA y marketing para hoteles: atención 24 horas en cualquier idioma, imagen audiovisual premium, email marketing y redes.", ia_hoteles)


# ================================================================= CONTACTO
def contacto(R):
    sectores = ["Hotelería", "Automoción", "Náutica", "Joyería", "Otro"]
    plazos = ["Inmediato", "En 30–90 días", "El próximo trimestre", "Solo estoy explorando"]
    rad = lambda nome, campo, l, pre: "".join(f'<label><input type="radio" name="{nome}" value="{e(x)}" data-campo="{campo}"{se(x == pre, " checked")}><span>{e(x)}</span></label>' for x in l)
    form = f'''<form class="form" data-mail="Solicitud desde la web" novalidate>
<div class="campo-duo"><div class="campo"><label for="c-nome">Nombre</label><input id="c-nome" name="nombre" autocomplete="name" data-campo="Nombre" data-req="Indique su nombre."><span class="erro" id="c-nome-erro"></span></div>
<div class="campo"><label for="c-emp">Empresa</label><input id="c-emp" name="empresa" autocomplete="organization" data-campo="Empresa" data-req="Indique el nombre de su empresa."><span class="erro" id="c-emp-erro"></span></div></div>
<div class="campo-duo"><div class="campo"><label for="c-mail">Email</label><input id="c-mail" name="email" type="email" autocomplete="email" data-campo="Email" data-req="Indique su email."><span class="erro" id="c-mail-erro"></span></div>
<div class="campo"><label for="c-tel">Teléfono <small>(opcional)</small></label><input id="c-tel" name="telefono" type="tel" autocomplete="tel" data-campo="Teléfono"></div></div>
<fieldset class="campo" style="border:0;padding:0;margin:0"><legend>Sector</legend><div class="radios">{rad("sector", "Sector", sectores, "")}</div></fieldset>
<fieldset class="campo" style="border:0;padding:0;margin:0"><legend>Plazo</legend><div class="radios">{rad("plazo", "Plazo", plazos, "")}</div></fieldset>
<div class="campo"><label for="c-msg">Objetivo o resumen</label><textarea id="c-msg" name="mensaje" data-campo="Objetivo" data-req="Cuéntenos en dos o tres líneas qué quiere conseguir." placeholder="Dos o tres líneas bastan. Qué quiere conseguir y qué le está frenando."></textarea><span class="erro" id="c-msg-erro"></span></div>
<fieldset class="campo" style="border:0;padding:0;margin:0"><legend>Contacto preferido</legend><div class="radios">{rad("pref", "Contacto preferido", ["Email", "Teléfono", "WhatsApp"], "Email")}</div></fieldset>
<div class="campo"><label for="c-cargo">Cargo <small>(opcional)</small></label><input id="c-cargo" name="cargo" autocomplete="organization-title" data-campo="Cargo"></div>
<input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
<div class="acoes"><button class="btn btn-claro" type="submit">Enviar solicitud <span class="fl">→</span></button></div>
<p class="form-nota">Al enviar se abre su correo con la solicitud ya escrita para {EMAIL}. Respuesta personal en un día laborable. Sus datos no se comparten.</p>
</form><div class="form-ok" data-ok hidden><b>Su correo ya tiene la solicitud preparada.</b><p class="texto">Si no se ha abierto, escríbanos a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    pasos3 = [("Leemos su caso", "Una persona del equipo revisa lo que nos cuenta y mira su empresa por fuera antes de responder. No hay respuesta automática."), ("Le respondemos en un día laborable", "Con una primera lectura de lo que haríamos y por dónde empezaríamos, por el canal que nos haya indicado."), ("Asesoría privada", "Media hora para contrastar el diagnóstico. El presupuesto llega después de esa conversación, ajustado a su caso.")]
    return (ph(R, "Contacto", L("Dos formas de empezar.", "<em>Elija la que le ahorre tiempo.</em>"), "Si todavía no sabe qué necesita, el diagnóstico lo resuelve en dos minutos. Si ya lo tiene claro, escriba directamente y le respondemos.")
            + sec(f'<div class="vias"><div class="via" data-sube><p class="etiqueta"><span class="n">A</span>No sé qué necesito</p><h2>El diagnóstico de dos minutos</h2><p class="texto">Ocho preguntas y una recomendación con punto de partida y primeras acciones. Sin compromiso.</p><div class="acoes">{btn(R + DIAG, "Pide su diagnóstico")}</div><p class="nota">Trato directo: habla con quien va a dirigir su proyecto. Trabajamos con pocas empresas a la vez.</p><address class="nota" style="font-style:normal;margin-top:1rem">IA &amp; Marketing Ferreras<br>Passeig de Gràcia 95, 5º 1ª · 08008 Barcelona<br><a class="enlace" href="mailto:{EMAIL}">{EMAIL}</a></address></div><div class="via" data-sube style="--i:1"><p class="etiqueta"><span class="n">B</span>Ya sé qué necesito</p><h2>Escríbanos</h2>{form}</div></div>')
            + sec(cab("01", "Qué pasa después", "Tres pasos, y ninguno <em>le compromete a nada.</em>") + passos(pasos3))
            + sec(cab("02", "Dónde tenemos más recorrido", "Cuatro sectores que conocemos <em>por dentro.</em>", "Hotelería, automoción, náutica y joyería. Fotografía de trabajos propios.") + sect_html(R, True)))


pagina("contacto/", "Contacto", "Dos vías: si ya sabe lo que necesita, un formulario corto. Si no lo tiene claro, un diagnóstico de dos minutos.", contacto)


# ================================================================= DIAGNÓSTICO
def diagnostico(R):
    form = f'''<form class="form" novalidate>
<div class="campo-duo"><div class="campo"><label for="d-nome">Nombre</label><input id="d-nome" name="nombre" autocomplete="name" data-req="Indique su nombre."><span class="erro" id="d-nome-erro"></span></div>
<div class="campo"><label for="d-emp">Empresa</label><input id="d-emp" name="empresa" autocomplete="organization" data-req="Indique el nombre de su empresa."><span class="erro" id="d-emp-erro"></span></div></div>
<div class="campo-duo"><div class="campo"><label for="d-mail">Email</label><input id="d-mail" name="email" type="email" autocomplete="email" data-req="Revise la dirección de email."><span class="erro" id="d-mail-erro"></span></div>
<div class="campo"><label for="d-tel">Teléfono <small>(opcional)</small></label><input id="d-tel" name="telefono" type="tel" autocomplete="tel"></div></div>
<div class="acoes"><button class="btn btn-claro" type="submit">Enviar a Ferreras <span class="fl">→</span></button></div>
<p class="form-nota">Se abre su correo con sus respuestas y la recomendación ya escritas para {EMAIL}. El presupuesto llega después de la asesoría privada.</p>
</form><div class="form-ok" data-ok hidden><b>Su correo ya tiene el diagnóstico preparado.</b><p class="texto">Si no se ha abierto, escríbanos a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    reco = f'''<div class="reco" data-reco hidden>
<p class="etiqueta"><span class="n">✓</span>Su recomendación</p>
<h2 class="titulo t-l" tabindex="-1" data-r="prioridad"></h2>
<p class="lead" data-r="porque"></p>
<div class="reco-grid"><div><span class="etiqueta">Punto de partida</span><b data-r="plano"></b><p class="texto"><a class="enlace" data-r="ruta-a" href="#"><span data-r="ruta"></span> <span class="fl">→</span></a></p></div><div><span class="etiqueta">Su presupuesto</span><b>Tras la asesoría</b><p class="texto">No trabajamos con tarifas cerradas. Tras una asesoría privada en la que entendamos su caso, le entregamos un presupuesto ajustado a lo que de verdad necesita.</p></div></div>
<div><h3 class="titulo t-s" style="margin-bottom:1.2rem">Sus tres primeras acciones</h3><ol data-r="acoes"></ol></div>
<div class="deps" data-r="deps"></div>
<p class="texto"><b>Siguiente paso:</b> <span data-r="prox"></span></p>
<div class="via">{form}</div>
<p><button type="button" class="enlace" data-recomeca><span class="fl">↺</span> Empezar de nuevo</button></p>
</div>'''
    return (ph(R, "Diagnóstico comercial", L("Ocho preguntas.", "Dos minutos.", "<em>Una recomendación concreta.</em>"), "No hay puntuaciones a la vista, ni descartes, ni presión. Al terminar sabrá qué priorizar, por dónde empezar y cuáles serían sus tres primeras acciones.", chips_=["Analizamos su marca", "Y cómo atiende hoy", "Propuesta a medida", "Sin compromiso"])
            + sec(f'<div class="diag" data-diag><div class="diag-lado"><div class="diag-prog" data-diag-prog aria-hidden="true"></div><div class="diag-placa" data-diag-placa aria-label="Sus respuestas"></div><p class="mini">Guardamos temporalmente sus respuestas en este navegador para que pueda retomar el diagnóstico. Los datos de contacto no se guardan y solo se envían cuando usted lo decide.</p></div><div><div class="diag-paso" data-diag-paso aria-live="polite"></div>{reco}</div></div>'))


pagina("diagnostico/", "Diagnóstico de 2 minutos", "Ocho preguntas, dos minutos y una recomendación concreta: qué priorizar, por dónde empezar y cuáles son sus tres primeras acciones. Sin precios y sin compromiso.", diagnostico)


# ================================================================= LEGAL (texto do site antigo)
CRAWL = Path(r"C:\Users\David\AppData\Local\Temp\claude\C--Users-David\680f0cb1-e6c4-42a0-8a28-f96d0df16250\scratchpad\ferreras\crawl\content.md")
LEGAL_TXT = (RAIZ / "_fonte" / "legal.json")


def legal_textos():
    if LEGAL_TXT.exists():
        return json.loads(LEGAL_TXT.read_text(encoding="utf-8"))
    s = CRAWL.read_text(encoding="utf-8")
    out = {}
    for slug in ("aviso-legal", "privacidad", "cookies"):
        bloco = s.split(f"========== https://www.marketingferreras.com/legal/{slug}")[1].split("==========")[0]
        linhas = bloco.split("\n")
        ini = next(i for i, l in enumerate(linhas) if l.startswith("[h1]"))
        fim = next(i for i, l in enumerate(linhas) if l.startswith("Tu departamento de marketing e IA. Estrategia"))
        out[slug] = linhas[ini:fim]
    LEGAL_TXT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def legal_pagina(slug, titulo):
    ls = legal_textos()[slug]

    def corpo(R):
        h1 = ls[0][4:].strip()
        partes = []
        for l in ls[1:]:
            if l.startswith("[h2]"):
                partes.append(f"<h2>{e(l[4:].strip())}</h2>")
            elif l.startswith("[h3]"):
                partes.append(f"<h3>{e(l[4:].strip())}</h3>")
            elif l.strip():
                t = e(l.strip()).replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
                partes.append(f"<p>{t}</p>")
        return (f'<section class="pag-hero" style="min-height:auto"><div class="ph-txt"><p class="migas"><a href="{R}">Inicio</a> <span aria-hidden="true">/</span> Legal</p><h1 class="titulo t-l">{e(h1)}</h1></div></section>'
                + sec(f'<div class="prosa">{"".join(partes)}</div>'))
    pagina(f"legal/{slug}/", titulo, f"{titulo} de IA & Marketing Ferreras.", corpo)


legal_pagina("aviso-legal", "Aviso legal")
legal_pagina("privacidad", "Política de privacidad")
legal_pagina("cookies", "Política de cookies")


# ================================================================= 404, robots, sitemap
def p404(R):
    return ph(R, "Error 404", L("Esta hora no existe", "<em>en nuestro reloj.</em>"), "La página que busca se ha movido o nunca existió.", btn(R or "./", "Volver al inicio") + btn(R + DIAG, "Pide su diagnóstico", "btn-linha"))


pagina("404/", "Página no encontrada", "La página que busca no existe.", p404)
# GitHub Pages sirve /404.html: con rutas absolutas desde la raíz del proyecto
(RAIZ / "404.html").write_text((RAIZ / "404" / "index.html").read_text(encoding="utf-8").replace('"../', '"/ferreras/'), encoding="utf-8")
(RAIZ / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
(RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{URL}{r}</loc></url>\n" for r in FEITAS if r != "404/") + "</urlset>\n", encoding="utf-8")
(RAIZ / ".nojekyll").write_text("", encoding="utf-8")
(RAIZ / "favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -30 315 316"><rect x="-40" y="-30" width="315" height="316" rx="60" fill="#00101f"/>{marca_paths()}</svg>', encoding="utf-8")
print(len(FEITAS), "páginas:", ", ".join(r or "/" for r in FEITAS))
