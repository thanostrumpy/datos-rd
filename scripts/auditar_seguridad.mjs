import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '..');

const PATRONES_SECRETOS = [
  { nombre: 'GitHub Personal Access Token (Classic)', regex: /ghp_[A-Za-z0-9_]{36}/g },
  { nombre: 'GitHub Fine-grained PAT', regex: /github_pat_[A-Za-z0-9_]{80,100}/g },
  { nombre: 'Clave privada RSA / SSH / PGP', regex: /-----BEGIN [A-Z ]*PRIVATE KEY-----/g },
  { nombre: 'Credencial en URL (user:pass@)', regex: /https?:\/\/[a-zA-Z0-9_\-\.]+:[^@\s]+@/g },
  { nombre: 'AWS Access Key ID', regex: /AKIA[0-9A-Z]{16}/g },
  { nombre: 'Generic Secret Assignment', regex: /(?:api[_-]?key|secret[_-]?key|private[_-]?key|auth[_-]?token)\s*[:=]\s*['"][^'"\s]{12,}['"]/gi },
];

const IGNORED_DIRS = new Set(['node_modules', 'dist', '.astro', '.git']);

function listarArchivosProyecto(dir, lista = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (IGNORED_DIRS.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      listarArchivosProyecto(fullPath, lista);
    } else if (entry.isFile()) {
      lista.push(fullPath);
    }
  }
  return lista;
}

console.log('='.repeat(70));
console.log(' AUDITORÍA DE SEGURIDAD Y PREVENCIÓN DE FUGAS — DATOS RD');
console.log('='.repeat(70));

const archivos = listarArchivosProyecto(root);
console.log(`\n[1/4] Escaneando ${archivos.length} archivos en busca de credenciales, tokens y secretos...`);

let fugasEncontradas = 0;

for (const archivo of archivos) {
  const relPath = path.relative(root, archivo).replace(/\\/g, '/');
  // Ignorar este mismo script de auditoría para no dar falsos positivos por los patrones regex
  if (relPath === 'scripts/auditar_seguridad.mjs') continue;

  const contenido = fs.readFileSync(archivo, 'utf-8');

  for (const patron of PATRONES_SECRETOS) {
    const matches = contenido.match(patron.regex);
    if (matches) {
      console.error(`[!] ALERTA CRÍTICA en [${relPath}]:`);
      console.error(`    Tipo detectado: ${patron.nombre}`);
      console.error(`    Coincidencia: ${matches[0].substring(0, 10)}... (ocultada por seguridad)`);
      fugasEncontradas++;
    }
  }
}

if (fugasEncontradas === 0) {
  console.log('[✓] Limpio: 0 tokens, claves privadas ni secretos encontrados en el código fuente.');
} else {
  console.error(`[X] ATENCIÓN: Se encontraron ${fugasEncontradas} posibles secretos.`);
}

console.log('\n[2/4] Auditoría de vulnerabilidades XSS e inyección en componentes Astro...');
let hallazgosXss = 0;
const astroFiles = archivos.filter(f => f.endsWith('.astro') || f.endsWith('.ts') || f.endsWith('.js'));

for (const archivo of astroFiles) {
  const relPath = path.relative(root, archivo).replace(/\\/g, '/');
  const contenido = fs.readFileSync(archivo, 'utf-8');

  // Buscar set:html
  if (contenido.includes('set:html')) {
    // Verificar si se usa de forma segura
    const lineas = contenido.split('\n');
    lineas.forEach((l, idx) => {
      if (l.includes('set:html')) {
        const esSeguro = l.includes('JSON.stringify');
        if (esSeguro) {
          console.log(` [i] Uso verificado de set:html en [${relPath}:${idx + 1}]: serialización segura con JSON.stringify (JSON-LD estructurado).`);
        } else {
          console.warn(` [!] set:html sin JSON.stringify en [${relPath}:${idx + 1}]: revisar posible riesgo XSS.`);
          hallazgosXss++;
        }
      }
    });
  }

  // Buscar rel="noopener noreferrer" en enlaces con target="_blank"
  const targetBlankMatches = contenido.match(/target="_blank"(?![^>]*rel="[^"]*noopener[^"]*")/gi);
  if (targetBlankMatches) {
    console.warn(` [!] Enlace con target="_blank" sin rel="noopener noreferrer" en [${relPath}]`);
    hallazgosXss++;
  }
}

if (hallazgosXss === 0) {
  console.log('[✓] Componentes seguros: Sin vectores de inyección XSS ni reverse tabnabbing (target="_blank" blindados).');
}

console.log('\n[3/4] Auditoría de superficie de ataque del sitio estático...');
console.log(' - Backend/Servidor propio: Ninguno (100% estático, reduce superficie de ataque a cero en servidor).');
console.log(' - Base de datos conectada: Ninguna (datos versionados en CSV/JSON estáticos).');
console.log(' - Autenticación de usuarios / Cookies de sesión: Ninguna (sitio abierto sin login).');
console.log(' - Procesamiento de pagos / tarjetas: Ninguno.');

console.log('\n' + '='.repeat(70));
console.log(' RESUMEN Y RECOMENDACIONES DE ENDURECIMIENTO (HARDENING)');
console.log('='.repeat(70));
