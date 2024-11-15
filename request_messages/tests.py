import pytest
from .models import Message, UserRequest
from .service import MessageService
from unittest.mock import patch


@pytest.mark.django_db
def test_add_message_to_request():

    user_request = UserRequest.objects.create(title="Test Request")
    user = "example@gmail.com"

    message = MessageService.add_message_to_request(
        user_request=user_request,
        sender_id=user,
        sender_type="User",
        text="Test Message",
        title="Test Title",
    )

    assert message.request == user_request
    assert message.sender_id == user
    assert message.sender_type == "User"
    assert message.text == "Test Message"
    assert message.title == "Test Title"
    assert message.sort == 1


@pytest.mark.django_db
def test_add_message_to_request_with_existing_messages():

    user_request = UserRequest.objects.create(title="Test Request")
    user = "example@gmail.com"

    Message.objects.create(
        request=user_request,
        sender_id=user,
        sender_type="User",
        title="Old Title",
        text="Old Message",
        sort=1,
    )

    new_message = MessageService.add_message_to_request(
        user_request=user_request,
        sender_id=user,
        sender_type="User",
        text="New Test Message",
        title="New Test Title",
    )

    assert new_message.sort == 2


@pytest.mark.django_db
@patch("user_requests.service.EmailNotification.send_user_email")
def test_send_user_email(mock_send_user_email):

    MessageService.send_user_email(
        title="Test Title",
        description="Test Description",
        recipient_mail="test@example.com",
    )

    mock_send_user_email.assert_called_once_with(
        subject="Test Title",
        message="Test Description",
        recipient_email="test@example.com",
    )
