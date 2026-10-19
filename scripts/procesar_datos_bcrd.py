#!/usr/bin/env python3
"""
Script automatizado de procesamiento y validación de datos oficiales.
Fuente: Banco Central de la República Dominicana (BCRD)
Proyecto: Datos RD

Procesa de forma reproducible:
1. Mercado cambiario spot (USD/DOP) -> data/raw/tasa_cambio_bcrd.csv
2. Inflación interanual (IPC) y costo de canasta familiar -> data/raw/inflacion_ipc_canasta_bcrd.csv
"""

import sys
import json
from pathlib import Path
import pandas as pd


def procesar_tasa_cambio(ruta_raw: Path, ruta_csv: Path, ruta_json: Path):
    print(f"[*] Procesando datos cambiarios oficiales desde: {ruta_raw.name}")
    df = pd.read_csv(ruta_raw, comment="#")
    df.columns = [c.strip().lower() for c in df.columns]

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["compra"] = pd.to_numeric(df["compra"])
    df["venta"] = pd.to_numeric(df["venta"])
    df = df.sort_values("fecha").reset_index(drop=True)

    df["fecha_fmt"] = df["fecha"].dt.strftime("%Y-%m")
    df["promedio"] = ((df["compra"] + df["venta"]) / 2).round(2)
    df["var_pct"] = (df["promedio"].pct_change() * 100).round(2).fillna(0.0)

    df_salida = df[["fecha_fmt", "compra", "venta", "promedio", "var_pct"]].rename(
        columns={"fecha_fmt": "fecha"}
    )
    df_salida.to_csv(ruta_csv, index=False)

    registros = df_salida.to_dict(orient="records")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

    print(f"[✓] Tasa de cambio guardada: {len(df_salida)} registros.")


def procesar_inflacion(ruta_raw: Path, ruta_csv: Path, ruta_json: Path):
    print(f"[*] Procesando datos de inflación oficiales desde: {ruta_raw.name}")
    df = pd.read_csv(ruta_raw, comment="#")
    df.columns = [c.strip().lower() for c in df.columns]

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["inflacion_interanual"] = pd.to_numeric(df["inflacion_interanual"]).round(2)
    df["inflacion_subyacente"] = pd.to_numeric(df["inflacion_subyacente"]).round(2)
    df["costo_canasta_promedio"] = pd.to_numeric(df["costo_canasta_promedio"]).round(2)
    df = df.sort_values("fecha").reset_index(drop=True)

    df["fecha_fmt"] = df["fecha"].dt.strftime("%Y-%m")
    df_salida = df[["fecha_fmt", "inflacion_interanual", "inflacion_subyacente", "costo_canasta_promedio"]].rename(
        columns={"fecha_fmt": "fecha", "costo_canasta_promedio": "costo_canasta"}
    )
    df_salida.to_csv(ruta_csv, index=False)

    registros = df_salida.to_dict(orient="records")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

    print(f"[✓] Inflación y canasta familiar guardadas: {len(df_salida)} registros.")


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent

    # 1. Tasa de cambio
    raw_tc = raiz / "data" / "raw" / "tasa_cambio_bcrd.csv"
    csv_tc = raiz / "data" / "processed" / "tasa_cambio_bcrd.csv"
    json_tc = raiz / "data" / "processed" / "tasa_cambio_bcrd.json"
    procesar_tasa_cambio(raw_tc, csv_tc, json_tc)

    # 2. Inflación e IPC
    raw_inf = raiz / "data" / "raw" / "inflacion_ipc_canasta_bcrd.csv"
    csv_inf = raiz / "data" / "processed" / "inflacion_ipc_canasta_bcrd.csv"
    json_inf = raiz / "data" / "processed" / "inflacion_ipc_canasta_bcrd.json"
    procesar_inflacion(raw_inf, csv_inf, json_inf)
