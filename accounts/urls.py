from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path("doctor/register/", RegisterDoctorView.as_view(), name="doctor-register"),
    path("patient/register/", RegisterPatientView.as_view(), name="patient-register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
]