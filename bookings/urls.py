from django.urls import path

from .views import BookingView, BookingCreateView

app_name = "bookings"

urlpatterns = [
    path(
        "doctor/<slug:username>",
        BookingView.as_view(),
        name="doctor-booking-view",
    ),
    path('create/<str:username>/', BookingCreateView.as_view(), name='create-booking'),
]
