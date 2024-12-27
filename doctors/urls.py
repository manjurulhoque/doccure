from django.urls import path

from .views import (
    DoctorDashboardView,
    schedule_timings,
    DoctorProfileUpdateView,
    DoctorProfileView,
    UpdateEducationAPIView,
    UpdateExperienceAPIView,
    UpdateRegistrationNumberAPIView,
    UpdateSpecializationAPIView,
    DoctorsListView,
    AppointmentListView,
    AppointmentDetailView,
    AppointmentActionView,
    MyPatientsView,
    AppointmentHistoryView,
    DoctorChangePasswordView,
    PrescriptionCreateView,
    PrescriptionDetailView,
)

app_name = "doctors"

urlpatterns = [
    path("", DoctorsListView.as_view(), name="list"),
    path("dashboard/", DoctorDashboardView.as_view(), name="dashboard"),
    path("schedule-timings/", schedule_timings, name="schedule-timings"),
    path(
        "profile-settings/",
        DoctorProfileUpdateView.as_view(),
        name="profile-setting",
    ),
    path(
        "<str:username>/profile/",
        DoctorProfileView.as_view(),
        name="doctor-profile",
    ),
    path(
        "update-education",
        UpdateEducationAPIView.as_view(),
        name="update-education",
    ),
    path(
        "update-experience",
        UpdateExperienceAPIView.as_view(),
        name="update-experience",
    ),
    path(
        "update-registration-number",
        UpdateRegistrationNumberAPIView.as_view(),
        name="update-registration-number",
    ),
    path(
        "update-specialization",
        UpdateSpecializationAPIView.as_view(),
        name="update-specialization",
    ),
    path(
        "appointments/",
        AppointmentListView.as_view(),
        name="appointments",
    ),
    path(
        "appointments/<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "appointments/<int:pk>/<str:action>/",
        AppointmentActionView.as_view(),
        name="appointment-action",
    ),
    path("my-patients/", MyPatientsView.as_view(), name="my-patients"),
    path(
        "my-patients/<int:patient_id>/history/",
        AppointmentHistoryView.as_view(),
        name="appointment-history",
    ),
    path(
        "change-password/",
        DoctorChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "appointment/<int:booking_id>/prescription/add/",
        PrescriptionCreateView.as_view(),
        name="add-prescription",
    ),
    path(
        "prescription/<int:pk>/",
        PrescriptionDetailView.as_view(),
        name="prescription-detail",
    ),
]
