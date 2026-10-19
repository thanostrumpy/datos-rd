import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://datosrd.com',
  integrations: [sitemap()],
  i18n: {
    defaultLocale: 'es',
    locales: ['es'],
  },
});
