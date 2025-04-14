from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from accounts.models import User, Profile
from doctors.models import Education, Experience, Specialty


class DoctorFactory(DjangoModelFactory):
    class Meta:
        model = User

    role = User.RoleChoices.DOCTOR
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    username = Faker("user_name")
    email = Faker("email")
    registration_number = Faker("random_int", min=100000, max=999999)
    is_active = True

    @post_generation
    def create_password(self, create, extracted, **kwargs):
        if not create:
            return
        self.set_password("password")

    @post_generation
    def create_profile(self, create, extracted, **kwargs):
        if not create:
            return
        Profile.objects.get_or_create(user=self)

    @post_generation
    def create_education(self, create, extracted, **kwargs):
        if not create:
            return
        Education.objects.get_or_create(user=self)

    @post_generation
    def create_experience(self, create, extracted, **kwargs):
        if not create:
            return
        Experience.objects.get_or_create(user=self)

    @post_generation
    def create_specialization(self, create, extracted, **kwargs):
        if not create:
            return
        specialty = Specialty.objects.create(
            name="Cardiology", description="Heart specialist"
        )
        specialty.doctors.add(self)
