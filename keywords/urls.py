from django.urls import include, path
from rest_framework.routers import DefaultRouter

from keywords.viewsets import GoogleAdsKeywordViewSet


router = DefaultRouter()
router.register("google_ads", GoogleAdsKeywordViewSet, basename="google-ads")

app_name = "keywords"

urlpatterns = [
    path("", include(router.urls)),
]
