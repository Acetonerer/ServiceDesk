from django.urls import path
from .views import SupportOperatorViewSet, UserRequestStatusUpdateViewSet

urlpatterns = [
    path(
        "support_ops/",
        SupportOperatorViewSet.as_view({"get": "list", "post": "create"}),
        name="support_operators_list_create",
    ),
    path(
        "<int:operator_id>/requests/<int:request_id>/progress/",
        UserRequestStatusUpdateViewSet.as_view({"post": "take_in_progress"}),
        name="take_request_in_progress",
    ),
    path(
        "<int:operator_id>/requests/<int:request_id>/close/",
        UserRequestStatusUpdateViewSet.as_view({"post": "close_request"}),
        name="close_request",
    ),
]
