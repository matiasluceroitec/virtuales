from django.urls import path

from home.views import (
    login_view,
    register_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login')
]