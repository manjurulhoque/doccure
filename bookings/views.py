from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest, Http404

from accounts.models import User

from mixins.custom_mixins import PatientRequiredMixin


class BookingTemplateView(PatientRequiredMixin, TemplateView):
    template_name = "bookings/booking.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            doctor = User.objects.get(username=kwargs['username'])
        except User.DoesNotExist:
            raise Http404
        return render(request, self.template_name, {"doctor": doctor})
