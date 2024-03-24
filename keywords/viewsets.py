from rest_framework.viewsets import ModelViewSet

from keywords.models import GoogleAdsKeyword
from keywords.serializers import GoogleAdsKeywordSerializer


class GoogleAdsKeywordViewSet(ModelViewSet):
    queryset = GoogleAdsKeyword.objects.all()
    serializer_class = GoogleAdsKeywordSerializer
    filterset_fields = ["id", "text"]
