from django.views.generic import TemplateView
from django.db.models import Count, Sum, Avg
from accounts.decorators import AdminRequiredMixin
from django.views.generic import ListView
from datetime import date
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from decimal import Decimal

from core.models import Review, Speciality
from accounts.models import User
from bookings.models import Booking, Prescription


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
        doctors = User.objects.filter(role="doctor").select_related("profile")[:5]
        for doctor in doctors:
            doctor.earned = (
                Booking.objects.filter(doctor=doctor, status="completed").aggregate(
                    total=Sum("doctor__profile__price_per_consultation")
                )["total"]
                or 0
            )
            doctor.reviews_count = 0  # Add review logic when implemented
        context["recent_doctors"] = doctors

        # Get recent patients with their appointments
        patients = User.objects.filter(role="patient").select_related("profile")[:5]
        for patient in patients:
            latest_appointment = (
                Booking.objects.filter(patient=patient)
                .order_by("-appointment_date")
                .first()
            )
            patient.last_visit = (
                latest_appointment.appointment_date if latest_appointment else None
            )
            patient.total_paid = (
                Booking.objects.filter(patient=patient, status="completed").aggregate(
                    total=Sum("doctor__profile__price_per_consultation")
                )["total"]
                or 0
            )
        context["recent_patients"] = patients

        # Get recent appointments
        context["recent_appointments"] = Booking.objects.select_related(
            "doctor", "doctor__profile", "patient", "patient__profile"
        ).order_by("-appointment_date")[:5]

        # Add recent prescriptions
        context["recent_prescriptions"] = Prescription.objects.select_related(
            "doctor", "patient", "booking"
        ).order_by("-created_at")[:10]

        return context


class AdminPatientsView(AdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/patients.html"
    context_object_name = "patients"
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.filter(role="patient").select_related("profile")

        # Add computed fields for each patient
        for patient in queryset:
            # Get last visit date
            latest_appointment = (
                Booking.objects.filter(patient=patient)
                .order_by("-appointment_date")
                .first()
            )
            patient.last_visit = (
                latest_appointment.appointment_date if latest_appointment else None
            )

            # Calculate total amount paid
            patient.total_paid = (
                Booking.objects.filter(patient=patient, status="completed").aggregate(
                    total=Sum("doctor__profile__price_per_consultation")
                )["total"]
                or 0
            )

            # Calculate age from DOB if available
            if patient.profile.dob:
                today = date.today()
                patient.profile.age = (
                    today.year
                    - patient.profile.dob.year
                    - (
                        (today.month, today.day)
                        < (patient.profile.dob.month, patient.profile.dob.day)
                    )
                )
            else:
                patient.profile.age = None

            # Get appointment stats
            patient.total_appointments = Booking.objects.filter(patient=patient).count()
            patient.completed_appointments = Booking.objects.filter(
                patient=patient, status="completed"
            ).count()

        return queryset


class AdminDoctorsView(AdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/doctors.html"
    context_object_name = "doctors"
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(role="doctor")


class AdminAppointmentsView(AdminRequiredMixin, ListView):
    model = Booking
    template_name = "dashboard/appointments.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.select_related(
            "doctor", "doctor__profile", "patient", "patient__profile"
        ).order_by("-appointment_date", "-appointment_time")


class AdminSpecialitiesView(AdminRequiredMixin, ListView):
    model = Speciality
    template_name = "dashboard/specialities.html"
    context_object_name = "specialities"
    paginate_by = 10

    def get_queryset(self):
        return Speciality.objects.all().order_by("name")


class SpecialityCreateView(AdminRequiredMixin, CreateView):
    model = Speciality
    fields = ["name", "description", "image"]
    template_name = "dashboard/specialities.html"
    success_url = reverse_lazy("admin-specialities")

    def form_valid(self, form):
        messages.success(self.request, "Speciality created successfully.")
        return super().form_valid(form)


class SpecialityUpdateView(AdminRequiredMixin, UpdateView):
    model = Speciality
    fields = ["name", "description", "image", "is_active"]
    template_name = "dashboard/specialities.html"
    success_url = reverse_lazy("admin-specialities")

    def form_valid(self, form):
        messages.success(self.request, "Speciality updated successfully.")
        return super().form_valid(form)


class SpecialityDeleteView(AdminRequiredMixin, DeleteView):
    model = Speciality
    success_url = reverse_lazy("admin-specialities")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Speciality deleted successfully.")
        return super().delete(request, *args, **kwargs)


class AdminPrescriptionsView(AdminRequiredMixin, ListView):
    model = Prescription
    template_name = "dashboard/prescriptions.html"
    context_object_name = "prescriptions"
    paginate_by = 10

    def get_queryset(self):
        return Prescription.objects.select_related(
            "doctor",
            "doctor__profile",
            "patient",
            "patient__profile",
            "booking",
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add summary stats
        context["total_prescriptions"] = self.model.objects.count()
        context["prescriptions_today"] = self.model.objects.filter(
            created_at__date=date.today()
        ).count()
        return context


class AdminReviewListView(AdminRequiredMixin, ListView):
    model = Review
    template_name = "dashboard/reviews.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.select_related(
            "doctor",
            "doctor__profile",
            "patient",
            "patient__profile",
            "booking",
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_reviews"] = self.model.objects.count()
        context["average_rating"] = (
            self.model.objects.aggregate(Avg("rating"))["rating__avg"] or 0
        )
        return context


class AppointmentReportView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/reports/appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get date range from query params or default to last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        # Get appointments data
        appointments = Booking.objects.filter(
            appointment_date__range=[start_date, end_date]
        ).select_related("doctor", "patient")

        # Monthly trend
        monthly_stats = list(
            appointments.annotate(month=TruncMonth("appointment_date"))
            .values("month")
            .annotate(
                total=Count("id"),
                completed=Count("id", filter=Q(status="completed")),
                cancelled=Count("id", filter=Q(status="cancelled")),
            )
            .order_by("month")
        )

        # Format dates for JSON
        for stat in monthly_stats:
            stat["month"] = stat["month"].strftime("%Y-%m-%d")

        # Status distribution
        status_stats = list(appointments.values("status").annotate(count=Count("id")))

        # Doctor performance
        doctor_stats = list(
            appointments.values("doctor__first_name", "doctor__last_name").annotate(
                total=Count("id"),
                completed=Count("id", filter=Q(status="completed")),
                cancelled=Count("id", filter=Q(status="cancelled")),
            )
        )

        context.update(
            {
                "monthly_stats": json.dumps(monthly_stats),
                "status_stats": json.dumps(status_stats),
                "doctor_stats": doctor_stats,
                "total_appointments": appointments.count(),
                "completed_appointments": appointments.filter(
                    status="completed"
                ).count(),
                "cancelled_appointments": appointments.filter(
                    status="cancelled"
                ).count(),
            }
        )
        return context


class RevenueReportView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/reports/revenue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add date filtering
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        completed_bookings = Booking.objects.filter(status="completed").select_related(
            "doctor__profile"
        )

        # Monthly revenue
        monthly_revenue = list(
            completed_bookings.annotate(month=TruncMonth("appointment_date"))
            .values("month")
            .annotate(revenue=Sum("doctor__profile__price_per_consultation"))
            .order_by("month")
        )

        # Format dates and convert Decimal to float for JSON
        for stat in monthly_revenue:
            stat["month"] = stat["month"].strftime("%Y-%m-%d")
            stat["revenue"] = float(stat["revenue"]) if stat["revenue"] else 0

        # Doctor revenue
        doctor_revenue = list(
            completed_bookings.values("doctor__first_name", "doctor__last_name")
            .annotate(
                revenue=Sum("doctor__profile__price_per_consultation"),
                appointments=Count("id"),
            )
            .order_by("-revenue")
        )

        # Convert Decimal to float for JSON
        for stat in doctor_revenue:
            stat["revenue"] = float(stat["revenue"]) if stat["revenue"] else 0

        # Add summary statistics
        context.update(
            {
                "total_appointments": completed_bookings.count(),
                "average_revenue_per_appointment": (
                    completed_bookings.aggregate(
                        avg=Avg("doctor__profile__price_per_consultation")
                    )["avg"]
                    or 0
                ),
                "highest_revenue_day": completed_bookings.annotate(
                    day=TruncDay("appointment_date")
                )
                .values("day")
                .annotate(total=Sum("doctor__profile__price_per_consultation"))
                .order_by("-total")
                .first(),
                "monthly_revenue_stats": json.dumps(monthly_revenue),
                "monthly_revenue": monthly_revenue,
                "doctor_revenue": doctor_revenue,
                "total_revenue": completed_bookings.aggregate(
                    total=Sum("doctor__profile__price_per_consultation")
                )["total"]
                or 0,
            }
        )

        # Add revenue by specialization
        # specialization_revenue = completed_bookings.values(
        #     "doctor__profile__specialization__name"
        # ).annotate(
        #     revenue=Sum("doctor__profile__price_per_consultation"),
        #     appointments=Count("id")
        # ).order_by("-revenue")

        context["specialization_revenue"] = 0  # specialization_revenue

        return context
