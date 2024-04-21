from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from campaigns.models import (
    TiktokBusinessCampaign,
    CrossroadsCampaign,
    TiktokAdvertiser,
)
from commons.admin import get_all_fieldnames


@admin.register(TiktokAdvertiser)
class TiktokAdvertiserAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_region_name",
        "get_total_ads",
        "get_phone_number",
        "get_email",
        "get_social_media",
    ]

    def get_region_name(self, obj):
        if obj.region:
            return obj.region.name

    get_region_name.short_description = "Region"
    get_region_name.admin_order_field = "region__name"

    def get_total_ads(self, obj):
        if obj.total_ads:
            return f"{obj.total_ads:,}"

    get_total_ads.short_description = "Ads"
    get_total_ads.admin_order_field = "total_ads"

    def get_phone_number(self, obj):
        if obj.phone_number:
            return format_html(
                f'<a href="tel: {obj.phone_number}">{obj.phone_number}</a>'
            )

    get_phone_number.short_description = "Phone"
    get_phone_number.admin_order_field = "phone_number"

    def get_email(self, obj):
        if obj.email:
            return format_html(f'<a href="mailto: {obj.email}">{obj.email}</a>')

    get_email.short_description = "Email"
    get_email.admin_order_field = "email"

    def get_social_media(self, obj):
        data = {
            "facebook": obj.facebook,
            "youtube": obj.youtube,
            "linkedin": obj.linkedin,
        }
        social_media = [
            format_html(
                f'<a href="{value}" target="_blank" rel="noopener noreferrer">{name.capitalize()}</a>'
            )
            for name, value in data.items()
            if value
        ]
        return mark_safe(", ".join(social_media))

    get_social_media.short_description = "Social Media"


@admin.register(TiktokBusinessCampaign)
class TiktokBusinessCampaignAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(TiktokBusinessCampaign)


@admin.register(CrossroadsCampaign)
class CrossroadsCampaignAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(CrossroadsCampaign)
