import pytest
from unittest.mock import patch
from django.conf import settings
from django.core.mail import send_mail
from .service import EmailNotification


@pytest.mark.django_db
@patch("user_requests.service.send_mail")
def test_send_user_email_success(mock_send_mail):

    mock_send_mail.return_value = 1

    response = EmailNotification.send_user_email(
        subject="Test Subject",
        message="Test Message",
        recipient_email="test@example.com"
    )

    mock_send_mail.assert_called_once_with(
        subject="Test Subject",
        message="Test Message",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["test@example.com"],
        fail_silently=False,
    )

    assert response["status"] == "success"
    assert response["message"] == "Письмо успешно отправлено!"


@pytest.mark.django_db
@patch("user_requests.service.send_mail")
def test_send_user_email_failure(mock_send_mail):

    mock_send_mail.side_effect = Exception("SMTP connection error")

    response = EmailNotification.send_user_email(
        subject="Test Subject",
        message="Test Message",
        recipient_email="test@example.com"
    )

    assert response["status"] == "error"
    assert "Ошибка при отправке письма" in response["message"]
    assert "SMTP connection error" in response["message"]
