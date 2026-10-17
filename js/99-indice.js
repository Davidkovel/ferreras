/* Ferreras: el índice de los casos. Con ratón, la tarjeta del caso sigue al cursor por encima de la lista (con inercia,
   inclinándose según la velocidad); clic en una línea abre o cierra su detalle. En pantallas táctiles sólo el detalle. */
(() => {
  const { $, $$, reduz } = SITE;
  const ic = $('[data-ic]');
  if (!ic) return;
  const fs = $$('[data-ic-i]', ic), card = $('[data-ic-card]', ic), cs = $$('[data-ic-c]', ic);
  fs.forEach((b) => b.addEventListener('click', () => {
    const d = document.getElementById(b.getAttribute('aria-controls')), abre = b.getAttribute('aria-expanded') !== 'true';
    b.setAttribute('aria-expanded', abre); d.hidden = !abre;
    if (abre && window.gsap && !reduz) gsap.from(d, { height: 0, opacity: 0, duration: 0.6, ease: 'power3.out', clearProps: 'height,opacity' });
    if (SITE.remede) SITE.remede();
  }));
  if (reduz || !window.gsap || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const qx = gsap.quickTo(card, 'x', { duration: 0.55, ease: 'power3' }), qy = gsap.quickTo(card, 'y', { duration: 0.55, ease: 'power3' });
  const qr = gsap.quickTo(card, 'rotation', { duration: 0.8, ease: 'power3' });
  let lx = 0, visto = false;
  ic.addEventListener('pointermove', (e) => {
    if (!visto) { gsap.set(card, { x: e.clientX, y: e.clientY }); visto = true; }
    qx(e.clientX); qy(e.clientY); qr(Math.max(-12, Math.min(12, (e.clientX - lx) * 0.6))); lx = e.clientX;
  }, { passive: true });
  fs.forEach((b) => b.addEventListener('pointerenter', () => {
    const k = b.dataset.icI;
    cs.forEach((c) => c.classList.toggle('on', c.dataset.icC === k));
    card.classList.add('on'); ic.classList.add('a-ver');
    $$('.ic-i', ic).forEach((li) => li.classList.toggle('foco', li.contains(b)));
  }));
  $('.ic-l', ic).addEventListener('pointerleave', () => { card.classList.remove('on'); ic.classList.remove('a-ver'); qr(0); visto = false; });
})();
