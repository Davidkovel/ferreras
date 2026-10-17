/* Ferreras: el mapa de los sectores. Cuando entra en pantalla, desde la casa en Barcelona se dibujan las rutas y se
   encienden los lugares donde ya hemos trabajado, uno tras otro; el mapa respira con el scroll. Sin interacción. */
(() => {
  const { $, $$, reduz } = SITE;
  const m = $('[data-mapa]');
  if (!m) return;
  if (reduz || !window.gsap) { m.classList.add('aceso'); return; }
  const rotas = $$('.mp-rota', m), pontos = $$('.mp-ponto', m), terra = $('.mp-terra', m);
  gsap.set(rotas, { strokeDashoffset: 1 });
  gsap.set(pontos, { opacity: 0 });
  gsap.timeline({ scrollTrigger: { trigger: m, start: 'top 70%', once: true } })
    .fromTo(terra, { opacity: 0, scale: 1.06, transformOrigin: '60% 60%' }, { opacity: 1, scale: 1, duration: 1.4, ease: 'power3.out' })
    .to(pontos[0], { opacity: 1, duration: 0.5 }, 0.6)
    .to(rotas, { strokeDashoffset: 0, duration: 1.4, stagger: 0.35, ease: 'power2.inOut' }, 0.9)
    .to(pontos.slice(1), { opacity: 1, duration: 0.5, stagger: 0.35 }, 1.9)
    .add(() => m.classList.add('aceso'));
  gsap.fromTo(terra, { y: 30 }, { y: -30, ease: 'none', scrollTrigger: { trigger: m, start: 'top bottom', end: 'bottom top', scrub: true } });
})();
