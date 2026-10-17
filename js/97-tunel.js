/* Ferreras: el producto en 3D con el scroll (CSS 3D + GSAP ScrollTrigger, sin WebGL).
   · El túnel de los casos: la cámara avanza; cada caso llega desde el fondo, alternando lados, y el más cercano se cuenta
     en el panel. Los sectores de la derecha llevan la cámara a su primer caso. El ratón inclina la cámara.
   · El anillo de los doce servicios: gira con el scroll como el bisel de un reloj; el de delante se cuenta debajo.
   Sólo se escriben transform y opacity. Con «reducir movimiento» no se carga y el CSS deja una lista legible. */
(() => {
  const { $, $$, reduz } = SITE;
  if (reduz || !window.gsap) return;
  const raton = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const irA = (y) => (SITE.lenis ? SITE.lenis.scrollTo(y, { duration: 1.6 }) : scrollTo({ top: y, behavior: 'smooth' }));

  /* ---------- el túnel ---------- */
  $$('[data-tunel]').forEach((sec) => {
    const mundo = $('[data-tn-mundo]', sec), cam = $('[data-tn-cam]', sec), info = $('[data-tn-info]', sec), num = $('[data-tn-n]', sec);
    const casos = $$('[data-tn-caso]', sec), pals = $$('.tn-pal', sec), tpl = $$('[data-tn-t]', sec), irs = $$('[data-tn-ir]', sec);
    const n = casos.length;
    const D = () => Math.max(900, innerWidth * 0.95);            // distancia entre casos, en profundidad
    let activo = -1;
    const mostra = (k) => {
      if (k === activo) return;
      activo = k;
      info.classList.remove('entra'); void info.offsetWidth;
      info.innerHTML = tpl[k].innerHTML; info.classList.add('entra');
      num.textContent = k + 1;
      const s = casos[k].dataset.sector;
      irs.forEach((b) => b.setAttribute('aria-current', casos[+b.dataset.tnIr].dataset.sector === s));
    };
    const pinta = (p) => {
      const d = D(), z = p * (n - 1) * d;
      mundo.style.transform = `translate3d(0,0,${z.toFixed(1)}px)`;
      casos.forEach((c, i) => {
        const rel = z - i * d;                                     // > 0: ya pasó la cámara
        const op = rel > 0 ? Math.max(0, 1 - rel / (d * 0.45)) : Math.max(0, 1 + rel / (d * 3.2));
        c.style.opacity = op.toFixed(3);
        c.style.visibility = op < 0.01 ? 'hidden' : 'visible';
      });
      pals.forEach((w, i) => { const rel = z - i * d; w.style.opacity = (rel > 0 ? Math.max(0, 1 - rel / (d * 0.6)) : Math.max(0, 1 + rel / (d * 2))).toFixed(3); });
      mostra(Math.min(n - 1, Math.max(0, Math.ceil(z / d - 0.2))));   // o primeiro caso que ainda está à frente da câmara
    };
    // os casos ficam no espaço uma vez (a distância depende da largura)
    const coloca = () => {
      const d = D();
      casos.forEach((c, i) => { c.style.transform = `translate3d(calc(-50% + ${c.style.getPropertyValue('--lado') * 17}vw), -50%, ${-i * d}px)`; });
      pals.forEach((w, i) => { w.style.transform = `translate3d(calc(-50% + ${w.style.getPropertyValue('--lado') * 30}vw), -50%, ${-i * d - d * 0.5}px)`; });
    };
    coloca(); addEventListener('resize', coloca);
    const st = ScrollTrigger.create({ trigger: sec, start: 'top top', end: 'bottom bottom', scrub: 0.6, onUpdate: (self) => pinta(self.progress), onRefresh: (self) => pinta(self.progress) });
    pinta(0);
    sec.classList.add('vivo');
    irs.forEach((b) => b.addEventListener('click', () => { const k = +b.dataset.tnIr; irA(st.start + (k / (n - 1)) * (st.end - st.start) + 2); }));
    if (raton) {
      const ry = gsap.quickTo(cam, 'rotationY', { duration: 1.2, ease: 'power3' }), rx = gsap.quickTo(cam, 'rotationX', { duration: 1.2, ease: 'power3' });
      sec.addEventListener('pointermove', (e) => { ry((e.clientX / innerWidth - 0.5) * 7); rx(-(e.clientY / innerHeight - 0.5) * 5); }, { passive: true });
      sec.addEventListener('pointerleave', () => { ry(0); rx(0); });
    }
  });

  /* ---------- el anillo ---------- */
  $$('[data-anel]').forEach((el) => {
    const roda = $('[data-an-roda]', el), cs = $$('.an-c', el), tpl = $$('[data-an-t]', el), info = $('[data-an-info]', el);
    let activo = 0;
    const pinta = (p) => {
      const rot = -p * 330;
      roda.style.setProperty('--rot', rot.toFixed(2) + 'deg');
      cs.forEach((c, i) => {
        const dif = (((i * 30 + rot) % 360) + 540) % 360 - 180;    // ângulo até à frente, -180..180
        const f = Math.max(0, Math.cos((dif * Math.PI) / 180));
        c.style.opacity = (0.18 + 0.82 * f * f).toFixed(3);
        c.classList.toggle('frente', Math.abs(dif) < 15);
      });
      const k = Math.min(11, Math.max(0, Math.round(p * 11)));
      if (k !== activo) { activo = k; info.classList.remove('entra'); void info.offsetWidth; info.innerHTML = tpl[k].innerHTML; info.classList.add('entra'); }
    };
    ScrollTrigger.create({ trigger: el, start: 'top top', end: 'bottom bottom', scrub: 0.6, onUpdate: (self) => pinta(self.progress), onRefresh: (self) => pinta(self.progress) });
    pinta(0);
    el.classList.add('vivo');
  });
})();
