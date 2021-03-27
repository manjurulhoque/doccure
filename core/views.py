from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from accounts.models import User


def home(request: HttpRequest) -> HttpResponse:
    doctors = User.objects.select_related('profile').filter(role="doctor")
    return render(request, 'home.html', {"doctors": doctors})
