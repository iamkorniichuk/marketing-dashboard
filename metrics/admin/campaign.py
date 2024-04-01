from django.contrib import admin

from metrics.models import (
    CampaignMetrics,
    ProxyCampaignMetrics,
)


@admin.register(CampaignMetrics)
class CampaignMetricsAdmin(admin.ModelAdmin):
    list_filter = ["crossroads_metrics__campaign__name"]
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
        return obj.tiktok_business_metrics.campaign.name

    get_tiktok_business_name.short_description = "Name"
    get_tiktok_business_name.admin_order_field = (
        "tiktok_business_metrics__campaign__name"
    )

    def get_tiktok_business_identifier(self, obj):
        return obj.tiktok_business_metrics.campaign.id

    get_tiktok_business_identifier.short_description = "Id"
    get_tiktok_business_identifier.admin_order_field = (
        "tiktok_business_metrics__campaign__id"
    )

    def get_crossroads_identifier(self, obj):
        return obj.crossroads_metrics.campaign.id

    get_crossroads_identifier.short_description = "CR Id"
    get_crossroads_identifier.admin_order_field = "crossroads_metrics__campaign__id"

    def get_tiktok_business_advertiser_id(self, obj):
        return obj.tiktok_business_metrics.campaign.advertiser.id

    get_tiktok_business_advertiser_id.short_description = "Advertiser Id"
    get_tiktok_business_advertiser_id.admin_order_field = (
        "tiktok_business_metrics__campaign__advertiser__id"
    )

    def get_tiktok_business_date(self, obj):
        return obj.tiktok_business_metrics.date

    get_tiktok_business_date.short_description = "Date"
    get_tiktok_business_date.admin_order_field = "tiktok_business_metrics__date"

    def get_crossroads_date(self, obj):
        return obj.crossroads_metrics.date

    get_crossroads_date.short_description = "CR Date"
    get_crossroads_date.admin_order_field = "crossroads_metrics__date"

    def get_tiktok_business_video_views_p25(self, obj):
        return obj.tiktok_business_metrics.video_views_p25

    get_tiktok_business_video_views_p25.short_description = "Video Views Per 25"
    get_tiktok_business_video_views_p25.admin_order_field = (
        "tiktok_business_metrics__video_views_p25"
    )

    def get_tiktok_business_video_views_p50(self, obj):
        return obj.tiktok_business_metrics.video_views_p50

    get_tiktok_business_video_views_p50.short_description = "Video Views Per 50"
    get_tiktok_business_video_views_p50.admin_order_field = (
        "tiktok_business_metrics__video_views_p50"
    )

    def get_tiktok_business_video_views_p75(self, obj):
        return obj.tiktok_business_metrics.video_views_p75

    get_tiktok_business_video_views_p75.short_description = "Video Views Per 75"
    get_tiktok_business_video_views_p75.admin_order_field = (
        "tiktok_business_metrics__video_views_p75"
    )

    def get_tiktok_business_video_views_p100(self, obj):
        return obj.tiktok_business_metrics.video_views_p100

    get_tiktok_business_video_views_p100.short_description = "Video Views Per 100"
    get_tiktok_business_video_views_p100.admin_order_field = (
        "tiktok_business_metrics__video_views_p100"
    )

    def get_tiktok_business_video_watched_2s(self, obj):
        return obj.tiktok_business_metrics.video_watched_2s

    get_tiktok_business_video_watched_2s.short_description = "Video Watched 2s"
    get_tiktok_business_video_watched_2s.admin_order_field = (
        "tiktok_business_metrics__video_watched_2s"
    )

    def get_tiktok_business_video_watched_6s(self, obj):
        return obj.tiktok_business_metrics.video_watched_6s

    get_tiktok_business_video_watched_6s.short_description = "Video Watched 6s"
    get_tiktok_business_video_watched_6s.admin_order_field = (
        "tiktok_business_metrics__video_watched_6s"
    )

    def get_tiktok_business_cpc(self, obj):
        return obj.tiktok_business_metrics.cpc

    get_tiktok_business_cpc.short_description = "CPC"
    get_tiktok_business_cpc.admin_order_field = "tiktok_business_metrics__cpc"

    def get_tiktok_business_ctr(self, obj):
        return obj.tiktok_business_metrics.ctr

    get_tiktok_business_ctr.short_description = "CTR"
    get_tiktok_business_ctr.admin_order_field = "tiktok_business_metrics__ctr"

    def get_tiktok_business_clicks(self, obj):
        return obj.tiktok_business_metrics.clicks

    get_tiktok_business_clicks.short_description = "Clicks"
    get_tiktok_business_clicks.admin_order_field = "tiktok_business_metrics__clicks"

    def get_tiktok_business_spend(self, obj):
        return obj.tiktok_business_metrics.spend

    get_tiktok_business_spend.short_description = "Spend"
    get_tiktok_business_spend.admin_order_field = "tiktok_business_metrics__spend"

    def get_crossroads_revenue(self, obj):
        return obj.crossroads_metrics.revenue

    get_crossroads_revenue.short_description = "CR Revenue"
    get_crossroads_revenue.admin_order_field = "crossroads_metrics__revenue"

    def get_tiktok_business_conversion(self, obj):
        return obj.tiktok_business_metrics.conversion

    get_tiktok_business_conversion.short_description = "Conversion"
    get_tiktok_business_conversion.admin_order_field = (
        "tiktok_business_metrics__conversion"
    )

    def get_tiktok_business_cost_per_conversion(self, obj):
        return obj.tiktok_business_metrics.cost_per_conversion

    get_tiktok_business_cost_per_conversion.short_description = "Cost Per Conversion"
    get_tiktok_business_cost_per_conversion.admin_order_field = (
        "tiktok_business_metrics__cost_per_conversion"
    )

    def get_crossroads_rpc(self, obj):
        return obj.crossroads_metrics.rpc

    get_crossroads_rpc.short_description = "CR RPC"
    get_crossroads_rpc.admin_order_field = "crossroads_metrics__rpc"

    def get_crossroads_rpv(self, obj):
        return obj.crossroads_metrics.rpv

    get_crossroads_rpv.short_description = "CR RPV"
    get_crossroads_rpv.admin_order_field = "crossroads_metrics__rpv"

    def get_crossroads_total_visitors(self, obj):
        return obj.crossroads_metrics.total_visitors

    get_crossroads_total_visitors.short_description = "CR Total Visitors"
    get_crossroads_total_visitors.admin_order_field = (
        "crossroads_metrics__total_visitors"
    )

    def get_crossroads_filtered_visitors(self, obj):
        return obj.crossroads_metrics.filtered_visitors

    get_crossroads_filtered_visitors.short_description = "CR Filtered Visitors"
    get_crossroads_filtered_visitors.admin_order_field = (
        "crossroads_metrics__filtered_visitors"
    )

    def get_crossroads_lander_visitors(self, obj):
        return obj.crossroads_metrics.lander_visitors

    get_crossroads_lander_visitors.short_description = "CR Lander Visitors"
    get_crossroads_lander_visitors.admin_order_field = (
        "crossroads_metrics__lander_visitors"
    )

    def get_crossroads_lander_searches(self, obj):
        return obj.crossroads_metrics.lander_searches

    get_crossroads_lander_searches.short_description = "CR Lander Searches"
    get_crossroads_lander_searches.admin_order_field = (
        "crossroads_metrics__lander_searches"
    )

    def get_crossroads_revenue_events(self, obj):
        return obj.crossroads_metrics.revenue_events

    get_crossroads_revenue_events.short_description = "CR Revenue Events"
    get_crossroads_revenue_events.admin_order_field = (
        "crossroads_metrics__revenue_events"
    )


@admin.register(ProxyCampaignMetrics)
class ProxyCampaignMetricsAdmin(admin.ModelAdmin):
    list_filter = ["crossroads_metrics__campaign__name"]
    list_display = [
        "get_tiktok_business_name",
        "get_tiktok_business_identifier",
        "get_crossroads_identifier",
        "get_tiktok_business_date",
        "get_crossroads_date",
        "get_crossroads_revenue",
        "get_tiktok_business_spend",
        "get_profit",
        "get_roi",
        "get_rpc",
        "get_cpa",
        "get_cpa_da",
        "get_hook_rate",
    ]

    def get_tiktok_business_name(self, obj):
        return obj.tiktok_business_metrics.campaign.name

    get_tiktok_business_name.short_description = "Name"
    get_tiktok_business_name.admin_order_field = (
        "tiktok_business_metrics__campaign__name"
    )

    def get_tiktok_business_identifier(self, obj):
        return obj.tiktok_business_metrics.campaign.id

    get_tiktok_business_identifier.short_description = "Id"
    get_tiktok_business_identifier.admin_order_field = (
        "tiktok_business_metrics__campaign__id"
    )

    def get_crossroads_identifier(self, obj):
        return obj.crossroads_metrics.campaign.id

    get_crossroads_identifier.short_description = "CR Id"
    get_crossroads_identifier.admin_order_field = "crossroads_metrics__campaign__id"

    def get_tiktok_business_date(self, obj):
        return obj.tiktok_business_metrics.date

    get_tiktok_business_date.short_description = "Date"
    get_tiktok_business_date.admin_order_field = "tiktok_business_metrics__date"

    def get_crossroads_date(self, obj):
        return obj.crossroads_metrics.date

    get_crossroads_date.short_description = "CR Date"
    get_crossroads_date.admin_order_field = "crossroads_metrics__date"

    def get_crossroads_revenue(self, obj):
        return obj.crossroads_metrics.revenue

    get_crossroads_revenue.short_description = "CR Revenue"
    get_crossroads_revenue.admin_order_field = "crossroads_metrics__revenue"

    def get_tiktok_business_spend(self, obj):
        return obj.tiktok_business_metrics.spend

    get_tiktok_business_spend.short_description = "Spend"
    get_tiktok_business_spend.admin_order_field = "tiktok_business_metrics__spend"

    def get_profit(self, obj):
        return obj.crossroads_metrics.revenue - obj.tiktok_business_metrics.spend

    get_profit.short_description = "Profit"

    def get_roi(self, obj):
        profit = obj.crossroads_metrics.revenue - obj.tiktok_business_metrics.spend
        return (
            safe_division(
                (profit - obj.tiktok_business_metrics.spend),
                obj.tiktok_business_metrics.spend,
            )
        ) * 100

    get_roi.short_description = "ROI"

    def get_rpc(self, obj):
        return safe_division(
            obj.crossroads_metrics.revenue, obj.tiktok_business_metrics.clicks
        )

    get_rpc.short_description = "RPC"

    def get_cpa(self, obj):
        return safe_division(
            obj.tiktok_business_metrics.spend, obj.tiktok_business_metrics.clicks
        )

    get_cpa.short_description = "CPA"

    def get_cpa_da(self, obj):
        return safe_division(
            obj.tiktok_business_metrics.spend, obj.crossroads_metrics.lander_visitors
        )

    get_cpa_da.short_description = "CPA DA"

    def get_hook_rate(self, obj):
        return (
            safe_division(
                obj.tiktok_business_metrics.video_views_p25,
                obj.tiktok_business_metrics.video_play_actions,
            )
            * 100
        )

    get_hook_rate.short_description = "Hook Rate"


def safe_division(number1, number2):
    try:
        return number1 / number2
    except ZeroDivisionError:
        return 0
