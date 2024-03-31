from django.contrib import admin
from commons.admin import get_all_fieldnames

from metrics.models import (
    CrossroadsKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
    GoogleAdsForecastKeywordMetrics,
)


@admin.register(CrossroadsKeywordMetrics)
class CrossroadsKeywordMetricsAdmin(admin.ModelAdmin):
    list_filter = ["campaign__name"]
    list_display = get_all_fieldnames(CrossroadsKeywordMetrics)


@admin.register(GoogleAdsHistoricalKeywordMetrics)
class GoogleAdsHistoricalKeywordMetricsAdmin(admin.ModelAdmin):
    list_filter = ["keyword__text"]
    list_display = [
        "get_keyword_text",
        "get_regions_names",
        "date",
        "average_month_search",
        "partners_average_month_search",
        "average_cpc",
        "partners_average_cpc",
        "low_page_bid",
        "partners_low_page_bid",
        "high_page_bid",
        "partners_high_page_bid",
    ]

    def get_keyword_text(self, obj):
        return obj.keyword.text

    get_keyword_text.short_description = "Keyword"
    get_keyword_text.admin_order_field = "keyword__text"

    def get_regions_names(self, obj):
        regions_names = obj.regions.values_list("name", flat=True)
        return ", ".join(regions_names)

    get_regions_names.short_description = "Regions"


@admin.register(GoogleAdsForecastKeywordMetrics)
class GoogleAdsForecastKeywordMetricsAdmin(admin.ModelAdmin):
    list_filter = ["keyword__text"]
    list_display = [
        "get_keyword_text",
        "get_regions_names",
        "start_date",
        "end_date",
        "impressions",
        "partners_impressions",
        "ctr",
        "partners_ctr",
        "average_cpc",
        "partners_average_cpc",
        "clicks",
        "partners_clicks",
        "cost",
        "partners_cost",
        "conversions",
        "partners_conversions",
        "conversion_rate",
        "partners_conversion_rate",
        "average_cpa",
        "partners_average_cpa",
    ]

    def get_keyword_text(self, obj):
        return obj.keyword.text

    get_keyword_text.short_description = "Keyword"
    get_keyword_text.admin_order_field = "keyword__text"

    def get_regions_names(self, obj):
        regions_names = obj.regions.values_list("name", flat=True)
        return ", ".join(regions_names)

    get_regions_names.short_description = "Regions"
