from rest_framework import serializers


class BasicUserInformationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    phone = serializers.CharField(required=False)
