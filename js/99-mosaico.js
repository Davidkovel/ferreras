/* Ferreras: los casos en mosaico. Al entrar, las fotografías se descubren una tras otra. Al tocar una, la imagen se abre
   desde su sitio hasta la pantalla entera (clip-path desde el rectángulo de la pieza) y la historia entra al lado;
   anterior/siguiente cambian de caso dentro; × o Esc la devuelven a su sitio. El foco va al cerrar y vuelve a la pieza. */
(() => {
  const { $, $$, reduz } = SITE;
  const mz = $('[data-mz]');
  if (!mz) return;
  const bs = $$('[data-mz-i]', mz), ab = $('[data-mz-ab]'), fEl = $('[data-mz-f]'), txt = $('[data-mz-txt]'), x = $('[data-mz-x]');
  const hs = $$('[data-mz-h]'), n = bs.length;
  const anima = !reduz && window.gsap;
  let atual = -1, origem = null;

  if (anima) gsap.from($$('.mz-t', mz), { clipPath: 'inset(100% 0% 0% 0%)', duration: 1, stagger: 0.08, ease: 'power3.out', scrollTrigger: { trigger: mz, start: 'top 80%', once: true } });

  const recorte = (r) => `inset(${r.top}px ${innerWidth - r.right}px ${innerHeight - r.bottom}px ${r.left}px round 6px)`;
  const enche = (i) => {
    atual = i;
    fEl.innerHTML = bs[i].querySelector('img, .caso-marca').outerHTML;
    const im = fEl.querySelector('img'); if (im) { im.removeAttribute('loading'); im.sizes = '100vw'; }
    txt.innerHTML = hs[i].innerHTML;
  };
  const abre = (i) => {
    origem = bs[i]; enche(i);
    ab.hidden = false; document.documentElement.classList.add('mz-aberto');
    if (SITE.lenis) SITE.lenis.stop();
    x.focus();
    if (!anima) return;
    gsap.fromTo(ab, { clipPath: recorte(origem.getBoundingClientRect()) }, { clipPath: 'inset(0px 0px 0px 0px round 0px)', duration: 0.9, ease: 'power3.inOut' });
    gsap.from($('.mz-ab-t', ab).children, { opacity: 0, y: 30, duration: 0.7, stagger: 0.08, delay: 0.45, ease: 'power3.out' });
  };
  const fecha = () => {
    if (ab.hidden) return;
    const acaba = () => { ab.hidden = true; document.documentElement.classList.remove('mz-aberto'); if (SITE.lenis) SITE.lenis.start(); bs[atual].focus(); };
    if (!anima) return acaba();
    gsap.to(ab, { clipPath: recorte(bs[atual].getBoundingClientRect()), duration: 0.7, ease: 'power3.inOut', onComplete: acaba });
  };
  const muda = (d) => {
    const i = (atual + d + n) % n;
    if (!anima) return enche(i);
    gsap.to([fEl, txt], { opacity: 0, duration: 0.25, onComplete: () => { enche(i); gsap.to([fEl, txt], { opacity: 1, duration: 0.45 }); } });
  };
  bs.forEach((b, i) => b.addEventListener('click', () => abre(i)));
  x.addEventListener('click', fecha);
  $('[data-mz-ant]').addEventListener('click', () => muda(-1));
  $('[data-mz-prox]').addEventListener('click', () => muda(1));
  addEventListener('keydown', (e) => {
    if (ab.hidden) return;
    if (e.key === 'Escape') fecha();
    if (e.key === 'ArrowRight') muda(1);
    if (e.key === 'ArrowLeft') muda(-1);
  });
})();
