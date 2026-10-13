import uuid
from django import forms
from django.core import signing
from .models import StockMovement


class MovementForm(forms.Form):
    movement_type = forms.ChoiceField(label='Tipo de movimiento', choices=StockMovement.MOVEMENT_TYPE_CHOICES)
    quantity = forms.IntegerField(label='Cantidad', min_value=-2147483647, max_value=2147483647,
        help_text='Entrada/salida: cantidad positiva. Ajuste: diferencia con signo, por ejemplo −2 o +3.')
    reason = forms.CharField(label='Motivo', max_length=200, widget=forms.Textarea(attrs={'rows': 2}))
    token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, component, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.component, self.user = component, user
        from .models import Stock
        self.balance = Stock.objects.filter(component=component).values_list('quantity', flat=True).first() or 0
        if not self.is_bound:
            self.initial['token'] = signing.dumps({'component': component.pk, 'user': user.pk,
                'balance': self.balance, 'request': str(uuid.uuid4())}, salt='stock-operation')

    def clean(self):
        data = super().clean()
        try:
            self.operation = signing.loads(data.get('token', ''), salt='stock-operation', max_age=3600)
            if self.operation['component'] != self.component.pk or self.operation['user'] != self.user.pk:
                raise signing.BadSignature
        except (signing.BadSignature, KeyError, TypeError):
            self.add_error(None, 'El formulario venció o no corresponde a esta sesión. Recarga la ficha.')
        kind, quantity = data.get('movement_type'), data.get('quantity')
        if quantity is not None:
            if quantity == 0 or (kind in (StockMovement.ENTRY, StockMovement.EXIT) and quantity < 0):
                self.add_error('quantity', 'Usa una cantidad positiva para entrada/salida y distinta de cero para ajuste.')
            self.expected_balance = self.balance + (-quantity if kind == StockMovement.EXIT else quantity)
            previous = StockMovement.objects.filter(request_id=self.operation['request']).exists() if hasattr(self, 'operation') else False
            if previous:
                self.expected_balance = self.balance
            if self.expected_balance < 0 and not previous:
                self.add_error('quantity', 'No hay suficientes existencias para este movimiento.')
            from .models import Stock
            maximum = Stock.objects.filter(component=self.component).values_list('maximum_quantity', flat=True).first()
            if maximum and self.expected_balance > maximum and not previous:
                self.add_error('quantity', 'El saldo previsto supera la cantidad máxima configurada.')
        return data
