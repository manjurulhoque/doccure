from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView

from accounts.models import User
from mixins.custom_mixins import PatientRequiredMixin
from patients.forms import PatientProfileForm


class PatientDashboardView(PatientRequiredMixin, TemplateView):
    template_name = "patients/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
