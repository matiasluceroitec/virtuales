from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from products.models import Product
from products.services.products import ProductService

def product_list(request):
    all_products = ProductService.get_all()
    total_price = ProductService.sum_total_price(all_products)

    return render(
        request, 
        'products/list.html',
        dict(
            products=all_products,
            otro_atributo='Atributo 2',
            total_price = total_price
        )
    )

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        'products/detail.html',
        dict(
            product=product,
        )
    )

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        Product.objects.create(
            name=name,
            stock=int(stock),
            price=float(price)
        )
        messages.success(request, 'Producto Creado')
    return render(
        request,
        'products/create.html'
    )


def order_list(request):
    return render(request, 'orders/list.html')

