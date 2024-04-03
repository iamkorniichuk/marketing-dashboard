from rest_framework.viewsets import ModelViewSet

from keyword_metrics.models import (
    CrossroadsKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
    GoogleAdsForecastKeywordMetrics,
)
from keyword_metrics.serializers import (
    CrossroadsKeywordMetricsSerializer,
    GoogleAdsHistoricalKeywordMetricsSerializer,
    GoogleAdsForecastKeywordMetricsSerializer,
)


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
