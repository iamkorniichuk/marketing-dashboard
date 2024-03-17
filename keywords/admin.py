from django.contrib import admin

from keywords.models import CrossroadsKeyword

from commons.admin import get_all_fieldnames


@admin.register(CrossroadsKeyword)
class CrossroadsKeywordAdmin(admin.ModelAdmin):
    list_display = get_all_fieldnames(CrossroadsKeyword)
