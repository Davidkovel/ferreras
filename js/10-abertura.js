(() => {
  const { $, $$, reduz } = SITE;
  /* ---------- APERTURA: la F se monta pieza a pieza, la señal azul cae en su sitio, las letras suben
     y el logotipo vuela a la cabecera (FLIP: sólo transform). Una vez por sesión; después, directo. ---------- */
  const ab = $('[data-abertura]'), hero = $('[data-hero]');
  const termina = () => { document.body.classList.remove('a-abrir'); hero && hero.classList.add('pronto'); SITE.aberto(); };
  let vista = false;
  try { vista = sessionStorage.getItem('ferreras.abertura') === '1'; } catch (e) {}
  if (!ab || reduz || vista) { ab && ab.remove(); termina(); return; }
  try { sessionStorage.setItem('ferreras.abertura', '1'); } catch (e) {}

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  scrollTo(0, 0);
  const raiz = document.documentElement;
  raiz.style.overflow = 'hidden';
  const solta = () => { raiz.style.overflow = ''; };
  setTimeout(solta, 6000); // garantía
  const T = SITE.token('--t-toque');
  const espera = (ms) => new Promise((r) => setTimeout(r, ms));
  const quadros = (n) => new Promise((r) => { const f = () => (--n <= 0 ? r() : requestAnimationFrame(f)); requestAnimationFrame(f); });

  Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), espera(900)])
    .then(() => quadros(2))
    .then(() => { ab.classList.add('monta'); return espera(T * 9.5); })
    .then(() => {
      const caixa = $('.caja', ab), alvo = $('[data-logo-alvo] svg');
      const a = caixa.getBoundingClientRect(), b = alvo.getBoundingClientRect();
      ab.classList.add('solta');
      caixa.style.transform = `translate3d(${b.left - a.left}px,${b.top - a.top}px,0) scale(${b.width / a.width})`;
      hero && hero.classList.add('pronto');
      let pousou = false;
      const pousa = () => {
        if (pousou) return; pousou = true;
        // el logotipo de la cabecera aparece debajo en el mismo píxel; sólo después se apaga el que voló
        document.body.classList.remove('a-abrir');
        ab.classList.add('pousou');
        solta();
        SITE.aberto();
        setTimeout(() => ab.remove(), T * 2);
      };
      caixa.addEventListener('transitionend', (e) => e.propertyName === 'transform' && pousa());
      setTimeout(pousa, T * 9);
    });
})();
