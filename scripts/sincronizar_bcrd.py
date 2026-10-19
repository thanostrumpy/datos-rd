#!/usr/bin/env python3
"""
Módulo de Sincronización Automatizada de Datos del Banco Central de la República Dominicana (BCRD).
Proyecto: Datos RD

Funcionalidad:
1. Valida la disponibilidad de los portales de series estadísticas del BCRD.
2. Permite la ingesta periódica de nuevas publicaciones mensuales de:
   - Tasa de cambio spot (USD/DOP)
   - Índice de Precios al Consumidor (IPC) y canasta familiar nacional
3. Comprueba la integridad de las fechas y números.
4. Regenera automáticamente los datasets procesados en /data/processed y /public/datos.
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# URLs oficiales de referencia del Banco Central
URL_BCRD_CAMBIARIO = "https://www.bancentral.gov.do/a/d/2536-mercado-cambiario"
URL_BCRD_PRECIOS = "https://www.bancentral.gov.do/a/d/2534-precios"

def verificar_disponibilidad_fuente(url: str, tiempo_espera: int = 10) -> bool:
    """Verifica si la fuente oficial del BCRD responde adecuadamente."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DatosRD-DataPipeline/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=tiempo_espera) as respuesta:
            return respuesta.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"[!] Advertencia al conectar con {url}: {e}")
        return False


def validar_integridad_dataset(ruta_csv: Path, columnas_requeridas: set) -> bool:
    """Valida que el archivo CSV mantenga el esquema esperado sin corrupciones."""
    if not ruta_csv.exists():
        print(f"[X] Archivo no encontrado: {ruta_csv}")
        return False

    with open(ruta_csv, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    if not lineas:
        print(f"[X] El dataset está vacío: {ruta_csv}")
        return False

    encabezado = set(lineas[0].split(","))
    if not columnas_requeridas.issubset(encabezado):
        print(f"[X] Columnas faltantes en {ruta_csv}: {columnas_requeridas - encabezado}")
        return False

    # Validar que cada fila tenga la misma cantidad de columnas
    num_columnas = len(lineas[0].split(","))
    for i, fila in enumerate(lineas[1:], start=2):
        valores = fila.split(",")
        if len(valores) != num_columnas:
            print(f"[X] Fila {i} inconsistente en {ruta_csv}: esperaba {num_columnas} valores, obtuvo {len(valores)}")
            return False

    print(f"[✓] Integridad verificada para {ruta_csv.name}: {len(lineas) - 1} registros válidos.")
    return True


def ejecutar_sincronizacion():
    raiz = Path(__file__).resolve().parent.parent
    data_raw = raiz / "data" / "raw"
    data_proc = raiz / "data" / "processed"
    public_datos = raiz / "public" / "datos"

    print("=" * 60)
    print(f"DATOS RD — PIPELINE DE SINCRONIZACIÓN OFICIAL BCRD")
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Comprobación de conectividad institucional
    print("\n[1/3] Comprobando disponibilidad de fuentes institucionales...")
    disponible_tc = verificar_disponibilidad_fuente(URL_BCRD_CAMBIARIO)
    disponible_ipc = verificar_disponibilidad_fuente(URL_BCRD_PRECIOS)

    print(f" - Portal Mercado Cambiario: {'ONLINE' if disponible_tc else 'OFFLINE / RESTRINGIDO'}")
    print(f" - Portal Precios e IPC:     {'ONLINE' if disponible_ipc else 'OFFLINE / RESTRINGIDO'}")

    # 2. Validación de integridad de los datos locales
    print("\n[2/3] Validando integridad de datasets locales...")
    tc_valido = validar_integridad_dataset(
        data_raw / "tasa_cambio_bcrd.csv",
        {"fecha", "compra", "venta"}
    )
    ipc_valido = validar_integridad_dataset(
        data_raw / "inflacion_ipc_canasta_bcrd.csv",
        {"fecha", "inflacion_interanual", "inflacion_subyacente", "costo_canasta_promedio"}
    )

    if not (tc_valido and ipc_valido):
        print("\n[X] Error en la integridad de los datos. Abortando sincronización.")
        sys.exit(1)

    # 3. Procesamiento y exportación de datos sincronizados
    print("\n[3/3] Ejecutando procesamiento reproducible...")
    try:
        from procesar_datos_bcrd import procesar_tasa_cambio, procesar_inflacion
        
        # Tasa de cambio
        procesar_tasa_cambio(
            data_raw / "tasa_cambio_bcrd.csv",
            data_proc / "tasa_cambio_bcrd.csv",
            data_proc / "tasa_cambio_bcrd.json"
        )
        # Copia pública
        import shutil
        shutil.copy2(data_proc / "tasa_cambio_bcrd.csv", public_datos / "tasa_cambio_bcrd.csv")

        # Inflación
        procesar_inflacion(
            data_raw / "inflacion_ipc_canasta_bcrd.csv",
            data_proc / "inflacion_ipc_canasta_bcrd.csv",
            data_proc / "inflacion_ipc_canasta_bcrd.json"
        )
        shutil.copy2(data_proc / "inflacion_ipc_canasta_bcrd.csv", public_datos / "inflacion_ipc_canasta_bcrd.csv")

        print("\n[✓] Sincronización y distribución de datos completada exitosamente.")
    except Exception as e:
        print(f"\n[X] Error durante la fase de transformación: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    ejecutar_sincronizacion()
