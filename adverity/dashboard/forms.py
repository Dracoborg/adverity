from django import forms

from adverity.dashboard.data.base import data


class FiltersForm(forms.Form):
    campaigns = forms.MultipleChoiceField(
        choices=[(name, name) for name in data.campaigns], required=False
    )
    datasources = forms.MultipleChoiceField(
        choices=[(name, name) for name in data.datasources], required=False
    )
