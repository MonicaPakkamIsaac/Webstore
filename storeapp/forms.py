from django import forms
from storeapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'num_units', )
        labels = {'num_units': 'Quantity'}


class InterestForm(forms.Form):
    interested = forms.IntegerField(widget=forms.RadioSelect(choices=[('1', 'Yes'), ('0', 'No')]), required=True, initial=1)
    comments = forms.CharField(widget=forms.Textarea(), label="Additional Comments", required=False)
