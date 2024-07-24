from django import forms

from shop.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class SearchForm(forms.Form):
    search = forms.CharField(min_length=2, max_length=50, required=False, label='')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'phone', 'address']

