from django.urls import include, path
from rest_framework.routers import DefaultRouter

from campaign_metrics.viewsets import CampaignMetricsViewSet


router = DefaultRouter()
router.register("", CampaignMetricsViewSet)

app_name = "campaign_metrics"

urlpatterns = [
    path("", include(router.urls)),
]
