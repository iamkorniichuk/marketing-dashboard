from rest_framework import serializers
from commons.serializers import RepresentativePkRelatedField

from campaigns.models import (
    CrossroadsCampaign,
    TiktokBusinessCampaign,
    TiktokAdvertiser,
)


class TiktokBusinessAdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiktokAdvertiser
        fields = "__all__"


class TiktokBusinessCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiktokBusinessCampaign
        fields = "__all__"

    advertiser = RepresentativePkRelatedField(
        queryset=TiktokAdvertiser.objects.all(),
        serializer_class=TiktokBusinessAdvertiserSerializer,
    )


class CrossroadsCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossroadsCampaign
        fields = "__all__"
