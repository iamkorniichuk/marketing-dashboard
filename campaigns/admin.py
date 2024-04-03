from django.contrib import admin

from campaigns.models import TiktokBusinessCampaign, CrossroadsCampaign
from commons.admin import get_all_fieldnames


@admin.register(TiktokBusinessCampaign)
class TiktokBusinessCampaignAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(TiktokBusinessCampaign)


@admin.register(CrossroadsCampaign)
class CrossroadsCampaignAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(CrossroadsCampaign)
