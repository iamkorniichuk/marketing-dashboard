from django.contrib import admin
from commons.admin import get_all_fieldnames

from metrics.models import CrossroadsKeywordMetrics, GoogleAdsHistoricalKeywordMetrics


@admin.register(CrossroadsKeywordMetrics)
class CrossroadsKeywordMetricsAdmin(admin.ModelAdmin):
    list_filter = ["campaign__name"]
    list_display = get_all_fieldnames(CrossroadsKeywordMetrics)


@admin.register(GoogleAdsHistoricalKeywordMetrics)
class GoogleAdsHistoricalKeywordMetricsAdmin(admin.ModelAdmin):
    list_filter = ["keyword__text"]
    list_display = [
        "get_keyword_text",
        "get_keyword_regions_names",
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

    def get_keyword_regions_names(self, obj):
        regions_names = obj.keyword.regions.values_list("name", flat=True)
        return ", ".join(regions_names)

    get_keyword_regions_names.short_description = "Regions"
