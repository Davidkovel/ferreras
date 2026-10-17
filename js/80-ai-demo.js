/* Demo del agente de IA: conversación simulada, sin servidor ni librerías.
   Uso: <div data-ai-demo="hotel"></div>  (hotel | nautica | joyeria | auto)
   data-ai-demo-tabs="off" oculta las pestañas de sector. */
(function () {
  'use strict';

  var SC = {
    hotel: {
      tab: 'Hotel', who: 'Hotel de montaña · Pirineo', lang: 'de', langName: 'alemán', hour: '23:40',
      steps: [
        ['c', 'Guten Abend! Haben Sie für morgen noch ein Doppelzimmer frei? Wir sind zwei Erwachsene mit Hund.',
              '¡Buenas noches! ¿Les queda una habitación doble para mañana? Somos dos adultos con perro.'],
        ['a', 'Guten Abend! Ich bin der digitale Assistent des Hotels. Für morgen ist noch ein Doppelzimmer mit Talblick frei, und Hunde sind bei uns willkommen (15 € pro Nacht).',
              '¡Buenas noches! Soy el asistente digital del hotel. Para mañana queda una doble con vistas al valle y los perros son bienvenidos (15 € por noche).'],
        ['c', 'Perfekt. Wir kommen erst gegen 22 Uhr an – ist das ein Problem?',
              'Perfecto. No llegaremos hasta las 22 h, ¿es un problema?'],
        ['a', 'Kein Problem: Sie bekommen einen Code für den späten Check-in. Soll ich das Zimmer für Sie vormerken? Bestätigung und Zahlung übernimmt morgen ab 8 Uhr unsere Rezeption.',
              'Ningún problema: recibirán un código para el check-in tardío. ¿Le reservo la habitación? La confirmación y el pago los cierra recepción mañana desde las 8 h.'],
        ['c', 'Ja, bitte!', '¡Sí, por favor!'],
        ['e', 'Prerreserva creada · Recepción la confirma a las 8:00']
      ]
    },
    nautica: {
      tab: 'Náutica', who: 'Club náutico · Costa Brava', lang: 'en', langName: 'inglés', hour: '02:15',
      steps: [
        ['c', 'Hi, we’re flying in from Miami next week. Could we charter a sailing yacht with a skipper on Saturday? We are 6.',
              'Hola, llegamos desde Miami la semana que viene. ¿Podríamos alquilar un velero con patrón el sábado? Somos 6.'],
        ['a', 'Good evening from the Costa Brava! I’m the club’s digital assistant. On Saturday we have a 14-metre sailing yacht with skipper available, full day from 10:00, up to 8 guests.',
              '¡Buenas noches desde la Costa Brava! Soy el asistente digital del club. El sábado hay libre un velero de 14 m con patrón, día completo desde las 10:00, hasta 8 personas.'],
        ['c', 'Sounds great. Can we stop at a cove for lunch?',
              'Suena genial. ¿Podemos parar en una cala para comer?'],
        ['a', 'Of course. The skipper usually anchors in Cala Montgó and we can arrange lunch on board. Shall I email you the proposal so the team confirms it in the morning?',
              'Claro. El patrón suele fondear en Cala Montgó y podemos organizar la comida a bordo. ¿Le envío la propuesta por email para que el equipo la confirme por la mañana?'],
        ['c', 'Yes, please.', 'Sí, por favor.'],
        ['e', 'Propuesta enviada · El equipo la confirma a las 9:00']
      ]
    },
    joyeria: {
      tab: 'Joyería', who: 'Joyería · Barcelona', lang: 'fr', langName: 'francés', hour: '21:05',
      steps: [
        ['c', 'Bonsoir, je suis à Barcelone jusqu’à mardi. Pourrais-je voir des bagues avec émeraude, autour de 3 carats ?',
              'Buenas noches, estoy en Barcelona hasta el martes. ¿Podría ver anillos con esmeralda, de unos 3 quilates?'],
        ['a', 'Bonsoir ! Je suis l’assistant numérique de la maison. Nous avons plusieurs pièces qui correspondent, dont une émeraude colombienne entourée de diamants. Je peux vous proposer une visite privée.',
              '¡Buenas noches! Soy el asistente digital de la casa. Tenemos varias piezas que encajan, entre ellas una esmeralda colombiana rodeada de diamantes. Puedo proponerle una visita privada.'],
        ['c', 'Lundi à 11 h, ce serait possible ?', '¿El lunes a las 11 h sería posible?'],
        ['a', 'Lundi à 11 h, c’est libre. Notre gemmologue vous recevra dans un salon privé. Je vous réserve ce créneau ?',
              'El lunes a las 11 h está libre. Nuestro gemólogo le recibirá en un salón privado. ¿Le reservo esa hora?'],
        ['c', 'Oui, merci.', 'Sí, gracias.'],
        ['e', 'Cita privada · lunes 11:00 · Aviso enviado al gemólogo']
      ]
    },
    auto: {
      tab: 'Automoción', who: 'Concesionario premium', lang: 'ar', langName: 'árabe', hour: '06:30', rtl: true,
      steps: [
        ['c', 'صباح الخير، هل سيارة بورشه 911 GT3 RS السوداء ما زالت متوفرة؟',
              'Buenos días, ¿sigue disponible el Porsche 911 GT3 RS negro?'],
        ['a', 'صباح الخير! أنا المساعد الرقمي للمعرض. نعم، السيارة متوفرة، ويمكننا إرسال فيديو مفصّل لها اليوم.',
              '¡Buenos días! Soy el asistente digital del concesionario. Sí, está disponible y podemos enviarle hoy un vídeo detallado.'],
        ['c', 'هل يمكن الشحن إلى دبي؟', '¿Se puede enviar a Dubái?'],
        ['a', 'نعم، ننظّم الشحن الدولي. سيتواصل معك مدير المبيعات اليوم الساعة العاشرة لتأكيد التفاصيل والسعر.',
              'Sí, organizamos el envío internacional. El director comercial le contactará hoy a las 10:00 para confirmar detalles y precio.'],
        ['c', 'ممتاز، شكراً.', 'Perfecto, gracias.'],
        ['e', 'Cliente cualificado · Comercial avisado para las 10:00']
      ]
    }
  };
  var ORDER = ['hotel', 'nautica', 'joyeria', 'auto'];
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function addMinutes(hhmm, m) {
    var p = hhmm.split(':'), t = (+p[0] * 60 + +p[1] + m) % 1440;
    return String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0');
  }

  function mount(root) {
    var key = SC[root.getAttribute('data-ai-demo')] ? root.getAttribute('data-ai-demo') : 'hotel';
    var timers = [], started = false;

    root.classList.add('aid');
    root.setAttribute('role', 'region');
    root.setAttribute('aria-label', 'Demostración del agente de IA');

    var tabs = el('div', 'aid-tabs');
    tabs.setAttribute('role', 'tablist');
    if (root.getAttribute('data-ai-demo-tabs') === 'off') tabs.hidden = true;
    ORDER.forEach(function (k) {
      var b = el('button', 'aid-tab', SC[k].tab);
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.dataset.k = k;
      b.addEventListener('click', function () { if (k !== key) { key = k; play(); } });
      tabs.appendChild(b);
    });

    var head = el('div', 'aid-head');
    var mark = el('span', 'aid-mark', 'IA');
    var who = el('div', 'aid-who');
    var name = el('strong', 'aid-name');
    var status = el('span', 'aid-status', 'Asistente digital · responde 24 h');
    who.appendChild(name); who.appendChild(status);
    var clock = el('span', 'aid-clock');
    head.appendChild(mark); head.appendChild(who); head.appendChild(clock);

    var log = el('div', 'aid-log');
    log.setAttribute('aria-live', 'polite');

    var foot = el('div', 'aid-foot');
    var note = el('p', 'aid-note');
    var replay = el('button', 'aid-replay', 'Ver de nuevo');
    replay.type = 'button';
    replay.hidden = true;
    replay.addEventListener('click', play);
    foot.appendChild(note); foot.appendChild(replay);

    root.textContent = '';
    root.appendChild(tabs); root.appendChild(head); root.appendChild(log); root.appendChild(foot);

    function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
    function toBottom() { log.scrollTop = log.scrollHeight; }

    function bubble(s, sc, time) {
      if (s[0] === 'e') {
        var ev = el('div', 'aid-event', s[1]);
        log.appendChild(ev);
        return ev;
      }
      var b = el('div', 'aid-msg ' + (s[0] === 'c' ? 'aid-c' : 'aid-a'));
      var t = el('p', 'aid-text', s[1]);
      t.lang = sc.lang;
      if (sc.rtl) t.dir = 'rtl';
      var tr = el('p', 'aid-tr', s[2]);
      tr.lang = 'es';
      var meta = el('span', 'aid-time', time);
      b.appendChild(t); b.appendChild(tr); b.appendChild(meta);
      log.appendChild(b);
      return b;
    }

    function play() {
      timers.forEach(clearTimeout);
      timers = [];
      var sc = SC[key];
      tabs.querySelectorAll('.aid-tab').forEach(function (b) {
        b.setAttribute('aria-selected', String(b.dataset.k === key));
      });
      name.textContent = sc.who;
      clock.textContent = sc.hour;
      note.textContent = 'Escribe en ' + sc.langName + ' · su equipo lo lee en español';
      replay.hidden = true;
      log.textContent = '';

      if (reduce) {
        sc.steps.forEach(function (s, i) { bubble(s, sc, addMinutes(sc.hour, i)).classList.add('aid-in'); });
        replay.hidden = false;
        toBottom();
        return;
      }

      var at = 500;
      sc.steps.forEach(function (s, i) {
        var time = addMinutes(sc.hour, Math.floor(i / 2));
        if (s[0] === 'a') {
          var typing;
          later(function () {
            typing = el('div', 'aid-typing');
            typing.appendChild(el('i')); typing.appendChild(el('i')); typing.appendChild(el('i'));
            typing.setAttribute('aria-label', 'El asistente está escribiendo');
            log.appendChild(typing);
            toBottom();
          }, at);
          at += Math.min(2200, Math.max(900, s[1].length * 14));
          later(function () {
            if (typing) typing.remove();
            bubble(s, sc, time).classList.add('aid-in');
            toBottom();
          }, at);
        } else {
          later(function () { bubble(s, sc, time).classList.add('aid-in'); toBottom(); }, at);
        }
        at += s[0] === 'c' ? 1500 : s[0] === 'e' ? 600 : 1800;
      });
      later(function () { replay.hidden = false; }, at);
    }

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (en) {
        if (!started && en[0].isIntersecting) { started = true; io.disconnect(); play(); }
      }, { threshold: 0.35 });
      io.observe(root);
    } else {
      play();
    }
  }

  function init() { document.querySelectorAll('[data-ai-demo]').forEach(mount); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
