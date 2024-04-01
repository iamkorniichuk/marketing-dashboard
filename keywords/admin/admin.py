from django.contrib import admin

from keywords.models import Keyword
from regions.forms import SelectRegionsActionForm

from .actions import (
    request_historical_metrics,
    request_forecast_metrics,
    request_competition_metrics,
)


@admin.register(Keyword)
class GoogleAdsKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text"]
    list_display = ["text"]
    actions = [
        request_historical_metrics,
        request_forecast_metrics,
        request_competition_metrics,
    ]
    action_form = SelectRegionsActionForm
