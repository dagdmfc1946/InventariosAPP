from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget
from django.contrib.auth.hashers import is_password_usable


class ApplicationUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(label='Perfil del inventario', choices=(('reader', 'Lector: consultar'), ('operator', 'Operador: registrar y editar')), initial='reader')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}
        help_texts = {'username': 'Usa este nombre para iniciar sesión. Debe ser único; admite letras, números y @/./+/-/_.'}
        labels = {'username': 'Nombre de usuario', 'first_name': 'Nombre', 'last_name': 'Apellidos', 'email': 'Correo electrónico'}

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
        return username


class PasswordStatusWidget(ReadOnlyPasswordHashWidget):
    template_name = 'core/widgets/password_status.html'

    def get_context(self, name, value, attrs):
        context = forms.Widget.get_context(self, name, None, attrs)
        usable = bool(value) and is_password_usable(value)
        context['status'] = 'Contraseña configurada.' if usable else 'Sin contraseña para iniciar sesión.'
        context['button_label'] = 'Cambiar contraseña' if usable else 'Establecer contraseña'
        return context


class ApplicationUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label='Contraseña', widget=PasswordStatusWidget,
        help_text='Por seguridad, la contraseña actual no se puede consultar. Usa el botón para establecer una nueva.',
    )
