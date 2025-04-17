from django.urls import path
from home.views import register_view

urlpatterns = [
    path('register/', register_view, name='register')
]