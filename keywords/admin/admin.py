from django.contrib import admin
from django import forms
from django.contrib.admin.helpers import ActionForm

from keywords.models import Keyword
from regions.models import Region

from .actions import request_historical_metrics, request_forecast_metrics


class RegionForm(ActionForm):
    x_field = forms.ModelChoiceField(queryset=Region.objects.all())


@admin.register(Keyword)
class GoogleAdsKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text"]
    list_display = ["text", "get_regions_names"]
    actions = [request_historical_metrics, request_forecast_metrics]
    action_form = RegionForm

    def get_regions_names(self, obj):
        regions_names = obj.regions.values_list("name", flat=True)
        return ", ".join(regions_names)

    get_regions_names.short_description = "Regions"
