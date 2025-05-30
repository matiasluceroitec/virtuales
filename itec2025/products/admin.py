from decimal import Decimal as D

from django.contrib import admin

from products.models import (
    Category,
    Customer, 
    Order, 
    Product,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'image', 'category')
    list_filter = ('name', 'category')
    search_fields = ('name', 'stock')

    actions = ['update_price_15']

    def update_price_15(self, request, queryset):
        for product in queryset:
            product.price = product.price * D(1.15)
            product.save()
        self.message_user(
            request,
            "Se proceso correctamente aumento de precios",
            level='success'
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date')
