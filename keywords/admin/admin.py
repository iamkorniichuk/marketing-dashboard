from django.contrib import admin

from keywords.models import UserKeyword, ChatGptKeyword
from regions.forms import SelectRegionsActionForm

from .actions import (
    request_historical_metrics,
    request_forecast_metrics,
    request_competition_metrics,
    request_similar_keywords,
)


@admin.register(UserKeyword)
class UserKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text"]
    list_display = ["text"]
    actions = [
        request_historical_metrics,
        request_forecast_metrics,
        request_competition_metrics,
        request_similar_keywords,
    ]
    action_form = SelectRegionsActionForm


@admin.register(ChatGptKeyword)
class ChatGptKeywordAdmin(admin.ModelAdmin):
    list_filter = ["text"]
    list_display = ["text", "get_based_on_keywords"]

    def get_based_on_keywords(self, obj):
        keywords = obj.based_on.values_list("text", flat=True)
        return ", ".join(keywords)
