from datetime import datetime
from rest_framework import serializers


class BasicUserInformationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField(required=False, allow_null=True)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate_dob(self, value):
        if value and value > datetime.now().date():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future"
            )
        return value
