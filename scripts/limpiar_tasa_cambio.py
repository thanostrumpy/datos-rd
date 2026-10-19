#!/usr/bin/env python3
"""
Script de procesamiento y limpieza para datos de Tasa de Cambio (USD/DOP).
Proyecto: Datos RD

Función:
1. Lee el archivo CSV bruto desde data/raw/.
2. Ignora líneas de comentarios informativos (#).
3. Estandariza fechas en formato ISO (YYYY-MM-DD).
4. Limpia valores numéricos y descarta o reporta registros nulos.
5. Ordena cronológicamente.
6. Exporta el resultado depurado a data/processed/ en formato CSV y JSON
   para su consumo directo por los componentes gráficos del sitio web.

Reproducibilidad:
Mismo archivo de entrada garantiza el mismo resultado de salida.
"""

import sys
import json
from pathlib import Path
import pandas as pd


def limpiar_tasa_cambio(ruta_entrada: Path, ruta_salida_csv: Path, ruta_salida_json: Path):
    """
    Limpia y transforma los datos de tasa de cambio.
    """
    print(f"[*] Leyendo archivo bruto: {ruta_entrada}")
    
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_entrada}")

    # 1. Leer CSV ignorando comentarios iniciales
    df = pd.read_csv(ruta_entrada, comment="#")

    # 2. Normalizar nombres de columnas a minúsculas y sin espacios
    df.columns = [c.strip().lower() for c in df.columns]

    columnas_esperadas = {"fecha", "compra", "venta"}
    if not columnas_esperadas.issubset(set(df.columns)):
        raise ValueError(f"El archivo debe contener las columnas: {columnas_esperadas}")

    # 3. Conversión y validación de tipos
    # Fechas
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    
    # Valores numéricos
    df["compra"] = pd.to_numeric(df["compra"], errors="coerce")
    df["venta"] = pd.to_numeric(df["venta"], errors="coerce")

    # 4. Tratamiento de valores nulos o inválidos
    total_filas = len(df)
    df = df.dropna(subset=["fecha", "compra", "venta"])
    filas_validas = len(df)
    
    if filas_validas < total_filas:
        print(f"[!] Se descartaron {total_filas - filas_validas} filas con valores nulos o no válidos.")

    # 5. Ordenamiento cronológico y reseteo de índice
    df = df.sort_values("fecha").reset_index(drop=True)

    # Formatear fecha a string YYYY-MM-DD para serialización limpia
    df["fecha_str"] = df["fecha"].dt.strftime("%Y-%m-%d")

    # 6. Cálculo de métricas adicionales de contexto
    # Promedio entre compra y venta
    df["promedio"] = ((df["compra"] + df["venta"]) / 2).round(2)
    # Variación porcentual interperíodo respecto al anterior
    df["var_pct"] = (df["promedio"].pct_change() * 100).round(2).fillna(0.0)

    # Asegurar que el directorio de salida existe
    ruta_salida_csv.parent.mkdir(parents=True, exist_ok=True)
    ruta_salida_json.parent.mkdir(parents=True, exist_ok=True)

    # 7. Exportación a CSV procesado
    columnas_finales = ["fecha_str", "compra", "venta", "promedio", "var_pct"]
    df_export = df[columnas_finales].rename(columns={"fecha_str": "fecha"})
    df_export.to_csv(ruta_salida_csv, index=False)
    print(f"[+] Archivo CSV procesado guardado en: {ruta_salida_csv}")

    # 8. Exportación a JSON estructurado para gráficos web
    registros = df_export.to_dict(orient="records")
    with open(ruta_salida_json, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)
    print(f"[+] Archivo JSON para visualización guardado en: {ruta_salida_json}")

    print(f"[✓] Proceso completado exitosamente. {len(df_export)} registros procesados.")
    return df_export


if __name__ == "__main__":
    # Rutas relativas a la raíz del repositorio
    raiz = Path(__file__).resolve().parent.parent
    entrada = raiz / "data" / "raw" / "tasa_cambio_ejemplo.csv"
    salida_csv = raiz / "data" / "processed" / "tasa_cambio_ejemplo.csv"
    salida_json = raiz / "data" / "processed" / "tasa_cambio_ejemplo.json"

    try:
        limpiar_tasa_cambio(entrada, salida_csv, salida_json)
    except Exception as e:
        print(f"[X] Error durante el procesamiento: {e}", file=sys.stderr)
        sys.exit(1)
