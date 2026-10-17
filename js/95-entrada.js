/* Ferreras: la entrada de cada página interior. Cada sala tiene la suya (unos 2,5 s) y después la cortina sube y deja
   la página en su sitio: La casa dibuja la marca; Marketing enfoca como un visor de cámara con su código de tiempo;
   IA saluda en doce idiomas; Sectores levanta sus cuatro columnas; Casos cuenta las visitas; Web traza su maqueta;
   IA para hoteles da la vuelta a las 24 horas; Contacto escribe a mano; las ocho preguntas se encienden una a una.
   No bloquea: cualquier gesto (rueda, tecla, toque) la acelera hasta el final. Con «reducir movimiento» no existe. */
(() => {
  const { $ } = SITE;
  // monta a entrada «pg» dentro de ov e devolve a linha de tempo; os capítulos da portada (99-capitulos.js) usam-na também
  SITE.entrada = (ov, pg, sub, fim) => {
  const h = (html) => { ov.insertAdjacentHTML('beforeend', html); return ov.lastElementChild; };
  const tl = gsap.timeline({ defaults: { ease: 'power3.out' }, onComplete: fim });
  const marca = document.querySelector('.topo-marca svg, .lg-m');

  const R = {
    'la-casa'() {
      const m = h(`<div class="en-casa">${marca ? marca.outerHTML : ''}<p>La casa</p></div>`);
      const ps = m.querySelectorAll('path');
      ps.forEach((p) => { const L = p.getTotalLength ? p.getTotalLength() : 600; gsap.set(p, { strokeDasharray: L, strokeDashoffset: L, fillOpacity: 0 }); });
      tl.to(ps, { strokeDashoffset: 0, duration: 1.4, stagger: 0.05, ease: 'power2.inOut' })
        .to(ps, { fillOpacity: 1, duration: 0.6 }, '-=0.3')
        .from(m.querySelector('p'), { yPercent: 120, opacity: 0, duration: 0.8 }, '-=0.5');
    },
    marketing() {
      const m = h('<div class="en-visor"><i class="c c1"></i><i class="c c2"></i><i class="c c3"></i><i class="c c4"></i><p class="rec"><b></b>REC</p><p class="tc">00:00:00:00</p><p class="nm">Marketing</p></div>');
      const tc = m.querySelector('.tc'), o = { f: 0 };
      tl.from(m.querySelectorAll('.c'), { scale: 2.4, opacity: 0, duration: 1.1, stagger: 0.06, ease: 'expo.out' })
        .to(o, { f: 75, duration: 2.2, ease: 'none', onUpdate: () => { const f = Math.round(o.f); tc.textContent = `00:00:0${Math.floor(f / 25)}:${String(f % 25).padStart(2, '0')}`; } }, 0)
        .from(m.querySelector('.nm'), { opacity: 0, letterSpacing: '0.6em', duration: 1.2 }, 0.5)
        .to(m.querySelectorAll('.c'), { scale: 0.9, duration: 0.5, ease: 'power2.inOut' }, 1.7);
    },
    'inteligencia-artificial'() {
      const pal = ['Buenas noches', 'Good evening', 'Bonsoir', 'Guten Abend', 'Buonasera', 'Boa noite', 'Goedenavond', 'Добрый вечер', 'こんばんは', '晚上好', 'مساء الخير', 'Inteligencia artificial'];
      const m = h('<div class="en-ia"><p class="w"></p><p class="s">más de veinte idiomas</p></div>');
      const w = m.querySelector('.w'), o = { i: 0 };
      tl.to(o, { i: pal.length - 1, duration: 2.1, ease: 'power1.in', onUpdate: () => { w.textContent = pal[Math.round(o.i)]; } })
        .from(m.querySelector('.s'), { opacity: 0, y: 12, duration: 0.6 }, 0.3);
      w.textContent = pal[0];
    },
    sectores() {
      const cols = [['hoteles', 'Hoteles'], ['automocion-lujo', 'Motor'], ['nautica', 'Mar'], ['joyeria-relojeria', 'Joyas']];
      const m = h(`<div class="en-sect">${cols.map(([k, t]) => `<div class="${k === sub ? 'esta' : ''}"><span>${t}</span></div>`).join('')}</div>`);
      const ds = m.querySelectorAll('div');
      tl.from(ds, { yPercent: 100, duration: 1, stagger: 0.12, ease: 'expo.out' })
        .from(m.querySelectorAll('span'), { opacity: 0, y: 30, duration: 0.6, stagger: 0.1 }, 0.5);
      if (sub) tl.to(m.querySelectorAll('div:not(.esta)'), { opacity: 0.18, duration: 0.5 }, 1.5).to(m.querySelector('.esta'), { flexGrow: 6, duration: 0.8, ease: 'power3.inOut' }, 1.6);
    },
    casos() {
      const m = h('<div class="en-casos"><p class="n">0</p><p class="s">visitas de media por pieza, en automoción</p></div>');
      const n = m.querySelector('.n'), o = { v: 0 };
      tl.to(o, { v: 300000, duration: 2, ease: 'power2.inOut', onUpdate: () => { n.textContent = Math.round(o.v).toLocaleString('es-ES'); } })
        .from(m.querySelector('.s'), { opacity: 0, y: 10, duration: 0.6 }, 0.4);
    },
    web() {
      const m = h('<div class="en-web"><svg viewBox="0 0 400 260" fill="none"><rect x="10" y="10" width="380" height="240" rx="6"/><path d="M10 34h380"/><rect x="30" y="54" width="200" height="16"/><rect x="30" y="80" width="140" height="10"/><rect x="250" y="54" width="120" height="96"/><rect x="30" y="170" width="105" height="60"/><rect x="148" y="170" width="105" height="60"/><rect x="265" y="170" width="105" height="60"/></svg><p>Web y ecommerce</p></div>');
      const els = m.querySelectorAll('rect, path');
      els.forEach((p) => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
      tl.to(els, { strokeDashoffset: 0, duration: 1.2, stagger: 0.12, ease: 'power2.inOut' })
        .from(m.querySelector('p'), { opacity: 0, y: 14, duration: 0.6 }, 1);
    },
    'ia-hoteles'() {
      const m = h('<div class="en-24"><div class="esf"><i class="ag"></i></div><p class="hh">00:00</p><p class="s">Su recepción, abierta toda la noche</p></div>');
      const hh = m.querySelector('.hh'), o = { m: 0 };
      tl.to(m.querySelector('.ag'), { rotation: 720, duration: 2.2, ease: 'power2.inOut' })
        .to(o, { m: 1439, duration: 2.2, ease: 'power2.inOut', onUpdate: () => { const v = Math.round(o.m); hh.textContent = `${String(Math.floor(v / 60)).padStart(2, '0')}:${String(v % 60).padStart(2, '0')}`; } }, 0)
        .from(m.querySelector('.s'), { opacity: 0, y: 10, duration: 0.6 }, 0.6);
    },
    contacto() {
      const m = h('<div class="en-firma"><p>Hablemos</p><i></i></div>');
      tl.fromTo(m.querySelector('p'), { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1.8, ease: 'power2.inOut' })
        .fromTo(m.querySelector('i'), { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: 'power2.inOut' }, 1.1);
    },
    diagnostico() {
      const m = h(`<div class="en-ocho"><ol>${'<li></li>'.repeat(8)}</ol><p>Ocho preguntas</p></div>`);
      tl.to(m.querySelectorAll('li'), { backgroundColor: 'rgba(214,188,134,1)', scale: 1, duration: 0.25, stagger: 0.2, ease: 'back.out(3)' })
        .from(m.querySelector('p'), { opacity: 0, y: 12, duration: 0.6 }, 0.5);
    },
  };
  (R[pg] || (() => tl.from(h(`<div class="en-casa">${marca ? marca.outerHTML : ''}</div>`), { opacity: 0, scale: 0.9, duration: 1 })))();
  // a cortina sobe e a página fica no seu sítio
  tl.to(ov, { clipPath: 'inset(0% 0% 100% 0%)', duration: 0.8, ease: 'power3.inOut' }, '+=0.2');
  return tl;
  };
  const ov = $('[data-entrada]');
  if (!ov) return;
  if (SITE.reduz || !window.gsap) { ov.remove(); return; }
  const tl = SITE.entrada(ov, ov.dataset.pagina || '', ov.dataset.sector || '', () => ov.remove());
  const acelera = () => { if (tl.progress() < 0.98) tl.timeScale(5); };
  ['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach((ev) => addEventListener(ev, acelera, { once: true, passive: true }));
})();
