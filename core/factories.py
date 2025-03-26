import factory.fuzzy
from faker import Faker

from accounts.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """A factory to random users for testing purposes."""

    class Meta:
        model = User

    first_name = factory.fuzzy.FuzzyText(length=10)
    last_name = factory.fuzzy.FuzzyText(length=10)
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    role = factory.fuzzy.FuzzyChoice(User.RoleChoices.choices, getter=lambda c: c[0])
    registration_number = factory.fuzzy.FuzzyInteger(100000, 999999)
    is_active = True
