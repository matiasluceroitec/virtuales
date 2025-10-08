from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from django.conf import settings


@dataclass
class DashboardResult:
    """
    Retornar el resultado de los KPIs y rutas a las imagenes

    kpis: Diccionario de metricas
    figures: Lista tuplas (titulo, ruta relativa)
    """
    kpis: Dict[str, Any]
    figures: List[Tuple[str, str]]


def _ensure_media_dir() -> Path:
    """
    Crea el directorio de salida de las imagenes de grafico si no exite
    """

    out_dir = Path(settings.MEDIA_ROOT) / "analytics"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def _save_fig(fig: plt.Figure, filename: str) -> str:
    """
    Guardar la figura y devuelve la ruta accesible por MEDIA_URL
    
    Return ejemplo "analytics/ventas.png"
    """

    # 1) Resolvemos el directorio de salida
    out_dir = _ensure_media_dir()

    # 2) Componemos la ruta
    path = out_dir / filename

    # 3) Guardamos la imagen
    fig.savefig(path)
    plt.close(fig)

    # 4) Devolvemos la ruta relativa
    #    relativa a MEDIA_ROOT para concatenar con MEDIA_URL en templates
    relative = Path(path).resolve().relative_to(Path(settings.MEDIA_ROOT).resolve())
    return str(relative).replace("\\", "/")


def build_bashboard(df: pd.DataFrame) -> DashboardResult:
    """
    Calcula KPIs y genera los graficos para mostrarlos
    a partir de un DataFrame
    """

    # Caso 0: si no hay datos, devolvemos KPIs en cero y sin imagenes
    if df is None or df.empty:
        kpis = {
            "total_ventas": 0.0,
            "cant_ordenes": 0.0,
            "ticket_medio": 0.0,
            "top_producto": "-",
        }
        figures = []
        return DashboardResult(kpis=kpis, figures=figures)
    
    # Caso 1: si hay info
    ## Paso 1: asegurar tipos y columnas necesarias
    df = df.copy()

    # a) Convertimos la fecha a datetime, "errors='coerce' -> NaT"
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # b) Convertimos a numericos los floats e int
    for col in ["price", "quantity", "total"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # c) Reemplazamos los NaN por 0
    df[["price", "quantity", "total"]] = df[["price", "quantity", "total"]].fillna(0)

    ## Paso 2 KPIs con pandas y numpy
    total_ventas = float(df["total"].sum())
    cant_ordenes = int(df["order_id"].nunique())
    ventas_por_orden = df.groupby("order_id")["total"].sum()
    ticket_medio = float(ventas_por_orden.mean()) if not ventas_por_orden.empty else 0.0

    ingresos_por_producto = (
        df.groupby("product")["total"].sum().sort_values(ascending=False)
    )
    top_producto = ingresos_por_producto.index[0]

    kpis = {
        "total_ventas": round(total_ventas, 2),
        "cant_ordenes": cant_ordenes,
        "ticket_medio": round(ticket_medio, 2),
        "top_producto": top_producto,
    }

    ## PASO 3 Creacion de graficos
    figures: List[Tuple[str, str]] = []

    ## 3.1 Ventas por dia (ultimos 60 dias)
    ### Normalizar los dias
    ### Filtramos ventana y reindexamos para envitar huecos en el eje x

    df_days = df[df["date"].notna()].copy()
    df_days["day"] = df_days["date"].dt.floor("D")
    if not df_days.empty:
        end_day = df_days["day"].max()
        start_day = end_day - pd.Timedelta(days=60)
        window = df_days[(df_days["day"] >= start_day) & (df_days["day"] <= end_day)]
        ventas_dia = window.groupby("day")["total"].sum().sort_index()
        idx = pd.date_range(start=start_day, end=end_day, freq="D")
        ventas_dia = ventas_dia.reindex(idx, fill_value=0.0).astype(float)
    else:
        ventas_dia = pd.Series(dtype=float)

    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ventas_dia.plot(ax=ax1)
    ax1.set_title("Ventas por dia")
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Ingresos")
    ruta1 = _save_fig(fig=fig1, filename="ventas_dia.png")
    figures.append(("Ventas por dia", ruta1))


    # Productos mas vendidos

    top10 = ingresos_por_producto.head(10)
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    top10.plot(kind="bar", ax=ax2)
    ax2.set_title("Productos mas vendidos")
    ax2.set_xlabel("Producto")
    ax2.set_ylabel("Ingresos")
    ruta2 = _save_fig(fig=fig2, filename="top_product.png")
    figures.append(("Productos más vendidos", ruta2))

    return DashboardResult(kpis=kpis, figures=figures)