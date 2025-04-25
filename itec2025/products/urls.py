from django.urls import path

from products.views import (
    ProductList,
    create_product,
    order_list, 
    product_detail,
    product_list, 
)

urlpatterns = [
    path(
        route='product_list/', 
        view=ProductList.as_view(), 
        name='product_list'
    ),
    path(
        route='product_create/', 
        view=create_product, 
        name='product_create'
    ),
    path(
        route='product_detail/<int:product_id>/',
        view=product_detail,
        name='product_detail'
    ),
    path(
        route='order_list/', 
        view=order_list, 
        name='order_list'
    ),
]
