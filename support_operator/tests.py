import pytest
from support_operator.models import SupportOperator
from user_requests.models import UserRequest


@pytest.mark.django_db
def test_assign_request_to_operator():
    """
    Тест на назначение оператора к заявке и смену статуса
    """
    operator = SupportOperator.objects.create(operator_name="Operator1", operator_id=1)
    user_request = UserRequest.objects.create(
        title="Test Request",
        description="This is a test request",
        user_email="test@example.com"
    )
    user_request.operator = operator
    user_request.status = "in_progress"
    user_request.save()

    assert user_request.operator == operator
    assert user_request.status == "in_progress"


@pytest.mark.django_db
def test_operator_creation():
    """
    Тест на создание оператора
    """
    operator = SupportOperator.objects.create(operator_name="Operator2", operator_id=2)
    assert operator.operator_name == "Operator2"
    assert operator.operator_id == 2
