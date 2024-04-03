from django.urls import include, path
from rest_framework.routers import DefaultRouter

from keywords.viewsets import KeywordViewSet


router = DefaultRouter()
router.register("google_ads", KeywordViewSet, basename="google-ads")

app_name = "keywords"

urlpatterns = [
    path("", include(router.urls)),
]
