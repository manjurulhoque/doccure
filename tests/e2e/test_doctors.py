import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from accounts.models import User
from tests.factories.doctor_factory import DoctorFactory
from tests.factories.booking_factory import BookingFactory


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
        """Test doctors list page displays correctly"""
        self.driver.get(f"{self.live_server_url}/doctors/")

        # Wait for doctors to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "doctor-widget"))
        )

        # Check doctor's name is displayed
        self.assertIn(
            self.doctor.first_name,
            self.driver.page_source,
            "Doctor's first name should be in the list",
        )

        # Check doctor's specialization is displayed
        self.assertIn(
            self.doctor.profile.specialization,
            self.driver.page_source,
            "Doctor's specialization should be in the list",
        )

        # Check doctor's city is displayed
        self.assertIn(
            self.doctor.profile.city,
            self.driver.page_source,
            "Doctor's city should be in the list",
        )

        # Check doctor's price is displayed
        self.assertIn(
            str(self.doctor.profile.price_per_consultation),
            self.driver.page_source,
            "Doctor's consultation price should be in the list",
        )

        # Check profile link exists
        profile_link = self.driver.find_element(
            By.XPATH,
            f"//a[contains(@href, '/doctors/{self.doctor.username}/profile/')]",
        )
        self.assertTrue(profile_link.is_displayed(), "Profile link should be visible")

    def test_doctor_profile(self):
        """Test doctor profile page displays correctly"""
        # Login as doctor
        self.driver.get(f"{self.live_server_url}/accounts/login/")
        self.driver.find_element(By.NAME, "username").send_keys(self.doctor.username)
        self.driver.find_element(By.NAME, "password").send_keys("password")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        self.driver.get(
            f"{self.live_server_url}/doctors/{self.doctor.username}/profile/"
        )

        # Check doctor's name is displayed
        self.assertIn(
            self.doctor.first_name,
            self.driver.page_source,
            "Doctor's first name should be in the profile",
        )
        self.assertIn(
            self.doctor.last_name,
            self.driver.page_source,
            "Doctor's last name should be in the profile",
        )

    def test_doctor_appointments(self):
        """Test doctor appointments page displays correctly"""
        # Login as doctor
        self.driver.get(f"{self.live_server_url}/accounts/login/")
        self.driver.find_element(By.NAME, "username").send_keys(self.doctor.username)
        self.driver.find_element(By.NAME, "password").send_keys("password")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(2)
        
        self.driver.get(f"{self.live_server_url}/doctors/appointments/")

        # # Wait for appointments to load
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "appointments-list"))
        # )
        # Check no appointments message is displayed
        self.assertIn(
            "No appointments found.",
            self.driver.page_source,
            "No appointments found should be displayed",
        )

        # Create a booking for the doctor
        BookingFactory.create_batch(5, doctor=self.doctor)

        # Refresh the page
        self.driver.refresh()

        # Check appointments title is displayed
        self.assertIn(
            "Appointments",
            self.driver.page_source,
            "Appointments title should be displayed",
        )
        # check class appointment-list is 5 times
        self.assertEqual(
            len(self.driver.find_elements(By.CLASS_NAME, "appointment-list")),
            5,
            "Appointment list should be 5 times",
        )
