from django.urls import path

from .views import DoctorDashboardView

app_name = "doctors"

urlpatterns = [
    path("dashboard/", DoctorDashboardView.as_view(), name="dashboard"),
]
