from django.urls import path
from request_messages.views import MessageViewSet, MessageSendViewSet

urlpatterns = [
    path(
        "requests/<int:request_id>/mgs/",
        MessageViewSet.as_view({"get": "list"}),
        name="get_list",
    ),
    path(
        "requests/<int:request_id>/mgs/create",
        MessageSendViewSet.as_view({"post": "send_message"}),
        name="post_mail",
    ),
]
