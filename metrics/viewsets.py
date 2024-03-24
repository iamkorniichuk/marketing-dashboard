from rest_framework.viewsets import ModelViewSet

from metrics.models import (
    CampaignMetrics,
    CrossroadsKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
    GoogleAdsForecastKeywordMetrics,
)
from metrics.serializers import (
    CampaignMetricsSerializer,
    CrossroadsKeywordMetricsSerializer,
    GoogleAdsHistoricalKeywordMetricsSerializer,
    GoogleAdsForecastKeywordMetricsSerializer,
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


class GoogleAdsHistoricalKeywordMetricsViewSet(ModelViewSet):
    queryset = GoogleAdsHistoricalKeywordMetrics.objects.all()
    serializer_class = GoogleAdsHistoricalKeywordMetricsSerializer
    filterset_fields = [
        "id",
        "date",
        "keyword__text",
    ]


class GoogleAdsForecastKeywordMetricsViewSet(ModelViewSet):
    queryset = GoogleAdsForecastKeywordMetrics.objects.all()
    serializer_class = GoogleAdsForecastKeywordMetricsSerializer
    filterset_fields = [
        "id",
        "start_date",
        "end_date",
        "keyword__text",
    ]
