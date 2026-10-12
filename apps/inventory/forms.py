from django import forms
from apps.components.models import Component
from .models import Location


class LocationForm(forms.ModelForm):
    components = forms.ModelMultipleChoiceField(
        label='Componentes en esta ubicación', queryset=Component.objects.all(), required=False,
        help_text='Puedes seleccionar varios. Los seleccionados se trasladarán aquí; los retirados quedarán sin ubicación.',
        widget=forms.SelectMultiple(attrs={'size': 8}),
    )

    class Meta:
        model = Location
        fields = ('shelf', 'box', 'drawer', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['components'].initial = self.instance.components.all()
