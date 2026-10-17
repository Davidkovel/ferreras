/* Ferreras: la portada guía con la cabecera. Después de que el reloj 3D entra en el hero, las pestañas de la cabecera
   aparecen una a una; con el scroll se enciende la pestaña de la parte que se está leyendo, y el reloj pequeño
   (93-reloj3d.js, modo «mini») recibe su nombre por el evento «ferreras:secao». */
(() => {
  const { $, $$, reduz } = SITE;
  if (!$('[data-hero]') || !window.gsap) return;
  const links = $$('.topo-lado a');
  const link = (h) => links.find((a) => (a.getAttribute('href') || '').replace(/^\.\//, '') === h);
  if (!reduz) {
    gsap.set(links, { opacity: 0, y: -14 });
    gsap.to(links, { opacity: 1, y: 0, duration: 0.8, stagger: 0.14, ease: 'power3.out', delay: 2.4 });
  }
  const MAPA = [['.mundos .pt-mkt', 'marketing/', 'Marketing'], ['.mundos .pt-ia', 'inteligencia-artificial/', 'Inteligencia artificial'],
                ['#trabajo', 'casos/', 'Rodaje'], ['.p-mit', null, 'Mediodía'], ['.p-sect', 'sectores/', 'Sectores'],
                ['.p-marca', 'la-casa/', 'Relojes Ferreras'], ['#diagnostico', null, 'Ocho preguntas']];
  let atual = '';
  const marca = (h, nome) => {
    if (nome === atual) return;
    atual = nome;
    links.forEach((a) => a.classList.toggle('agora', !!h && a === link(h)));
    dispatchEvent(new CustomEvent('ferreras:secao', { detail: nome }));
  };
  MAPA.forEach(([sel, h, nome]) => {
    const el = $(sel);
    if (el) ScrollTrigger.create({ trigger: el, start: 'top 55%', end: 'bottom 55%', onToggle: (s) => s.isActive && marca(h, nome) });
  });
  ScrollTrigger.create({ trigger: '[data-hero]', start: 'top top', end: 'bottom 55%', onToggle: (s) => s.isActive && marca(null, '') });
})();
