/* Ferreras: los dos mundos de la portada (Marketing e IA). Cada uno se abre al entrar en pantalla: la ventana pasa de un
   rectángulo con margen a pantalla entera, la imagen se asienta y el texto sube. Sólo clip-path, transform y opacity. */
(() => {
  const { $$, reduz } = SITE;
  if (reduz || !window.gsap) return;
  // a noite da IA começa azul e acaba em laranja: o contraste acontece à vista, com o scroll
  const ia = document.querySelector('[data-mundos] .pt-ia');
  if (ia) gsap.fromTo(ia, { '--ia-1': '#0f1830', '--ia-2': '#05070d' }, { '--ia-1': '#e0641c', '--ia-2': '#4a1606', duration: 2.4, ease: 'power2.inOut', delay: 0.4,
    scrollTrigger: { trigger: ia, start: 'top 25%', toggleActions: 'play none none reverse' } });
  $$('[data-mundos] .pt-mundo').forEach((m) => {
    const media = m.querySelector('.filme, .pt-ia-fundo'), txt = m.querySelector('.pt-txt');
    gsap.timeline({ scrollTrigger: { trigger: m, start: 'top 85%', end: 'top 15%', scrub: 0.7 } })
      .fromTo(m, { clipPath: 'inset(9% 7% 9% 7% round 18px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'power2.out' }, 0)
      .fromTo(media, { scale: 1.18 }, { scale: 1, ease: 'none' }, 0)
      .fromTo(txt, { y: 70, opacity: 0 }, { y: 0, opacity: 1, ease: 'power3.out' }, 0.35);
  });
})();
