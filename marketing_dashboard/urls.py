from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .schema import schema_view


urlpatterns = [
    path("api/metrics/", include("metrics.urls")),
    path("api/keywords/", include("keywords.urls")),
    path(
        "api/schema/",
        schema_view.with_ui(),
        name="schema",
    ),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
