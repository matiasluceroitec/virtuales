import pandas as pd

from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):

    help = "Carga productos a partir de un archivo CSV o XLSX"

    def add_arguments(self, parser):
        parser.add_argument(
            'archivo', 
            type=str,
            help='Ruta hacia el archivo'
        )

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        if archivo.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.endswith('.xlsx'):
            df = pd.read_excel(archivo)
        else:
            self.stdout.write(
                self.style.ERROR(
                    "Formato no compatible"
                )
            )

        for no_lo_usamos, row in df.iterrows():
            category, _ = Category.objects.get_or_create(
                name=row['category']
            )
            Product.objects.create(
                name=row['name'],
                price=row['price'],
                stock=row['stock'],
                category=category
            )
        
        self.stdout.write(self.style.SUCCESS("Productos cargados correctamente"))