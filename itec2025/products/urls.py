from django.urls import path

from products.views import (
    OrderCreate,
    OrderDetailCreate,
    OrderList, 
    ProductCreate,
    ProductCreateView,
    ProductDelete,
    ProductDetail,
    ProductList,
)

urlpatterns = [
    path(
        route='product_list/', 
        view=ProductList.as_view(), 
        name='product_list'
    ),
    path(
        route='product_create/', 
        view=ProductCreateView.as_view(), 
        name='product_create'
    ),
    path(
        route='product_detail/<int:product_id>/',
        view=ProductDetail.as_view(),
        name='product_detail'
    ),
     path(
        route='product_delete/<int:product_id>/',
        view=ProductDelete.as_view(),
        name='product_delete'
    ),
    path(
        route='order_list/', 
        view=OrderList.as_view(), 
        name='order_list'
    ),
    path(
        route='order_create/', 
        view=OrderCreate.as_view(), 
        name='order_create'
    ),
    path(
        route='order/<int:order_id>/detail/', 
        view=OrderDetailCreate.as_view(), 
        name='order_detail'
    ),
]
