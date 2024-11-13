import pytest
from user_requests.models import UserRequest
from user_requests.service import EmailNotification


@pytest.mark.django_db
def test_create_new_user_request():
    """
    Тест для создания новой заявки
    """
    user_request = UserRequest.objects.create(
        title="Test Request",
        description="This is a test request",
        user_email="test@example.com"
    )
    assert user_request.title == "Test Request"
    assert user_request.status == "new"
    assert user_request.operator is None


@pytest.mark.django_db
def test_send_creation_notification(mocker):
    """
    Тест на отправку уведомления при создании заявки
    """
    mocker.patch.object(EmailNotification, 'send_user_email', return_value={"status": "success"})
    email_service = EmailNotification()
    response = email_service.send_request_created_notification("test@example.com")
    print(response)
    assert response["status"] == "success"
