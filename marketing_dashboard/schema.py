from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg.openapi import Info


schema_view = get_schema_view(
    Info(
        title=_("marketing-dashboard"),
        default_version="v0.0.0",
    ),
    public=True,
    permission_classes=[AllowAny],
)
