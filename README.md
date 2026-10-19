# Datos RD — Periodismo de Datos de República Dominicana

Plataforma estática y automatizada de periodismo de datos y análisis original sobre la realidad económica, social e institucional de República Dominicana.

El proyecto está diseñado bajo una premisa fundamental: **costo cero de infraestructura** (solo dominio propio), máxima velocidad de carga (Lighthouse 100), diseño accesible con soporte para modo claro/oscuro, y **total transparencia metodológica basada en fuentes públicas oficiales verificadas** (sin cifras inventadas ni datos de muestra).

---

## 📁 Estructura del Repositorio

```text
/
├── AGENTS.md                  # Reglas éticas, editoriales y técnicas obligatorias
├── README.md                   # Esta documentación
├── astro.config.mjs            # Configuración de Astro, i18n y Sitemap
├── package.json                # Scripts y dependencias del proyecto
├── tsconfig.json               # Configuración estricta de TypeScript
├── .env.example                # Plantilla de variables de entorno
├── .github/workflows/ci.yml    # CI/CD: validación y auditoría de enlaces en cada push
├── data/
│   ├── raw/                    # Series originales del BCRD sin modificar
│   │   ├── tasa_cambio_bcrd.csv
│   │   └── inflacion_ipc_canasta_bcrd.csv
│   └── processed/              # Datos limpios listos para componentes gráficos
│       ├── tasa_cambio_bcrd.json / .csv
│       └── inflacion_ipc_canasta_bcrd.json / .csv
├── scripts/                    # Scripts reproducibles de automatización y auditoría
│   ├── requirements.txt        # Dependencias de Python (pandas)
│   ├── procesar_datos_bcrd.py  # Limpieza y transformación de series BCRD
│   ├── sincronizar_bcrd.py     # Pipeline de sincronización y validación de integridad
│   ├── verificar_enlaces.js    # Auditoría de 0 enlaces rotos en dist/
│   └── generar_og_png.js       # Generador de tarjetas Open Graph (1200x630)
├── src/
│   ├── config/site.ts          # Centralización de metadatos, correos y newsletter
│   ├── content/
│   │   ├── config.ts           # Esquema Zod de validación estricta de artículos
│   │   └── articulos/          # Análisis individuales en Markdown
│   ├── components/             # Gráficos SVG (líneas/barras), tarjetas y alertas
│   ├── layouts/                # BaseLayout y ArticuloLayout con microdatos Schema.org
│   ├── styles/global.css       # Estilos accesibles con modo claro y oscuro
│   └── pages/                  # Portada, catálogo de datos, metodología y páginas legales
└── public/
    ├── favicon.svg             # Identidad gráfica provisional
    ├── og-default.png / .svg   # Imagen predeterminada para redes sociales (1200x630)
    └── datos/                  # Enlaces de descarga directa de los archivos CSV
```

---

## 🚀 Inicio Rápido en Local

### Requisitos previos
- **Node.js** v20 o superior.
- **Python** 3.9+ (para ejecutar los scripts de `/scripts`).

### Comandos de desarrollo
```bash
# 1. Instalar dependencias de Node
npm install

# 2. Iniciar servidor local de desarrollo
npm run dev

# 3. Compilar versión estática para producción
npm run build

# 4. Auditar integridad de enlaces internos (verifica 0 enlaces rotos)
npm run check:links

# 5. Previsualizar la compilación estática localmente
npm run preview
```

---

## ⚙️ Configuración Centralizada

Para personalizar los datos de contacto, enlaces y redes del sitio sin tocar el código fuente, edita el archivo [`src/config/site.ts`](src/config/site.ts):

```typescript
export const SITE_CONFIG = {
  nombre: 'Datos RD',
  siteUrl: 'https://datosrd.com',
  autor: 'Redacción Datos RD',
  emailContacto: 'contacto@datosrd.com',
  emailPrivacidad: 'privacidad@datosrd.com',
  newsletterUrl: 'https://datosrd.substack.com/subscribe', // Reemplaza con tu enlace de Substack o Beehiiv
  githubUrl: 'https://github.com/tu-usuario/proyecto-datos-rd',
};
```

---

## 🔄 Automatización y Sincronización de Datos (BCRD)

El portal cuenta con un pipeline automatizado en Python para ingerir datos oficiales del Banco Central de la República Dominicana:

```bash
# Ejecutar pipeline de sincronización y validación de esquemas:
python scripts/sincronizar_bcrd.py
```

Este script:
1. Verifica la disponibilidad de los portales estadísticos del BCRD (`bancentral.gov.do`).
2. Valida la integridad matemática y de columnas de los archivos brutos en `data/raw/`.
3. Transforma y exporta a `data/processed/` en formatos JSON y CSV.
4. Actualiza los archivos públicos en `public/datos/` para que los lectores descarguen la versión más reciente.

---

## ✍️ Publicación de Nuevos Artículos

1. Crea un archivo en `src/content/articulos/AAAA-MM-DD-slug.md`.
2. Completa el frontmatter con validación obligatoria:
   ```yaml
   ---
   titulo: "Título claro y descriptivo del análisis"
   descripcion: "Resumen conciso para SEO (máximo 160 caracteres)."
   fecha: 2026-10-18
   actualizado: 2026-10-18
   categoria: "economia" # economia | precios | energia | presupuesto | transporte | seguridad | educacion | otros
   etiquetas: ["banco central", "inflacion"]
   fuentes:
     - nombre: "Banco Central de la República Dominicana (BCRD)"
       url: "https://www.bancentral.gov.do/a/d/2534-precios"
       fecha_consulta: 2026-10-18
   estado: "borrador" # borrador | revisado | publicado
   tipo: "analisis"   # analisis | explicativo | datos-del-mes | opinion
   ---
   ```
3. Estructura el contenido en las 6 secciones normativas de `AGENTS.md`:
   - Resumen en 3 líneas
   - El dato clave (con gráfico o tabla)
   - Contexto histórico y comparativo
   - Qué significa para el ciudadano
   - Límites del análisis
   - Fuentes y metodología

---

## ☁️ Despliegue Gratuito (Costo Cero)

### Cloudflare Pages (Opción recomendada)
1. Conecta tu repositorio de GitHub o GitLab en [dash.cloudflare.com](https://dash.cloudflare.com).
2. Selecciona **Pages** > **Create application** > **Connect to Git**.
3. Parámetros de compilación:
   - **Framework preset:** `Astro`
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
4. Haz clic en **Save and Deploy**. Cloudflare generará un subdominio SSL gratuito con CDN global de latencia ultra baja.
5. Asocia tu dominio propio (por ejemplo `datosrd.com`) en la pestaña **Custom domains**.

### GitHub Pages (Alternativa)
El archivo `.github/workflows/ci.yml` incluido valida automáticamente la compilación y la ausencia de enlaces rotos en cada commit. Para publicar directamente en GitHub Pages, cambia la fuente de despliegue a **GitHub Actions** en los ajustes del repositorio.

---

## 🛡️ Principios Editoriales y Éticos
- **Cero datos inventados:** Cada cifra proviene de instituciones públicas verificables (BCRD, ONE, Hacienda, DIGEPRES).
- **Independencia y neutralidad:** Análisis descriptivo de datos sin proselitismo político ni opiniones partidarias.
- **Transparencia radical:** Todos los datos que sustentan los gráficos están disponibles para libre descarga en el catálogo de `/datos`.
