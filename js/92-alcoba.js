/* Ferreras: la vitrina. El reloj llega a un nicho a oscuras, bajo un foco, desmontado (como en «The Watch» de 60fps):
   fondo, rotor, calibre con sus ruedas y su volante, caja, esfera, agujas y cristal, separados en profundidad. Con el
   scroll las piezas se colocan una a una y la lista marca cuál se está montando; el reloj montado pasa a ser el reloj
   vivo de la casa (marca la hora de Barcelona), se aparta para el texto y la cámara entra en la esfera hasta fundirse
   con el marfil de «Marca propia». Capas a distinta velocidad y profundidad con el ratón (como en Cartier W&W).
   Una sola línea de tiempo GSAP atada al scroll. */
(() => {
  const { $, $$, reduz } = SITE;
  const sec = $('[data-alcoba]');
  if (!sec || reduz || !window.gsap) return;
  const q = (s) => $(s, sec);
  const reloj = q('[data-al-reloj]'), tilt = q('[data-al-tilt]'), nicho = q('[data-al-nicho]'), cono = q('[data-al-cono]');
  const grande = q('[data-al-grande]'), polvo = q('[data-al-polvo]'), txt = q('[data-al-txt]'), vela = q('[data-al-vela]');
  const vivo = $('.reloj', tilt), pila = q('[data-dz-pila]'), dz = q('[data-dz]'), capas = $$('[data-dz-capa]', sec);
  const lista = q('[data-dz-lista]'), pasos = $$('[data-dz-paso]', sec), pe = q('[data-dz-pe]');
  const linhas = $$('.al-l > span', txt), etq = $('.etiqueta', txt);
  const capa = (c) => capas.find((x) => x.classList.contains(c));
  const rotor = $('svg', capa('dz-rotor'));
  // orden de montaje: [capas que bajan juntas, paso de la lista que se enciende]
  const MONTA = [[['dz-fondo', 'dz-rotor'], 0], [['dz-calibre'], 1], [['dz-caixa', 'dz-esfera'], 2], [['dz-agujas'], 3], [['dz-cristal'], 4]];

  gsap.matchMedia().add({ g: '(min-width: 801px)', m: '(max-width: 800px)' }, ({ conditions: { g } }) => {
    const tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: 0.9 } });
    // 1. el nicho se abre, el foco se enciende y las piezas llegan separadas
    tl.fromTo(nicho, { clipPath: 'inset(48% 42% 30% 42% round 400px)', scale: 0.92 }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', scale: 1, duration: 2.2, ease: 'power2.out' }, 0)
      .fromTo(cono, { opacity: 0 }, { opacity: 1, duration: 1.6 }, 0.6)
      .fromTo(reloj, { yPercent: 60, opacity: 0 }, { yPercent: g ? 0 : -14, opacity: 1, duration: 2.2, ease: 'power3.out' }, 0.3)
      .set(reloj, { scale: g ? 0.82 : 0.78 }, 0)
      .fromTo(pila, { rotationX: 62, rotationZ: -28 }, { rotationX: 0, rotationZ: 0, duration: 4.6, ease: 'power1.inOut' }, 2.4)
      .fromTo(lista, { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.9 }, 1.3)
      .fromTo(grande, { xPercent: 12, opacity: 0 }, { xPercent: -12, opacity: 1, duration: 14 }, 0)
      .fromTo(polvo, { yPercent: 12 }, { yPercent: -26, duration: 14 }, 0)
      .fromTo(rotor, { rotation: 0 }, { rotation: 720, transformOrigin: '50% 50%', duration: 7 }, 0);
    capas.forEach((c) => gsap.set(c, { z: +c.dataset.z * (g ? 1 : 0.7) }));
    gsap.set(vivo, { opacity: 0 });
    // 2. pieza a pieza: cada capa baja a su sitio y la lista marca la que se ha colocado
    MONTA.forEach(([cls, k], i) => {
      const t = 2.6 + i * 0.85;
      tl.to(cls.map(capa), { z: (j, el) => capas.indexOf(el) * 0.6, duration: 1, ease: 'power3.inOut' }, t)
        .to(pasos[k], { opacity: 1, duration: 0.4 }, t + 0.5);
    });
    tl.fromTo(pe, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.6 }, 7)
      // 3. el reloj montado es el reloj vivo de la casa
      .to(dz, { opacity: 0, duration: 0.6 }, 7.5)
      .to(vivo, { opacity: 1, duration: 0.6 }, 7.4)
      .to(lista, { opacity: 0, x: -24, duration: 0.7 }, 7.9)
      // 4. el reloj se aparta y el texto entra línea a línea
      .to(reloj, { xPercent: g ? 64 : 0, yPercent: g ? 0 : -24, scale: g ? 0.96 : 0.7, duration: 1.8, ease: 'power2.inOut' }, 8.2)
      .fromTo(etq, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.8 }, 8.7)
      .fromTo(linhas, { yPercent: 112 }, { yPercent: 0, duration: 1, stagger: 0.32, ease: 'power3.out' }, 8.9)
      // 5. (pausa para leer) la cámara entra en la esfera y todo se funde en marfil
      .to(txt, { opacity: 0, y: -40, duration: 1 }, 10.9)
      .to(reloj, { xPercent: 0, yPercent: 0, scale: g ? 4.4 : 3.8, duration: 2.4, ease: 'power2.in' }, 11.1)
      .to([nicho, grande], { scale: 1.5, opacity: 0, duration: 2, ease: 'power2.in' }, 11.3)
      .to(cono, { opacity: 0, duration: 1.3 }, 11.5)
      .to(vela, { opacity: 1, duration: 1.1 }, 13)
      .set({}, {}, 14.2);
    // al volver hacia arriba la lista se recalcula sola: el estado de cada paso depende sólo del progreso
    tl.eventCallback('onUpdate', () => {
      const t = tl.time();
      pasos.forEach((p, n) => p.classList.toggle('puesta', t >= 3.5 + n * 0.85));
    });
  });

  // profundidad con el ratón: cada capa se mueve según su distancia (el reloj además se inclina)
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const qt = (el, p) => gsap.quickTo(el, p, { duration: 1.1, ease: 'power3' });
    const ry = qt(tilt, 'rotationY'), rx = qt(tilt, 'rotationX'), px = qt(polvo, 'x'), py = qt(polvo, 'y');
    const gx = qt(q('.al-grande'), 'x'), fx = qt(q('.al-fondo'), 'x'), fy = qt(q('.al-fondo'), 'y');
    sec.addEventListener('pointermove', (e) => {
      const nx = e.clientX / innerWidth - 0.5, ny = e.clientY / innerHeight - 0.5;
      ry(nx * 18); rx(-ny * 14); px(nx * -60); py(ny * -40); gx(nx * 36); fx(nx * -16); fy(ny * -10);
    }, { passive: true });
    sec.addEventListener('pointerleave', () => { ry(0); rx(0); px(0); py(0); gx(0); fx(0); fy(0); });
  }
})();
