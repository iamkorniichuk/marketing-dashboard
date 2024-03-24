from rest_framework import serializers

from regions.models import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"
