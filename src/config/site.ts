export interface ConfigSitio {
  nombre: string;
  nombreCorto: string;
  tagline: string;
  descripcion: string;
  siteUrl: string;
  autor: string;
  emailContacto: string;
  emailPrivacidad: string;
  newsletterUrl: string;
  githubUrl: string;
  locale: string;
}

export const SITE_CONFIG: ConfigSitio = {
  nombre: 'Datos RD',
  nombreCorto: 'Datos RD',
  tagline: 'Periodismo de datos local de República Dominicana',
  descripcion:
    'Análisis cuantitativo original, gráficos interactivos y datos verificables sobre economía, precios, energía y presupuesto público en República Dominicana.',
  siteUrl: 'https://datosrd.com',
  autor: 'Redacción Datos RD',
  emailContacto: 'contacto@datosrd.com',
  emailPrivacidad: 'privacidad@datosrd.com',
  newsletterUrl: 'https://datosrd.substack.com/subscribe',
  githubUrl: 'https://github.com/tu-usuario/proyecto-datos-rd',
  locale: 'es_DO',
};
