from django.urls import include, path
from rest_framework.routers import DefaultRouter

from metrics.viewsets import (
    CampaignMetricsViewSet,
    CrossroadsKeywordMetricsViewSet,
    GoogleAdsHistoricalKeywordMetricsViewSet,
    GoogleAdsForecastKeywordMetricsViewSet,
)


router = DefaultRouter()
router.register("campaigns", CampaignMetricsViewSet, basename="campaign")
router.register(
    "keywords/crossroads", CrossroadsKeywordMetricsViewSet, basename="crossroads"
)
router.register(
    "keywords/google_ads/historical",
    GoogleAdsHistoricalKeywordMetricsViewSet,
    basename="google-ads-historical",
)
router.register(
    "keywords/google_ads/forecast",
    GoogleAdsForecastKeywordMetricsViewSet,
    basename="google-ads-forecast",
)

app_name = "metrics"

urlpatterns = [
    path("", include(router.urls)),
]
