from django.urls import include, path
from rest_framework.routers import DefaultRouter

from keyword_metrics.viewsets import (
    CrossroadsKeywordMetricsViewSet,
    GoogleAdsHistoricalKeywordMetricsViewSet,
    GoogleAdsForecastKeywordMetricsViewSet,
)


router = DefaultRouter()
router.register("crossroads", CrossroadsKeywordMetricsViewSet, basename="crossroads")
router.register(
    "google_ads/historical",
    GoogleAdsHistoricalKeywordMetricsViewSet,
    basename="google-ads-historical",
)
router.register(
    "google_ads/forecast",
    GoogleAdsForecastKeywordMetricsViewSet,
    basename="google-ads-forecast",
)

app_name = "keyword_metrics"

urlpatterns = [
    path("", include(router.urls)),
]
