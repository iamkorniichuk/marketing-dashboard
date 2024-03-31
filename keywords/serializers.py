from rest_framework import serializers

from keywords.models import Keyword


class GoogleAdsKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"
