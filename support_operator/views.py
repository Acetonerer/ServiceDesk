from rest_framework import viewsets, status
from rest_framework.response import Response
from user_requests.models import UserRequest
from user_requests.service import EmailNotification
from .models import SupportOperator
from .serializers import SupportOperatorSerializer
from .service import OperatorAssignmentService
from request_messages.service import MessageService


class SupportOperatorViewSet(viewsets.ModelViewSet):
    """
    Управление операторами
    """

    queryset = SupportOperator.objects.all()
    serializer_class = SupportOperatorSerializer

    def create(self, request, *args, **kwargs):
        """
        Регистрация нового оператора
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRequestStatusUpdateViewSet(viewsets.ViewSet):
    """
    Обновление статуса заявки и назначение оператора
    """

    @staticmethod
    def take_in_progress(request, operator_id, request_id):
        """
        Принятие заявки в работу оператором
        """
        user_request = OperatorAssignmentService.get_request_by_id(request_id)
        if not user_request:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

        if user_request.status != "new":
            return Response(
                {"error": "Заявка уже в работе или закрыта"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        operator = OperatorAssignmentService.get_operator_by_id(operator_id)
        if not operator:
            return Response(
                {"error": "Оператор не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        response = OperatorAssignmentService.assign_operator_to_request(
            user_request, operator
        )
        EmailNotification().send_request_in_progress_notification(
            user_request.user_email
        )
        MessageService.add_message_to_request(
            user_request,
            sender_id=operator_id,
            sender_type="operator",
            text="Ваше обращение взято в работу оператором",
            title="Ваше обращение принято оператором",
        )

        return Response(
            {"status": "Заявка принята в работу"}, status=response["http_status"]
        )

    @staticmethod
    def close_request(request, operator_id, request_id):
        """
        Закрытие заявки оператором
        """
        user_request = OperatorAssignmentService.get_request_by_id(request_id)
        if not user_request:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

        response = OperatorAssignmentService.close_request(user_request)
        if "error" in response:
            return Response(response, status=response["status"])

        EmailNotification().send_request_closed_notification(user_request.user_email)
        MessageService.add_message_to_request(
            user_request,
            sender_id=operator_id,
            sender_type="operator",
            text="Ваше обращение успешно закрыто. Спасибо за обращение!",
            title="Ваше обращение закрыто",
        )

        return Response({"status": "Заявка закрыта"}, status=response["http_status"])
