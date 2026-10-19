import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async (context) => {
  const articulos = await getCollection('articulos');
  const articulosOrdenados = articulos.sort(
    (a, b) => b.data.fecha.getTime() - a.data.fecha.getTime()
  );

  return rss({
    title: 'Datos RD — Periodismo de datos de República Dominicana',
    description: 'Análisis original y visualización de datos sobre economía, precios y actualidad dominicana.',
    site: context.site ? context.site.toString() : 'https://datosrd.com',
    items: articulosOrdenados.map((articulo) => ({
      title: articulo.data.titulo,
      pubDate: articulo.data.fecha,
      description: articulo.data.descripcion,
      link: `/articulos/${articulo.slug}/`,
      categories: [articulo.data.categoria, ...articulo.data.etiquetas],
    })),
    customData: '<language>es-DO</language>',
  });
};
