from django.urls import path

from .views import DoctorDashboardView, schedule_timings

app_name = "doctors"

urlpatterns = [
    path("dashboard/", DoctorDashboardView.as_view(), name="dashboard"),
    path("schedule-timings/", schedule_timings, name="schedule-timings"),
]
