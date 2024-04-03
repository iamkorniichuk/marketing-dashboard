from rest_framework.viewsets import ModelViewSet

from keywords.models import Keyword
from keywords.serializers import KeywordSerializer


class KeywordViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    filterset_fields = ["id", "text"]
