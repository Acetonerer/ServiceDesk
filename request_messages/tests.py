import pytest
from request_messages.models import Message
from user_requests.models import UserRequest
from support_operator.models import SupportOperator  # Добавляем импорт модели оператора
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_add_message_to_request():
    """
    Тест на добавление сообщения к заявке
    """
    user_request = UserRequest.objects.create(
        title="Test Request",
        description="This is a test request",
        user_email="test@example.com"
    )
    message = Message.objects.create(
        request=user_request,
        sender_id="test_user",
        sender_type="user",
        title="Test Message",
        text="This is a test message",
        sort=1
    )
    assert message.title == "Test Message"
    assert message.request == user_request


@pytest.mark.django_db
def test_send_message_view(django_user_model):
    """
    Тест на отправку сообщения через API
    Сначала инициализируем клиент
    Также создаём тестового оператора
    """

    client = Client()

    user_request = UserRequest.objects.create(
        title="Test Request",
        description="This is a test request",
        user_email="test@example.com",
    )

    operator = SupportOperator.objects.create(operator_id=1, operator_name="Test Operator")

    data = {
        "title": "API Test Message",
        "description": "This is a test message from the API",
        "recipient_mail": "test@example.com",
        "operator_id": operator.operator_id
    }

    url = reverse("post_mail", kwargs={"request_id": user_request.request_id})
    response = client.post(url, data, content_type="application/json")

    assert response.status_code == 201
    assert response.json()["status"] == "Сообщение отправлено и сохранено."

    message = Message.objects.filter(request=user_request).first()
    assert message is not None
    assert message.title == "API Test Message"
    assert message.text == "This is a test message from the API"
