from django.contrib import admin

from campaigns.models import TiktokBusinessCampaign, CrossroadsCampaign, MergedCampaign


@admin.register(TiktokBusinessCampaign)
class TiktokBusinessCampaignAdmin(admin.ModelAdmin):
    pass


@admin.register(CrossroadsCampaign)
class CrossroadsCampaignAdmin(admin.ModelAdmin):
    pass


@admin.register(MergedCampaign)
class MergedCampaignAdmin(admin.ModelAdmin):
    pass
