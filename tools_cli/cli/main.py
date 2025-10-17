from decimal import Decimal as D
from typing import Optional


import typer
from rich.console import Console
from rich.table import Table
from .django_setup import setup_django

# 1) Inicializar Django (para importar los modelos)
setup_django()

from products.models import (
    Category, Customer, Order, OrderDetail, Product
)


app = typer.Typer(help="CLI de Typer + Django ORM")
console = Console()

product_app = typer.Typer(help="Opera los productos")
app.add_typer(product_app, name="products")

@product_app.command("list")
def product_list(
    limit: Optional[int] = typer.Option(None ,help="Numero de filas a mostrar"),
    in_stock_only: bool = typer.Option(False, help="Solo con stock"),
    min_price: Optional[float] = typer.Option(None, help="Precio minimo"),
    max_price: Optional[float] = typer.Option(None, help="Precio maximos"),
    category: Optional[str] = typer.Option(None, help="Nombre categoria")
):
    
    qs = Product.objects.all()
    if in_stock_only:
        qs = qs.filter(stock__gt=0)
    if min_price is not None:
        qs = qs.filter(price__gte=min_price)
    if max_price is not None:
        qs = qs.filter(price__lte=max_price)
    if category:
        qs = qs.filter(category__name=category)
    if limit:
        qs = qs[:limit]

    table = Table(title="Productos")
    table.add_column("Id", justify="right")
    table.add_column("Nombre")
    table.add_column("Categoria")
    table.add_column("Precio",overflow="ellipsis",)
    table.add_column("Stock")

    for prod in qs:
        table.add_row(
            str(prod.id),
            prod.name,
            prod.category.name if prod.category else "-",
            str(prod.price),
            str(prod.stock)
        )
    console.print(table)


@product_app.command("apply_updted")
def apply_updted(
    suba: Optional[int] = typer.Option(None ,help="Porcentage a aumentar el valor del producto"),
    baje: Optional[int] = typer.Option(None ,help="Porcentage a disminuir el valor del producto"),
    category: Optional[str] = typer.Option(None, help="Nombre categoria")
):
    qs = Product.objects.all()

    if category:
        qs = qs.filter(category__name=category)
    if suba and suba > 0:
        for prod in qs:
            prod.price *= 1 + D(suba / 100)
            prod.price = D(prod.price).quantize(D('0.01'))
            prod.save()
    if baje and baje > 0 :
        for prod in qs:
            prod.price *= 1 - D(baje / 100)
            prod.price = D(prod.price).quantize(D('0.01'))
            prod.save()  

    table = Table(title="Productos")
    table.add_column("Id", justify="right")
    table.add_column("Nombre")
    table.add_column("Categoria")
    table.add_column("Precio",overflow="ellipsis",)
    table.add_column("Stock")

    for prod in qs:
        table.add_row(
            str(prod.id),
            prod.name,
            prod.category.name if prod.category else "-",
            str(prod.price),
            str(prod.stock)
        )
    console.print(table)