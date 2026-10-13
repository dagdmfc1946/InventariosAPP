from django import forms
from .models import Supplier, SupplierOffer


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'contact', 'phone', 'email', 'website', 'notes')
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}


class SupplierOfferForm(forms.ModelForm):
    class Meta:
        model = SupplierOffer
        fields = ('supplier', 'part_number', 'price', 'currency', 'minimum_quantity', 'url', 'date_consulted', 'notes')
        widgets = {'date_consulted': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   'notes': forms.Textarea(attrs={'rows': 3})}

    def clean_currency(self):
        return self.cleaned_data['currency'].strip().upper()
