from django.contrib import admin

from commons.admin import get_all_fieldnames
from regions.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(Region)
