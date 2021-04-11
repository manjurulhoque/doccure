from django import forms

from accounts.models import User


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
