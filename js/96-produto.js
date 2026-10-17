/* Ferreras: el producto. Las doce horas (Marketing e IA): cada hora es un servicio; la aguja va hasta la elegida y el
   centro de la esfera lo cuenta; mientras nadie toca, avanza sola cada pocos segundos (sólo a la vista y sin «reducir
   movimiento»). La gama a escala (Web): los planes como relojes de distinto tamaño; tocar uno abre su ficha. */
(() => {
  const { $, $$, reduz } = SITE;

  $$('[data-doce]').forEach((dc) => {
    const bs = $$('[data-h]', dc), centro = $('.doce-c', dc), tpl = $$('[data-hora-t]', dc);
    let i = 0, tocou = false, visto = false, giro = 0;
    const vai = (k, foco) => {
      k = (k + 12) % 12;
      // a agulha anda sempre para a frente, como num relógio
      giro += ((k - i + 12) % 12) || (k === i ? 0 : 12);
      i = k;
      dc.style.setProperty('--giro', giro);
      bs.forEach((b, n) => b.setAttribute('aria-pressed', n === k));
      centro.classList.remove('entra'); void centro.offsetWidth;
      centro.innerHTML = tpl[k].innerHTML; centro.classList.add('entra');
      if (foco) bs[k].focus();
    };
    bs.forEach((b, n) => b.addEventListener('click', () => { tocou = true; vai(n); }));
    dc.addEventListener('keydown', (e) => {
      if (!e.target.matches('[data-h]')) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); tocou = true; vai(i + 1, true); }
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); tocou = true; vai(i - 1, true); }
    });
    $('[data-doce-ant]', dc).addEventListener('click', () => { tocou = true; vai(i - 1); });
    $('[data-doce-prox]', dc).addEventListener('click', () => { tocou = true; vai(i + 1); });
    dc.addEventListener('pointerenter', () => { tocou = true; });
    new IntersectionObserver(([en]) => { visto = en.isIntersecting; }, { threshold: 0.4 }).observe(dc);
    if (!reduz) setInterval(() => { if (visto && !tocou && !document.hidden) vai(i + 1); }, 3600);
  });

  $$('[data-gama]').forEach((g) => {
    const ts = $$('[data-gama-t]', g);
    const escolhe = (t, foco) => {
      ts.forEach((x) => {
        const on = x === t;
        x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        const f = document.getElementById(x.getAttribute('aria-controls'));
        f.hidden = !on;
        if (on) { f.classList.remove('entra'); void f.offsetWidth; f.classList.add('entra'); }
      });
      if (foco) t.focus();
      if (SITE.remede) SITE.remede();
    };
    ts.forEach((t, n) => {
      t.addEventListener('click', () => escolhe(t));
      t.addEventListener('keydown', (e) => {
        const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (d) { e.preventDefault(); escolhe(ts[(n + d + ts.length) % ts.length], true); }
      });
    });
  });
})();
