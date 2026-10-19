#!/usr/bin/env node
/**
 * Script de Auditoría de Enlaces Internos e Integridad de Rutas Estáticas.
 * Proyecto: Datos RD
 *
 * Examina los archivos HTML generados en la carpeta `dist/` para comprobar
 * que cada enlace interno, recurso o archivo enlazado exista físicamente.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distDir = path.resolve(__dirname, '../dist');

if (!fs.existsSync(distDir)) {
  console.error('[X] El directorio dist/ no existe. Ejecuta primero "npm run build".');
  process.exit(1);
}

function buscarArchivosHtml(dir, lista = []) {
  const archivos = fs.readdirSync(dir);
  for (const archivo of archivos) {
    const rutaCompleta = path.join(dir, archivo);
    const stat = fs.statSync(rutaCompleta);
    if (stat.isDirectory()) {
      buscarArchivosHtml(rutaCompleta, lista);
    } else if (archivo.endsWith('.html')) {
      lista.push(rutaCompleta);
    }
  }
  return lista;
}

const htmlFiles = buscarArchivosHtml(distDir);
console.log(`[*] Analizando ${htmlFiles.length} páginas generadas en dist/...`);

let totalEnlacesRevisados = 0;
let errores = 0;

const regexHref = /(?:href|src)=["']([^"']+)["']/g;

for (const file of htmlFiles) {
  const contenido = fs.readFileSync(file, 'utf-8');
  const fileRelativo = path.relative(distDir, file);
  let match;

  while ((match = regexHref.exec(contenido)) !== null) {
    const url = match[1];

    // Ignorar enlaces externos, anclas o protocolos especiales
    if (
      url.startsWith('http://') ||
      url.startsWith('https://') ||
      url.startsWith('mailto:') ||
      url.startsWith('tel:') ||
      url.startsWith('javascript:') ||
      url.startsWith('#') ||
      url.startsWith('data:')
    ) {
      continue;
    }

    totalEnlacesRevisados++;

    // Extraer ruta limpia sin hash ni query params
    const rutaLimpia = url.split('#')[0].split('?')[0];
    if (!rutaLimpia) continue; // Solo era un ancla #

    // Comprobar destino en dist
    let rutaDestino;
    if (rutaLimpia.startsWith('/')) {
      rutaDestino = path.join(distDir, rutaLimpia.substring(1));
    } else {
      rutaDestino = path.resolve(path.dirname(file), rutaLimpia);
    }

    // Posibles candidatos para rutas en Astro (directorio con index.html o archivo exacto)
    const existeArchivoExacto = fs.existsSync(rutaDestino) && fs.statSync(rutaDestino).isFile();
    const existeComoDirectorioConIndex = fs.existsSync(path.join(rutaDestino, 'index.html'));
    const existeConHtml = fs.existsSync(`${rutaDestino}.html`);

    if (!existeArchivoExacto && !existeComoDirectorioConIndex && !existeConHtml) {
      console.error(`[!] Enlace roto detectado en [${fileRelativo}]: "${url}" -> no se encuentra en disco.`);
      errores++;
    }
  }
}

console.log('\n' + '='.repeat(60));
console.log(`Total de enlaces internos auditados: ${totalEnlacesRevisados}`);
if (errores === 0) {
  console.log('[✓] ÉXITO: 0 enlaces rotos detectados en todo el sitio estático.');
  process.exit(0);
} else {
  console.error(`[X] FALLO: Se encontraron ${errores} enlaces rotos.`);
  process.exit(1);
}
