(() => {
  const { $, $$, reduz } = SITE;
  const EMAIL = 'administracion@marketingferreras.com';

  /* ---------- «qué incluye»: la línea activa (ratón encima o, sin ratón, la que cruza el centro de la pantalla)
     enciende su imagen o su vídeo en la ventana de al lado; sólo el vídeo activo descarga y toca ---------- */
  $$('[data-indice]').forEach((ind) => {
    const ixs = $$('[data-ix]', ind), ivs = $$('[data-iv]', ind);
    let k = 0, dentro = false;
    const liga = (n) => {
      k = n;
      ixs.forEach((x, i) => x.classList.toggle('on', i === n));
      ivs.forEach((x, i) => {
        x.classList.toggle('on', i === n);
        const v = $('video', x); if (!v) return;
        if (i === n && dentro && !reduz) { if (!v.src) v.src = v.dataset.src; v.muted = true; v.playsInline = true; const p = v.play(); p && p.catch && p.catch(() => {}); }
        else if (!v.paused) v.pause();
      });
    };
    const fino = matchMedia('(hover:hover) and (pointer:fine)').matches;
    ixs.forEach((x, i) => { x.addEventListener('pointerenter', () => fino && liga(i)); x.addEventListener('focusin', () => liga(i)); });
    new IntersectionObserver(([e]) => { dentro = e.isIntersecting; liga(k); }, { threshold: 0.15 }).observe(ind);
    if (!fino) {
      const io = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && liga(ixs.indexOf(e.target))), { rootMargin: '-45% 0px -45% 0px' });
      ixs.forEach((x) => io.observe(x));
    }
  });

  /* ---------- SECTORES, el palco: el scroll cambia de sector dentro de una escena fija (computador);
     el índice de la izquierda lleva la barra del sector activo y salta a cualquiera ---------- */
  $$('[data-palco]').forEach((pc) => {
    const ms = $$('[data-pl-m]', pc), ts = $$('[data-pl-t]', pc), is = $$('[data-pl-i]', pc), ws = $$('[data-pl-w]', pc), N = ms.length;
    const fixo = matchMedia('(min-width: 901px)');
    let k = 0, pAnt = '';
    const liga = (n) => { if (n === k) return; k = n; [ms, ts, is, ws].forEach((l) => l.forEach((x, j) => x.classList.toggle('on', j === n))); };
    SITE.aCada(() => {
      if (!fixo.matches) return;
      const p = SITE.fixado(pc) * N, n = Math.min(N - 1, Math.floor(p));
      liga(n);
      const f = Math.min(1, p - n).toFixed(3);
      if (f !== pAnt) { pAnt = f; pc.style.setProperty('--p', f); }
    });
    is.forEach((li, j) => $('button', li).addEventListener('click', () => {
      const c = SITE.caixa(pc);
      scrollTo({ top: c.top + (c.height - innerHeight) * (j + 0.15) / N, behavior: reduz ? 'auto' : 'smooth' });
    }));
  });

  /* ---------- resultados: filtrar por sector o por problema ---------- */
  const fbox = $('[data-filtros]');
  if (fbox) {
    const casos = $$('[data-caso]'), conteo = $('[data-conteo]');
    const estado = { sector: 'todos', problema: 'todos' };
    $$('button[data-f]', fbox).forEach((b) => b.addEventListener('click', () => {
      const tipo = b.dataset.f;
      estado[tipo] = b.dataset.v;
      $$(`button[data-f="${tipo}"]`, fbox).forEach((o) => o.setAttribute('aria-pressed', o === b));
      let n = 0;
      casos.forEach((c) => {
        const ok = (estado.sector === 'todos' || c.dataset.sector === estado.sector) && (estado.problema === 'todos' || c.dataset.problema.split(' ').includes(estado.problema));
        c.hidden = !ok; if (ok) n++;
      });
      conteo.textContent = n === 1 ? '1 caso' : n + ' casos';
      SITE.remede();
    }));
  }

  /* ---------- FORMULARIOS: los mismos campos, reglas y destino que la web original (POST a /api/leads de
     marketingferreras.com, mismo formato). Desde otro dominio la respuesta no se puede leer (no-cors): se valida aquí
     con las reglas del servidor y, si la red falla, queda el correo ya escrito como salida. ---------- */
  const API = 'https://www.marketingferreras.com/api/leads';
  const UTM = (() => {
    const q = new URLSearchParams(location.search), o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach((k) => { const v = q.get(k); if (v) o[k] = v.replace(/[^\w\-. ]/g, '').slice(0, 64); });
    return o;
  })();
  const envia = (dados) => fetch(API, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(dados), keepalive: true });
  const valida = (form) => {
    let primeiro = null;
    const pref = $('[name="preferencia"]:checked', form);
    $$('[data-req],[name="telefono"]', form).forEach((el) => {
      const v = el.type === 'checkbox' ? el.checked : el.value.trim();
      let msg = '';
      if (el.name === 'telefono') {
        const precisa = el.dataset.req || (pref && pref.value !== 'email');
        if (precisa && !v) msg = el.dataset.req || 'Si prefiere que le llamemos, necesitamos un teléfono.';
        else if (v && el.dataset.minDig && v.replace(/\D/g, '').length < +el.dataset.minDig) msg = el.dataset.req;
      } else if (!v) msg = el.dataset.req;
      else if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v)) msg = el.dataset.req;
      else if (el.dataset.min && v.length < +el.dataset.min) msg = el.dataset.req;
      else if (/^(nombre|empresa|hotel)$/.test(el.name) && v.length < 2) msg = el.dataset.req;
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      const e = el.id && $('#' + el.id + '-erro'); if (e) e.textContent = msg;
      if (msg && !primeiro) primeiro = el;
    });
    if (primeiro) primeiro.focus();
    return !primeiro;
  };
  const val = (f, n) => {
    const el = $(`[name="${n}"]`, f); if (!el) return '';
    if (el.type === 'radio') { const c = $(`[name="${n}"]:checked`, f); return c ? c.value : ''; }
    return el.type === 'checkbox' ? el.checked : el.value.trim();
  };
  const contato = (f, emp = 'empresa') => ({ nombre: val(f, 'nombre'), empresa: val(f, emp), email: val(f, 'email'), telefono: val(f, 'telefono'), cargo: val(f, 'cargo') || '', preferencia: val(f, 'preferencia') || 'email', consentimiento: !!val(f, 'consentimiento') });
  const estado = (box, k) => box && $$('[data-e]', box).forEach((x) => (x.hidden = x.dataset.e !== k));
  const mailto = (assunto, linhas) => `mailto:${EMAIL}?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(linhas.join('\n'))}`;
  const resumo = (d) => [`Nombre: ${d.contact.nombre}`, `Empresa: ${d.contact.empresa}`, `Email: ${d.contact.email}`, d.contact.telefono && `Teléfono: ${d.contact.telefono}`, ...Object.values(d.short || {})].filter(Boolean);
  // envía y pinta el estado; devuelve true si salió (con no-cors, «salió» es lo máximo que el navegador nos deja saber)
  const despacha = async (d, box, assunto, linhas) => {
    if (d.website) { estado(box, 'ok'); return true; } // campo trampa relleno: se finge el envío
    estado(box, 'a');
    try { await envia(d); estado(box, 'ok'); return true; }
    catch (e) { estado(box, 'ko'); const m = box && $('[data-mailto]', box); if (m) m.href = mailto(assunto, linhas); return false; }
  };
  const PAYLOAD = {
    contacto: (f) => ({ kind: 'contacto', submissionId: 'ctc_' + Date.now(), contact: contato(f), short: { servicio: 'Sector: ' + val(f, 'sector'), objetivo: val(f, 'objetivo'), plazo: val(f, 'plazo') }, website: val(f, 'website'), meta: { path: '/contacto', utm: UTM } }),
    hotel: (f) => ({ kind: 'contacto', submissionId: 'hot_' + Date.now(), contact: { ...contato(f, 'hotel'), cargo: '', preferencia: 'telefono' },
      short: { servicio: 'Agentes IA para hoteles', objetivo: ['Habitaciones: ' + val(f, 'habitaciones'), val(f, 'mejora') ? 'Qué quiere mejorar o automatizar: ' + val(f, 'mejora') : null].filter(Boolean).join('\n\n'), plazo: 'Solicitud de estudio (campaña hoteles)' },
      website: val(f, 'website'), meta: { path: '/ia-hoteles', utm: UTM } }),
  };
  $$('form[data-lead]').forEach((f) => {
    const box = $('[data-envio]', f), b = $('button[type="submit"]', f);
    f.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      if (!valida(f)) return;
      const d = PAYLOAD[f.dataset.lead](f);
      b.disabled = true;
      const ok = await despacha(d, box, 'Solicitud desde la web', resumo(d));
      if (ok) { b.hidden = true; $$('input,textarea', f).forEach((x) => (x.disabled = true)); f.classList.add('enviado'); } else b.disabled = false;
      SITE.remede();
    });
  });

  /* ---------- DIAGNÓSTICO: ocho preguntas, la placa registra cada respuesta y la recomendación sale en el acto ---------- */
  const dg = $('[data-diag]');
  if (!dg) return;
  const P = [
    { id: 'sector', q: '¿En qué sector opera su empresa?', a: 'Nos permite comparar su situación con trabajos equivalentes.', o: [['hoteles', 'Hotel o alojamiento'], ['joyeria-relojeria', 'Joyería o relojería'], ['automocion-lujo', 'Automoción'], ['nautica', 'Náutica, yates o puertos'], ['inmobiliaria-premium', 'Inmobiliaria premium'], ['b2b', 'Servicios profesionales o B2B'], ['otro', 'Otro sector']] },
    { id: 'objetivo', q: '¿Cuál es su objetivo principal ahora mismo?', a: 'Si todavía no lo tiene claro, puede decirlo: es una respuesta habitual y útil.', o: [['autoridad', 'Autoridad y marca'], ['leads', 'Leads y ventas'], ['web', 'Nueva web o ecommerce'], ['atencion', 'Atención 24/7'], ['tramites', 'Trámites comerciales'], ['eficiencia', 'Eficiencia interna'], ['no-lo-se', 'No lo sé todavía']] },
    { id: 'friccion', q: '¿Cuál es hoy su mayor fricción?', a: 'Lo que más le está costando dinero o tiempo, aunque no sea lo más urgente.', o: [['perdemos-consultas', 'Perdemos consultas por lentitud, horario o idioma'], ['saturacion', 'El equipo está saturado de tareas repetitivas'], ['trafico-no-convierte', 'Entra tráfico en la web y no convierte'], ['percepcion', 'La imagen no refleja el nivel real del negocio'], ['proceso-manual', 'Un proceso crítico sigue siendo manual'], ['inconsistencia', 'Comunicamos a rachas, sin constancia'], ['explorando', 'Estamos explorando opciones']] },
    { id: 'activos', q: '¿Con qué cuenta ya?', a: 'Puede marcar varias. Reutilizamos todo lo que sea aprovechable.', multi: true, o: [['web', 'Web propia'], ['redes', 'Redes sociales activas'], ['crm', 'CRM'], ['equipo', 'Equipo de marketing o comercial'], ['contenido', 'Contenido audiovisual propio'], ['reservas', 'Herramienta de reservas o gestión'], ['ninguno', 'Prácticamente ninguno']] },
    { id: 'volumen', q: '¿Qué volumen de consultas u operaciones maneja?', a: 'Una estimación es suficiente.', o: [['bajo', 'Menos de 100 al mes'], ['medio', 'Entre 100 y 500 al mes'], ['alto', 'Entre 500 y 2.000 al mes'], ['muy-alto', 'Más de 2.000 al mes'], ['no-lo-se', 'No lo sé']] },
    { id: 'plazo', q: '¿En qué plazo querría empezar?', a: 'Nos ayuda a saber si conviene una llamada esta semana o dentro de un tiempo.', o: [['inmediato', 'Inmediato'], ['30-90', 'En 30–90 días'], ['trimestre', 'El próximo trimestre'], ['exploracion', 'Solo estoy explorando']] },
    { id: 'inversion', q: '¿Qué inversión orientativa contempla?', a: 'Orientativa. Sirve para no proponerle algo que no encaja con su momento.', o: [['menos-1000', 'Menos de 1.000 €/mes'], ['1000-2000', '1.000–2.000 €/mes'], ['2000-4000', '2.000–4.000 €/mes'], ['4000-mas', 'Más de 4.000 €/mes'], ['proyecto-4-8', 'Proyecto de 4.000–8.000 €'], ['proyecto-8-15', 'Proyecto de 8.000–15.000 €'], ['proyecto-15-mas', 'Proyecto de más de 15.000 €'], ['no-lo-se', 'No lo sé']] },
    { id: 'rol', q: '¿Cuál es su papel en la decisión?', a: 'Para preparar la conversación con la información adecuada.', o: [['propiedad', 'Propiedad, CEO o dirección general'], ['direccion', 'Dirección comercial, marketing u operaciones'], ['responsable', 'Responsable con capacidad de influencia'], ['investigacion', 'Investigación o proveedor externo']] },
  ];
  const ROT = { sector: 'Sector', objetivo: 'Objetivo', friccion: 'Fricción', activos: 'Activos', volumen: 'Volumen', plazo: 'Plazo', inversion: 'Inversión', rol: 'Su papel' };
  const RUTA = { marketing: ['Marketing estratégico', 'marketing/'], web: ['Web y ecommerce', 'web/'], ia: ['Agentes IA y automatización', 'inteligencia-artificial/'], integrado: ['Sistema integrado', 'contacto/'] };
  const PLANO = { marketing: ['Base de Autoridad', 'Autoridad & Demanda', 'Liderazgo de Mercado'], web: ['Web Signature', 'Web de Captación', 'Ecommerce o Digital Flagship'], ia: ['Asistente IA 24/7', 'Agente IA Operativo', 'Sistema Multiagente'], integrado: ['Web Signature + Base de Autoridad', 'Web de Captación + Autoridad & Demanda', 'Web de Captación + Autoridad & Demanda + Agente IA Operativo'] };
  const PORQUE = {
    marketing: ['Construir autoridad antes que volumen', 'Su prioridad no es publicar más: es que lo que publique cambie cómo le perciben y produzca conversaciones comerciales.'],
    web: ['Convertir la atención que ya genera', 'Ya llega gente. El problema está en que la web informa pero no guía, no demuestra y no cualifica.'],
    ia: ['Dejar de perder lo que ya entra', 'El coste mayor hoy no está en captar más, sino en las consultas que se enfrían y en las horas que consume lo repetitivo.'],
    integrado: ['Conectar percepción, captación y atención', 'Las fricciones que ha señalado no son independientes: resolver solo una dejaría el cuello de botella intacto en la siguiente.'],
  };
  const ACOES = {
    marketing: ['Definir la línea editorial y los dos formatos que van a construir autoridad en su sector.', 'Planificar la primera sesión de producción con el material que ya existe en la empresa.', 'Fijar el punto de partida y los indicadores que se revisarán cada mes.'],
    web: ['Auditar la ruta actual del visitante y localizar exactamente dónde abandona.', 'Reescribir el mensaje y ordenar la evidencia que hoy vive fuera de la web.', 'Implantar la cualificación y la medición de oportunidades reales.'],
    ia: ['Mapear qué consultas y tareas se repiten, en qué canal y en qué franja horaria.', 'Definir el alcance del agente: qué responde, qué consulta y qué requiere una persona.', 'Implantar en entorno de pruebas con permisos mínimos antes de abrir el canal.'],
    integrado: ['Diagnóstico conjunto de percepción, captación y atención para ordenar prioridades.', 'Construir primero la pieza que desbloquea a las demás, normalmente la web o la atención.', 'Conectar el seguimiento para que ninguna oportunidad se quede sin respuesta.'],
  };
  // la misma lógica de la web original
  const recomenda = (r) => {
    const a = r.activos || [];
    const mk = r.objetivo === 'autoridad' || r.friccion === 'percepcion' || r.friccion === 'inconsistencia';
    const wb = r.objetivo === 'web' || r.friccion === 'trafico-no-convierte';
    const ia = ['atencion', 'tramites', 'eficiencia'].includes(r.objetivo) || ['perdemos-consultas', 'saturacion', 'proceso-manual'].includes(r.friccion);
    const rota = [mk, wb, ia].filter(Boolean).length > 1 ? 'integrado' : ia ? 'ia' : wb ? 'web' : mk ? 'marketing' : r.objetivo === 'leads' ? 'integrado' : 'marketing';
    let s = 0;
    if (r.volumen === 'alto') s += 1; if (r.volumen === 'muy-alto') s += 2;
    if (a.includes('crm')) s += 1; if (a.includes('reservas')) s += 1; if (a.includes('ninguno')) s -= 1;
    if (['4000-mas', 'proyecto-8-15', 'proyecto-15-mas'].includes(r.inversion)) s += 2; else if (['2000-4000', 'proyecto-4-8'].includes(r.inversion)) s += 1; else if (r.inversion === 'menos-1000') s -= 2;
    const nivel = s >= 3 ? 2 : s >= 1 ? 1 : 0;
    const deps = [];
    if (rota === 'ia' || rota === 'integrado') { deps.push('Consumos de voz, WhatsApp, modelos y APIs, facturados aparte según volumen.'); if (a.includes('reservas') || a.includes('crm')) deps.push('Las integraciones dependen de que exista API, permisos y un entorno donde probar.'); }
    if (rota === 'marketing' || rota === 'integrado') deps.push('Inversión publicitaria, desplazamientos y dietas, presupuestados aparte.');
    if (rota === 'web' || rota === 'integrado') deps.push('Dominio, alojamiento y licencias de terceros, a nombre de su empresa.');
    if (a.includes('ninguno')) deps.push('Al no partir de activos previos, la primera fase incluye producción de base.');
    const prox = r.plazo === 'exploracion' ? 'Le enviamos la recomendación por escrito y, si lo prefiere, material para valorarlo con calma antes de hablar.' : 'Una conversación de 30 minutos para contrastar el diagnóstico y cerrar alcance.';
    return { rota, ruta: RUTA[rota], plano: PLANO[rota][nivel], porque: PORQUE[rota], acoes: ACOES[rota], deps, prox };
  };

  // iconos de línea (24×24) y fotografías de las opciones: se ve antes de leerse
  const IC = {
    estrella: '<path d="M12 3.5l2.5 5.3 5.8.7-4.3 3.9 1.1 5.7L12 16.3l-5.1 2.8 1.1-5.7-4.3-3.9 5.8-.7z"/>',
    diana: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8"/>',
    web: '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M3 9h18M6 6.8h.01M8.5 6.8h.01"/>',
    reloj: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.2 2"/>',
    doc: '<path d="M7 3.5h7l4 4V20.5H7z"/><path d="M14 3.5v4h4M10 12h5M10 15.5h5"/>',
    engrane: '<circle cx="12" cy="12" r="3"/><path d="M12 3.5v3M12 17.5v3M3.5 12h3M17.5 12h3M6 6l2.1 2.1M15.9 15.9 18 18M6 18l2.1-2.1M15.9 8.1 18 6"/>',
    duda: '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.6a2.5 2.5 0 1 1 3.4 2.3c-.6.3-1 .8-1 1.4v.6M12 16.8h.01"/>',
    edificio: '<path d="M5 20.5V5.5l7-2 7 2v15M9 8.5h.01M15 8.5h.01M9 12h.01M15 12h.01M9 15.5h.01M15 15.5h.01M10.5 20.5v-3h3v3"/>',
    maletin: '<rect x="3.5" y="7.5" width="17" height="12" rx="2"/><path d="M9 7.5V5.5h6v2M3.5 12.5h17"/>',
    puntos: '<path d="M6 12h.01M12 12h.01M18 12h.01" stroke-width="3"/>',
    noche: '<path d="M19 14.5A7.5 7.5 0 1 1 9.5 5a6 6 0 0 0 9.5 9.5z"/>',
    gente: '<circle cx="9" cy="8" r="3"/><path d="M3.5 19.5c.6-3 2.8-4.5 5.5-4.5s4.9 1.5 5.5 4.5M16 5.5a3 3 0 0 1 0 5.6M17.5 15.2c1.6.6 2.6 2 3 4.3"/>',
    curva: '<path d="M3.5 18.5h17M5 15l4-4 3.5 3 6.5-7"/>',
    ojo: '<path d="M2.5 12s3.5-6.5 9.5-6.5S21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/>',
    capas: '<path d="m12 4 8.5 4.5L12 13 3.5 8.5z"/><path d="m3.5 12.5 8.5 4.5 8.5-4.5M3.5 16.5 12 21l8.5-4.5"/>',
    redes: '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>',
    crm: '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8.5 9.5v10"/>',
    camara: '<rect x="3" y="7" width="13" height="10" rx="2"/><path d="m16 10.5 5-3v9l-5-3"/>',
    calendario: '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
    vacio: '<circle cx="12" cy="12" r="8.5"/><path d="M6 18 18 6"/>',
    rayo: '<path d="M13 3 5 13.5h6L10 21l8-10.5h-6z"/>',
    corona: '<path d="M4 17.5 3 8l5 4 4-6.5 4 6.5 5-4-1 9.5z"/><path d="M4 20.5h16"/>',
    persona: '<circle cx="12" cy="8" r="3.5"/><path d="M5 20.5c.8-4 3.6-6 7-6s6.2 2 7 6"/>',
    lupa: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',
  };
  const ICO = {
    sector: { 'inmobiliaria-premium': 'edificio', b2b: 'maletin', otro: 'puntos' },
    objetivo: { autoridad: 'estrella', leads: 'diana', web: 'web', atencion: 'reloj', tramites: 'doc', eficiencia: 'engrane', 'no-lo-se': 'duda' },
    friccion: { 'perdemos-consultas': 'noche', saturacion: 'gente', 'trafico-no-convierte': 'curva', percepcion: 'ojo', inconsistencia: 'capas', 'proceso-manual': 'engrane', 'no-lo-se': 'duda' },
    activos: { web: 'web', redes: 'redes', crm: 'crm', equipo: 'gente', contenido: 'camara', reservas: 'calendario', ninguno: 'vacio' },
    plazo: { inmediato: 'rayo', '30-90': 'calendario', trimestre: 'calendario', exploracion: 'lupa' },
    rol: { propiedad: 'corona', direccion: 'maletin', responsable: 'persona', investigacion: 'lupa' },
  };
  const FOTO = { hoteles: 'ia-hotel-atencion-atardecer', 'joyeria-relojeria': 'diamantes-anillos', 'automocion-lujo': 'tn-autosport-deportivos', nautica: 'yate-vistas', 'inmobiliaria-premium': 'ia-hotel-estudio-establecimiento', b2b: 'ia-portada-esfera', otro: 'reloj-detalle-f' };
  const NIVEL = { volumen: { bajo: 1, medio: 2, alto: 3, 'muy-alto': 4 }, inversion: { 'menos-1000': 1, '1000-2000': 2, '2000-4000': 3, '4000-mas': 4, 'proyecto-4-8': 2, 'proyecto-8-15': 3, 'proyecto-15-mas': 4 } };
  const ETAPA = (k) => (k === 0 ? 'Su empresa' : k < 4 ? 'Su objetivo' : k < 8 ? 'Su momento' : 'Contacto');

  const raiz = dg.dataset.raiz || '';
  const CHAVE = 'ferreras.diagnostico.v4';
  let r = {}, ct = {};
  try { r = JSON.parse(sessionStorage.getItem(CHAVE) || '{}'); } catch (e) {}
  const pre = new URLSearchParams(location.search).get('sector');
  if (pre && P[0].o.some(([v]) => v === pre)) r.sector = pre;
  const guarda = () => { try { sessionStorage.setItem(CHAVE, JSON.stringify(r)); } catch (e) {} };

  const passoEl = $('[data-diag-paso]', dg), recoEl = $('[data-reco]', dg), placa = $('[data-placa]', dg), selo = $('[data-selo]', dg);
  const N = P.length; // 8 preguntas; el paso N es el contacto
  const rotulo = (p, v) => { if (Array.isArray(v)) return v.map((x) => p.o.find((o) => o[0] === x)?.[1]).filter(Boolean).join(', ') || 'Sin respuesta'; return v === null ? 'Sin respuesta' : p.o.find((o) => o[0] === v)?.[1] || 'Elegir'; };
  const pintaPlaca = () => P.forEach((p) => {
    const b = $(`[data-pl="${p.id}"]`, placa); if (!b) return;
    const v = r[p.id];
    b.textContent = v === undefined ? 'Elegir' : rotulo(p, v);
    b.classList.toggle('vazio', v === undefined);
    b.parentElement.classList.toggle('atual', P[i] === p);
  });
  let i = P.findIndex((p) => r[p.id] === undefined); if (i < 0) i = N;
  const POS = [0, 0.25, 0.333, 0.417, 0.5, 0.625, 0.75, 0.875, 1];
  const marca = (k) => dg.style.setProperty('--k', (k >= N ? 1 : POS[k]).toFixed(4));
  const icone = (p, v, j) => {
    if (p.id === 'sector' && FOTO[v]) return `<img class="op-f" src="${raiz}img/${FOTO[v]}-900.webp" alt="" loading="lazy" decoding="async">`;
    if (NIVEL[p.id]) { const n = NIVEL[p.id][v]; return n ? `<span class="op-n" style="--n:${n}" aria-hidden="true"><i></i><i></i><i></i><i></i></span>` : `<svg class="op-i" viewBox="0 0 24 24" aria-hidden="true">${IC.duda}</svg>`; }
    const k = ICO[p.id] && ICO[p.id][v];
    return k ? `<svg class="op-i" viewBox="0 0 24 24" aria-hidden="true">${IC[k]}</svg>` : '';
  };
  const ir = (k) => { i = k; desenha(); const top = dg.getBoundingClientRect().top + scrollY - 110; if (Math.abs(scrollY - top) > 40 && scrollY > top) scrollTo({ top, behavior: reduz ? 'auto' : 'smooth' }); };

  const desenha = () => {
    marca(i); pintaPlaca();
    recoEl.hidden = true; passoEl.hidden = false;
    if (i >= N) return contactoPasso();
    const p = P[i], v = r[p.id], foto = p.id === 'sector';
    passoEl.innerHTML = `
      <p class="etiqueta"><span class="n">Paso ${i + 1} de ${N + 1}</span>${ETAPA(i)}</p>
      <h3 class="dj-q" tabindex="-1">${p.q}</h3>
      <p class="dj-a">${p.a}</p>
      <div class="dj-ops${foto ? ' com-foto' : ''}" role="group" aria-label="${p.q}">${p.o.map(([val, txt], j) => `<button type="button" class="op" data-v="${val}" aria-pressed="${p.multi ? (v || []).includes(val) : v === val}"><kbd>${String.fromCharCode(65 + j)}</kbd><span class="op-t">${txt}</span>${icone(p, val, j)}</button>`).join('')}</div>
      <div class="dj-nav">
        <button type="button" class="enlace" data-atras ${i ? '' : 'hidden'}><span class="fl">←</span> Atrás</button>
        <span class="acoes"><button type="button" class="btn btn-linha btn-peq" data-salta>Prefiero no responder</button>${p.multi ? '<button type="button" class="btn btn-oscuro btn-peq" data-segue>Continuar <span class="fl">→</span></button>' : ''}</span>
      </div>`;
    $('h3', passoEl).focus({ preventScroll: true });
    SITE.remede();
  };
  const avanca = () => { guarda(); ir(i + 1); };
  passoEl.addEventListener('click', (e) => {
    if (i >= N) return;
    const p = P[i];
    const op = e.target.closest('.op');
    if (op) {
      const v = op.dataset.v;
      if (p.multi) {
        let l = Array.isArray(r[p.id]) ? r[p.id] : [];
        if (v === 'ninguno') l = l.includes('ninguno') ? [] : ['ninguno'];
        else { l = l.filter((x) => x !== 'ninguno'); l = l.includes(v) ? l.filter((x) => x !== v) : [...l, v]; }
        r[p.id] = l; guarda();
        $$('.op', passoEl).forEach((b) => b.setAttribute('aria-pressed', l.includes(b.dataset.v)));
        pintaPlaca();
      } else { r[p.id] = v; $$('.op', passoEl).forEach((b) => b.setAttribute('aria-pressed', b === op)); pintaPlaca(); setTimeout(avanca, reduz ? 0 : 320); }
      return;
    }
    if (e.target.closest('[data-segue]')) { if (!r[p.id]) r[p.id] = []; avanca(); }
    if (e.target.closest('[data-salta]')) { r[p.id] = null; avanca(); }
    if (e.target.closest('[data-atras]')) ir(Math.max(0, i - 1));
  });
  // la placa también navega: cada línea lleva a su pregunta
  $$('[data-pl-l]', placa).forEach((l) => {
    l.tabIndex = 0; l.setAttribute('role', 'button');
    const vai = () => { if (!recoEl.hidden) return; const k = P.findIndex((p) => p.id === l.dataset.plL); if (k >= 0) ir(k); };
    l.addEventListener('click', vai); l.addEventListener('keydown', (e) => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), vai()));
  });
  addEventListener('keydown', (e) => {
    if (passoEl.hidden || i >= N || e.altKey || e.ctrlKey || e.metaKey || /input|textarea|select/i.test(document.activeElement.tagName)) return;
    const r0 = dg.getBoundingClientRect(); if (r0.bottom < 0 || r0.top > innerHeight) return;
    const k = e.key.toUpperCase().charCodeAt(0) - 65;
    const b = $$('.op', passoEl)[k];
    if (e.key.length === 1 && b) { e.preventDefault(); b.click(); }
  });

  const fld = (id, n, rot, t, req, auto, opc) => `<div class="campo"><label for="${id}">${rot}${opc ? ' <small>(opcional)</small>' : ''}</label><input id="${id}" name="${n}" type="${t}" autocomplete="${auto}"${req ? ` data-req="${req}"` : ''} value="${(ct[n] || '').replace(/"/g, '&quot;')}"><span class="erro" id="${id}-erro"></span></div>`;
  function contactoPasso() {
    const pf = ct.preferencia || 'email';
    passoEl.innerHTML = `
      <p class="etiqueta"><span class="n">Paso ${N + 1} de ${N + 1}</span>Contacto</p>
      <h3 class="dj-q" tabindex="-1">¿A quién le enviamos la recomendación?</h3>
      <p class="dj-a">La verá en el acto. Una persona del equipo la revisa y le responde en un día laborable.</p>
      <form class="form-l dj-form" novalidate><div class="campos">
        ${fld('dj-nome', 'nombre', 'Nombre', 'text', 'Indique su nombre.', 'name')}${fld('dj-emp', 'empresa', 'Empresa', 'text', 'Indique el nombre de su empresa.', 'organization')}
        ${fld('dj-mail', 'email', 'Email', 'email', 'Revise la dirección de email.', 'email')}${fld('dj-tel', 'telefono', 'Teléfono', 'tel', '', 'tel', true)}
        ${fld('dj-cargo', 'cargo', 'Cargo', 'text', '', 'organization-title', true)}
        <fieldset class="campo largo pills"><legend>Prefiero que me contacten por</legend><div>${[['email', 'Email'], ['telefono', 'Teléfono'], ['whatsapp', 'WhatsApp']].map(([v, t]) => `<label><input type="radio" name="preferencia" value="${v}"${v === pf ? ' checked' : ''}><span>${t}</span></label>`).join('')}</div></fieldset>
        <div class="campo largo consent"><label class="check"><input type="checkbox" id="dj-ok" name="consentimiento" data-req="Necesitamos su consentimiento para poder responderle."${ct.consentimiento ? ' checked' : ''}><i aria-hidden="true"></i><span>He leído la <a href="${raiz}legal/privacidad/">política de privacidad</a> y acepto que Ferreras me contacte sobre esta solicitud.</span></label><span class="erro" id="dj-ok-erro"></span></div>
        <input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
      </div><div class="dj-nav"><button type="button" class="enlace" data-atras><span class="fl">←</span> Atrás</button><button type="submit" class="btn btn-oscuro">Ver mi recomendación <span class="fl">→</span></button></div></form>`;
    const f = $('form', passoEl);
    const lembra = () => $$('input', f).forEach((x) => { if (x.name && x.name !== 'website') ct[x.name] = x.type === 'checkbox' ? x.checked : x.type === 'radio' ? (x.checked ? x.value : ct[x.name]) : x.value; });
    f.addEventListener('input', lembra); f.addEventListener('change', lembra);
    $('[data-atras]', f).addEventListener('click', () => { lembra(); ir(N - 1); });
    f.addEventListener('submit', (ev) => {
      ev.preventDefault();
      if (!valida(f)) return;
      lembra();
      const contact = contato(f);
      const d = { kind: 'configurador', submissionId: `cfg_${Date.now()}_${r.sector || 'na'}`, contact, website: val(f, 'website'), answers: r, meta: { path: location.pathname.includes('diagnostico') ? '/diagnostico' : '/', utm: UTM } };
      mostraReco(d);
    });
    $('h3', passoEl).focus({ preventScroll: true });
    SITE.remede();
  }

  function mostraReco(d) {
    const x = recomenda(r);
    marca(N + 0.0001); dg.classList.add('chegou');
    passoEl.hidden = true; recoEl.hidden = false;
    recoEl.innerHTML = `
      <p class="etiqueta"><span class="n">✓</span>Su recomendación</p>
      <h3 class="dj-q">${x.porque[0]}</h3>
      <p class="dj-a">${x.porque[1]}</p>
      <div class="reco-g"><div><span class="etiqueta">Punto de partida</span><b>${x.plano}</b><a class="enlace" href="${raiz}${x.ruta[1]}">${x.ruta[0]} <span class="fl">→</span></a></div>
        <div><span class="etiqueta">Siguiente paso</span><p>${x.prox}</p></div></div>
      <p class="etiqueta reco-t">Sus tres primeras acciones</p>
      <ol class="reco-acoes">${x.acoes.map((a) => `<li>${a}</li>`).join('')}</ol>
      ${x.deps.length ? `<div class="deps"><b>Dependencias y costes previsibles</b>${x.deps.map((a) => `<p>${a}</p>`).join('')}</div>` : ''}
      <div class="envio" data-envio aria-live="polite"><p class="envio-a" data-e="a" hidden>Enviando su solicitud…</p>
        <div class="envio-ok" data-e="ok" hidden><b>Solicitud recibida.</b><p>Le responderemos en un día laborable.</p></div>
        <div class="envio-ko" data-e="ko" hidden><b>No hemos podido conectar.</b><p>Sus respuestas siguen aquí. <button type="button" class="enlace" data-reenvia>Reintentar</button> o escríbanos a <a data-mailto href="mailto:${EMAIL}">${EMAIL}</a>.</p></div></div>
      <p><button type="button" class="enlace" data-recomeca><span class="fl">↺</span> Empezar de nuevo</button></p>`;
    const box = $('[data-envio]', recoEl);
    const linhas = [...resumo({ contact: d.contact }), '', 'Respuestas del diagnóstico:', ...P.map((p) => `· ${ROT[p.id]}: ${r[p.id] === undefined ? '—' : rotulo(p, r[p.id])}`), '', `Recomendación: ${x.porque[0]}`, `Punto de partida: ${x.plano}`];
    const vai = async () => {
      const ok = await despacha(d, box, 'Diagnóstico · ' + d.contact.empresa, linhas);
      if (ok) {
        const t = new Date(), z = (n) => String(n).padStart(2, '0');
        $('[data-selo-t]', selo).textContent = `${z(t.getDate())}.${z(t.getMonth() + 1)}.${t.getFullYear()} · ${z(t.getHours())}:${z(t.getMinutes())}`;
        selo.hidden = false; requestAnimationFrame(() => selo.classList.add('on'));
      }
      SITE.remede();
    };
    recoEl.addEventListener('click', (e) => { if (e.target.closest('[data-reenvia]')) vai(); });
    $('[data-recomeca]', recoEl).onclick = () => { r = {}; guarda(); selo.hidden = true; selo.classList.remove('on'); dg.classList.remove('chegou'); ir(0); };
    vai();
    recoEl.focus({ preventScroll: true });
    SITE.remede();
  }
  desenha();
})();
