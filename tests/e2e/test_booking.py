import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.factories.doctor_factory import DoctorFactory
from tests.factories.schedule_factory import ScheduleFactory
from tests.factories.user_factory import UserFactory
from accounts.models import User


class DoctorTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.patient = UserFactory(role=User.RoleChoices.PATIENT)

    def setUp(self):
        """Initialize WebDriver and create test user"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.doctor = DoctorFactory()
        self.schedule = ScheduleFactory.create_schedule(self.doctor)

    def tearDown(self):
        """Close the WebDriver"""
        self.driver.quit()

    def test_booking_flow(self):
        """Test booking flow from doctor's profile to booking creation"""
        self.driver.get(f"{self.live_server_url}/accounts/login/")
        self.driver.find_element(By.NAME, "username").send_keys(self.patient.username)
        self.driver.find_element(By.NAME, "password").send_keys("password")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(1)

        # Navigate to doctor's profile
        self.driver.get(
            f"{self.live_server_url}/bookings/doctor/{self.doctor.username}"
        )
        time.sleep(1)
        self.driver.find_element(By.CLASS_NAME, "timing").click()
        # Click on the schedule
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        self.assertIn(
            "Appointment booked successfully",
            self.driver.page_source,
            "Appointment should be booked successfully",
        )
