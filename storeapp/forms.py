from django import forms
from storeapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'num_units', )
        labels = {'num_units': 'Quantity'}