/* Ferreras: la vitrina. El reloj sale de un nicho a oscuras bajo un foco, como una pieza de museo; las capas se mueven a
   velocidades distintas (fondo, nicho, letra grande, reloj, polvo de luz) y siguen al ratón; después la cámara entra en
   la esfera y la escena se funde con el marfil de «Marca propia». Una línea de tiempo GSAP atada al scroll. */
(() => {
  const { $, $$, reduz } = SITE;
  const sec = $('[data-alcoba]');
  if (!sec || reduz || !window.gsap) return;
  const q = (s) => $(s, sec);
  const reloj = q('[data-al-reloj]'), tilt = q('[data-al-tilt]'), nicho = q('[data-al-nicho]'), cono = q('[data-al-cono]');
  const grande = q('[data-al-grande]'), polvo = q('[data-al-polvo]'), txt = q('[data-al-txt]'), vela = q('[data-al-vela]');
  const linhas = $$('.al-l > span', txt), etq = $('.etiqueta', txt);

  gsap.matchMedia().add({ g: '(min-width: 801px)', m: '(max-width: 800px)' }, ({ conditions: { g } }) => {
    gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: 0.9 } })
      // 1. el nicho se abre y el foco se enciende; el reloj sube a su sitio
      .fromTo(nicho, { clipPath: 'inset(48% 42% 30% 42% round 400px)', scale: 0.92 }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', scale: 1, duration: 2.2, ease: 'power2.out' }, 0)
      .fromTo(cono, { opacity: 0 }, { opacity: 1, duration: 1.6 }, 0.6)
      .fromTo(reloj, { yPercent: 70, scale: 0.45, opacity: 0, rotation: -16 }, { yPercent: 0, scale: g ? 0.82 : 0.9, opacity: 1, rotation: 0, duration: 2.4, ease: 'power3.out' }, 0.3)
      .fromTo(grande, { xPercent: 12, opacity: 0 }, { xPercent: -12, opacity: 1, duration: 9 }, 0)
      .fromTo(polvo, { yPercent: 12 }, { yPercent: -26, duration: 10 }, 0)
      // 2. el reloj se aparta y el texto entra línea a línea
      .to(reloj, { xPercent: g ? 64 : 0, yPercent: g ? 0 : -24, scale: g ? 0.96 : 0.7, duration: 2, ease: 'power2.inOut' }, 2.6)
      .fromTo(etq, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.8 }, 3)
      .fromTo(linhas, { yPercent: 112 }, { yPercent: 0, duration: 1, stagger: 0.32, ease: 'power3.out' }, 3.2)
      // 3. (pausa para leer) la cámara entra en la esfera y todo se funde en marfil
      .to(txt, { opacity: 0, y: -40, duration: 1 }, 6.2)
      .to(reloj, { xPercent: 0, yPercent: 0, scale: g ? 4.4 : 3.8, duration: 2.6, ease: 'power2.in' }, 6.4)
      .to([nicho, grande], { scale: 1.5, opacity: 0, duration: 2.2, ease: 'power2.in' }, 6.6)
      .to(cono, { opacity: 0, duration: 1.4 }, 6.8)
      .to(vela, { opacity: 1, duration: 1.2 }, 8.6)
      .set({}, {}, 10);
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
