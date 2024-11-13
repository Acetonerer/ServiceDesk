from django.conf import settings
from django.core.mail import send_mail
from request_messages.models import Message


class EmailNotification:
    """
    Класс для отправки автосообщений пользователю
    """

    def __init__(self):
        self.from_email = settings.EMAIL_HOST_USER

    @staticmethod
    def send_user_email(subject, message, recipient_email):
        """
        Отправляет email через SMTP
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            return {"status": "success", "message": "Письмо успешно отправлено!"}
        except Exception as error:
            return {
                "status": "error",
                "message": f"Ошибка при отправке письма: {error}",
            }

    def send_request_created_notification(self, user_email):
        """
        Уведомление о создании запроса
        """
        subject = "Ваше обращение получено"
        message = (
            f"Здравствуйте, {user_email}!\n\nМы получили ваше обращение."
            f"\n\nЭто сообщение сгенерировано автоматически."
            f"\n\nПожалуйста, не отвечайте на него."
        )
        return self.send_user_email(subject, message, user_email)

    def send_request_in_progress_notification(self, user_email):
        """
        Уведомление о принятии запроса в работу
        """
        subject = "Ваше обращение принято оператором"
        message = (
            f"Здравствуйте, {user_email}!\n\nВаше обращение взято в работу оператором."
            f"\n\nЭто сообщение сгенерировано автоматически."
            f"\n\nПожалуйста, не отвечайте на него."
        )
        return self.send_user_email(subject, message, user_email)

    def send_request_closed_notification(self, user_email):
        """
        Уведомление о закрытии запроса
        """
        subject = "Ваше обращение закрыто"
        message = (
            f"Здравствуйте, {user_email}!\n\nВаше обращение успешно закрыто. Спасибо за обращение!"
            f"\n\nЭто сообщение сгенерировано автоматически."
            f"\n\nПожалуйста, не отвечайте на него."
        )
        return self.send_user_email(subject, message, user_email)
