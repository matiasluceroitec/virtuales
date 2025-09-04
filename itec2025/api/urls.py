from django.urls import path

from api.views import (
    CategoryDetailAPIView,
    CategoryListCreateAPIView,
    CustomerListCreateView,
    ProductListCreateApiView,
    UserListCreateView, 
    UserRetrieveUpdateDestroyView, 
)

urlpatterns = [
    #User
    path(
        "users/", UserListCreateView.as_view(), name="users-list"
    ),
    path(
        "users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="users-detail"
    ),
    # Customer
    path(
        "customer/", CustomerListCreateView.as_view(), name="customer-list"
    ),
    # Category
    path(
        "categories/", CategoryListCreateAPIView.as_view(), name="categories-list"
    ),
    path(
        "categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"
    ),
    path(
        "products/", ProductListCreateApiView.as_view(), name="products-list"
    ),
]