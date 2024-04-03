from rest_framework import serializers

from keywords.models import BaseKeyword


class BaseKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseKeyword
        fields = ["text"]
