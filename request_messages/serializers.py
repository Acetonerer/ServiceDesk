from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения списка сообщений по request_id
    """
    class Meta:
        model = Message
        fields = ['request', 'sender_id', 'sender_type', 'sort', 'text', 'title']


class SendUserMessageSerializer(serializers.Serializer):
    """
    Сериализатор для отправки сообщения на почту пользователя через API
    """
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    recipient_mail = serializers.EmailField()
    operator_id = serializers.IntegerField()
