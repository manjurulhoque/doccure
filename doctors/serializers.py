from rest_framework import serializers

from doctors.models import Education


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'college', 'degree', 'year_of_completion']
