/* Ferreras: luz. Una capa encima del núcleo, con GSAP + ScrollTrigger + Lenis (en vendor/, sin CDN):
   scroll con inercia, la luz que sigue al ratón por las secciones de noche, destellos de cine sobre el filme del hero,
   el reflejo que cruza el cristal del reloj con el scroll, fotografías con profundidad y botones magnéticos.
   Sólo se escriben transform, opacity y variables CSS; con «reducir movimiento» no se carga nada de esto. */
(() => {
  const { $, $$, reduz } = SITE;
  if (reduz || !window.gsap) return;
  const { gsap } = window;
  gsap.registerPlugin(ScrollTrigger);
  const raton = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- scroll con inercia (sólo rueda y trackpad; el dedo sigue nativo) ---------- */
  if (window.Lenis && raton) {
    document.documentElement.classList.remove('suave');
    $$('.carril, .menu, [data-diag], .chat-lista').forEach((el) => el.setAttribute('data-lenis-prevent', ''));
    const lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.95, anchors: { offset: -80 } });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    SITE.lenis = lenis;
    // el menú de pantalla entera para el scroll de la página mientras está abierto
    const menu = $('[data-menu]');
    if (menu) new MutationObserver(() => (menu.hidden ? lenis.start() : lenis.stop())).observe(menu, { attributes: true, attributeFilter: ['hidden'] });
  }

  /* ---------- la luz que sigue al ratón: una linterna cálida sobre la noche ---------- */
  if (raton) {
    const foco = document.createElement('div');
    foco.className = 'foco'; foco.setAttribute('aria-hidden', 'true');
    document.body.append(foco);
    const fx = gsap.quickTo(foco, 'x', { duration: 0.9, ease: 'power3' });
    const fy = gsap.quickTo(foco, 'y', { duration: 0.9, ease: 'power3' });
    let visto = false;
    addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      if (!visto) { gsap.set(foco, { x: e.clientX, y: e.clientY }); visto = true; }
      fx(e.clientX); fy(e.clientY);
      foco.classList.add('on');
    }, { passive: true });
    document.addEventListener('pointerleave', () => foco.classList.remove('on'));
    // sobre el marfil la linterna se apaga: allí la luz ya es el papel
    $$('[data-claro], .claro').forEach((sec) => ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%', toggleClass: { targets: foco, className: 'sobre-claro' } }));
  }

  /* ---------- destellos de cine sobre el filme del hero (luz que entra por el objetivo) ---------- */
  const hero = $('[data-hero]');
  if (hero) {
    const luz = document.createElement('div');
    luz.className = 'hero-luz'; luz.setAttribute('aria-hidden', 'true');
    luz.innerHTML = '<i class="hl-a"></i><i class="hl-b"></i><i class="hl-raya"></i>';
    $('.hero-velo', hero).after(luz);
    // al bajar, la luz se abre como cuando el coche sale del túnel
    gsap.to(luz, { '--abre': 1, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* ---------- el reflejo que cruza el cristal del reloj grande con el scroll ---------- */
  $$('.marca-reloj .reloj, .trofeu .reloj, .al-reloj .reloj').forEach((r) => {
    const d = document.createElement('div');
    d.className = 'destello'; d.setAttribute('aria-hidden', 'true');
    r.append(d);
    gsap.fromTo(d, { xPercent: -120 }, { xPercent: 120, ease: 'none', scrollTrigger: { trigger: r, start: 'top 90%', end: 'bottom 10%', scrub: 0.6 } });
  });

  /* ---------- fotografías con profundidad: la imagen se mueve más despacio que su ventana ---------- */
  $$('.dep-foto img, .marca-c .ventana img, .est-foto img, .sx-media img, .cc-foto img, .placa-foto img, .pag-media img').forEach((im) => {
    im.classList.add('prof');
    gsap.fromTo(im, { '--py': '-7%' }, { '--py': '7%', ease: 'none', scrollTrigger: { trigger: im.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- las cifras en contorno (24 h, 100, BCN) derivan despacio: van por detrás de todo ---------- */
  $$('.contorno').forEach((c, i) => gsap.fromTo(c, { '--dx': (i % 2 ? -6 : 6) + 'vw' }, { '--dx': (i % 2 ? 6 : -6) + 'vw', ease: 'none', scrollTrigger: { trigger: c.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));

  /* ---------- títulos: la palabra en oro recibe un reflejo cuando entra ---------- */
  $$('.titulo em').forEach((em) => {
    em.classList.add('reflejo');
    ScrollTrigger.create({ trigger: em, start: 'top 85%', once: true, onEnter: () => em.classList.add('brilla') });
  });

  /* ---------- botones magnéticos y con brillo ---------- */
  if (raton) $$('.btn').forEach((b) => {
    if (b.closest('.barra-dx')) return; // la barra fija ya usa transform para entrar
    const bx = gsap.quickTo(b, 'x', { duration: 0.5, ease: 'power3' }), by = gsap.quickTo(b, 'y', { duration: 0.5, ease: 'power3' });
    b.addEventListener('pointermove', (e) => {
      const r = b.getBoundingClientRect();
      bx((e.clientX - r.left - r.width / 2) * 0.22); by((e.clientY - r.top - r.height / 2) * 0.32);
    });
    b.addEventListener('pointerleave', () => { gsap.to(b, { x: 0, y: 0, duration: 0.9, ease: 'elastic.out(1, 0.45)' }); });
  });

  /* ---------- cursor: un aro que sigue al ratón con retardo, crece sobre lo que se pulsa y dice qué hace
     (awwwards-3d, patrón 18). Es un añadido: el cursor del sistema sigue ahí y en pantallas táctiles no existe ---------- */
  if (raton) {
    const cur = document.createElement('div');
    cur.className = 'cursor'; cur.setAttribute('aria-hidden', 'true'); cur.innerHTML = '<span></span>';
    document.body.append(cur);
    const rot = cur.firstChild;
    const cx = gsap.quickTo(cur, 'x', { duration: 0.35, ease: 'power3' }), cy = gsap.quickTo(cur, 'y', { duration: 0.35, ease: 'power3' });
    addEventListener('pointermove', (e) => { if (e.pointerType !== 'mouse') return; cx(e.clientX); cy(e.clientY); cur.classList.add('on'); }, { passive: true });
    document.addEventListener('pointerleave', () => cur.classList.remove('on'));
    const diz = (el) => (el.closest('.carril') ? 'Arrastrar' : el.closest('[data-rx]') ? 'Deslizar' : el.closest('.sect a, .cc, .puerta, .marca-c, .pilar') ? 'Ver' : '');
    document.addEventListener('pointerover', (e) => {
      const alvo = e.target.closest('a, button, [data-rx], .carril, label, input, textarea');
      const t = alvo ? diz(e.target) : '';
      cur.classList.toggle('sobre', !!alvo);
      cur.classList.toggle('com-rotulo', !!t);
      if (t && rot.textContent !== t) rot.textContent = t;
    });
  }

  // cuando el núcleo vuelve a medir (imágenes, fuentes), los disparadores también
  addEventListener('load', () => ScrollTrigger.refresh());
})();
