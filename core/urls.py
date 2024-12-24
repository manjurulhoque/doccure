from django.urls import path
from .views import home, TermsView, PrivacyView

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
]
