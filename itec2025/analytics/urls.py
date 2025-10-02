from django.urls import path

from analytics.views import DashboardView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="analytics-dashboard")
]
