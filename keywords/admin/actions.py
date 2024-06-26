from django.contrib import admin

from keyword_metrics.generators import (
    generate_forecast_metrics,
    generate_historical_metrics,
    generate_keyword_competition,
)
from keywords.generators import (
    generate_similar_keywords,
    generate_marketing_type_choice,
)
from regions.forms import SelectRegionsActionForm


@admin.action(description="Request forecast metrics")
def request_forecast_metrics(modeladmin, request, queryset):
    form = SelectRegionsActionForm(request.POST)
    form.full_clean()
    generate_forecast_metrics(queryset, form.cleaned_data["regions"])


@admin.action(description="Request historical metrics")
def request_historical_metrics(modeladmin, request, queryset):
    form = SelectRegionsActionForm(request.POST)
    form.full_clean()
    generate_historical_metrics(queryset, form.cleaned_data["regions"])


@admin.action(description="Request competition metrics")
def request_competition_metrics(modeladmin, request, queryset):
    form = SelectRegionsActionForm(request.POST)
    form.full_clean()
    generate_keyword_competition(queryset, form.cleaned_data["regions"][0])


@admin.action(description="Request similar keywords")
def request_similar_keywords(modeladmin, request, queryset):
    form = SelectRegionsActionForm(request.POST)
    form.full_clean()
    generate_similar_keywords(
        queryset, form.cleaned_data["regions"], cpc_limit=form.cleaned_data["cpc_limit"]
    )


@admin.action(description="Request marketing type")
def request_marketing_type(modeladmin, request, queryset):
    generate_marketing_type_choice(queryset)
