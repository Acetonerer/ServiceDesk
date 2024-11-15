import pytest
from rest_framework import status
from user_requests.models import UserRequest
from .models import SupportOperator
from .service import OperatorAssignmentService
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.mark.django_db
def test_assign_operator_to_request():

    user_request = UserRequest.objects.create(title="Test Request", status="new")
    operator = SupportOperator.objects.create(operator_id=1, operator_name="Operator One")

    response = OperatorAssignmentService.assign_operator_to_request(
        user_request=user_request,
        operator=operator
    )

    user_request.refresh_from_db()
    assert user_request.operator == operator
    assert user_request.status == "in_progress"
    assert response["status"] == "in_progress"
    assert response["operator_id"] == operator.operator_id
    assert response["operator_name"] == operator.operator_name
    assert response["http_status"] == status.HTTP_200_OK


@pytest.mark.django_db
def test_close_request_in_progress():

    user_request = UserRequest.objects.create(title="Test Request", status="in_progress")

    response = OperatorAssignmentService.close_request(user_request=user_request)

    user_request.refresh_from_db()
    assert user_request.status == "closed"
    assert response["status"] == "closed"
    assert response["http_status"] == status.HTTP_200_OK


@pytest.mark.django_db
def test_close_request_not_in_progress():

    user_request = UserRequest.objects.create(title="Test Request", status="new")

    response = OperatorAssignmentService.close_request(user_request=user_request)

    user_request.refresh_from_db()
    assert user_request.status == "new"
    assert response["error"] == "Заявка может быть закрыта только со статусом 'in_progress'."
    assert response["status"] == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_support_operator():
    client = APIClient()
    url = reverse("support_operators_list_create")
    data = {
        "operator_id": 1,
        "operator_name": "Operator One",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["operator_id"] == data["operator_id"]
    assert response.data["operator_name"] == data["operator_name"]

    operator = SupportOperator.objects.get(operator_id=data["operator_id"])
    assert operator.operator_name == data["operator_name"]
