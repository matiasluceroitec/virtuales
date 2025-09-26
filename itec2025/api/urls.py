from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)
from api.views import (
    CategoryDetailAPIView,
    CategoryListCreateAPIView,
    CategoryViewSet,
    CustomerListCreateView,
    CustomerViewSet,
    ProductListCreateApiView,
    UserListCreateView, 
    UserRetrieveUpdateDestroyView, 
)

router = DefaultRouter()
router.register('customers-vs', CustomerViewSet, basename='customers-vs')
router.register('category-vs', CategoryViewSet, basename='category-vs')

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
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    ## REGRISTRO DE ROUTERS
    path("", include(router.urls))
]