from django import forms

from accounts.models import User


class PatientProfileForm(forms.ModelForm):
    """
    Patent profile update form
    """

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar"]
