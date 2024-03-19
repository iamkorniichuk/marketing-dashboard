from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from metrics.viewsets import CampaignMetricsViewSet, CrossroadsKeywordMetricsViewSet

metrics_router = DefaultRouter()
metrics_router.register("campaigns", CampaignMetricsViewSet, basename="campaign")
metrics_router.register(
    "keywords/crossroads", CrossroadsKeywordMetricsViewSet, basename="crossroads"
)

urlpatterns = [
    path("api/metrics/", include(metrics_router.urls)),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
