from django import forms

from .models import Category, Component, Specification
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class CategoryContextForm(forms.Form):
    name = forms.CharField(label='Nombre de la nueva categoría', max_length=120)
    description = forms.CharField(label='Descripción', required=False, widget=forms.Textarea(attrs={'rows': 2}))

    def clean(self):
        data = super().clean()
        if data.get('name'):
            slug = slugify(data['name'])
            if not slug:
                self.add_error('name', 'Incluye al menos una letra o número en el nombre.')
            else:
                self.category = Category(name=data['name'], slug=slug, description=data.get('description', ''))
                try:
                    self.category.full_clean()
                except ValidationError as error:
                    self.add_error('name', error.messages)
        return data


class ComponentEditForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ('category', 'reference', 'name', 'value', 'part_number', 'location', 'is_active')


SpecificationFormSet = inlineformset_factory(
    Component, Specification, fields=('attribute', 'value', 'unit'), extra=1,
    can_delete=True, max_num=50, validate_max=True, absolute_max=60,
)


class ComponentQuickCreateForm(forms.ModelForm):
    initial_quantity = forms.IntegerField(label='Cantidad inicial', min_value=0, initial=0)
    minimum_quantity = forms.IntegerField(label='Cantidad mínima', min_value=0, initial=0)
    maximum_quantity = forms.IntegerField(
        label='Cantidad máxima', min_value=0, initial=0,
        help_text='Deja 0 si no necesitas un límite máximo.',
    )

    class Meta:
        model = Component
        fields = ['category', 'reference', 'name', 'value', 'part_number', 'location']
        labels = {
            'category': 'Categoría', 'reference': 'Referencia', 'name': 'Nombre',
            'value': 'Valor', 'part_number': 'Número de parte',
        }
        help_texts = {'reference': 'Debe ser única dentro de la categoría.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Selecciona una categoría'
        for name, field in self.fields.items():
            field.widget.attrs['aria-describedby'] = f'id_{name}_help id_{name}_errors'

    def clean(self):
        cleaned = super().clean()
        maximum = cleaned.get('maximum_quantity')
        if maximum:
            if cleaned.get('initial_quantity', 0) > maximum:
                self.add_error('initial_quantity', 'La cantidad inicial no puede superar el máximo.')
            if cleaned.get('minimum_quantity', 0) > maximum:
                self.add_error('minimum_quantity', 'El mínimo no puede superar el máximo.')
        return cleaned
