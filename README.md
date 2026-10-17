# IA & Marketing Ferreras · propuesta de rediseño

Concepto: **«Las 24 horas»**. Un reloj Ferreras (la esfera real de la marca) acompaña la página y sus agujas avanzan
con el scroll: de día el marketing que atrae (oro), de noche la IA que atiende (la señal azul del logotipo). A las
23:40 entra una consulta en alemán y el agente la pasa a recepción; veinticuatro horas después, el diagnóstico.

Sitio estático (HTML, CSS y JavaScript sin dependencias), publicado en GitHub Pages con `noindex`: es una propuesta,
no el sitio oficial. Todos los textos, fotografías, vídeos y casos proceden de marketingferreras.com y de sus redes.

- `index.html` y una carpeta por página; `estilo.css`; `js/` (un archivo por sección); `img/`, `video/`, `fonts/`.
- `_fonte/build.py` escribe todas las páginas a partir del contenido (`_fonte/paginas.py`): `python -I _fonte/build.py`.
- Los formularios no envían datos a ningún servidor: abren el correo con el mensaje ya escrito para
  administracion@marketingferreras.com.
