from rest_framework import serializers
from commons.serializers import RepresentativePkRelatedField

from campaigns.serializers import (
    TiktokBusinessCampaignSerializer,
    TiktokBusinessCampaign,
    CrossroadsCampaignSerializer,
    CrossroadsCampaign,
)
from metrics.models import (
    TiktokBusinessCampaignMetrics,
    CrossroadsCampaignMetrics,
    CampaignMetrics,
    CrossroadsKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
    GoogleAdsForecastKeywordMetrics,
)
from keywords.models import GoogleAdsKeyword
from keywords.serializers import GoogleAdsKeywordSerializer


class TiktokBusinessCampaignMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiktokBusinessCampaignMetrics
        fields = "__all__"

    campaign = RepresentativePkRelatedField(
        queryset=TiktokBusinessCampaign.objects.all(),
        serializer_class=TiktokBusinessCampaignSerializer,
    )


class CrossroadsCampaignMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossroadsCampaignMetrics
        fields = "__all__"

    campaign = RepresentativePkRelatedField(
        queryset=CrossroadsCampaign.objects.all(),
        serializer_class=CrossroadsCampaignSerializer,
    )


class CampaignMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignMetrics
        fields = "__all__"

    tiktok_business_metrics = RepresentativePkRelatedField(
        queryset=TiktokBusinessCampaignMetrics.objects.all(),
        serializer_class=TiktokBusinessCampaignMetricsSerializer,
    )
    crossroads_metrics = RepresentativePkRelatedField(
        queryset=CrossroadsCampaignMetrics.objects.all(),
        serializer_class=CrossroadsCampaignMetricsSerializer,
    )


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
        queryset=GoogleAdsKeyword.objects.all(),
        serializer_class=GoogleAdsKeywordSerializer,
    )


class GoogleAdsForecastKeywordMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAdsForecastKeywordMetrics
        fields = "__all__"

    keyword = RepresentativePkRelatedField(
        queryset=GoogleAdsKeyword.objects.all(),
        serializer_class=GoogleAdsKeywordSerializer,
    )
