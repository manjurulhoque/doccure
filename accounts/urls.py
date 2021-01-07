from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path("doctor/register/", RegisterEmployeeView.as_view(), name="doctor-register"),
    path("patient/register/", RegisterEmployerView.as_view(), name="patient-register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
]
