from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import User


def home(request: HttpRequest) -> HttpResponse:
    doctors = (
        User.objects.select_related("profile")
        .filter(role="doctor")
        .filter(is_superuser=False)
    )
    return render(request, "home.html", {"doctors": doctors})


class TermsView(TemplateView):
    template_name = "core/terms.html"


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"
