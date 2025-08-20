from django.urls import path

from api.views import (
    CustomerListCreateView,
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
]