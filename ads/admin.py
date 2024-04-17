from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg

from ads.models import TiktokAd


@admin.register(TiktokAd)
class TiktokAdAdmin(admin.ModelAdmin):
    list_filter = ["advertiser__name"]
    list_display = [
        "id",
        "get_url_tag",
        "get_advertiser_name",
        "get_advertiser_region",
        "get_advertiser_total_ads",
        "first_shown",
        "last_shown",
        "paid_for",
        "get_total_viewers",
        "get_ages",
        "get_genders",
        "get_viewers",
    ]

    def get_advertiser_name(self, obj):
        return obj.advertiser.name

    get_advertiser_name.short_description = "Adv"
    get_advertiser_name.admin_order_field = "advertiser__name"

    def get_advertiser_region(self, obj):
        region = obj.advertiser.region
        if region:
            return region.name

    get_advertiser_region.short_description = "Adv Region"
    get_advertiser_region.admin_order_field = "advertiser__region"

    def get_advertiser_total_ads(self, obj):
        total_ads = obj.advertiser.total_ads
        if total_ads:
            return f"{total_ads:,}"

    get_advertiser_total_ads.short_description = "Adv Total Ads"
    get_advertiser_total_ads.admin_order_field = "advertiser__total_ads"

    def get_total_viewers(self, obj):
        return f"{obj.total_viewers:,}"

    get_total_viewers.short_description = "Viewers"
    get_total_viewers.admin_order_field = "total_viewers"

    def get_url_tag(self, obj):
        return format_html(
            f'<a href="{obj.get_absolute_url()}" target="_blank" rel="noopener noreferrer">Link</a>'
        )

    get_url_tag.short_description = "URL"

    def get_ages(self, obj):
        data = obj.ages.all().aggregate(min_avg=Avg("min_age"), max_avg=Avg("max_age"))
        return f"{int(data['min_avg'])}-{int(data['max_avg'])}"

    get_ages.short_description = "Avg Age"

    def get_genders(self, obj):
        data = {
            "male": obj.genders.filter(is_male=True).exists(),
            "female": obj.genders.filter(is_female=True).exists(),
            "unknown": obj.genders.filter(is_unknown=True).exists(),
        }
        genders = [name.capitalize() for name, value in data.items() if value]
        return ", ".join(genders)

    get_genders.short_description = "Genders"

    def get_viewers(self, obj):
        count = obj.viewers.count()
        viewers = obj.viewers.values_list("unique_viewers", flat=True).order_by(
            "unique_viewers"
        )
        return f"{viewers[int(round(count/2))]:,}"

    get_viewers.short_description = "Median Viewers"
