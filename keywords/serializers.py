from rest_framework import serializers
from commons.serializers import RepresentativePkRelatedField

from regions.models import Region
from regions.serializers import RegionSerializer
from keywords.models import GoogleAdsKeyword


class GoogleAdsKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAdsKeyword
        fields = "__all__"

    regions = RepresentativePkRelatedField(
        queryset=Region.objects.all(),
        serializer_class=RegionSerializer,
        many=True,
    )
