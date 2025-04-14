from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from accounts.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    role = User.RoleChoices.PATIENT
    is_active = True
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    @post_generation
    def create_password(self, create, extracted, **kwargs):
        if not create:
            return
        self.set_password("password")
