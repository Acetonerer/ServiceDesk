from rest_framework import serializers
from user_requests.models import UserRequest


class UserRequestSerializer(serializers.ModelSerializer):

    date_create = serializers.DateTimeField(format="%d-%m-%Y, %H:%M")
    date_update = serializers.DateTimeField(format="%d-%m-%Y, %H:%M")

    class Meta:
        model = UserRequest
        fields = "__all__"
