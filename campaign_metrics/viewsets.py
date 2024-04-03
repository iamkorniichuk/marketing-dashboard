from rest_framework.viewsets import ModelViewSet

from campaign_metrics.models import CampaignMetrics
from campaign_metrics.serializers import CampaignMetricsSerializer


class CampaignMetricsViewSet(ModelViewSet):
    queryset = CampaignMetrics.objects.all()
    serializer_class = CampaignMetricsSerializer
    filterset_fields = [
        "id",
        "date",
        "tiktok_business_metrics__campaign__name",
        "tiktok_business_metrics__campaign__id",
        "crossroads_metrics__campaign__name",
        "crossroads_metrics__campaign__id",
    ]
