from django.contrib import admin
from commons.admin import get_all_fieldnames

from keywords.models import Keyword
from regions.forms import SelectRegionsActionForm

from .actions import (
    request_historical_metrics,
    request_forecast_metrics,
    request_competition_metrics,
    request_similar_keywords,
)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    fields = ["text"]
    list_filter = ["text", "is_generated_by_chat_gpt"]
    list_display = get_all_fieldnames(Keyword)
    actions = [
        request_historical_metrics,
        request_forecast_metrics,
        request_competition_metrics,
        request_similar_keywords,
    ]
    action_form = SelectRegionsActionForm
