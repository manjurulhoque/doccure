import time

from django.test import LiveServerTestCase
from selenium import webdriver

from accounts.models import User
from tests.factories.doctor_factory import DoctorFactory


class DoctorTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        DoctorFactory.create_batch(5)

    def setUp(self):
        """Initialize WebDriver and create test user"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.doctor = DoctorFactory()

    def tearDown(self):
        """Close the WebDriver"""
        self.driver.quit()
        User.objects.filter(role=User.RoleChoices.DOCTOR).delete()

    def test_doctors_list(self):
        self.driver.get(f"{self.live_server_url}/doctors/")
        self.assertIn(
            self.doctor.first_name,
            self.driver.page_source,
            "Doctor should be in the list",
        )

    def test_doctor_profile(self):
        self.driver.get(
            f"{self.live_server_url}/doctors/{self.doctor.username}/profile/"
        )
        self.assertIn(
            self.doctor.first_name,
            self.driver.page_source,
            "Doctor first name should be in the list",
        )
        self.assertIn(
            self.doctor.last_name,
            self.driver.page_source,
            "Doctor last name should be in the list",
        )
        self.assertIn(
            "Doctor Profile",
            self.driver.page_source,
            "Doctor profile should be in the list",
        )

    def test_doctor_appointments(self):
        self.driver.get(
            f"{self.live_server_url}/doctors/appointments/"
        )
        self.assertIn(
            "Appointments",
            self.driver.page_source,
            "Appointments should be in the list",
        )
        self.assertIn(
            "Appointment Date",
            self.driver.page_source,
            "Appointment date should be in the list",
        )
