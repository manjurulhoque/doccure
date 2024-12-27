from django.urls import path

from .views import (
    PatientDashboardView,
    PatientProfileUpdateView,
    AppointmentDetailView,
    AppointmentCancelView,
    AppointmentPrintView,
    ChangePasswordView,
    AddReviewView,
)

app_name = "patients"

urlpatterns = [
    path("dashboard/", PatientDashboardView.as_view(), name="dashboard"),
    path(
        "profile-settings/",
        PatientProfileUpdateView.as_view(),
        name="profile-setting",
    ),
    path(
        "appointments/<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "appointments/<int:pk>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment-cancel",
    ),
    path(
        "appointments/<int:pk>/print/",
        AppointmentPrintView.as_view(),
        name="appointment-print",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "appointment/<int:booking_id>/review/",
        AddReviewView.as_view(),
        name="add-review",
    ),
]
