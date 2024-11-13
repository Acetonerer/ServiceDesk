from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from user_requests.models import UserRequest
from .models import SupportOperator
from user_requests.service import EmailNotification


class OperatorAssignmentService:

    @staticmethod
    def get_request_by_id(request_id):
        """
        Возвращает заявку по ID или None, если не найдена.
        """
        try:
            return UserRequest.objects.get(pk=request_id)
        except UserRequest.DoesNotExist:
            return None

    @staticmethod
    def get_operator_by_id(operator_id):
        """
        Возвращает оператора по ID или None, если не найден.
        """
        try:
            return SupportOperator.objects.get(pk=operator_id)
        except SupportOperator.DoesNotExist:
            return None

    @staticmethod
    def assign_operator_to_request(user_request, operator):
        """
        Назначает оператора на заявку и меняет статус на 'in_progress'.
        """
        user_request.operator = operator
        user_request.status = "in_progress"
        user_request.save()
        return {
            "status": "in_progress",
            "operator_id": operator.operator_id,
            "operator_name": operator.operator_name,
            "http_status": status.HTTP_200_OK,
        }

    @staticmethod
    def close_request(user_request):
        """
        Закрывает заявку, если статус 'in_progress'.
        """
        if user_request.status != "in_progress":
            return {
                "error": "Заявка может быть закрыта только со статусом 'in_progress'.",
                "status": status.HTTP_400_BAD_REQUEST,
            }
        user_request.status = "closed"
        user_request.save()
        return {"status": "closed", "http_status": status.HTTP_200_OK}
