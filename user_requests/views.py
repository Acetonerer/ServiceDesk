from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserRequest
from .serializers import UserRequestSerializer
from .service import EmailNotification
from request_messages.service import MessageService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend


class UserRequestViewSet(viewsets.ModelViewSet):

    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['date_create', 'status', 'operator_id']

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'ordering', openapi.IN_QUERY,
            description="Поле для сортировки",
            type=openapi.TYPE_STRING
        ),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Фильтрация и сортировка обращений по запросу
        """
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


@api_view(['POST'])
def email_webhook(request):
    """
    Обработка входящих email-сообщений через webhook
    """

    messages = request.data.get("messages", [])
    messages.reverse()

    for message_data in messages:
        title = message_data.get('title')
        description = message_data.get('description')
        user_email = message_data.get('user_email')

        existing_request = UserRequest.objects.filter(
            user_email=user_email,
            status__in=["new", "in_progress"]
        ).first()

        if user_email == 'service.desk.2077@gmail.com':
            continue

        if existing_request:
            MessageService.add_message_to_request(
                existing_request,
                sender_id=user_email,
                sender_type="user",
                text=description,
                title=title
            )
        else:
            new_request = UserRequest.objects.create(
                title=title,
                description=description,
                status="new",
                user_email=user_email,
            )
            EmailNotification().send_request_created_notification(user_email)
            MessageService.add_message_to_request(
                new_request,
                sender_id=user_email,
                sender_type="user",
                text=description,
                title=title
            )

    return Response({"status": "processed"}, status=status.HTTP_200_OK)

