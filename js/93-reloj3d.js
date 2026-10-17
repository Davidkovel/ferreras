/* Ferreras: el reloj en 3D (módulo ES, sólo en la portada). Dos escenas con el mismo reloj:
   · la portada: el reloj entero a la derecha del título; se gira arrastrando con el ratón o el dedo (como Cartier W&W),
     con inercia, y cuando nadie lo toca gira despacio solo; por detrás se lee el fondo grabado;
   · la vitrina: sustituye al reloj dibujado cuando hay WebGL2:
   fondo de acero grabado, rotor, platina con perlage y puentes, ruedas y volante en relieve, caja con asas y corona,
   la esfera verdadera como textura (el corazón abierto deja ver el volante), agujas a la hora de Barcelona y un cristal
   de zafiro con refracción. Three.js r170 de vendor/, entorno RoomEnvironment, tono ACES, color sRGB (awwwards-3d).
   No hay línea de tiempo propia: lee window.FERRERAS_3D, que la línea de tiempo de la vitrina (92-alcoba.js) mueve con
   el scroll, y lo persigue con un amortiguado independiente de los fps. Sin WebGL2 o con «reducir movimiento» no se
   carga nada y queda el reloj dibujado. */
const sec = document.querySelector('[data-alcoba]');
const heroSec = document.querySelector('[data-hero-3d]');
const R3 = window.FERRERAS_3D;
const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
const temGL = (() => { try { return !!document.createElement('canvas').getContext('webgl2'); } catch (e) { return false; } })();

if (!reduz && temGL) {
  if (heroSec) arranca('hero').catch(() => {});
  // o relógio pequeno que acompanha a leitura da portada: só depois de o hero acabar de entrar
  if (heroSec) setTimeout(() => arranca('mini').catch(() => {}), 2500);
  if (sec && R3) new IntersectionObserver(([e], o) => { if (e.isIntersecting) { o.disconnect(); arranca('vitrina').catch(() => {}); } }, { rootMargin: '160% 0px' }).observe(sec);
}

async function arranca(modo) {
  const hero = modo === 'hero', mini = modo === 'mini';
  let caixaMini = null;
  if (mini) {
    caixaMini = document.createElement('div');
    caixaMini.className = 'mini3d'; caixaMini.setAttribute('aria-hidden', 'true');
    caixaMini.innerHTML = '<span class="mini3d-r" data-mini-r></span>';
    document.body.append(caixaMini);
  }
  const THREE = await import('three');
  const { RoomEnvironment } = await import('three/addons/environments/RoomEnvironment.js');
  await document.fonts.ready;
  const palco = mini ? caixaMini : hero ? heroSec : sec.querySelector('.al-palco');
  const movil = () => innerWidth <= 800;
  const raiz = (window.FERRERAS && window.FERRERAS.raiz) || '';

  const canvas = document.createElement('canvas');
  canvas.className = mini ? 'mini3d-c' : hero ? 'hero-3d' : 'al-3d';
  canvas.setAttribute('aria-hidden', 'true');
  if (mini) caixaMini.prepend(canvas);
  else if (hero) heroSec.querySelector('.hero-grid').before(canvas);
  else sec.querySelector('[data-al-polvo]').before(canvas);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.95;
  pmrem.dispose();
  const camera = new THREE.PerspectiveCamera(28, 1, 0.05, 60);
  // el foco cálido del nicho viene de arriba; un contraluz frío recorta el canto
  const llave = new THREE.DirectionalLight(0xffe0b0, 2.4); llave.position.set(0.6, 4, 5); scene.add(llave);
  const recorte = new THREE.DirectionalLight(0x9db6ff, 0.9); recorte.position.set(-4, -1.5, -3); scene.add(recorte);

  // ---------------------------------------------------------------- materiales
  const oro = new THREE.MeshStandardMaterial({ color: 0xd9b46e, metalness: 1, roughness: 0.2 });
  const oroRueda = new THREE.MeshStandardMaterial({ color: 0xd2a85c, metalness: 1, roughness: 0.32 });
  const acero = new THREE.MeshStandardMaterial({ color: 0xc8ccd0, metalness: 1, roughness: 0.3 });
  const rubi = new THREE.MeshPhysicalMaterial({ color: 0xb3122e, metalness: 0, roughness: 0.08, clearcoat: 1, emissive: 0x3a0008 });
  const azul = new THREE.MeshStandardMaterial({ color: 0x0022f1, metalness: 0.3, roughness: 0.35, emissive: 0x00104a });

  // ---------------------------------------------------------------- texturas pintadas (canvas 2D)
  const lienzo = (n, pinta) => { const c = document.createElement('canvas'); c.width = c.height = n; pinta(c.getContext('2d'), n); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };
  const platinaTex = lienzo(1024, (x, n) => {
    const c = n / 2;
    const g = x.createRadialGradient(c * 0.85, c * 0.75, 40, c, c, c);
    g.addColorStop(0, '#eceff1'); g.addColorStop(0.6, '#b3b9be'); g.addColorStop(1, '#7c838a');
    x.fillStyle = g; x.fillRect(0, 0, n, n);
    // perlage: círculos solapados por toda la platina
    x.strokeStyle = 'rgba(255,255,255,.22)'; x.lineWidth = 2;
    for (let i = 0; i < 260; i++) { const a = i * 2.39996, r = Math.sqrt(i / 260) * c * 0.95; x.beginPath(); x.arc(c + r * Math.cos(a), c + r * Math.sin(a), 30, 0, 7); x.stroke(); }
    // puentes con Côtes de Genève
    const puente = (pts) => {
      x.save(); x.beginPath(); pts.forEach(([px, py], i) => (i ? x.lineTo(px * n, py * n) : x.moveTo(px * n, py * n))); x.closePath();
      x.fillStyle = '#d4d8db'; x.fill(); x.clip();
      x.translate(c, c); x.rotate(-0.42);
      for (let s = -n; s < n; s += 26) { const lg = x.createLinearGradient(s, 0, s + 26, 0); lg.addColorStop(0, '#c1c6ca'); lg.addColorStop(0.5, '#eef0f2'); lg.addColorStop(1, '#c1c6ca'); x.fillStyle = lg; x.fillRect(s, -n, 26, 2 * n); }
      x.restore();
      x.beginPath(); pts.forEach(([px, py], i) => (i ? x.lineTo(px * n, py * n) : x.moveTo(px * n, py * n))); x.closePath(); x.strokeStyle = '#5f6468'; x.lineWidth = 3; x.stroke();
    };
    puente([[0.18, 0.62], [0.42, 0.56], [0.62, 0.66], [0.66, 0.86], [0.38, 0.9], [0.2, 0.8]]);
    puente([[0.62, 0.52], [0.86, 0.42], [0.92, 0.6], [0.78, 0.72]]);
    // tornillos azulados
    [[0.3, 0.7], [0.55, 0.82], [0.8, 0.55], [0.24, 0.42]].forEach(([px, py]) => {
      x.beginPath(); x.arc(px * n, py * n, 13, 0, 7); x.fillStyle = '#21407f'; x.fill();
      x.strokeStyle = '#0c1630'; x.lineWidth = 3; x.beginPath(); x.moveTo(px * n - 10, py * n); x.lineTo(px * n + 10, py * n); x.stroke();
    });
  });
  const fondoTex = lienzo(1024, (x, n) => {
    const c = n / 2;
    x.fillStyle = '#b9bec2'; x.fillRect(0, 0, n, n);
    for (let r = 4; r < c; r += 3) { x.beginPath(); x.arc(c, c, r, 0, 7); x.strokeStyle = `rgba(${r % 2 ? 255 : 90},${r % 2 ? 255 : 95},${r % 2 ? 255 : 100},.08)`; x.lineWidth = 2; x.stroke(); }
    x.fillStyle = '#4a4f54'; x.textAlign = 'center'; x.textBaseline = 'middle';
    const anel = 'AUTOMÁTICO · MECANISMO SUIZO · ENSAMBLADO EN BARCELONA · ';
    x.font = '500 34px Jost, Futura, sans-serif';
    const passo = (Math.PI * 2) / anel.length;
    [...anel].forEach((ch, i) => { x.save(); x.translate(c, c); x.rotate(i * passo); x.fillText(ch, 0, -c * 0.8); x.restore(); });
    x.font = '400 92px "Bodoni Moda", Didot, serif'; x.fillText('Ferreras', c, c - 10);
    x.font = '500 28px Jost, Futura, sans-serif'; x.fillText('BARCELONA', c, c + 80);
    x.beginPath(); x.arc(c, c, c * 0.68, 0, 7); x.strokeStyle = '#c49a52'; x.lineWidth = 6; x.stroke();
  });
  const esferaTex = await new THREE.TextureLoader().loadAsync(`${raiz}img/dial-ferreras.webp`);
  esferaTex.colorSpace = THREE.SRGBColorSpace; esferaTex.anisotropy = 8;

  // ---------------------------------------------------------------- geometrías
  const extruye = (shape, d, bevel = 0.004) => new THREE.ExtrudeGeometry(shape, { depth: d, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 2, curveSegments: 48 });
  const dentada = (r, dentes) => {
    const s = new THREE.Shape(), passo = (Math.PI * 2) / dentes;
    for (let i = 0; i < dentes; i++) {
      [[-0.32, 0.9], [-0.18, 1], [0.18, 1], [0.32, 0.9]].forEach(([da, k], j) => {
        const a = i * passo + da * passo, p = [r * k * Math.cos(a), r * k * Math.sin(a)];
        (i || j ? s.lineTo : s.moveTo).call(s, ...p);
      });
    }
    const furo = new THREE.Path(); furo.absarc(0, 0, r * 0.7, 0, Math.PI * 2, true); s.holes.push(furo);
    return s;
  };
  const roda = (r, dentes, x, y, z) => {
    const g = new THREE.Group();
    g.add(new THREE.Mesh(extruye(dentada(r, dentes), 0.022, 0.003), oroRueda));
    for (let i = 0; i < 5; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(r * 0.12, r * 1.4, 0.016), oroRueda); b.rotation.z = (i / 5) * Math.PI; b.position.z = 0.011; g.add(b); }
    const eixo = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.18, r * 0.18, 0.03, 32), oroRueda); eixo.rotation.x = Math.PI / 2; eixo.position.z = 0.012; g.add(eixo);
    const pedra = new THREE.Mesh(new THREE.SphereGeometry(0.016, 20, 12), rubi); pedra.position.z = 0.03; g.add(pedra);
    g.position.set(x, y, z);
    return g;
  };
  const disco = (r, h, mats, segs = 128) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, segs), mats); m.rotation.x = Math.PI / 2; return m; };
  const lanca = (comp, larg, cola) => { const s = new THREE.Shape(); s.moveTo(0, -cola); s.lineTo(larg, 0.06); s.lineTo(larg * 0.35, comp * 0.92); s.lineTo(0, comp); s.lineTo(-larg * 0.35, comp * 0.92); s.lineTo(-larg, 0.06); s.closePath(); return s; };

  // ---------------------------------------------------------------- as peças (mesma ordem que _fonte/despiece.py)
  const relogio = new THREE.Group();
  const pecas = [];
  const peca = (montado, separado) => { const g = new THREE.Group(); g.userData = { montado, separado }; relogio.add(g); pecas.push(g); return g; };

  const fondo = peca(-0.11, -1.55);
  const fondoMat = new THREE.MeshStandardMaterial({ map: fondoTex, metalness: 0.9, roughness: 0.34 });
  fondo.add(disco(0.99, 0.04, [acero, fondoMat, acero]));
  const costas = new THREE.Mesh(new THREE.CircleGeometry(0.985, 128), fondoMat); costas.rotation.y = Math.PI; costas.position.z = -0.022; fondo.add(costas);

  const rotor = peca(-0.07, -1.05);
  const rs = new THREE.Shape(); rs.absarc(0, 0, 0.86, 0, Math.PI, false); rs.absarc(0, 0, 0.13, Math.PI, 0, true);
  const rotorMalla = new THREE.Mesh(extruye(rs, 0.018, 0.003), oro); rotor.add(rotorMalla);

  const calibre = peca(-0.035, -0.55);
  calibre.add(disco(0.9, 0.04, [acero, new THREE.MeshStandardMaterial({ map: platinaTex, metalness: 0.85, roughness: 0.32 }), acero]));
  const rodas = [roda(0.15, 30, 0.27, 0.36, 0.02), roda(0.12, 26, -0.33, 0.2, 0.02), roda(0.2, 36, 0.06, -0.36, 0.02), roda(0.1, 22, 0.42, -0.2, 0.02)];
  rodas.forEach((r) => calibre.add(r));
  const volante = new THREE.Group();
  volante.add(new THREE.Mesh(new THREE.TorusGeometry(0.19, 0.016, 16, 96), oro));
  for (let i = 0; i < 3; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.19, 0.01), oro); b.position.y = 0.095; const p = new THREE.Group(); p.add(b); p.rotation.z = (i / 3) * Math.PI * 2; volante.add(p); }
  const espiral = new THREE.BufferGeometry().setFromPoints(Array.from({ length: 220 }, (_, i) => { const a = i * 0.16, r = 0.02 + i * 0.0006; return new THREE.Vector3(r * Math.cos(a), r * Math.sin(a), 0.006); }));
  volante.add(new THREE.Line(espiral, new THREE.LineBasicMaterial({ color: 0x2f3236 })));
  const pivote = new THREE.Mesh(new THREE.SphereGeometry(0.02, 20, 12), rubi); pivote.position.z = 0.012; volante.add(pivote);
  volante.position.set(-0.08, 0.38, 0.045);
  calibre.add(volante);

  const caixa = peca(0, 0);
  const perfil = [[0.93, -0.12], [1.02, -0.12], [1.065, -0.08], [1.07, 0.01], [1.04, 0.06], [0.98, 0.085], [0.94, 0.075], [0.93, -0.12]].map(([r, z]) => new THREE.Vector2(r, z));
  const aro = new THREE.Mesh(new THREE.LatheGeometry(perfil, 160), oro.clone()); aro.material.side = THREE.DoubleSide; aro.rotation.x = Math.PI / 2; caixa.add(aro);
  [[-0.36, 1], [0.36, 1], [-0.36, -1], [0.36, -1]].forEach(([x, s]) => { const a = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.22, 0.07, 2, 2, 2), oro); a.position.set(x, s * 1.05, -0.035); caixa.add(a); });
  const coroa = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.14, 40), oro); coroa.rotation.z = Math.PI / 2; coroa.position.set(1.13, 0, -0.02); caixa.add(coroa);
  // o bracelete inteiro e fechado: elos de aço com o central dourado, das asas de cima às de baixo pela parte de trás,
  // como um relógio pousado no seu expositor (elipse: altura das asas × fundo do pulso)
  const eloAco = new THREE.BoxGeometry(0.22, 0.13, 0.06), eloOro = new THREE.BoxGeometry(0.2, 0.13, 0.065);
  const bracelete = new THREE.Group();
  const NE = 24, AY = 1.1, DZ = 1.15;
  for (let k = 0; k < NE; k++) {
    const t = 0.06 + (k / (NE - 1)) * (Math.PI - 0.12);
    const elo = new THREE.Group();
    elo.position.set(0, AY * Math.cos(t), -0.04 - DZ * Math.sin(t));
    elo.rotation.x = Math.atan2(-DZ * Math.cos(t), -AY * Math.sin(t));
    [-0.22, 0.22].forEach((x) => { const m = new THREE.Mesh(eloAco, acero); m.position.x = x; elo.add(m); });
    elo.add(new THREE.Mesh(eloOro, oro));
    bracelete.add(elo);
  }
  caixa.add(bracelete);

  const esfera = peca(0.012, 0.5);
  const esferaMalla = new THREE.Mesh(new THREE.CircleGeometry(0.93, 160), new THREE.MeshStandardMaterial({ map: esferaTex, alphaTest: 0.5, metalness: 0.15, roughness: 0.42, envMapIntensity: 0.55 }));
  esferaMalla.position.z = 0.05; esfera.add(esferaMalla);

  const agujas = peca(0.06, 0.95);
  const hora = new THREE.Mesh(extruye(lanca(0.46, 0.045, 0.08), 0.006, 0.002), oro); hora.position.z = 0.0;
  const minuto = new THREE.Mesh(extruye(lanca(0.72, 0.035, 0.1), 0.006, 0.002), oro); minuto.position.z = 0.012;
  const segundo = new THREE.Group();
  const sl = new THREE.Mesh(new THREE.BoxGeometry(0.008, 0.95, 0.004), new THREE.MeshStandardMaterial({ color: 0x0b1a36, metalness: 0.4, roughness: 0.4 })); sl.position.y = 0.3; segundo.add(sl);
  const ponta = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.006), azul); ponta.position.y = 0.76; segundo.add(ponta);
  segundo.position.z = 0.024;
  const tampa = disco(0.032, 0.03, oro, 40); tampa.position.z = 0.03;
  agujas.add(hora, minuto, segundo, tampa);

  const cristal = peca(0.1, 1.4);
  // zafiro: transparente sobre la página (la refracción de three oscurece lo que hay detrás de un lienzo transparente),
  // con capa de barniz para que los reflejos del entorno corran por encima
  cristal.add(disco(0.955, 0.028, new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 0, roughness: 0.02, clearcoat: 1, clearcoatRoughness: 0.02, ior: 1.77, transparent: true, opacity: 0.08, envMapIntensity: 1.6, depthWrite: false })));

  scene.add(relogio);

  // ---------------------------------------------------------------- composição: o mesmo sítio e tamanho que o reloj dibujado
  let W = 1, H = 1;
  const mede = () => {
    W = mini ? (canvas.clientWidth || 108) : palco.clientWidth; H = mini ? (canvas.clientHeight || 108) : palco.clientHeight;
    renderer.setPixelRatio(Math.min(devicePixelRatio, movil() ? 1.5 : 1.75));
    renderer.setSize(W, H, false);
    camera.aspect = W / H; camera.updateProjectionMatrix();
  };
  mede();
  addEventListener('resize', () => requestAnimationFrame(mede));
  const tg = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));

  // a hora de Barcelona, lida uma vez por segundo; os segundos correm suaves entre leituras
  const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Madrid', hour: 'numeric', minute: 'numeric', second: 'numeric', hourCycle: 'h23' });
  let base = 0, lida = 0;
  const leHora = () => { const p = Object.fromEntries(fmt.formatToParts(new Date()).map((x) => [x.type, x.value])); base = +p.hour * 3600 + +p.minute * 60 + +p.second; lida = performance.now(); };
  leHora(); setInterval(leHora, 1000);

  // ---------------------------------------------------------------- laço: só desenha com a vitrina à vista e a aba ativa
  let visivel = false, ultimo = performance.now();
  new IntersectionObserver(([e]) => { visivel = e.isIntersecting; }, { rootMargin: '10% 0px' }).observe(hero ? heroSec : sec);
  const t0 = performance.now();
  const trabalha = (agora) => {
    // o calibre trabalha: rodas a girar e o volante a oscilar a 4 Hz; as agulhas na hora de Barcelona
    const t = agora / 1000;
    rodas.forEach((r, i) => (r.rotation.z = t * (i % 2 ? -0.6 : 0.45) * (1 + i * 0.3)));
    volante.rotation.z = Math.sin(t * Math.PI * 2 * 4) * 2.4;
    const s = base + (agora - lida) / 1000;
    segundo.rotation.z = -((s % 60) / 60) * Math.PI * 2;
    minuto.rotation.z = -(((s / 60) % 60) / 60) * Math.PI * 2;
    hora.rotation.z = -(((s / 3600) % 12) / 12) * Math.PI * 2;
  };

  if (mini) {
    // ------------------------------------------------ o relógio pequeno: gira com o scroll e diz em que parte da portada está
    pecas.forEach((p) => (p.position.z = p.userData.montado));
    const rot = caixaMini.querySelector('[data-mini-r]');
    addEventListener('ferreras:secao', (e) => { rot.textContent = e.detail || ''; caixaMini.classList.toggle('com-r', !!e.detail); });
    let ry = 0;
    const al = document.querySelector('[data-alcoba]');
    const passo = (agora) => {
      requestAnimationFrame(passo);
      const dt = Math.min(64, agora - ultimo); ultimo = agora;
      const r = al ? al.getBoundingClientRect() : null;
      const on = scrollY > innerHeight * 0.85 && !(r && r.top < innerHeight * 0.5 && r.bottom > innerHeight * 0.5);   // some-se enquanto a vitrina ocupa o ecrã
      caixaMini.classList.toggle('on', on);
      if (!on || document.hidden) return;
      ry += (scrollY * 0.006 - ry) * (1 - Math.exp(-dt / 120));
      const s = Math.min(W, H), dist = 2.5 / (2 * tg) * (H / s);
      camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0);
      relogio.position.set(0, 0, 0);
      relogio.rotation.set(0.32 + Math.sin(agora / 1600) * 0.05, ry, 0);
      rotorMalla.rotation.z = agora / 900;
      trabalha(agora);
      renderer.render(scene, camera);
    };
    requestAnimationFrame(passo);
    return;
  }
  if (hero) {
    // ------------------------------------------------ portada: girar arrastrando, con inercia (awwwards-3d, patrón 21)
    pecas.forEach((p) => (p.position.z = p.userData.montado));
    const rot = { y: -0.38, x: 0.14, ay: -0.38, ax: 0.14, vy: 0 };
    const intro = scrollY < 40;   // a entrada só ao abrir a página no topo
    let ti = performance.now();   // começa quando a abertura (o rasto de luz e o logótipo) acabar
    if (window.SITE && SITE.abertura) SITE.abertura.then(() => { ti = performance.now(); });
    let arrasta = false, lx = 0, ly = 0, tocado = 0, mx = 0, my = 0;
    heroSec.addEventListener('pointerdown', (e) => {
      if (e.target.closest('a, button')) return;
      arrasta = true; lx = e.clientX; ly = e.clientY; rot.vy = 0; tocado = performance.now(); heroSec.classList.add('a-girar');
    });
    addEventListener('pointermove', (e) => {
      mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5;
      if (!arrasta) return;
      const dx = e.clientX - lx, dy = e.clientY - ly; lx = e.clientX; ly = e.clientY;
      rot.ay += dx * 0.009; rot.vy = dx * 0.009;
      rot.ax = Math.max(-0.7, Math.min(0.9, rot.ax + dy * 0.006));
      tocado = performance.now();
    }, { passive: true });
    const solta = () => { arrasta = false; heroSec.classList.remove('a-girar'); };
    addEventListener('pointerup', solta); addEventListener('pointercancel', solta);
    const passo = (agora) => {
      requestAnimationFrame(passo);
      const dt = Math.min(64, agora - ultimo); ultimo = agora;
      if (!visivel || document.hidden) return;
      const k = 1 - Math.exp(-dt / 110);
      if (!arrasta) {
        rot.ay += rot.vy * (dt / 16); rot.vy *= Math.pow(0.93, dt / 16);           // inércia ao largar
        if (agora - tocado > 2600 && agora - ti > 3200) rot.ay += dt * 0.00018;    // sozinho, gira devagar
      }
      rot.y += (rot.ay - rot.y) * k; rot.x += (rot.ax - rot.x) * k;
      const g = !movil();
      // a entrada: 0–45 % desmonta-se e monta-se ao centro, a girar sobre si; 45–100 % vai para o seu sítio
      const pi = intro ? Math.max(0, Math.min(1, (agora - ti) / 2200)) : 1;
      if (pi > 0.82 && !heroSec.classList.contains('texto-on')) heroSec.classList.add('texto-on');
      const suave = (x) => x * x * (3 - 2 * x);
      const monta = suave(Math.min(1, pi / 0.5)), vai = suave(Math.max(0, (pi - 0.45) / 0.55));
      pecas.forEach((pc) => { pc.position.z = pc.userData.montado + (pc.userData.separado - pc.userData.montado) * 0.55 * (1 - monta); });
      const giro = (1 - suave(Math.min(1, pi / 0.85))) * Math.PI * 2;
      const q = Math.min(1, scrollY / Math.max(1, heroSec.offsetHeight));
      const final = (g ? Math.min(0.64 * H, 0.42 * W) : 0.7 * W);
      const dpx = (final + (Math.min(0.78 * H, 0.6 * W) - final) * (1 - vai)) * (1 - 0.28 * q);
      const dist = (2.9 * H) / (2 * tg * dpx);
      const cx = W / 2 + ((g ? W * 0.7 : W / 2) - W / 2) * vai, cy = H / 2 + ((g ? H * 0.45 : H * 0.3) - H / 2) * vai - q * H * 0.18;
      const ppx = (2 * dist * tg) / H;
      relogio.position.set((cx - W / 2) * ppx, -(cy - H / 2) * ppx, 0);
      camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0);
      relogio.rotation.set(rot.x + my * 0.12 + 0.55 * (1 - monta), rot.y + mx * 0.2 + giro, 0);
      const op = (1 - Math.max(0, q - 0.35) * 1.8).toFixed(3); if (op !== canvas.style.opacity) canvas.style.opacity = op;
      rotorMalla.rotation.z = agora / 900;
      trabalha(agora);
      renderer.render(scene, camera);
    };
    requestAnimationFrame(passo);
    heroSec.classList.add('com-3d');
    return;
  }
  const atual = { entra: 0, tiltX: 62, tiltZ: -28, rotor: 0, lado: 0, zoom: 0, mx: 0, my: 0, p0: 1, p1: 1, p2: 1, p3: 1, p4: 1, p5: 1, p6: 1 };
  const passo = (agora) => {
    requestAnimationFrame(passo);
    const dt = Math.min(64, agora - ultimo); ultimo = agora;
    if (!visivel || document.hidden) return;
    const k = 1 - Math.exp(-dt / 90);
    for (const c in atual) atual[c] += ((R3[c] ?? atual[c]) - atual[c]) * k;
    const g = !movil();
    // tamanho e centro, em píxeis, iguais aos do reloj dibujado (92-alcoba.js / estilo.css)
    const wpx = g ? Math.min(0.52 * H, 0.36 * W) : 0.72 * W;
    const esc = g ? 0.82 + 0.14 * atual.lado : 0.78 - 0.08 * atual.lado;
    const dpx = wpx * esc * (0.55 + 0.45 * atual.entra);
    const dist = (2.12 * H) / (2 * tg * dpx);
    const cx = W / 2 + (g ? atual.lado * 0.64 * wpx * 0.96 : 0);
    const cy = g ? H / 2 + (1 - atual.entra) * 0.35 * H : 0.4 * H - wpx * (0.14 + 0.1 * atual.lado) + (1 - atual.entra) * 0.35 * H;
    const ppx = (2 * dist * tg) / H; // mundo por píxel à distância da câmara
    relogio.position.set((cx - W / 2) * ppx, -(cy - H / 2) * ppx, 0);
    camera.position.set(relogio.position.x * atual.zoom, relogio.position.y * atual.zoom, dist * (1 - 0.82 * atual.zoom));
    camera.lookAt(relogio.position.x * atual.zoom, relogio.position.y * atual.zoom, 0);
    relogio.rotation.set(-THREE.MathUtils.degToRad(atual.tiltX) - atual.my * 0.25, atual.mx * 0.32, THREE.MathUtils.degToRad(-atual.tiltZ));
    pecas.forEach((p, i) => { const s = atual['p' + i]; p.position.z = p.userData.montado + (p.userData.separado - p.userData.montado) * s; });
    rotorMalla.rotation.z = atual.rotor;
    trabalha(agora);
    renderer.render(scene, camera);
  };
  requestAnimationFrame(passo);
  sec.classList.add('com-3d');
}
