from django.shortcuts import render
from django.views.generic.base import TemplateView


class PatientDashboardView(TemplateView):
    template_name = "patients/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
