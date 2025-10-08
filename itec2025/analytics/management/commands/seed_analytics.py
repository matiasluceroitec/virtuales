from typing import List
from datetime import datetime, timedelta
import random

import numpy as np
from django.core.management.base import BaseCommand
from django.utils import timezone

from products.models import Customer, Product, Category, Order, OrderDetail


class Command(BaseCommand):
    help = "Genera datos de ejemplo para el dashboard de analytics"

    def add_arguments(self, parser):
        parser.add_argument("--orders", type=int, default=100, help="Cantidad de órdenes a crear")
        parser.add_argument("--days", type=int, default=30, help="Rango de días hacia atrás para fechas")
        parser.add_argument("--seed", type=int, default=42, help="Semilla RNG para reproducibilidad")

    def handle(self, *args, **options):
        rng_seed = int(options["seed"])  # reproducible
        np.random.seed(rng_seed)
        random.seed(rng_seed)

        orders_count = int(options["orders"])
        days_back = int(options["days"])

        self.stdout.write(self.style.NOTICE("Sembrando datos de analytics..."))

        # 1) Categorías
        categories = [
            ("Electrónica",),
            ("Hogar",),
            ("Deportes",),
            ("Libros",),
            ("Moda",),
        ]
        cat_objs = []
        for (name,) in categories:
            obj, _ = Category.objects.get_or_create(name=name)
            cat_objs.append(obj)

        # 2) Productos
        product_names = [
            "Auriculares", "Mouse", "Teclado", "Zapatillas", "Pantalón",
            "Silla", "Lampara", "Pelota", "Camiseta", "Libro Python",
            "Monitor", "Parlante", "Mochila", "Bicicleta", "Mate",
        ]
        prod_objs: List[Product] = []
        for name in product_names:
            cat = random.choice(cat_objs)
            price = round(float(np.random.uniform(5, 500)), 2)
            prod, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    "price": price,
                    "stock": int(np.random.randint(10, 200)),
                    "category": cat,
                },
            )
            # Si ya existía, actualizamos precio/stock al vuelo para variar
            if prod.price != price:
                prod.price = price
                prod.stock = int(np.random.randint(10, 200))
                prod.category = cat
                prod.save()
            prod_objs.append(prod)

        # 3) Customers
        cust_objs: List[Customer] = []
        for i in range(30):
            email = f"alumno{i+1}@itec.local"
            cust, _ = Customer.objects.get_or_create(
                email=email,
                defaults={"name": f"Alumno {i+1}", "phone": str(1000 + i)},
            )
            cust_objs.append(cust)

        # 4) Órdenes
        now = timezone.now()
        order_objs: List[Order] = []
        for _ in range(orders_count):
            cust = random.choice(cust_objs)
            # Fecha aleatoria dentro del rango
            delta_days = int(np.random.randint(0, max(days_back, 1)))
            order_date = now - timedelta(days=5)
            order = Order.objects.create(customer=cust, date=order_date)
            order_objs.append(order)

            # 5) Detalles (1-5 productos por orden)
            n_items = int(np.random.randint(1, 6))
            chosen_products = random.sample(prod_objs, k=min(n_items, len(prod_objs)))
            for p in chosen_products:
                qty = int(np.random.randint(1, 5))
                OrderDetail.objects.create(order=order, product=p, quantity=qty)

        self.stdout.write(self.style.SUCCESS(
            f"Listo. Órdenes creadas: {len(order_objs)} | Productos: {len(prod_objs)} | Clientes: {len(cust_objs)}"
        ))