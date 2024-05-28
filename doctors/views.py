from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from decorators import user_is_doctor
from doctors.forms import DoctorProfileForm
from doctors.models import Education
from doctors.models.general import *
from doctors.serializers import EducationSerializer
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


def convert_to_24_hour_format(time_str):
    if time_str == '00:00 AM':
        time_str = '12:00 AM'
    return datetime.strptime(time_str, "%I:%M %p").time()


@login_required
@user_is_doctor
def schedule_timings(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST
        for i in range(7):
            if data.get(f"day_{i}", None):
                start_times = data.getlist(f"start_time_{i}", default=[])
                end_times = data.getlist(f"end_time_{i}", default=[])
                for index in range(len(start_times)):
                    start = convert_to_24_hour_format(start_times[index])
                    end = convert_to_24_hour_format(end_times[index])
                    time_range, time_created = TimeRange.objects.get_or_create(
                        start=start, end=end
                    )
                    day, created = d[i].objects.get_or_create(
                        user=request.user
                    )
                    ranges = day.time_range
                    if time_range.id not in list(
                            ranges.values_list("id", flat=True)
                    ):
                        day.time_range.add(time_range)

        return HttpResponsePermanentRedirect(reverse_lazy("doctors:schedule-timings"))

    return render(request, "doctors/schedule-timings.html")


class DoctorProfileUpdateView(DoctorRequiredMixin, generic.UpdateView):
    model = User
    template_name = "doctors/profile-settings.html"
    form_class = DoctorProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class DoctorProfileView(generic.DetailView):
    context_object_name = "doctor"
    model = User
    slug_url_kwarg = "username"
    slug_field = "username"
    template_name = "doctors/profile.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)

        slug_field = self.get_slug_field()

        try:
            obj = queryset.select_related("profile").get(**{slug_field: slug})
        except User.DoesNotExist:
            raise Http404

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = datetime.now().strftime("%-d %b %Y")
        return context


class UpdateEducationAPIView(DoctorRequiredMixin, UpdateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        # instance = self.get_object()
        data = request.POST
        degrees = data.getlist('degree', default=[])
        colleges = data.getlist('college', default=[])
        years = data.getlist('year_of_completion', default=[])
        for i in range(len(degrees)):
            degree = degrees[i]
            college = colleges[i]
            year_of_completion = years[i]
            serializer = self.get_serializer(data={
                'degree': degree,
                'college': college,
                'year_of_completion': year_of_completion,
            })
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response([])
