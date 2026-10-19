import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '..');

const svgPath = path.join(root, 'public', 'og-default.svg');
const pngPath = path.join(root, 'public', 'og-default.png');

try {
  const sharp = (await import('sharp')).default;
  const svgBuffer = fs.readFileSync(svgPath);
  await sharp(svgBuffer)
    .resize(1200, 630)
    .png({ quality: 90 })
    .toFile(pngPath);
  console.log(`[✓] Imagen Open Graph PNG generada con éxito en: ${pngPath}`);
} catch (err) {
  console.warn(`[!] sharp no pudo renderizar directamente (${err.message}). Creando fallback PNG.`);
  // Fallback: si sharp no está en el entorno del sistema, copiamos el SVG como fallback
  fs.copyFileSync(svgPath, pngPath.replace('.png', '.svg'));
}
