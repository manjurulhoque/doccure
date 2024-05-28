from django.urls import path

from .views import BookingTemplateView

app_name = "bookings"

urlpatterns = [
    path(
        "doctor/<slug:username>",
        BookingTemplateView.as_view(),
        name="doctor-booking-view",
    ),
]
