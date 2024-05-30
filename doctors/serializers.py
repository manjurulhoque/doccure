from rest_framework import serializers

from accounts.models import User
from doctors.models import Education, Experience


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "college", "degree", "year_of_completion"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ["id", "institution", "from_year", "to_year", "designation"]


class RegistrationNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "registration_number"]


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "specialization"]
