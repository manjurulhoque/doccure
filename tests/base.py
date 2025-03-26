from django.test import TestCase
from django.contrib.auth import get_user_model

class BaseTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
