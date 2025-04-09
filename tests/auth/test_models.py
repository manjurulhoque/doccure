from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings

from accounts.models import User, Profile
from doctors.models import Specialty
from core import factories


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Test user creation with required fields"""
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))
        self.assertEqual(self.user.role, "patient")  # Default role

    def test_create_doctor_user(self):
        """Test creating a doctor user"""
        doctor_data = {
            "username": "doctor",
            "email": "doctor@example.com",
            "password": "doctorpass123",
            "first_name": "Doctor",
            "last_name": "Test",
            "role": "doctor",
            "registration_number": 12345
        }
        doctor = User.objects.create_user(**doctor_data)
        
        # Create a specialty and associate it with the doctor
        specialty = Specialty.objects.create(
            name="Cardiology",
            description="Heart specialist"
        )
        specialty.doctors.add(doctor)
        
        self.assertEqual(doctor.role, "doctor")
        self.assertEqual(doctor.registration_number, 12345)
        self.assertTrue(doctor.check_password(doctor_data["password"]))
        self.assertEqual(doctor.specialties.count(), 1)
        self.assertEqual(doctor.specialties.first().name, "Cardiology")

    def test_get_full_name(self):
        """Test get_full_name method"""
        # Test with first and last name
        self.assertEqual(self.user.get_full_name(), "Test User")
        
        # Test with only username
        user_no_name = User.objects.create_user(
            username="noname",
            email="noname@example.com",
            password="testpass123"
        )
        self.assertEqual(user_no_name.get_full_name(), "noname")

    def test_get_doctor_profile(self):
        """Test get_doctor_profile method"""
        doctor = User.objects.create_user(
            username="doctor",
            email="doctor@example.com",
            password="doctorpass123",
            role="doctor"
        )
        expected_url = reverse("doctors:doctor-profile", kwargs={"username": "doctor"})
        self.assertEqual(doctor.get_doctor_profile(), expected_url)

    def test_rating_properties(self):
        """Test rating related properties"""
        # Test default values
        self.assertEqual(self.user.rating, 4)  # Default value
        self.assertEqual(self.user.average_rating, 0)  # No reviews
        self.assertEqual(self.user.rating_count, 0)  # No reviews
        
        # Test rating distribution
        distribution = self.user.rating_distribution
        self.assertEqual(distribution, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0})


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.profile = self.user.profile

    def test_profile_creation(self):
        """Test profile is created automatically for user"""
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.avatar.name, "defaults/user.png")

    def test_profile_str_representation(self):
        """Test string representation of profile"""
        self.assertEqual(str(self.profile), "Profile of testuser")

    def test_profile_image_property(self):
        """Test profile image property"""
        # Test default image
        self.assertEqual(
            self.profile.image,
            f"{settings.MEDIA_URL}defaults/user.png"
        )

        # Test custom avatar
        avatar_content = b"fake image content"
        avatar = SimpleUploadedFile(
            "test.jpg",
            avatar_content,
            content_type="image/jpeg"
        )
        self.profile.avatar = avatar
        self.profile.save()
        
        self.assertTrue(self.profile.avatar.storage.exists(self.profile.avatar.name))
        self.assertEqual(self.profile.image, self.profile.avatar.url)

    def test_profile_fields(self):
        """Test profile field updates"""
        # Update profile fields
        self.profile.phone = "+1234567890"
        self.profile.dob = timezone.now().date()
        self.profile.about = "Test about"
        self.profile.specialization = "Cardiologist"
        self.profile.gender = "male"
        self.profile.address = "123 Test St"
        self.profile.city = "Test City"
        self.profile.state = "Test State"
        self.profile.postal_code = "12345"
        self.profile.country = "Test Country"
        self.profile.price_per_consultation = "100.00"
        self.profile.blood_group = "A+"
        self.profile.allergies = "None"
        self.profile.medical_conditions = "None"
        self.profile.save()

        # Refresh from database and verify
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, "+1234567890")
        self.assertEqual(self.profile.about, "Test about")
        self.assertEqual(self.profile.specialization, "Cardiologist")
        self.assertEqual(self.profile.gender, "male")
        self.assertEqual(self.profile.address, "123 Test St")
        self.assertEqual(self.profile.city, "Test City")
        self.assertEqual(self.profile.state, "Test State")
        self.assertEqual(self.profile.postal_code, "12345")
        self.assertEqual(self.profile.country, "Test Country")
        self.assertEqual(str(self.profile.price_per_consultation), "100.00")
        self.assertEqual(self.profile.blood_group, "A+")
        self.assertEqual(self.profile.allergies, "None")
        self.assertEqual(self.profile.medical_conditions, "None")

    def test_profile_choices(self):
        """Test profile choice fields"""
        # Test gender choices
        valid_genders = ["male", "female", "other"]
        for gender in valid_genders:
            self.profile.gender = gender
            self.profile.save()
            self.profile.refresh_from_db()
            self.assertEqual(self.profile.gender, gender)

        # Test blood group choices
        valid_blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        for blood_group in valid_blood_groups:
            self.profile.blood_group = blood_group
            self.profile.save()
            self.profile.refresh_from_db()
            self.assertEqual(self.profile.blood_group, blood_group)
