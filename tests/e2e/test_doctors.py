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
        self.assertIn(self.doctor.first_name, self.driver.page_source, "Doctor should be in the list")
