from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, View
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse

from accounts.models import User
from bookings.models import Booking
from mixins.custom_mixins import PatientRequiredMixin
from patients.forms import PatientProfileForm


class PatientDashboardView(PatientRequiredMixin, TemplateView):
    template_name = "patients/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointments"] = (
            Booking.objects.select_related('doctor', 'doctor__profile')
            .filter(patient=self.request.user)
            .order_by('-appointment_date', '-appointment_time')
        )
        return context


class PatientProfileUpdateView(PatientRequiredMixin, UpdateView):
    model = User
    form_class = PatientProfileForm
    template_name = "patients/profile-setting.html"
    success_url = reverse_lazy("patients:profile-setting")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        if form.cleaned_data.get("avatar"):
            user.profile.avatar = form.cleaned_data["avatar"]
            user.profile.save()

        return HttpResponsePermanentRedirect(self.get_success_url())


class AppointmentDetailView(DetailView):
    model = Booking
    template_name = 'patients/appointment-detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Booking.objects.select_related(
            'doctor', 
            'doctor__profile',
            'patient', 
            'patient__profile'
        ).filter(patient=self.request.user)


class AppointmentCancelView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(
            Booking, 
            pk=pk, 
            patient=request.user,
            status__in=['pending', 'confirmed']
        )
        
        appointment.status = 'cancelled'
        appointment.save()
        
        messages.success(request, 'Appointment cancelled successfully')
        return redirect('patients:dashboard')


class AppointmentPrintView(DetailView):
    model = Booking
    template_name = 'patients/appointment-print.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Booking.objects.select_related(
            'doctor', 
            'doctor__profile',
            'patient', 
            'patient__profile'
        ).filter(patient=self.request.user)

    def render_to_response(self, context):
        html_string = render_to_string(self.template_name, context, request=self.request)
        return HttpResponse(html_string)
