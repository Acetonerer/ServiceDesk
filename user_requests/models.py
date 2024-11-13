from django.db import models
from support_operator.models import SupportOperator


class UserRequest(models.Model):

    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыто'),
    ]

    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    user_email = models.CharField(max_length=255)
    operator = models.ForeignKey(SupportOperator, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_requests'
        ordering = ['-date_create']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

