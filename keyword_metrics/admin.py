from django.contrib import admin
from django.utils.html import format_html
from commons.admin import get_all_fieldnames

from keyword_metrics.models import (
    CrossroadsKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
    GoogleAdsForecastKeywordMetrics,
    GoogleSearchKeywordMetrics,
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


@admin.register(GoogleSearchKeywordMetrics)
class GoogleSearchKeywordMetricsAdmin(admin.ModelAdmin):
    list_filter = ["keyword__text"]
    list_display = [
        "get_keyword_text",
        "date",
        "get_region_name",
        "competition",
        "average_cpc",
        "partners_average_cpc",
        "low_page_bid",
        "partners_low_page_bid",
        "high_page_bid",
        "partners_high_page_bid",
        "get_volume_trends_img_tag",
    ]

    def get_keyword_text(self, obj):
        return obj.keyword.text

    get_keyword_text.short_description = "Keyword"
    get_keyword_text.admin_order_field = "keyword__text"

    def get_region_name(self, obj):
        return obj.region.name

    get_region_name.short_description = "Region"

    def get_volume_trends_img_tag(self, obj):
        return format_html(f'<img src="{obj.volume_trends_image.url}" height="100"/>')

    get_volume_trends_img_tag.short_description = "Volume Trends"
