from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView

from decorators import user_is_doctor
from doctors.models import *
from mixins.custom_mixins import DoctorRequiredMixin

d = {
    0: Sunday,
    1: Monday,
    2: Tuesday,
    3: Wednesday,
    4: Thursday,
    5: Friday,
    6: Saturday,
}


class DoctorDashboardView(DoctorRequiredMixin, TemplateView):
    template_name = "doctors/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
@user_is_doctor
def schedule_timings(request):
    if request.method == 'POST':
        data = request.POST
        for i in range(7):
            if data.get(f'day_{i}', None):
                start_times = data.getlist(f'start_time_{i}', default=[])
                end_times = data.getlist(f'end_time_{i}', default=[])
                for index in range(len(start_times)):
                    start = start_times[index]
                    end = end_times[index]
                    time_range, time_created = TimeRange.objects.get_or_create(start=start, end=end)
                    day, created = d[i].objects.get_or_create(user=request.user)
                    ranges = day.time_range
                    if time_range.id not in list(ranges.values_list('id', flat=True)):
                        day.time_range.add(time_range)

    return render(request, 'doctors/schedule-timings.html')
