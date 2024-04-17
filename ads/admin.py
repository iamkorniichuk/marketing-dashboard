from django.contrib import admin
from django.utils.html import format_html

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
        "total_viewers",
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
        return obj.advertiser.total_ads

    get_advertiser_total_ads.short_description = "Adv Total Ads"
    get_advertiser_total_ads.admin_order_field = "advertiser__total_ads"

    def get_url_tag(self, obj):
        return format_html(
            f'<a href="{obj.get_absolute_url()}" target="_blank" rel="noopener noreferrer">Link</a>'
        )

    get_url_tag.short_description = "URL"

    def get_ages(self, obj):
        results = []
        for age in obj.ages.all():
            results.append(f"{age.region.country_code}: {age.min_age}-{age.max_age}")
        return ", ".join(results)

    get_ages.short_description = "Ages"

    def get_genders(self, obj):
        results = []
        for gender in obj.genders.all():
            genders_code = []
            if gender.is_male:
                genders_code.append("M")
            if gender.is_female:
                genders_code.append("F")
            if gender.is_unknown:
                genders_code.append("U")
            results.append(f"{gender.region.country_code}: {''.join(genders_code)}")
        return ", ".join(results)

    get_genders.short_description = "Genders"

    def get_viewers(self, obj):
        results = []
        for viewer in obj.viewers.all():
            results.append(f"{viewer.region.country_code}: {viewer.unique_viewers}")
        return ", ".join(results)

    get_viewers.short_description = "Viewers"
