from django.contrib import admin

from campaigns.models import (
    TiktokBusinessCampaign,
    CrossroadsCampaign,
    MergedCampaign,
    CrossroadsToTiktokBusinessIdentifiers,
)
from commons.admin import get_all_fieldnames


@admin.register(TiktokBusinessCampaign)
class TiktokBusinessCampaignAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(TiktokBusinessCampaign)


@admin.register(CrossroadsCampaign)
class CrossroadsCampaignAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(CrossroadsCampaign)


@admin.register(MergedCampaign)
class MergedCampaignAdmin(admin.ModelAdmin):
    list_filter = ["crossroads__name"]
    list_display = [
        "get_tiktok_business_name",
        "get_tiktok_business_identifier",
        "get_crossroads_identifier",
        "get_tiktok_business_advertiser_id",
        "get_tiktok_business_date",
        "get_crossroads_date",
        "get_tiktok_business_video_views_p25",
        "get_tiktok_business_video_views_p50",
        "get_tiktok_business_video_views_p75",
        "get_tiktok_business_video_views_p100",
        "get_tiktok_business_video_watched_2s",
        "get_tiktok_business_video_watched_6s",
        "get_tiktok_business_cpc",
        "get_tiktok_business_ctr",
        "get_tiktok_business_clicks",
        "get_tiktok_business_spend",
        "get_crossroads_revenue",
        "get_tiktok_business_conversion",
        "get_tiktok_business_cost_per_conversion",
        "get_crossroads_rpc",
        "get_crossroads_rpv",
        "get_crossroads_total_visitors",
        "get_crossroads_filtered_visitors",
        "get_crossroads_lander_visitors",
        "get_crossroads_lander_searches",
        "get_crossroads_revenue_events",
    ]

    def get_tiktok_business_name(self, obj):
        return obj.tiktok_business.name

    get_tiktok_business_name.short_description = "Name"
    get_tiktok_business_name.admin_order_field = "tiktok_business__name"

    def get_tiktok_business_identifier(self, obj):
        return obj.tiktok_business.identifier

    get_tiktok_business_identifier.short_description = "Id"
    get_tiktok_business_identifier.admin_order_field = "tiktok_business__identifier"

    def get_crossroads_identifier(self, obj):
        return obj.crossroads.identifier

    get_crossroads_identifier.short_description = "Crossroads Id"
    get_crossroads_identifier.admin_order_field = "crossroads__identifier"

    def get_tiktok_business_advertiser_id(self, obj):
        return obj.tiktok_business.advertiser_id

    get_tiktok_business_advertiser_id.short_description = "Advertiser Id"
    get_tiktok_business_advertiser_id.admin_order_field = (
        "tiktok_business__advertiser_id"
    )

    def get_tiktok_business_date(self, obj):
        return obj.tiktok_business.date

    get_tiktok_business_date.short_description = "Date"
    get_tiktok_business_date.admin_order_field = "tiktok_business__date"

    def get_crossroads_date(self, obj):
        return obj.crossroads.date

    get_crossroads_date.short_description = "Crossroads Date"
    get_crossroads_date.admin_order_field = "crossroads__date"

    def get_tiktok_business_video_views_p25(self, obj):
        return obj.tiktok_business.video_views_p25

    get_tiktok_business_video_views_p25.short_description = "Video Views Per 25"
    get_tiktok_business_video_views_p25.admin_order_field = (
        "tiktok_business__video_views_p25"
    )

    def get_tiktok_business_video_views_p50(self, obj):
        return obj.tiktok_business.video_views_p50

    get_tiktok_business_video_views_p50.short_description = "Video Views Per 50"
    get_tiktok_business_video_views_p50.admin_order_field = (
        "tiktok_business__video_views_p50"
    )

    def get_tiktok_business_video_views_p75(self, obj):
        return obj.tiktok_business.video_views_p75

    get_tiktok_business_video_views_p75.short_description = "Video Views Per 75"
    get_tiktok_business_video_views_p75.admin_order_field = (
        "tiktok_business__video_views_p75"
    )

    def get_tiktok_business_video_views_p100(self, obj):
        return obj.tiktok_business.video_views_p100

    get_tiktok_business_video_views_p100.short_description = "Video Views Per 100"
    get_tiktok_business_video_views_p100.admin_order_field = (
        "tiktok_business__video_views_p100"
    )

    def get_tiktok_business_video_watched_2s(self, obj):
        return obj.tiktok_business.video_watched_2s

    get_tiktok_business_video_watched_2s.short_description = "Video Watched 2s"
    get_tiktok_business_video_watched_2s.admin_order_field = (
        "tiktok_business__video_watched_2s"
    )

    def get_tiktok_business_video_watched_6s(self, obj):
        return obj.tiktok_business.video_watched_6s

    get_tiktok_business_video_watched_6s.short_description = "Video Watched 6s"
    get_tiktok_business_video_watched_6s.admin_order_field = (
        "tiktok_business__video_watched_6s"
    )

    def get_tiktok_business_cpc(self, obj):
        return obj.tiktok_business.cpc

    get_tiktok_business_cpc.short_description = "CPC"
    get_tiktok_business_cpc.admin_order_field = "tiktok_business__cpc"

    def get_tiktok_business_ctr(self, obj):
        return obj.tiktok_business.ctr

    get_tiktok_business_ctr.short_description = "CTR"
    get_tiktok_business_ctr.admin_order_field = "tiktok_business__ctr"

    def get_tiktok_business_clicks(self, obj):
        return obj.tiktok_business.clicks

    get_tiktok_business_clicks.short_description = "Clicks"
    get_tiktok_business_clicks.admin_order_field = "tiktok_business__clicks"

    def get_tiktok_business_spend(self, obj):
        return obj.tiktok_business.spend

    get_tiktok_business_spend.short_description = "Spend"
    get_tiktok_business_spend.admin_order_field = "tiktok_business__spend"

    def get_crossroads_revenue(self, obj):
        return obj.crossroads.revenue

    get_crossroads_revenue.short_description = "Crossroads Revenue"
    get_crossroads_revenue.admin_order_field = "crossroads__revenue"

    def get_tiktok_business_conversion(self, obj):
        return obj.tiktok_business.conversion

    get_tiktok_business_conversion.short_description = "Conversion"
    get_tiktok_business_conversion.admin_order_field = "tiktok_business__conversion"

    def get_tiktok_business_cost_per_conversion(self, obj):
        return obj.tiktok_business.cost_per_conversion

    get_tiktok_business_cost_per_conversion.short_description = "Cost Per Conversion"
    get_tiktok_business_cost_per_conversion.admin_order_field = (
        "tiktok_business__cost_per_conversion"
    )

    def get_crossroads_rpc(self, obj):
        return obj.crossroads.rpc

    get_crossroads_rpc.short_description = "Crossroads RPC"
    get_crossroads_rpc.admin_order_field = "crossroads__rpc"

    def get_crossroads_rpv(self, obj):
        return obj.crossroads.rpv

    get_crossroads_rpv.short_description = "Crossroads RPV"
    get_crossroads_rpv.admin_order_field = "crossroads__rpv"

    def get_crossroads_total_visitors(self, obj):
        return obj.crossroads.total_visitors

    get_crossroads_total_visitors.short_description = "Crossroads Total Visitors"
    get_crossroads_total_visitors.admin_order_field = "crossroads__total_visitors"

    def get_crossroads_filtered_visitors(self, obj):
        return obj.crossroads.filtered_visitors

    get_crossroads_filtered_visitors.short_description = "Crossroads Filtered Visitors"
    get_crossroads_filtered_visitors.admin_order_field = "crossroads__filtered_visitors"

    def get_crossroads_lander_visitors(self, obj):
        return obj.crossroads.lander_visitors

    get_crossroads_lander_visitors.short_description = "Crossroads Lander Visitors"
    get_crossroads_lander_visitors.admin_order_field = "crossroads__lander_visitors"

    def get_crossroads_lander_searches(self, obj):
        return obj.crossroads.lander_searches

    get_crossroads_lander_searches.short_description = "Crossroads Lander Searches"
    get_crossroads_lander_searches.admin_order_field = "crossroads__lander_searches"

    def get_crossroads_revenue_events(self, obj):
        return obj.crossroads.revenue_events

    get_crossroads_revenue_events.short_description = "Crossroads Revenue Events"
    get_crossroads_revenue_events.admin_order_field = "crossroads__revenue_events"


@admin.register(CrossroadsToTiktokBusinessIdentifiers)
class CrossroadsToTiktokBusinessIdentifiersAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(CrossroadsToTiktokBusinessIdentifiers)
