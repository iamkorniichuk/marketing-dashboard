from django.urls import include, path
from rest_framework.routers import DefaultRouter

from metrics.viewsets import CampaignMetricsViewSet, CrossroadsKeywordMetricsViewSet


router = DefaultRouter()
router.register("campaigns", CampaignMetricsViewSet, basename="campaign")
router.register(
    "keywords/crossroads", CrossroadsKeywordMetricsViewSet, basename="crossroads"
)

urlpatterns = [
    path("", include(router.urls)),
]
