from django.shortcuts import render
from django.views.generic.base import TemplateView

from mixins.custom_mixins import DoctorRequiredMixin


class DoctorDashboardView(DoctorRequiredMixin, TemplateView):
    template_name = "doctors/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def schedule_timings(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'doctors/schedule-timings.html')
