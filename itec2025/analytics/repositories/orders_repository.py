"""
Aisla el acceso a la base de datos, y devuelve una estructura lista para pandas.
No contiene logica de negocio
"""

import pandas as pd

from products.models import Order, OrderDetail, Product, Category


def fetch_orders_dataframe() -> pd.DataFrame:
    """
    Carga ordenes con sus detalles a un Dataframe

    Returns:
        DataFrame con columnas: order_id, date, product, category,
        price, quantity, total
    """

    qs = (
        OrderDetail.objects
        .select_related('order', 'product', 'product__category')
        .values(
            "order_id",
            "order__date",
            "product__name",
            "product__price",
            "product__category__name",
            "quantity"
        )
    )

    rows = list(qs)

    if not rows:
        return pd.DataFrame(
            columns=[
                "order_id",
                "date",
                "product",
                "category",
                "price",
                "quantity",
                "total"
            ]
        )
    # GENERA EL DATAFRAME A PARTIR DE UNA LISTA DE OBJETOS
    df = pd.DataFrame(rows)

    #RENOMBRAR COLUMNAS
    df = df.rename(
        columns={
            "order__date": "date",
            "product__name": "product",
            "product__price": "price",
            "product__category__name": "category",
        }
    )

    df["total"] = df["price"] * df["quantity"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df
