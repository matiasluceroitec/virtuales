from django.urls import path

from home.views import (
    HomeView,
    LoginView,
    LogoutView,
    RegisterView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='index'),
]