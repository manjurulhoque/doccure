from django import forms

from accounts.models import User
from core.models import Review


class PatientProfileForm(forms.ModelForm):
    """
    Patent profile update form
    """

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    avatar = forms.ImageField(required=False)
    dob = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    blood_group = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select Blood Group"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ],
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select Gender"),
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    )
    phone = forms.CharField(required=False)
    medical_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "List any chronic conditions, surgeries, etc.",
            }
        ),
    )
    allergies = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "List any allergies to medications, food, etc.",
            }
        ),
    )
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            # Add phone number validation if needed
            if not phone.isdigit():
                raise forms.ValidationError(
                    "Phone number should contain only digits"
                )
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")
        if postal_code:
            # Add postal code validation if needed
            if not postal_code.isdigit():
                raise forms.ValidationError(
                    "Postal code should contain only digits"
                )
        return postal_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Current Password"}
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm New Password",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("The new passwords don't match")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-control"}),
            "review": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your review here...",
                }
            ),
        }
