from django import forms
from .models import Datasheet


class DatasheetUploadForm(forms.ModelForm):
    class Meta:
        model = Datasheet
        fields = ('file',)
        widgets = {'file': forms.ClearableFileInput(attrs={'accept': '.pdf,application/pdf'})}
