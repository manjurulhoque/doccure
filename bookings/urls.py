from django.urls import path

from .views import (
    BookingView,
    BookingCreateView,
    BookingSuccessView,
    BookingInvoiceView,
    BookingListView,
)

app_name = "bookings"

urlpatterns = [
    path(
        "doctor/<slug:username>",
        BookingView.as_view(),
        name="doctor-booking-view",
    ),
    path(
        "create/<str:username>/",
        BookingCreateView.as_view(),
        name="create-booking",
    ),
    path(
        "<int:booking_id>/success/",
        BookingSuccessView.as_view(),
        name="booking-success",
    ),
    path(
        "<int:booking_id>/invoice/",
        BookingInvoiceView.as_view(),
        name="booking-invoice",
    ),
    path(
        "list/",
        BookingListView.as_view(),
        name="booking-list",
    ),
]
