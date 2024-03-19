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


class CrossroadsKeywordMetricsViewSet(ModelViewSet):
    queryset = CrossroadsKeywordMetrics.objects.all()
    serializer_class = CrossroadsKeywordMetricsSerializer
