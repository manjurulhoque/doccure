from django.urls import path

from .views import (
    DoctorDashboardView,
    schedule_timings,
    DoctorProfileUpdateView
)

app_name = "doctors"

urlpatterns = [
    path("dashboard/", DoctorDashboardView.as_view(), name="dashboard"),
    path("schedule-timings/", schedule_timings, name="schedule-timings"),
    path("profile-settings/", DoctorProfileUpdateView.as_view(), name="profile-setting"),
]
