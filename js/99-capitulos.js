/* Ferreras: los capítulos de la portada. Al llegar con el scroll a cada parte grande (Marketing, IA, el rodaje, los
   sectores, la marca, las ocho preguntas) aparece durante poco más de un segundo su propia entrada, la misma que abre su
   página (visor de cámara, idiomas, contador, columnas, la marca que se dibuja, ocho puntos), y la cortina sube.
   Una sola cada vez, sólo una vez por visita; un gesto la acelera; no corre para lo que ya quedó atrás al cargar. */
(() => {
  const { $, reduz } = SITE;
  if (reduz || !window.gsap || !SITE.entrada || !$('[data-hero]')) return;
  const CAP = [['.mundos .pt-mkt', 'marketing'], ['.mundos .pt-ia', 'inteligencia-artificial'], ['#trabajo', 'casos'],
               ['.p-sect', 'sectores'], ['.p-marca', 'la-casa'], ['#diagnostico', 'diagnostico']];
  const yCarga = scrollY, t0 = performance.now();
  let atual = null;
  const corre = (pg) => {
    if (atual) atual.progress(1);
    const ov = document.createElement('div');
    ov.className = 'entrada capitulo'; ov.setAttribute('aria-hidden', 'true');
    document.body.append(ov);
    const tl = SITE.entrada(ov, pg, '', () => { ov.remove(); if (atual === tl) atual = null; });
    tl.timeScale(1.8);
    atual = tl;
    const acelera = () => tl.isActive() && tl.timeScale(5);
    addEventListener('wheel', acelera, { once: true, passive: true });
    addEventListener('touchmove', acelera, { once: true, passive: true });
  };
  CAP.forEach(([sel, pg]) => {
    const el = $(sel);
    if (!el) return;
    ScrollTrigger.create({
      trigger: el, start: 'top 65%', once: true,
      onEnter: () => {
        // o que já ficou acima ao abrir a página (voltar atrás, âncora) não tem entrada
        if (performance.now() - t0 < 1200 || el.getBoundingClientRect().top + scrollY < yCarga) return;
        corre(pg);
      },
    });
  });
})();
