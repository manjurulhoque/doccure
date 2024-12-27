import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views.admin_views import (
    AdminDashboardView,
    AdminPatientsView,
    AdminDoctorsView,
    AdminAppointmentsView,
    AdminSpecialitiesView,
    SpecialityCreateView,
    SpecialityUpdateView,
    SpecialityDeleteView,
    AdminPrescriptionsView,
    AdminReviewListView,
    AppointmentReportView,
    RevenueReportView,
)

admin.site.site_header = "Doccure Admin"
admin.site.site_title = "Doccure Admin Portal"
admin.site.index_title = "Welcome to Doccure Admin Portal"


urlpatterns = (
    [
        path("super-admin/", admin.site.urls),
        path("accounts/", include("accounts.urls")),
        path("patients/", include("patients.urls")),
        path("doctors/", include("doctors.urls")),
        path("bookings/", include("bookings.urls")),
        path("", include("core.urls")),
        path("__debug__/", include(debug_toolbar.urls)),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path(
            "admin/",
            include(
                [
                    path(
                        "",
                        AdminDashboardView.as_view(),
                        name="admin-dashboard",
                    ),
                    path(
                        "patients/",
                        AdminPatientsView.as_view(),
                        name="admin-patients",
                    ),
                    path(
                        "doctors/",
                        AdminDoctorsView.as_view(),
                        name="admin-doctors",
                    ),
                    path(
                        "appointments/",
                        AdminAppointmentsView.as_view(),
                        name="admin-appointments",
                    ),
                    path(
                        "specialities/",
                        AdminSpecialitiesView.as_view(),
                        name="admin-specialities",
                    ),
                    path(
                        "specialities/create/",
                        SpecialityCreateView.as_view(),
                        name="admin-speciality-create",
                    ),
                    path(
                        "specialities/<int:pk>/update/",
                        SpecialityUpdateView.as_view(),
                        name="admin-speciality-update",
                    ),
                    path(
                        "specialities/<int:pk>/delete/",
                        SpecialityDeleteView.as_view(),
                        name="admin-speciality-delete",
                    ),
                    path(
                        "prescriptions/",
                        AdminPrescriptionsView.as_view(),
                        name="admin-prescriptions",
                    ),
                    path(
                        "reviews/",
                        AdminReviewListView.as_view(),
                        name="admin-reviews",
                    ),
                    path(
                        "reports/appointments/",
                        AppointmentReportView.as_view(),
                        name="admin-appointment-report",
                    ),
                    path(
                        "reports/revenue/",
                        RevenueReportView.as_view(),
                        name="admin-revenue-report",
                    ),
                ],
            ),
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
