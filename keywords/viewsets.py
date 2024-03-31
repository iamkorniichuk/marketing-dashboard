from rest_framework.viewsets import ModelViewSet

from keywords.models import Keyword
from keywords.serializers import GoogleAdsKeywordSerializer


class GoogleAdsKeywordViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = GoogleAdsKeywordSerializer
    filterset_fields = ["id", "text"]
