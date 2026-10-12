from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ApplicationUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(label='Perfil del inventario', choices=(('reader', 'Lector: consultar'), ('operator', 'Operador: registrar y editar')), initial='reader')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        labels = {'first_name': 'Nombre', 'last_name': 'Apellidos', 'email': 'Correo electrónico'}
