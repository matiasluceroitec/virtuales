from typing import Any, Dict

from django.views.generic import TemplateView

from analytics.repositories.orders_repository import fetch_orders_dataframe
from analytics.services.dashboard_service import build_bashboard

class DashboardView(TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        df = fetch_orders_dataframe()
        result = build_bashboard(df)
        ctx["kpis"] = result.kpis
        ctx["figures"] = result.figures
        return ctx