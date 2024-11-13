from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Message
from support_operator.models import SupportOperator
from .serializers import MessageSerializer, SendUserMessageSerializer
from support_operator.service import OperatorAssignmentService
from user_requests.service import EmailNotification
from request_messages.service import MessageService


class MessageViewSet(viewsets.ModelViewSet):
    """
    Класс отображения списка сообщений по request_id
    """

    serializer_class = MessageSerializer

    def get_queryset(self):
        request_id = self.kwargs.get("request_id")
        if request_id:
            return Message.objects.filter(request_id=request_id)
        return Message.objects.none()


class MessageSendViewSet(viewsets.ModelViewSet):
    """
    Класс для отправки сообщений на пользовательский email
    через API
    """
    serializer_class = SendUserMessageSerializer

    @staticmethod
    def send_message(request, request_id=None):

        serializer = SendUserMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_data = serializer.validated_data

        user_request = OperatorAssignmentService.get_request_by_id(request_id)
        if not user_request:
            return Response({"error": "Заявка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        operator = OperatorAssignmentService.get_operator_by_id(message_data['operator_id'])
        if not operator:
            return Response({"error": "Оператор не найден."}, status=status.HTTP_404_NOT_FOUND)

        if user_request.status == 'closed':
            return Response(
                {"error": "Нельзя отправлять сообщения в закрытую заявку."},
                status=status.HTTP_400_BAD_REQUEST
            )

        MessageService.add_message_to_request(
            user_request=user_request,
            sender_id=message_data['operator_id'],
            sender_type='operator',
            title=message_data['title'],
            text=message_data['description'],
        )

        MessageService.send_user_email(
            title=message_data['title'],
            description=message_data['description'],
            recipient_mail=message_data['recipient_mail']
        )

        return Response({"status": "Сообщение отправлено и сохранено."}, status=status.HTTP_201_CREATED)
