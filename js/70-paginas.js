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

  /* ---------- formularios sin servidor: validan junto al campo y abren el correo ya escrito ---------- */
  const valida = (form) => {
    let primeiro = null;
    $$('[data-req]', form).forEach((el) => {
      const v = el.type === 'checkbox' ? el.checked : el.value.trim();
      let msg = '';
      if (!v) msg = el.dataset.req;
      else if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(el.value.trim())) msg = 'Revise la dirección de email.';
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      const e = $('#' + el.id + '-erro'); if (e) e.textContent = msg;
      if (msg && !primeiro) primeiro = el;
    });
    if (primeiro) primeiro.focus();
    return !primeiro;
  };
  const correo = (assunto, linhas) => { location.href = `mailto:${EMAIL}?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(linhas.join('\n'))}`; };
  $$('form[data-mail]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if ($('[name="website"]', form)?.value) return; // campo trampa
      if (!valida(form)) return;
      const linhas = $$('[data-campo]', form).map((el) => {
        if (el.type === 'radio' && !el.checked) return null;
        const v = el.type === 'checkbox' ? (el.checked ? 'Sí' : 'No') : el.value.trim();
        return v ? `${el.dataset.campo}: ${v}` : null;
      }).filter(Boolean);
      correo(form.dataset.mail, [...linhas, '', 'Enviado desde la web (propuesta de rediseño).']);
      const ok = $('[data-ok]', form.parentElement); if (ok) { ok.hidden = false; SITE.remede(); }
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
  const RUTA = { marketing: ['Marketing estratégico', '../marketing/'], web: ['Web y ecommerce', '../web/'], ia: ['Agentes IA y automatización', '../inteligencia-artificial/'], integrado: ['Sistema integrado', '../contacto/'] };
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

  const CHAVE = 'ferreras.diagnostico.v2';
  let r = {};
  try { r = JSON.parse(sessionStorage.getItem(CHAVE) || '{}'); } catch (e) {}
  const pre = new URLSearchParams(location.search).get('sector');
  if (pre && P[0].o.some(([v]) => v === pre)) r.sector = pre;
  const guarda = () => { try { sessionStorage.setItem(CHAVE, JSON.stringify(r)); } catch (e) {} };

  const passoEl = $('[data-diag-paso]', dg), recoEl = $('[data-reco]', dg), prog = $('[data-diag-prog]', dg), placa = $('[data-diag-placa]', dg);
  prog.innerHTML = P.map(() => '<i></i>').join('');
  placa.innerHTML = P.map((p) => `<div><span>${ROT[p.id]}</span><b class="vazio" data-pl="${p.id}">—</b></div>`).join('');
  const rotulo = (p, v) => { if (Array.isArray(v)) return v.map((x) => p.o.find((o) => o[0] === x)?.[1]).filter(Boolean).join(', ') || '—'; return p.o.find((o) => o[0] === v)?.[1] || (v === null ? 'Sin respuesta' : '—'); };
  const pintaPlaca = () => P.forEach((p) => { const b = $(`[data-pl="${p.id}"]`, placa), v = r[p.id]; b.textContent = v === undefined ? '—' : rotulo(p, v); b.classList.toggle('vazio', v === undefined); });
  let i = P.findIndex((p) => r[p.id] === undefined); if (i < 0) i = P.length;

  const desenha = () => {
    $$('i', prog).forEach((b, j) => b.classList.toggle('on', j < i));
    pintaPlaca();
    if (i >= P.length) return mostraReco();
    recoEl.hidden = true; passoEl.hidden = false;
    const p = P[i], v = r[p.id];
    passoEl.innerHTML = `
      <p class="etiqueta"><span class="n">Paso ${i + 1} de ${P.length}</span> Sin compromiso</p>
      <h2 tabindex="-1">${p.q}</h2>
      <p class="nota">${p.a}</p>
      <div class="opcoes" role="group" aria-label="${p.q}">${p.o.map(([val, txt], j) => `<button type="button" class="opcao" data-v="${val}" aria-pressed="${p.multi ? (v || []).includes(val) : v === val}"><kbd>${String.fromCharCode(65 + j)}</kbd>${txt}</button>`).join('')}</div>
      <div class="diag-acoes">
        <button type="button" class="enlace" data-atras ${i ? '' : 'hidden'}><span class="fl">←</span> Atrás</button>
        <span class="acoes"><button type="button" class="btn btn-linha btn-peq" data-salta>Prefiero no responder</button>${p.multi ? '<button type="button" class="btn btn-claro btn-peq" data-segue>Continuar <span class="fl">→</span></button>' : ''}</span>
      </div>`;
    $('h2', passoEl).focus({ preventScroll: true });
    SITE.remede();
  };
  const avanca = () => { guarda(); i++; desenha(); const top = dg.getBoundingClientRect().top + scrollY - 100; if (scrollY > top) scrollTo({ top, behavior: reduz ? 'auto' : 'smooth' }); };
  passoEl.addEventListener('click', (e) => {
    const p = P[i];
    const op = e.target.closest('.opcao');
    if (op) {
      const v = op.dataset.v;
      if (p.multi) {
        let l = Array.isArray(r[p.id]) ? r[p.id] : [];
        if (v === 'ninguno') l = l.includes('ninguno') ? [] : ['ninguno'];
        else { l = l.filter((x) => x !== 'ninguno'); l = l.includes(v) ? l.filter((x) => x !== v) : [...l, v]; }
        r[p.id] = l; guarda();
        $$('.opcao', passoEl).forEach((b) => b.setAttribute('aria-pressed', l.includes(b.dataset.v)));
        pintaPlaca();
      } else { r[p.id] = v; $$('.opcao', passoEl).forEach((b) => b.setAttribute('aria-pressed', b === op)); setTimeout(avanca, reduz ? 0 : 260); }
      return;
    }
    if (e.target.closest('[data-segue]')) { if (!r[p.id]) r[p.id] = []; avanca(); }
    if (e.target.closest('[data-salta]')) { r[p.id] = null; avanca(); }
    if (e.target.closest('[data-atras]')) { i = Math.max(0, i - 1); desenha(); }
  });
  addEventListener('keydown', (e) => {
    if (passoEl.hidden || e.altKey || e.ctrlKey || e.metaKey || /input|textarea|select/i.test(document.activeElement.tagName)) return;
    const k = e.key.toUpperCase().charCodeAt(0) - 65;
    const b = $$('.opcao', passoEl)[k];
    if (e.key.length === 1 && b) { e.preventDefault(); b.click(); }
  });

  function mostraReco() {
    const x = recomenda(r);
    passoEl.hidden = true; recoEl.hidden = false;
    $('[data-r="prioridad"]', recoEl).textContent = x.porque[0];
    $('[data-r="porque"]', recoEl).textContent = x.porque[1];
    $('[data-r="plano"]', recoEl).textContent = x.plano;
    $('[data-r="ruta"]', recoEl).textContent = x.ruta[0];
    $('[data-r="ruta-a"]', recoEl).href = x.ruta[1];
    $('[data-r="acoes"]', recoEl).innerHTML = x.acoes.map((a) => `<li>${a}</li>`).join('');
    const d = $('[data-r="deps"]', recoEl); d.hidden = !x.deps.length; d.innerHTML = '<b>Dependencias y costes previsibles</b>' + x.deps.map((a) => `<p>${a}</p>`).join('');
    $('[data-r="prox"]', recoEl).textContent = x.prox;
    const env = $('form', recoEl);
    env.onsubmit = (e) => {
      e.preventDefault();
      if (!valida(env)) return;
      const c = (n) => $(`[name="${n}"]`, env).value.trim();
      correo('Diagnóstico · ' + c('empresa'), [
        `Nombre: ${c('nombre')}`, `Empresa: ${c('empresa')}`, `Email: ${c('email')}`, c('telefono') ? `Teléfono: ${c('telefono')}` : null,
        '', 'Respuestas del diagnóstico:', ...P.map((p) => `· ${ROT[p.id]}: ${r[p.id] === undefined ? '—' : rotulo(p, r[p.id])}`),
        '', `Recomendación: ${x.porque[0]}`, `Punto de partida: ${x.plano} (${x.ruta[0]})`,
      ].filter((l) => l !== null));
      $('[data-ok]', recoEl).hidden = false;
    };
    $('[data-recomeca]', recoEl).onclick = () => { r = {}; guarda(); i = 0; desenha(); };
    $('h2', recoEl).focus({ preventScroll: true });
    SITE.remede();
  }
  desenha();
})();
