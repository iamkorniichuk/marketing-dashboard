from django.contrib import admin
from commons.admin import get_all_fieldnames

from keywords.models import UserKeyword, ChatGptKeyword
from regions.forms import SelectRegionsActionForm

from .actions import (
    request_historical_metrics,
    request_forecast_metrics,
    request_competition_metrics,
    request_similar_keywords,
    request_marketing_type,
)


@admin.register(UserKeyword)
class UserKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text", "marketing"]
    list_display = get_all_fieldnames(UserKeyword)
    actions = [
        request_historical_metrics,
        request_forecast_metrics,
        request_competition_metrics,
        request_similar_keywords,
        request_marketing_type,
    ]
    action_form = SelectRegionsActionForm


@admin.register(ChatGptKeyword)
class ChatGptKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text", "marketing"]
    list_display = ["text", "marketing", "get_based_on_keywords"]
    actions = [
        request_historical_metrics,
        request_forecast_metrics,
        request_competition_metrics,
        request_similar_keywords,
        request_marketing_type,
    ]
    action_form = SelectRegionsActionForm

    def get_based_on_keywords(self, obj):
        keywords = obj.based_on.values_list("text", flat=True)
        return ", ".join(keywords)
