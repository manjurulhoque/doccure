from django.views.generic import TemplateView
from django.db.models import Count, Sum
from accounts.decorators import AdminRequiredMixin
from django.views.generic import ListView
from datetime import date
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.models import Speciality

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
        context['recent_prescriptions'] = Prescription.objects.select_related(
            'doctor', 'patient', 'booking'
        ).order_by('-created_at')[:10]

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
        return Speciality.objects.all().order_by('name')


class SpecialityCreateView(AdminRequiredMixin, CreateView):
    model = Speciality
    fields = ['name', 'description', 'image']
    template_name = "dashboard/specialities.html"
    success_url = reverse_lazy('admin-specialities')

    def form_valid(self, form):
        messages.success(self.request, 'Speciality created successfully.')
        return super().form_valid(form)


class SpecialityUpdateView(AdminRequiredMixin, UpdateView):
    model = Speciality
    fields = ['name', 'description', 'image', 'is_active']
    template_name = "dashboard/specialities.html"
    success_url = reverse_lazy('admin-specialities')

    def form_valid(self, form):
        messages.success(self.request, 'Speciality updated successfully.')
        return super().form_valid(form)


class SpecialityDeleteView(AdminRequiredMixin, DeleteView):
    model = Speciality
    success_url = reverse_lazy('admin-specialities')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Speciality deleted successfully.')
        return super().delete(request, *args, **kwargs)
