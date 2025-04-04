from django.urls import path

from products.views import product_list, order_list

urlpatterns = [
    path(
        route='product_list/', 
        view=product_list, 
        name='product_list'
    ),
    path(
        route='order_list/', 
        view=order_list, 
        name='order_list'
    ),
]
