from django.contrib import admin

from metrics.generators import generate_forecast_metrics, generate_historical_metrics
from regions.forms import SelectRegionsActionForm

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


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
