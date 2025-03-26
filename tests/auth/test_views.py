from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APIClient

from tests.base import BaseTestCase
from core import factories


class AccountsTests(BaseTestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))

    def test_login_view(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_successful_login(self):
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(reverse("accounts:login"), login_data)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_failed_login_wrong_password(self):
        login_data = {
            "username": self.user_data["username"],
            "password": "wrongpassword",
        }
        response = self.client.post(reverse("accounts:login"), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "User Does Not Exist")

    def test_failed_login_nonexistent_user(self):
        login_data = {
            "username": "nonexistentuser",
            "password": "somepassword",
        }
        response = self.client.post(reverse("accounts:login"), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "User Does Not Exist")

    def test_doctor_register_view(self):
        response = self.client.get(reverse("accounts:doctor-register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_patient_register_view(self):
        response = self.client.get(reverse("accounts:patient-register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_successful_doctor_register(self):
        user_data = {
            "first_name": "Doctor",
            "last_name": "Test",
            "email": "doctor@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(reverse("accounts:doctor-register"), user_data)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_successful_patient_register(self):
        user_data = {
            "first_name": "Patient",
            "last_name": "Test",
            "username": "patienttest",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(reverse("accounts:patient-register"), user_data)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        # Login first
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        self.assertTrue(self.client.session.get("_auth_user_id"))

        # Test logout
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(self.client.session.get("_auth_user_id"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @override_settings(MEDIA_ROOT="/tmp")
    def test_update_basic_user_information(self):
        client = APIClient()
        # Create and login a user
        client.force_login(self.user)
        
        # Test updating user information
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "dob": "1996-01-01",
            "phone": "1234567890"
        }
        
        # Test without avatar
        response = client.put(
            reverse("accounts:update-basic-information"),
            data=data,
            format='json'  # Changed to use JSON format
        )
        self.assertEqual(response.status_code, 200)
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")
        self.assertEqual(self.user.profile.phone, "1234567890")
        self.assertEqual(str(self.user.profile.dob), "1996-01-01")
        
        # Test with avatar
        avatar_content = b"fake image content"
        avatar = SimpleUploadedFile(
            "test.jpg",
            avatar_content,
            content_type="image/jpeg"
        )
        data["avatar"] = avatar
        
        response = client.put(
            reverse("accounts:update-basic-information"),
            data=data,
            format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        
        # Test error case
        client.logout()
        response = client.put(
            reverse("accounts:update-basic-information"),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, 302)  # Login required
