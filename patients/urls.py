from django.urls import path

from .views import PatientDashboardView, PatientProfileUpdateView

app_name = "patients"

urlpatterns = [
    path("dashboard/", PatientDashboardView.as_view(), name="dashboard"),
    path("profile-setting/", PatientProfileUpdateView.as_view(), name="profile-setting"),
]
