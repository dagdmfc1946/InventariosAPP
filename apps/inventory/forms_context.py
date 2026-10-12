from django import forms
from .models import Location


class LocationContextForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('shelf', 'box', 'drawer', 'description')
