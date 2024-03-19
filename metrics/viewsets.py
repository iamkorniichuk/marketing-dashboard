from rest_framework.viewsets import ModelViewSet

from metrics.serializers import (
    CampaignMetrics,
    CampaignMetricsSerializer,
    CrossroadsKeywordMetrics,
    CrossroadsKeywordMetricsSerializer,
)


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


class CrossroadsKeywordMetricsViewSet(ModelViewSet):
    queryset = CrossroadsKeywordMetrics.objects.all()
    serializer_class = CrossroadsKeywordMetricsSerializer
    filterset_fields = [
        "id",
        "date",
        "campaign__name",
        "campaign__id",
        "lander_keyword",
    ]
