from django.db.models import Max
from .models import Message
from user_requests.service import EmailNotification


class MessageService:
    """
    Класс для обработки сообщений в заявках
    """

    @staticmethod
    def add_message_to_request(user_request, sender_id, sender_type, text, title):
        """
        Метод добавления сообщения в заявку
        """
        max_sort = (
            Message.objects.filter(request=user_request).aggregate(Max("sort"))[
                "sort__max"
            ]
            or 0
        )
        sort = max_sort + 1

        return Message.objects.create(
            request=user_request,
            sender_id=sender_id,
            sender_type=sender_type,
            title=title,
            text=text,
            sort=sort,
        )

    @staticmethod
    def send_user_email(title, description, recipient_mail):
        """
        Метод отправки сообщения на почту пользователя через API
        """
        EmailNotification().send_user_email(
            subject=title,
            message=description,
            recipient_email=recipient_mail,
        )
