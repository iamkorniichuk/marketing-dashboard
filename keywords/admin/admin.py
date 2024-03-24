from django.contrib import admin

from keywords.models import GoogleAdsKeyword

from .actions import request_historical_metrics, request_forecast_metrics


@admin.register(GoogleAdsKeyword)
class GoogleAdsKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text"]
    list_display = ["text", "get_regions_names"]
    actions = [request_historical_metrics, request_forecast_metrics]

    def get_regions_names(self, obj):
        regions_names = obj.regions.values_list("name", flat=True)
        return ", ".join(regions_names)

    get_regions_names.short_description = "Regions"
