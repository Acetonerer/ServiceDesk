from .views import UserRequestViewSet
from django.urls import path
from .views import email_webhook


urlpatterns = [
    path('user_requests/', UserRequestViewSet.as_view({'get': 'list'}), name='user_requests'),

    path('webhook/email/', email_webhook, name='email_webhook'),
]

