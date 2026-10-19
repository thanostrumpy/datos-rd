# AGENTS.md — Datos RD (análisis de datos de noticias locales de República Dominicana)

## 1. Qué es este proyecto
Un sitio web de **periodismo de datos y análisis** sobre la actualidad de República Dominicana. No es un agregador ni un sitio de noticias genéricas: cada publicación aporta **análisis original** (gráficos, comparativas, contexto y datos verificables) sobre un tema de actualidad local.

- **Idioma del sitio y del contenido:** español dominicano neutro, claro y sin jerga innecesaria.
- **Audiencia:** dominicanos que quieren entender los números detrás de las noticias (economía, precios, tasa de cambio, inflación, energía, transporte, seguridad, educación, presupuesto público).
- **Objetivo de negocio:** construir tráfico orgánico y un newsletter, y monetizar por etapas (afiliados relevantes, luego AdSense cuando haya volumen).
- **Restricción:** costo cero de infraestructura. Solo se admite gasto en el dominio propio.

## 2. Reglas editoriales (NO negociables)
1. **Nunca copiar ni reescribir artículos de otros medios.** Se pueden citar hechos con atribución, pero el texto debe ser propio. Citas textuales: máximo una frase corta, siempre con enlace a la fuente.
2. **Cada artículo debe incluir al menos un elemento original:** un gráfico, una tabla comparativa, un cálculo propio o contexto histórico con datos.
3. **Toda cifra lleva fuente y fecha.** Formato: "Fuente: Banco Central de la República Dominicana, datos a septiembre 2026" con enlace.
4. **No inventar datos, citas ni fuentes.** Si un dato no se puede verificar, se omite o se marca claramente como estimación con su método.
5. **Distinguir hecho de interpretación.** Las opiniones se etiquetan como análisis u opinión.
6. **Neutralidad política.** Se analizan datos, no se hace campaña a favor o en contra de partidos o personas.
7. **Personas privadas:** no publicar datos personales. Sobre figuras públicas, solo información de interés público y verificable.
8. **Contenido generado con IA:** el agente puede redactar borradores, pero todo artículo se marca como `borrador` hasta que el autor humano lo verifique y lo apruebe. El agente nunca publica por su cuenta.
9. **Correcciones:** si un dato resulta erróneo, se corrige y se añade una nota visible de "Actualización/Corrección" con fecha.

## 3. Fuentes de datos preferidas (públicas y gratuitas)
Priorizar siempre fuentes oficiales y abiertas:
- Banco Central de la República Dominicana (BCRD): tasa de cambio, inflación, PIB, remesas.
- Oficina Nacional de Estadística (ONE): estadísticas oficiales.
- Ministerio de Hacienda y Dirección General de Presupuesto (DIGEPRES): presupuesto y ejecución.
- Dirección General de Contrataciones Públicas: compras del Estado.
- Portal de Datos Abiertos del gobierno dominicano (datos.gob.do).
- Superintendencia de Bancos, Superintendencia de Valores, Pro Consumidor, SIE (energía e hidrocarburos), INTRANT (tránsito).
- Organismos internacionales: Banco Mundial, FMI, CEPAL, cuando aporten comparación regional.

Antes de usar una fuente nueva: verificar que sus datos sean públicos y revisar sus términos de uso. Guardar siempre la URL, la fecha de consulta y la licencia, si la hay.

## 4. Stack técnico
Elegido por ser gratuito, rápido y compatible con SEO:
- **Framework:** Astro (sitio estático), con contenido en Markdown/MDX.
- **Estilos:** CSS simple o Tailwind. Diseño sobrio, legible y optimizado para móvil.
- **Gráficos:** librerías de gráficos que funcionen sin servidor (por ejemplo Chart.js o Observable Plot), con datos embebidos en el sitio.
- **Datos:** archivos CSV/JSON versionados en el repositorio dentro de `/data`.
- **Procesamiento:** scripts en Python (pandas) en `/scripts` para limpiar y transformar datos. Los resultados se guardan en `/data/processed`.
- **Hosting:** Cloudflare Pages o GitHub Pages (plan gratuito).
- **Newsletter:** formulario de un servicio con plan gratuito (Beehiiv o Substack), sin backend propio.
- **Analítica:** una herramienta gratuita y respetuosa con la privacidad (por ejemplo Cloudflare Web Analytics).

No agregar dependencias de pago, servicios con tarjeta obligatoria ni servidores propios sin aprobación explícita del autor.

## 5. Estructura del repositorio
```
/
├── AGENTS.md
├── README.md
├── astro.config.mjs
├── package.json
├── data/
│   ├── raw/            # datos originales, sin modificar
│   └── processed/      # datos limpios listos para graficar
├── scripts/            # Python para limpieza y análisis
├── src/
│   ├── content/
│   │   └── articulos/  # un archivo .md por artículo
│   ├── components/     # gráficos, tablas, tarjetas, avisos
│   ├── layouts/
│   └── pages/
└── public/
```

## 6. Formato de cada artículo
Archivo en `src/content/articulos/AAAA-MM-DD-slug.md` con este frontmatter:

```yaml
---
titulo: ""
descripcion: ""        # máximo 160 caracteres, para SEO
fecha: AAAA-MM-DD
actualizado: AAAA-MM-DD
categoria: ""          # economia | precios | energia | presupuesto | transporte | seguridad | educacion | otros
etiquetas: []
fuentes:
  - nombre: ""
    url: ""
    fecha_consulta: AAAA-MM-DD
estado: borrador       # borrador | revisado | publicado
tipo: analisis         # analisis | explicativo | datos-del-mes | opinion
---
```

Estructura del cuerpo:
1. **Resumen en 3 líneas** (qué pasó y qué dicen los datos).
2. **El dato clave** con su gráfico o tabla.
3. **Contexto** (cómo se compara con meses o años anteriores, o con otros países).
4. **Qué significa para el ciudadano** (impacto práctico).
5. **Límites del análisis** (qué no dicen los datos).
6. **Fuentes y metodología.**

## 7. Reglas de código
- Sitio **estático**, sin backend. Todo debe poder construirse con `npm run build`.
- Rendimiento: puntuación alta en Lighthouse, imágenes optimizadas, sin scripts innecesarios.
- Accesibilidad: contraste suficiente, texto alternativo en gráficos, tablas con encabezados.
- SEO: títulos únicos, meta descripción, datos estructurados de tipo Article, sitemap y RSS.
- Cada gráfico incluye título, unidades, fuente y fecha del dato.
- Código comentado donde no sea evidente. Scripts de Python reproducibles: mismo dato de entrada, mismo resultado.
- No hardcodear claves ni tokens. Usar variables de entorno y nunca subirlas al repositorio.

## 8. Páginas obligatorias del sitio
- **Inicio:** últimos análisis, un gráfico destacado y suscripción al newsletter.
- **Artículos:** listado con filtros por categoría.
- **Datos:** catálogo de los conjuntos de datos usados, con descarga en CSV.
- **Metodología:** cómo se recopilan, limpian y verifican los datos.
- **Sobre el proyecto:** quién lo hace y por qué.
- **Contacto y correcciones:** vía para reportar errores.
- **Política de privacidad, términos y aviso legal:** necesarias para AdSense y afiliados.
- **Aviso de afiliados** visible en cualquier contenido con enlaces de afiliado.

## 9. Monetización (por etapas)
1. **Etapa 1 (0 a 3 meses):** construir el sitio, publicar con regularidad y abrir el newsletter. Sin anuncios.
2. **Etapa 2:** enlaces de afiliados **solo si son relevantes y útiles** para el lector (por ejemplo herramientas financieras o de datos), siempre con aviso claro.
3. **Etapa 3:** solicitar AdSense cuando el sitio tenga contenido original suficiente, páginas legales completas y tráfico constante.

El agente no debe llenar el sitio de anuncios ni de enlaces de afiliados que perjudiquen la experiencia o la credibilidad.

## 10. Cómo trabajar con el agente
- **Antes de grandes cambios:** proponer un plan breve y esperar aprobación.
- **Cambios pequeños:** hacerlos directamente y resumir qué se cambió.
- **Al crear un artículo:** listar primero las fuentes y los datos que se usarán, y luego redactar el borrador.
- **Si falta un dato o hay duda sobre una cifra:** preguntar, no suponer.
- **Verificación:** antes de dar una tarea por terminada, correr `npm run build` y comprobar que no hay enlaces rotos ni errores.
- **Commits:** mensajes cortos y descriptivos en español (por ejemplo "Agrega análisis de inflación de septiembre").
- **Idioma de trabajo:** responder y documentar en español.

## 11. Lo que el agente NO debe hacer
- Publicar contenido sin aprobación humana.
- Copiar, parafrasear de forma cercana o "reescribir" notas de otros medios.
- Generar artículos en masa sin análisis ni datos propios.
- Inventar cifras, citas, entrevistas o fuentes.
- Usar imágenes con derechos de autor sin licencia. Preferir gráficos propios o imágenes libres con atribución.
- Añadir servicios de pago o dependencias que obliguen a gastar dinero.
