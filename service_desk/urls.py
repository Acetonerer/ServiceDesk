"""
URL configuration for service_desk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib import admin
from django.urls import path, include
from .template_view import home

schema_view = get_schema_view(
    openapi.Info(
        title="ServiceDesk API",
        default_version="v1",
        description="API для работы с обращениями",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url="https://servicedesk.stoutdev.ru",
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema_swagger_ui",
    ),
    path("admin/", admin.site.urls),
    path("requests/", include("user_requests.urls")),
    path("mgs/", include("request_messages.urls")),
    path("ops/", include("support_operator.urls")),
    path('', home, name='home'),
]
