from django.http import HttpResponsePermanentRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from accounts.models import User
from mixins.custom_mixins import DoctorRequiredMixin


class DoctorDashboardView(DoctorRequiredMixin, TemplateView):
    template_name = "doctors/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
