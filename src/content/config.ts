import { defineCollection, z } from 'astro:content';

const articulos = defineCollection({
  type: 'content',
  schema: z.object({
    titulo: z.string(),
    descripcion: z.string().max(160, 'La descripción debe tener un máximo de 160 caracteres para SEO'),
    fecha: z.coerce.date(),
    actualizado: z.coerce.date().optional(),
    categoria: z.enum([
      'economia',
      'precios',
      'energia',
      'presupuesto',
      'transporte',
      'seguridad',
      'educacion',
      'otros',
    ]),
    etiquetas: z.array(z.string()).default([]),
    fuentes: z.array(
      z.object({
        nombre: z.string(),
        url: z.string().url(),
        fecha_consulta: z.coerce.date(),
      })
    ),
    estado: z.enum(['borrador', 'revisado', 'publicado']).default('borrador'),
    tipo: z.enum(['analisis', 'explicativo', 'datos-del-mes', 'opinion']).default('analisis'),
  }),
});

export const collections = {
  articulos,
};
