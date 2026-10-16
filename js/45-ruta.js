(() => {
  const { $, $$, reduz, clamp, ecra } = SITE;
  /* ---------- LA RUTA (home, computador): un GT3 visto desde arriba sale de «Qué hacemos», baja por el arcén izquierdo
     detrás del scroll, entra en los túneles (el interludio y el raio X: pasa por debajo y sale por el otro lado) y
     termina en la carretera del diagnóstico, donde se convierte en el marcador de los pasos.
     La carretera se calcula una vez por dibujo (Bézier propias, tabla de puntos cada ~4 px; sin getPointAtLength);
     el coche sólo mueve transform; la estela de luz se pinta en un canvas fijo del tamaño de la pantalla. ---------- */
  const ruta = $('[data-ruta]'), cv = $('[data-ruta-luz]');
  if (!ruta || !cv) return;
  const main = ruta.parentElement, svg = $('[data-ruta-svg]', ruta), via = $('[data-ruta-p]', ruta), carro = $('[data-coche]', ruta);
  const ini = $('[data-ruta-ini]'), dj = $('[data-diag]', main), linha = dj && $('.dj-linha', dj);
  const ativo = () => !reduz && innerWidth >= 1100 && ini && linha;
  const cx = cv.getContext('2d');
  let LUT = [], V = 0, cur = -1, vel = 0, pronto = false, chegou = null, mTop = 0, mLeft = 0, dpr = 1;

  // cúbica: devolve pontos a cada ~4 px (com o «v» que avança só com a altura, salvo na curva final)
  const cubica = (a, b, c, d, final, out) => {
    const n = Math.max(8, Math.ceil((Math.hypot(d.x - a.x, d.y - a.y) + Math.hypot(c.x - b.x, c.y - b.y)) / 4));
    for (let k = 1; k <= n; k++) {
      const t = k / n, u = 1 - t;
      const x = u * u * u * a.x + 3 * u * u * t * b.x + 3 * u * t * t * c.x + t * t * t * d.x;
      const y = u * u * u * a.y + 3 * u * u * t * b.y + 3 * u * t * t * c.y + t * t * t * d.y;
      const p = out[out.length - 1];
      out.push({ x, y, v: p.v + (final ? Math.hypot(x - p.x, y - p.y) : Math.abs(y - p.y)) });
    }
  };
  const reta = (a, d, out) => cubica(a, { x: a.x, y: a.y + (d.y - a.y) / 3 }, { x: d.x, y: a.y + (d.y - a.y) * 2 / 3 }, d, false, out);

  function constroi() {
    if (!ativo()) { ruta.hidden = true; cv.hidden = true; document.body.classList.remove('com-ruta'); pronto = false; return; }
    ruta.hidden = false; cv.hidden = false; document.body.classList.add('com-ruta');
    const m = main.getBoundingClientRect(); mTop = m.top + scrollY; mLeft = m.left + scrollX;
    const W = m.width, H = m.height;
    const gut = parseFloat(getComputedStyle(ini.closest('.sec') || main).paddingLeft) || 40;
    const xl = gut / 2, xr = W - gut / 2;
    const ri = ini.getBoundingClientRect(), y0 = ri.top - m.top + 6;
    const tun = $$('[data-ruta-tunel]').map((t) => t.getBoundingClientRect()).filter((r) => r.top - m.top > y0).sort((a, b) => a.top - b.top);
    const rl = linha.getBoundingClientRect(), fim = { x: rl.left - m.left + 6, y: rl.top - m.top + rl.height / 2 };
    const pts = [{ x: xl, y: y0, v: 0 }];
    let x = xl, d = 'M' + xl.toFixed(1) + ' ' + y0.toFixed(1);
    for (const r of tun) {
      const a = r.top - m.top + r.height * 0.18, b = r.bottom - m.top - r.height * 0.18, nx = x === xl ? xr : xl;
      if (a <= pts[pts.length - 1].y + 10 || b >= fim.y - 260) continue;
      reta(pts[pts.length - 1], { x, y: a }, pts);
      const mid = (a + b) / 2;
      cubica({ x, y: a }, { x, y: mid }, { x: nx, y: mid }, { x: nx, y: b }, false, pts);
      d += ` L${x.toFixed(1)} ${a.toFixed(1)} C${x.toFixed(1)} ${mid.toFixed(1)} ${nx.toFixed(1)} ${mid.toFixed(1)} ${nx.toFixed(1)} ${b.toFixed(1)}`;
      x = nx;
    }
    // a aproximação final: desce pelo arcém e vira para a direita, a entrar na estrada do diagnóstico
    const yA = fim.y - Math.min(240, Math.max(140, (fim.x - x) * 1.2));
    reta(pts[pts.length - 1], { x, y: yA }, pts);
    const c1 = { x, y: fim.y - (fim.y - yA) * 0.25 }, c2 = { x: fim.x - Math.max(60, (fim.x - x) * 0.55), y: fim.y };
    cubica({ x, y: yA }, c1, c2, fim, true, pts);
    d += ` L${x.toFixed(1)} ${yA.toFixed(1)} C${c1.x.toFixed(1)} ${c1.y.toFixed(1)} ${c2.x.toFixed(1)} ${c2.y.toFixed(1)} ${fim.x.toFixed(1)} ${fim.y.toFixed(1)}`;
    LUT = pts; V = pts[pts.length - 1].v;
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    via.setAttribute('d', d);
    dpr = Math.min(2, devicePixelRatio || 1);
    cv.width = Math.round(innerWidth * dpr); cv.height = Math.round(innerHeight * dpr);
    pronto = true; cur = -1;
  }

  // ponto da tabela para um «v» (pesquisa binária + interpolação)
  const em = (v) => {
    let lo = 0, hi = LUT.length - 1;
    while (lo < hi) { const md = (lo + hi) >> 1; if (LUT[md].v < v) lo = md + 1; else hi = md; }
    const b = LUT[lo], a = LUT[Math.max(0, lo - 1)], k = b.v - a.v > 0 ? (v - a.v) / (b.v - a.v) : 1;
    return { i: lo, x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, ang: Math.atan2(b.y - a.y, b.x - a.x) };
  };

  let angAnt = 0;
  SITE.aCada((t, e) => {
    if (!pronto) return;
    const alvo = clamp(e.y + e.h * 0.62 - mTop - LUT[0].y, 0, V);
    if (cur < 0) cur = alvo;
    const ant = cur;
    cur += (alvo - cur) * (1 - Math.exp(-e.dt / 90));
    if (Math.abs(alvo - cur) < 0.3) cur = alvo;
    const dv = Math.abs(cur - ant);
    vel += (clamp(dv / Math.max(8, e.dt) / 2.2) - vel) * 0.12;
    if (dv < 0.01 && !e.mexeu && vel < 0.01) return;
    const p = em(cur);
    // o ângulo segue a tangente; parado na ponta, guarda o último (o coche não «vira» por arredondamentos)
    let ang = p.ang - Math.PI / 2;
    if (Math.abs(ang - angAnt) > Math.PI) ang += ang < angAnt ? Math.PI * 2 : -Math.PI * 2;
    angAnt = ang;
    carro.style.transform = `translate3d(${p.x.toFixed(1)}px,${p.y.toFixed(1)}px,0) rotate(${(ang * 180 / Math.PI).toFixed(2)}deg)`;
    carro.style.setProperty('--v', vel.toFixed(3));
    const fimJa = cur >= V - 1.5;
    if (fimJa !== chegou) { chegou = fimJa; ruta.classList.toggle('chegou', fimJa); dj.classList.toggle('ruta-ok', fimJa); }
    // a estela: o último troço percorrido, do ouro apagado à luz quente junto ao coche
    cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cx.clearRect(0, 0, e.w, e.h);
    const ox = mLeft - scrollX, oy = mTop - e.y, ini0 = Math.max(0, p.i - 260), passos = 14;
    cx.lineCap = 'round'; cx.lineJoin = 'round';
    for (let s = 0; s < passos; s++) {
      const a = ini0 + Math.floor((p.i - ini0) * s / passos), b = ini0 + Math.floor((p.i - ini0) * (s + 1) / passos);
      if (b <= a) continue;
      const k = (s + 1) / passos;
      cx.strokeStyle = `rgba(${Math.round(194 + 61 * k * k)},${Math.round(162 + 70 * k * k)},${Math.round(99 + 110 * k * k)},${(0.08 + 0.75 * k * k).toFixed(3)})`;
      cx.lineWidth = 1 + 1.6 * k;
      cx.beginPath(); cx.moveTo(LUT[a].x + ox, LUT[a].y + oy);
      for (let j = a + 1; j <= b; j++) cx.lineTo(LUT[j].x + ox, LUT[j].y + oy);
      if (s === passos - 1) cx.lineTo(p.x + ox, p.y + oy);
      cx.stroke();
    }
    // farolins: um rasto vermelho curto quando acelera
    if (vel > 0.05) {
      const a = Math.max(0, p.i - 22);
      cx.strokeStyle = `rgba(255,48,40,${(0.65 * vel).toFixed(3)})`; cx.lineWidth = 3;
      cx.beginPath(); cx.moveTo(LUT[a].x + ox, LUT[a].y + oy);
      for (let j = a + 1; j < p.i; j++) cx.lineTo(LUT[j].x + ox, LUT[j].y + oy);
      cx.stroke();
    }
  });

  let pend = 0;
  const refaz = () => { if (pend) return; pend = 1; SITE.quieto(200).then(() => { pend = 0; constroi(); }); };
  addEventListener('resize', refaz, { passive: true });
  addEventListener('load', refaz);
  if ('ResizeObserver' in window) new ResizeObserver(refaz).observe(main);
  SITE.abertura.then(refaz);
})();
