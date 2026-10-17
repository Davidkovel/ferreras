/* Ferreras: el portal de la portada. Una línea de tiempo atada al scroll: la cámara entra por el corazón abierto de la
   esfera (el hueco de la imagen verdadera) hasta el mundo del Marketing; una iris lo cierra y deja ver la esfera de
   noche; por su corazón se entra en el mundo de la IA. Sólo transform, opacity y clip-path. */
(() => {
  const { $, reduz } = SITE;
  const sec = $('[data-portal]');
  if (!sec || reduz || !window.gsap) return;
  const e1 = $('[data-pt-e1]', sec), e2 = $('[data-pt-e2]', sec), mkt = $('[data-pt-mkt]', sec), ia = $('[data-pt-ia]', sec), intro = $('[data-pt-intro]', sec);
  const tm = $('.pt-mkt .pt-txt', sec), ti = $('.pt-ia .pt-txt', sec);
  sec.classList.add('vivo');
  // o coração (o hueco) da esfera fica a 50,4 % e a 29,3 % da imagem: a escala faz-se a partir daí
  gsap.set([e1, e2], { transformOrigin: '50.4% 29.3%' });
  const tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: 0.8 } });
  tl.to(intro, { opacity: 0, y: -60, duration: 0.6 }, 0.2)
    .fromTo(e1, { scale: 1, rotation: -8 }, { scale: 14, rotation: 0, duration: 2.6, ease: 'power2.in' }, 0.3)
    .to(e1, { opacity: 0, duration: 0.4 }, 2.6)
    .fromTo(mkt, { scale: 1.25 }, { scale: 1, duration: 2.8, ease: 'power2.out' }, 0.3)
    .fromTo(tm, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 2.4)
    // pausa no Marketing; depois a íris fecha-o e aparece a esfera de noite
    .to(tm, { opacity: 0, y: -40, duration: 0.6 }, 4.6)
    .fromTo(mkt, { clipPath: 'circle(150% at 50% 50%)' }, { clipPath: 'circle(0% at 50% 50%)', duration: 1.4, ease: 'power2.inOut' }, 4.8)
    .fromTo(e2, { scale: 0.6, rotation: 10, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 1.2, ease: 'power2.out' }, 5.4)
    .to(e2, { scale: 14, duration: 2.4, ease: 'power2.in' }, 6.8)
    .to(e2, { opacity: 0, duration: 0.4 }, 8.8)
    .fromTo(ia, { scale: 1.25 }, { scale: 1, duration: 2.6, ease: 'power2.out' }, 6.8)
    .fromTo(ti, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 8.8)
    .set({}, {}, 10.5);
})();
