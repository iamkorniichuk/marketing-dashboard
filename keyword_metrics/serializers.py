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
from keywords.models import BaseKeyword
from keywords.serializers import BaseKeywordSerializer


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
        queryset=BaseKeyword.objects.all(),
        serializer_class=BaseKeywordSerializer,
    )


class GoogleAdsForecastKeywordMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAdsForecastKeywordMetrics
        fields = "__all__"

    keyword = RepresentativePkRelatedField(
        queryset=BaseKeyword.objects.all(),
        serializer_class=BaseKeywordSerializer,
    )
