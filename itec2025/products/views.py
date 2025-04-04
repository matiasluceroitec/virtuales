from django.shortcuts import render

from products.services.products import ProductService

def product_list(request):
    all_products = ProductService.get_all()

    return render(
        request, 
        'products/list.html',
        {
            'products': all_products,
            'otro_atributo': 'Atributo 2'
        }
    )

def order_list(request):
    return render(request, 'orders/list.html')
