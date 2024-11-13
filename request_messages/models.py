from django.db import models
from user_requests.models import UserRequest


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sort = models.IntegerField()
    request = models.ForeignKey(
        UserRequest, related_name="messages", on_delete=models.CASCADE
    )
    sender_id = models.CharField(max_length=50)
    sender_type = models.CharField(max_length=30)
    title = models.TextField()
    text = models.TextField()

    class Meta:
        db_table = "request_messages"

    def __str__(self):
        return f'Message with title "{self.title}" from sender {self.sender_id}'
