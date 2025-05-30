import csv

from django.contrib import admin

from home.models import FileUpload
from products.models import Category, Product
# Register your models here.



@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    actions = ['load_data_from_file']

    def load_data_from_file(self, request, queryset):
        for file_obj in queryset:
            if not file_obj.file.name.endswith('.csv'):
                self.message_user(
                    request,
                    f"Solo soporta archivos csv, el archivo {file_obj.file.name} esta en otro formato",
                    level='error'
                )
                continue
                
            with open(file_obj.file.path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    category, _ = Category.objects.get_or_create(
                        name=row['category']
                    )
                    Product.objects.create(
                        name=row['name'],
                        price=row['price'],
                        stock=row['stock'],
                        category=category
                    )
        self.message_user(
            request,
            f"Se proceso correctamente el archivo y se crearon los productos",
            level='success'
        )
    load_data_from_file.short_description = "Cargar Productos"