/* Ferreras v5. Um ficheiro: núcleo (um laço rAF, caixas medidas em lote), hoja de contactos, cabeçalho, vídeos,
   lista de trabalho, filtros, formulários (mesmo formato e destino que a web original) e a conversa do diagnóstico. */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const { raiz = '', email: EMAIL = '' } = window.FERRERAS || {};
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const suave = (t) => 1 - Math.pow(1 - t, 3);

  /* ---------- núcleo: medir em lote fora do laço; o laço só lê scrollY e escreve transform/opacity ---------- */
  const medidores = [], pintores = [];
  let W = innerWidth, H = innerHeight, sujo = true;
  const mede = () => { W = innerWidth; H = innerHeight; medidores.forEach((f) => f()); sujo = true; };
  let ultimoY = -1;
  const laco = () => {
    const y = scrollY;
    if (y !== ultimoY || sujo) { pintores.forEach((f) => f(y)); tom(y); ultimoY = y; sujo = false; }
    requestAnimationFrame(laco);
  };
  addEventListener('resize', () => requestAnimationFrame(mede));
  addEventListener('load', mede);
  if (window.ResizeObserver) new ResizeObserver(() => requestAnimationFrame(mede)).observe(document.body);
  const topo = (el) => el.getBoundingClientRect().top + scrollY;

  /* ---------- cabeçalho: tinta sobre papel, papel sobre o filme e sobre as secções escuras ---------- */
  const cab = $('[data-cab]');
  let escuros = [], heroClaro = false;
  medidores.push(() => { escuros = $$('[data-escuro]').map((el) => [topo(el), topo(el) + el.offsetHeight]); });
  const tom = (y) => {
    const linha = y + 36;
    const claro = heroClaro || escuros.some(([a, b]) => linha >= a && linha < b);
    cab.classList.toggle('claro', claro);
    cab.classList.toggle('fundo', !claro && y > 8);
  };

  /* ---------- menu de ecrã inteiro ---------- */
  const menu = $('[data-menu]'), abre = $('[data-menu-abre]'), fecha = $('[data-menu-fecha]');
  const poeMenu = (on) => {
    menu.hidden = !on; abre.setAttribute('aria-expanded', on); document.body.style.overflow = on ? 'hidden' : '';
    (on ? fecha : abre).focus();
  };
  abre.addEventListener('click', () => poeMenu(true));
  fecha.addEventListener('click', () => poeMenu(false));
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) poeMenu(false); });

  /* ---------- vídeos: escolher o ficheiro pela largura real; só descarregam e tocam à vista ---------- */
  const deitado = () => W > H * 0.9 || W > 800;
  const escolhe = (v) => {
    const base = v.dataset.filme;
    if (!base) { const s = $('source', v); return s && s.dataset.src; }
    const lento = navigator.connection && navigator.connection.saveData;
    const px = W * (devicePixelRatio || 1);
    if (deitado()) return `${base}-${!lento && px > 1440 ? 1080 : 720}.mp4`;
    v.poster = `${base}-v720-poster.webp`;
    return `${base}-v${!lento && px > 800 ? 1080 : 720}.mp4`;
  };
  const toca = (v) => { const p = v.play(); if (p) p.catch(() => {}); };
  const vio = new IntersectionObserver((es) => es.forEach(({ target: v, isIntersecting: dentro }) => {
    if (dentro) { if (!v.dataset.ok) { v.src = escolhe(v); v.dataset.ok = 1; } if (!reduz) toca(v); }
    else if (!v.paused) v.pause();
  }), { rootMargin: '25% 0px' });
  $$('[data-vd]').forEach((v) => vio.observe(v));
  addEventListener('pageshow', (e) => e.persisted && $$('[data-vd]').forEach((v) => v.dataset.ok && !reduz && v.getBoundingClientRect().bottom > 0 && toca(v)));

  /* ---------- hoja de contactos: o lápis marca o fotograma; o scroll leva-o até ser o filme ---------- */
  const hoja = $('[data-hoja]');
  if (hoja) {
    const palco = $('[data-palco]', hoja), folha = $('[data-folha]', hoja), marcado = $('[data-marcado]', hoja);
    const txt = $('[data-hoja-txt]', hoja), pe = $('[data-hoja-pie]', hoja), lapiz = $('.lapiz', marcado);
    let ini = 0, curso = 1, fx = 0, fy = 0, cx = 0, cy = 0, S = 1, ult = '';
    requestAnimationFrame(() => document.body.classList.add('pronto'));
    medidores.push(() => {
      ini = topo(hoja); curso = Math.max(1, hoja.offsetHeight - palco.offsetHeight);
      fx = folha.offsetLeft; fy = folha.offsetTop;                 // a folha dentro do palco (sem transform)
      const w = marcado.offsetWidth, h = marcado.offsetHeight;
      cx = marcado.offsetLeft + w / 2; cy = marcado.offsetTop + h / 2; // centro do fotograma dentro da folha
      S = Math.max(palco.offsetWidth / w, palco.offsetHeight / h) * 1.002;
    });
    if (!reduz) pintores.push((y) => {
      const p = clamp((y - ini) / curso);
      const z = suave(clamp((p - 0.06) / 0.66));                      // zoom entre 6 % e 72 % do percurso
      const s = Math.pow(S, z);                                       // escala geométrica: o zoom parece constante
      const alvoX = fx + cx + (palco.offsetWidth / 2 - fx - cx) * z;
      const alvoY = fy + cy + (palco.offsetHeight / 2 - fy - cy) * z;
      const tx = alvoX - fx - cx * s, ty = alvoY - fy - cy * s;
      const t = `translate3d(${tx.toFixed(1)}px,${ty.toFixed(1)}px,0) scale(${s.toFixed(4)})`;
      if (t !== ult) { folha.style.transform = t; ult = t; }
      txt.style.opacity = (1 - clamp(z * 2.6)).toFixed(3);
      txt.style.transform = `translate3d(0,${(-40 * z).toFixed(1)}px,0)`;
      lapiz.style.opacity = (1 - clamp(z * 4)).toFixed(3);
      pe.style.opacity = clamp((p - 0.74) / 0.12).toFixed(3);
      heroClaro = z > 0.55 && y + 36 < ini + hoja.offsetHeight;
    });
  }

  /* ---------- trabalho: a fotografia segue o cursor (só com rato) ---------- */
  const tl = $('[data-tl]'), cur = $('[data-cursor]');
  if (tl && cur && matchMedia('(hover: hover) and (min-width: 961px)').matches) {
    const im = $('img', cur);
    let mx = 0, my = 0, px = 0, py = 0, vivo = false;
    tl.addEventListener('mousemove', (e) => { mx = e.clientX; my = e.clientY; });
    $$('a', tl).forEach((a) => a.addEventListener('mouseenter', (e) => {
      if (im.getAttribute('src') !== a.dataset.prev) im.src = a.dataset.prev;
      if (!vivo) { px = mx = e.clientX; py = my = e.clientY; }
      vivo = true; cur.classList.add('on');
    }));
    tl.addEventListener('mouseleave', () => { vivo = false; cur.classList.remove('on'); });
    pintores.push(() => {
      if (!vivo) return;
      const k = reduz ? 1 : 0.16;
      px += (mx - px) * k; py += (my - py) * k;
      cur.style.transform = `translate3d(${(px + 28).toFixed(1)}px,${(py - cur.offsetHeight / 2).toFixed(1)}px,0)`;
      sujo = true;
    });
  }

  /* ---------- filtros dos casos ---------- */
  const casos = $('[data-casos]');
  if (casos) {
    const bs = $$('[data-filtro]');
    const filtra = (k) => {
      bs.forEach((b) => b.setAttribute('aria-pressed', b.dataset.filtro === k));
      $$('.cs', casos).forEach((c) => { c.hidden = !!k && c.dataset.sector !== k; });
      mede();
    };
    bs.forEach((b) => b.addEventListener('click', () => filtra(b.dataset.filtro)));
    const q = new URLSearchParams(location.search).get('sector');
    if (q && bs.some((b) => b.dataset.filtro === q)) filtra(q);
  }

  /* ---------- formulários: os mesmos campos, regras e destino que a web original (POST a /api/leads, mesmo
     formato). De outro domínio a resposta não se lê (no-cors): valida-se aqui e, se a rede falhar, fica o correio. ---------- */
  const API = 'https://www.marketingferreras.com/api/leads';
  const UTM = (() => {
    const q = new URLSearchParams(location.search), o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach((k) => { const v = q.get(k); if (v) o[k] = v.replace(/[^\w\-. ]/g, '').slice(0, 64); });
    return o;
  })();
  const envia = (d) => fetch(API, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(d), keepalive: true });
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
      const er = el.id && $('#' + el.id + '-erro'); if (er) er.textContent = msg;
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
  const despacha = async (d, box, assunto, linhas) => {
    if (d.website) { estado(box, 'ok'); return true; } // campo armadilha preenchido: finge-se o envio
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
      mede();
    });
  });

  /* ---------- a conversa: as oito perguntas do diagnóstico original, uma mensagem de cada vez ---------- */
  const conv = $('[data-conv]');
  if (conv) {
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
    const RUTA = { marketing: ['Marketing', 'servicios/#marketing'], web: ['Web y ecommerce', 'servicios/#web'], ia: ['Inteligencia artificial', 'servicios/#ia'], integrado: ['Marketing e inteligencia artificial', 'servicios/'] };
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
    // a mesma lógica da web original
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
      return { ruta: RUTA[rota], plano: PLANO[rota][nivel], porque: PORQUE[rota], acoes: ACOES[rota], deps, prox };
    };

    const CHAVE = 'ferreras.conversa.v5';
    let r = {};
    try { r = JSON.parse(sessionStorage.getItem(CHAVE) || '{}'); } catch (e) {}
    const guarda = () => { try { sessionStorage.setItem(CHAVE, JSON.stringify(r)); } catch (e) {} };
    const lista = $('[data-conv-l]', conv), ops = $('[data-conv-ops]', conv);
    const N = P.length;
    const rotulo = (p, v) => (v === null ? 'Prefiero no responder' : Array.isArray(v) ? (v.map((x) => p.o.find((o) => o[0] === x)?.[1]).filter(Boolean).join(', ') || 'Ninguna') : p.o.find((o) => o[0] === v)?.[1] || '');
    const falta = () => { const k = P.findIndex((p) => r[p.id] === undefined); return k < 0 ? N : k; };
    const ferreras = (q, a) => `<li class="cv-f"><p>${q}</p>${a ? `<small>${a}</small>` : ''}</li>`;

    // a conversa inteira desenha-se de novo a partir das respostas: voltar atrás é só apagar uma resposta
    const desenha = (foco = true) => {
      const i = falta();
      let h = ferreras('Hola. Le hacemos ocho preguntas y le devolvemos una recomendación concreta, en el acto.', '');
      for (let k = 0; k < i; k++) {
        const p = P[k];
        h += ferreras(p.q, '') + `<li class="cv-u">${rotulo(p, r[p.id])}<button type="button" data-muda="${p.id}" aria-label="Cambiar la respuesta: ${p.q}">Cambiar</button></li>`;
      }
      if (i < N) {
        const p = P[i];
        h += ferreras(p.q, p.a);
        const v = r[p.id];
        ops.innerHTML = p.o.map(([val, t]) => `<button type="button" class="op" data-v="${val}" aria-pressed="${p.multi ? (Array.isArray(v) && v.includes(val)) : false}">${t}</button>`).join('')
          + `<div class="linha-acoes">${p.multi ? '<button type="button" class="pilula" data-segue>Continuar</button>' : ''}<button type="button" class="sub" data-salta>Prefiero no responder</button><span class="sub" aria-hidden="true" style="text-decoration:none">${i + 1} de ${N}</span></div>`;
      } else {
        h += ferreras('Gracias. ¿A quién le enviamos la recomendación?', 'La verá en el acto. Una persona del equipo la revisa y le responde en un día laborable.');
        ops.innerHTML = contactoForm();
        ligaForm();
      }
      lista.innerHTML = h;
      if (foco) { const b = $('.op, input', ops); if (b) b.focus({ preventScroll: true }); }
      mede();
    };
    const fld = (id, n, rot, t, req, auto, opc) => `<div class="campo"><label for="${id}">${rot}${opc ? ' <small>(opcional)</small>' : ''}</label><input id="${id}" name="${n}" type="${t}" autocomplete="${auto}"${req ? ` data-req="${req}"` : ''}><span class="erro" id="${id}-erro"></span></div>`;
    const contactoForm = () => `<form class="form" novalidate><div class="campos">
        ${fld('cv-nome', 'nombre', 'Nombre', 'text', 'Indique su nombre.', 'name')}${fld('cv-emp', 'empresa', 'Empresa', 'text', 'Indique el nombre de su empresa.', 'organization')}
        ${fld('cv-mail', 'email', 'Email', 'email', 'Revise la dirección de email.', 'email')}${fld('cv-tel', 'telefono', 'Teléfono', 'tel', '', 'tel', true)}
        ${fld('cv-cargo', 'cargo', 'Cargo', 'text', '', 'organization-title', true)}
        <fieldset class="campo largo opcoes"><legend>Prefiero que me contacten por</legend><div>${[['email', 'Email'], ['telefono', 'Teléfono'], ['whatsapp', 'WhatsApp']].map(([v, t], j) => `<label><input type="radio" name="preferencia" value="${v}"${j ? '' : ' checked'}><span>${t}</span></label>`).join('')}</div></fieldset>
        <div class="campo largo consent"><label class="check"><input type="checkbox" id="cv-ok" name="consentimiento" data-req="Necesitamos su consentimiento para poder responderle."><span>He leído la <a href="${raiz}legal/privacidad/">política de privacidad</a> y acepto que Ferreras me contacte sobre esta solicitud.</span></label><span class="erro" id="cv-ok-erro"></span></div>
        <input type="text" name="website" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
      </div><button type="submit" class="pilula">Ver mi recomendación</button></form>`;
    const ligaForm = () => {
      const f = $('form', ops);
      f.addEventListener('submit', (ev) => {
        ev.preventDefault();
        if (!valida(f)) return;
        const d = { kind: 'configurador', submissionId: `cfg_${Date.now()}_${r.sector || 'na'}`, contact: contato(f), website: val(f, 'website'), answers: r, meta: { path: '/diagnostico', utm: UTM } };
        mostraReco(d);
      });
    };
    const mostraReco = (d) => {
      const x = recomenda(r);
      lista.insertAdjacentHTML('beforeend', `<li class="cv-u">${d.contact.nombre}, ${d.contact.empresa}</li>`);
      ops.innerHTML = `<div class="reco" tabindex="-1">
          <h3 class="t-l">${x.porque[0]}</h3><p class="t-m">${x.porque[1]}</p>
          <div class="reco-g"><div><span>Punto de partida</span><b>${x.plano}</b><a class="enl" href="${raiz}${x.ruta[1]}">${x.ruta[0]}</a></div><div><span>Siguiente paso</span><p>${x.prox}</p></div></div>
          <div><b>Sus tres primeras acciones</b><ol>${x.acoes.map((a) => `<li>${a}</li>`).join('')}</ol></div>
          ${x.deps.length ? `<div class="deps"><b>Dependencias y costes previsibles</b>${x.deps.map((a) => `<p>${a}</p>`).join('')}</div>` : ''}
          <div class="envio" data-envio aria-live="polite"><p data-e="a" hidden>Enviando su solicitud…</p>
            <div data-e="ok" hidden><b>Solicitud recibida.</b><p>Le responderemos en un día laborable.</p></div>
            <div data-e="ko" hidden><b>No hemos podido conectar.</b><p>Sus respuestas siguen aquí. <button type="button" class="sub" data-reenvia>Reintentar</button> o escríbanos a <a data-mailto href="mailto:${EMAIL}">${EMAIL}</a>.</p></div></div>
          <p><button type="button" class="sub" data-recomeca>Empezar de nuevo</button></p></div>`;
      const box = $('[data-envio]', ops);
      const linhas = [...resumo({ contact: d.contact }), '', 'Respuestas del diagnóstico:', ...P.map((p) => `· ${ROT[p.id]}: ${r[p.id] === undefined ? '—' : rotulo(p, r[p.id])}`), '', `Recomendación: ${x.porque[0]}`, `Punto de partida: ${x.plano}`];
      const vai = () => despacha(d, box, 'Diagnóstico · ' + d.contact.empresa, linhas).then(mede);
      $('[data-reenvia]', ops).addEventListener('click', vai);
      $('[data-recomeca]', ops).addEventListener('click', () => { r = {}; guarda(); desenha(); });
      vai();
      $('.reco', ops).focus({ preventScroll: true });
      mede();
    };

    ops.addEventListener('click', (e) => {
      const i = falta(); if (i >= N) return;
      const p = P[i], op = e.target.closest('.op');
      if (op) {
        const v = op.dataset.v;
        if (p.multi) {
          let l = Array.isArray(r._multi) ? r._multi : [];
          if (v === 'ninguno') l = l.includes('ninguno') ? [] : ['ninguno'];
          else { l = l.filter((x) => x !== 'ninguno'); l = l.includes(v) ? l.filter((x) => x !== v) : [...l, v]; }
          r._multi = l;
          $$('.op', ops).forEach((b) => b.setAttribute('aria-pressed', l.includes(b.dataset.v)));
        } else { r[p.id] = v; guarda(); desenha(); }
        return;
      }
      if (e.target.closest('[data-segue]')) { r[p.id] = r._multi || []; delete r._multi; guarda(); desenha(); }
      if (e.target.closest('[data-salta]')) { r[p.id] = null; delete r._multi; guarda(); desenha(); }
    });
    lista.addEventListener('click', (e) => {
      const b = e.target.closest('[data-muda]'); if (!b) return;
      delete r[b.dataset.muda]; // só esta volta a ser perguntada; as outras respostas ficam
      delete r._multi; guarda(); desenha();
    });
    delete r._multi;
    desenha(false);
  }

  mede();
  requestAnimationFrame(laco);
})();
