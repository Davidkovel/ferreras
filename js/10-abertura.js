(() => {
  const { $, $$, reduz } = SITE;
  /* ---------- APERTURA: sobre el vídeo de los coches, una estela de luz (la de unos faros) cruza la pantalla y cada
     letra del logotipo nace cuando la cabeza de la estela pasa por debajo; después el logotipo vuela a la cabecera
     (FLIP: sólo transform). Una vez por sesión. Nunca bloquea el scroll: cualquier gesto la termina en el acto. ---------- */
  const ab = $('[data-abertura]'), hero = $('[data-hero]');
  const termina = () => { document.body.classList.remove('a-abrir'); hero && hero.classList.add('pronto'); SITE.aberto(); };
  let vista = false;
  try { vista = sessionStorage.getItem('ferreras.abertura') === '1'; } catch (e) {}
  // volver con «atrás» a mitad de página o abrir con #ancla: directo, sin apertura
  if (!ab || reduz || vista || scrollY > 40 || location.hash) { ab && ab.remove(); termina(); return; }
  try { sessionStorage.setItem('ferreras.abertura', '1'); } catch (e) {}

  const D = 1500;                              // la estela tarda esto en cruzar la pantalla
  const E = [0.62, 0.04, 0.3, 1];              // acelera como un coche al salir y frena al llegar (la misma curva en CSS)
  ab.style.setProperty('--t-rasto', D + 'ms');
  ab.style.setProperty('--e-rasto', `cubic-bezier(${E.join(',')})`);
  // inversa de la curva: en qué momento la cabeza llega a la fracción f del ancho
  const bz = (t, a, b) => 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3;
  const quando = (f) => { let t = 0; while (t < 1 && bz(t, E[1], E[3]) < f) t += 0.005; return bz(t, E[0], E[2]); };

  const T = SITE.token('--t-toque');
  const espera = (ms) => new Promise((r) => setTimeout(r, ms));
  const quadros = (n) => new Promise((r) => { const f = () => (--n <= 0 ? r() : requestAnimationFrame(f)); requestAnimationFrame(f); });
  const caixa = $('.caja', ab), rw = $('.rasto-w', ab);
  let pousou = false;
  const pousa = () => {
    if (pousou) return; pousou = true;
    // el logotipo de la cabecera aparece debajo en el mismo píxel; sólo después se apaga el que voló
    document.body.classList.remove('a-abrir');
    hero && hero.classList.add('pronto');
    ab.classList.add('pousou');
    SITE.aberto();
    gestos.forEach((g) => removeEventListener(g, salta, true));
    setTimeout(() => ab.remove(), T * 3);
  };
  const salta = () => { ab.classList.add('rapido'); pousa(); };
  const gestos = ['wheel', 'touchstart', 'pointerdown', 'keydown'];
  gestos.forEach((g) => addEventListener(g, salta, { passive: true, capture: true }));
  setTimeout(pousa, 6000); // garantía

  Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), espera(400)])
    .then(() => quadros(2))
    .then(() => {
      if (pousou) return;
      const a = caixa.getBoundingClientRect(), W = innerWidth;
      rw.style.top = Math.round(a.bottom + Math.max(10, a.height * 0.12)) + 'px';
      $$('.pz,.pz-senal,.letra', ab).forEach((p) => {
        const r = p.getBoundingClientRect();
        p.style.animationDelay = Math.round(quando((r.left + r.width * 0.35) / W) * D) + 'ms';
      });
      ab.classList.add('monta');
      return espera(D + 380);
    })
    .then(() => {
      if (pousou) return;
      const alvo = $('[data-logo-alvo] svg');
      const a = caixa.getBoundingClientRect(), b = alvo.getBoundingClientRect();
      ab.classList.add('solta');
      caixa.style.transform = `translate3d(${b.left - a.left}px,${b.top - a.top}px,0) scale(${b.width / a.width})`;
      hero && hero.classList.add('pronto');
      caixa.addEventListener('transitionend', (e) => e.propertyName === 'transform' && pousa());
      setTimeout(pousa, T * 7.5);
    });
})();
