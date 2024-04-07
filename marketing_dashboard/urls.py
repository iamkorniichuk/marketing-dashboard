from django.contrib import admin
from django.urls import include, path

from .schema import schema_view


urlpatterns = [
    path("api/campaign_metrics/", include("campaign_metrics.urls")),
    path("api/keyword_metrics/", include("keyword_metrics.urls")),
    path(
        "api/schema/",
        schema_view.with_ui(),
        name="schema",
    ),
    path("admin/", admin.site.urls),
]
