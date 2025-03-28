from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

User = get_user_model()


class HomePageTest(LiveServerTestCase):
    def setUp(self):
        """Initialize WebDriver and create test user"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Close the WebDriver"""
        self.driver.quit()

    def test_home_page_title(self):
        """Test that the home page title is correct"""
        self.driver.get(self.live_server_url)
        self.assertIn("Home", self.driver.title)


class UserLoginTest(LiveServerTestCase):
    def setUp(self):
        """Initialize WebDriver and create test user"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        self.test_user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def tearDown(self):
        """Close the WebDriver"""
        self.driver.quit()

    def test_login(self):
        """Test user login functionality"""
        self.driver.get(f"{self.live_server_url}/accounts/login/")

        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        login_button.click()

        time.sleep(2)  # Wait for page transition

        # Verify login success
        self.assertIn("Dashboard", self.driver.page_source)

    def test_logout(self):
        """Test user logout functionality"""
        # First login
        self.driver.get(f"{self.live_server_url}/accounts/login/")
        
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        login_button.click()

        time.sleep(2)  # Wait for page transition

        # Click the user menu dropdown
        user_menu = self.driver.find_element(By.CLASS_NAME, "dropdown-toggle")
        user_menu.click()

        time.sleep(1)  # Wait for dropdown to open

        # Find and click the logout link in the dropdown
        logout_button = self.driver.find_element(By.XPATH, "//a[@href='/accounts/logout/']")
        logout_button.click()

        time.sleep(2)  # Wait for page transition

        # Verify logout success
        self.assertIn("Login", self.driver.page_source)
        self.assertIn("You are now logged out", self.driver.page_source)

