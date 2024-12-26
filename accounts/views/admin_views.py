from django.views.generic import TemplateView
from django.db.models import Count, Sum
from accounts.decorators import AdminRequiredMixin
from django.views.generic import ListView

from accounts.models import User
from bookings.models import Booking


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Count statistics
        context["doctors_count"] = User.objects.filter(role="doctor").count()
        context["patients_count"] = User.objects.filter(role="patient").count()
        context["appointments_count"] = Booking.objects.count()

        # Calculate total revenue
        context["total_revenue"] = (
            Booking.objects.filter(status="completed").aggregate(
                total=Sum("doctor__profile__price_per_consultation")
            )["total"]
            or 0
        )

        # Get recent doctors with their stats
        doctors = User.objects.filter(role="doctor").select_related("profile")[
            :5
        ]
        for doctor in doctors:
            doctor.earned = (
                Booking.objects.filter(
                    doctor=doctor, status="completed"
                ).aggregate(
                    total=Sum("doctor__profile__price_per_consultation")
                )[
                    "total"
                ]
                or 0
            )
            doctor.reviews_count = 0  # Add review logic when implemented
        context["recent_doctors"] = doctors

        # Get recent patients with their appointments
        patients = User.objects.filter(role="patient").select_related(
            "profile"
        )[:5]
        for patient in patients:
            latest_appointment = (
                Booking.objects.filter(patient=patient)
                .order_by("-appointment_date")
                .first()
            )
            patient.last_visit = (
                latest_appointment.appointment_date
                if latest_appointment
                else None
            )
            patient.total_paid = (
                Booking.objects.filter(
                    patient=patient, status="completed"
                ).aggregate(
                    total=Sum("doctor__profile__price_per_consultation")
                )[
                    "total"
                ]
                or 0
            )
        context["recent_patients"] = patients

        # Get recent appointments
        context["recent_appointments"] = Booking.objects.select_related(
            "doctor", "doctor__profile", "patient", "patient__profile"
        ).order_by("-appointment_date")[:5]

        return context


class AdminPatientsView(AdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/patients.html"
    context_object_name = "patients"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Patients"
        return context


class AdminDoctorsView(AdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/doctors.html"
    context_object_name = "doctors"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Doctors"
        return context
