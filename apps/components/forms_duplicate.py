from django import forms


class ComponentDuplicateForm(forms.Form):
    reference = forms.CharField(label='Nueva referencia', max_length=80)
    name = forms.CharField(label='Nombre del nuevo componente', max_length=200)
