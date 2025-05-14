from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class':'form-control w-25 personalizado',
                    'placeholder': 'Ingrese el nombre del producto',
                    'style':'background: aquamarine'
                }
            )
        }