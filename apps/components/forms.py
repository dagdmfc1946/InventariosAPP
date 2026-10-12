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


COMPONENT_LABELS = {
    'reference': 'Referencia interna', 'name': 'Nombre del componente',
    'value': 'Valor técnico', 'part_number': 'Número de parte del fabricante',
}
COMPONENT_HELP = {
    'reference': 'Tu código para identificarlo; debe ser único dentro de la categoría.',
    'name': 'Un nombre reconocible, por ejemplo Resistencia o Sensor de temperatura LM35.',
    'value': 'Dato técnico, por ejemplo 10 kΩ, 100 µF o 5 V. No es el precio; usa especificaciones para otros atributos.',
    'part_number': 'Código del fabricante, por ejemplo LM358N. Puedes dejarlo vacío si no lo conoces.',
    'location': 'Lugar donde lo guardas. Puedes asignarlo después desde la ficha.',
}


class ComponentEditForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ('category', 'reference', 'name', 'value', 'part_number', 'location', 'is_active')
        labels = COMPONENT_LABELS
        help_texts = COMPONENT_HELP


SpecificationFormSet = inlineformset_factory(
    Component, Specification, fields=('attribute', 'value', 'unit'), extra=1,
    can_delete=True, max_num=50, validate_max=True, absolute_max=60,
)


class ComponentQuickCreateForm(forms.ModelForm):
    initial_quantity = forms.IntegerField(label='Cantidad inicial', min_value=0, initial=0)
    minimum_quantity = forms.IntegerField(label='Mínimo de aviso', min_value=0, initial=0,
        help_text='El resumen avisa cuando el saldo es igual o inferior a este número. Con 0, avisa al agotarse.')
    maximum_quantity = forms.IntegerField(
        label='Máximo permitido', min_value=0, initial=0,
        help_text='Deja 0 si no necesitas un límite máximo.',
    )

    class Meta:
        model = Component
        fields = ['category', 'reference', 'name', 'value', 'part_number', 'location']
        labels = COMPONENT_LABELS
        help_texts = COMPONENT_HELP

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Selecciona una categoría'
        self.fields['location'].empty_label = 'Sin asignar — completar después'
        self.fields['value'].widget.attrs['placeholder'] = 'Ej.: 10 kΩ / 100 µF / 5 V'
        self.fields['part_number'].widget.attrs['placeholder'] = 'Ej.: LM358N'
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
