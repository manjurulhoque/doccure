from django import forms

from accounts.models import User
from bookings.models import Prescription
from ckeditor.widgets import CKEditorWidget


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["symptoms", "diagnosis", "medications", "notes"]
        widgets = {
            "symptoms": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "diagnosis": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "medications": CKEditorWidget(config_name="default"),
            "notes": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }
