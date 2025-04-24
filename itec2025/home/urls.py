from django.urls import path

from home.views import (
    home_view,
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='index'),
]