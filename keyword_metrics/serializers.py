from rest_framework import serializers
from commons.serializers import RepresentativePkRelatedField

from campaigns.serializers import (
    CrossroadsCampaignSerializer,
    CrossroadsCampaign,
)
from keyword_metrics.models import (
    CrossroadsKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
    GoogleAdsForecastKeywordMetrics,
)
from keywords.models import Keyword
from keywords.serializers import KeywordSerializer


class CrossroadsKeywordMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossroadsKeywordMetrics
        fields = "__all__"

    campaign = RepresentativePkRelatedField(
        queryset=CrossroadsCampaign.objects.all(),
        serializer_class=CrossroadsCampaignSerializer,
    )


class GoogleAdsHistoricalKeywordMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAdsHistoricalKeywordMetrics
        fields = "__all__"

    keyword = RepresentativePkRelatedField(
        queryset=Keyword.objects.all(),
        serializer_class=KeywordSerializer,
    )


class GoogleAdsForecastKeywordMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAdsForecastKeywordMetrics
        fields = "__all__"

    keyword = RepresentativePkRelatedField(
        queryset=Keyword.objects.all(),
        serializer_class=KeywordSerializer,
    )
