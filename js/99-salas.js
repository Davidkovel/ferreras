/* Ferreras: las salas de producto. Marketing es un proyector: la película corre con el scroll y el fotograma que pasa por
   la ventana se abre en pantalla entera (se descubre de abajo arriba, como un obturador), con su código de tiempo.
   IA es una constelación: doce puntos en una esfera que gira con el scroll; el que llega al frente se enciende.
   Sólo transform, opacity y clip-path; con «reducir movimiento» queda la lista. */
(() => {
  const { $, $$, reduz } = SITE;
  if (reduz || !window.gsap) return;
  const troca = (el, html) => { el.classList.remove('entra'); void el.offsetWidth; el.innerHTML = html; el.classList.add('entra'); };

  /* ---------- el proyector ---------- */
  // no telemóvel o projector dá lugar à lista (CSS); só o computador projecta
  if (matchMedia('(min-width: 801px)').matches) $$('[data-proj]').forEach((el) => {
    const telas = $$('[data-pj-tela]', el), tpl = $$('[data-pj-t]', el), txt = $('[data-pj-txt]', el), rolo = $('[data-pj-rolo]', el), tc = $('[data-pj-tc]', el);
    const n = telas.length, prog = $$('.pj-prog i', el);
    let k = -1;
    const pinta = (p) => {
      const f = $('.pj-f', rolo), h = f ? f.offsetHeight + parseFloat(getComputedStyle(rolo).rowGap || 0) : 0;
      rolo.style.transform = `translate3d(0,${(-p * (n - 1) * h).toFixed(1)}px,0)`;
      const quadros = Math.round(p * (n - 1) * 3 * 25);
      tc.textContent = `00:00:${String(Math.floor(quadros / 25)).padStart(2, '0')}:${String(quadros % 25).padStart(2, '0')}`;
      // cada fotograma acende-se quando passa pela janela: opacidade e escala presas ao scroll, sem estado
      const pos = p * (n - 1);
      telas.forEach((t, i) => { const d = Math.abs(pos - i); const o = Math.max(0, 1 - d * 1.6); t.style.opacity = o.toFixed(3); t.style.transform = `scale(${(1 + Math.min(d, 1) * 0.08).toFixed(4)})`; t.style.zIndex = o > 0 ? Math.round(o * 10) : 0; });
      const i = Math.min(n - 1, Math.max(0, Math.round(pos)));
      if (i !== k) { k = i; troca(txt, tpl[i].innerHTML); prog.forEach((x, n) => x.classList.toggle('on', n <= i)); }
    };
    ScrollTrigger.create({ trigger: el, start: 'top top', end: 'bottom bottom', scrub: 0.5, onUpdate: (s) => pinta(s.progress), onRefresh: (s) => pinta(s.progress) });
    el.classList.add('vivo');
    pinta(0);
  });

  /* ---------- la constelación ---------- */
  $$('[data-const]').forEach((el) => {
    const nos = $$('[data-ct-no]', el), tpl = $$('[data-ct-t]', el), txt = $('[data-ct-txt]', el), svg = $('[data-ct-linhas]', el), palco = $('.ct-palco', el);
    const n = nos.length;
    // longitude de 30 em 30 graus (o scroll traz cada um à frente pela ordem), latitudes a ondular
    const P = nos.map((_, i) => ({ lon: (i * 30 * Math.PI) / 180, lat: Math.sin(i * 1.7) * 0.62 }));
    const pares = [];
    for (let i = 0; i < n; i++) { pares.push([i, (i + 1) % n]); if (i % 2 === 0) pares.push([i, (i + 5) % n]); }
    svg.innerHTML = pares.map(() => '<line/>').join('');
    const linhas = $$('line', svg);
    let k = -1, rot = 0, alvo = 0, mx = 0, my = 0, ultimo = performance.now(), visivel = false;
    new IntersectionObserver(([e]) => { visivel = e.isIntersecting; }).observe(el);
    ScrollTrigger.create({ trigger: el, start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: (s) => { alvo = -s.progress * (n - 1) * (Math.PI / 6); const i = Math.round(s.progress * (n - 1)); if (i !== k) { k = i; troca(txt, tpl[i].innerHTML); nos.forEach((x, j) => x.classList.toggle('frente', j === i)); } } });
    el.addEventListener('pointermove', (e) => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; }, { passive: true });
    const passo = (agora) => {
      requestAnimationFrame(passo);
      const dt = Math.min(64, agora - ultimo); ultimo = agora;
      if (!visivel) return;
      rot += (alvo - rot) * (1 - Math.exp(-dt / 140));
      const W = palco.clientWidth, H = palco.clientHeight, R = Math.min(W * 0.32, H * 0.36), cx = W * (W > 800 ? 0.62 : 0.5), cy = H * (W > 800 ? 0.5 : 0.36);
      const inc = 0.32 + my * 0.3, ca = Math.cos(inc), sa = Math.sin(inc), f = R * 3.2;
      const pos = P.map((p) => {
        const a = p.lon + rot + mx * 0.4;
        let x = Math.cos(p.lat) * Math.sin(a), y = Math.sin(p.lat), z = Math.cos(p.lat) * Math.cos(a);
        const y2 = y * ca - z * sa, z2 = y * sa + z * ca;
        const esc = f / (f - z2 * R);
        return { x: cx + x * R * esc, y: cy + y2 * R * esc, z: z2, esc };
      });
      nos.forEach((no, i) => {
        const q = pos[i];
        no.style.transform = `translate3d(${q.x.toFixed(1)}px,${q.y.toFixed(1)}px,0) scale(${(0.55 + 0.45 * q.esc).toFixed(3)})`;
        no.style.opacity = (0.25 + 0.75 * ((q.z + 1) / 2)).toFixed(3);
        no.style.zIndex = Math.round((q.z + 1) * 50);
      });
      linhas.forEach((l, j) => {
        const [a, b] = pares[j], A = pos[a], B = pos[b];
        l.setAttribute('x1', A.x.toFixed(1)); l.setAttribute('y1', A.y.toFixed(1)); l.setAttribute('x2', B.x.toFixed(1)); l.setAttribute('y2', B.y.toFixed(1));
        l.style.opacity = (0.08 + 0.32 * ((A.z + B.z + 2) / 4)).toFixed(3);
      });
    };
    requestAnimationFrame(passo);
    el.classList.add('vivo');
  });
})();
