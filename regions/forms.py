from django import forms
from django.contrib.admin.helpers import ActionForm

from regions.models import Region


class SelectRegionsActionForm(ActionForm):
    regions = forms.ModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
    )
