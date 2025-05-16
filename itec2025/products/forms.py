from django import forms

from products.models import (
    Customer, 
    Order, 
    OrderDetail,
    Product,
)


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


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone"]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class':'form-control w-25 personalizado',
                    'placeholder': 'Ingrese el nombre del Cliente',
                }
            ),
            'email': forms.EmailInput(),
            'phone': forms.TextInput()
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']

        widgets = {
            'customer': forms.Select(
                attrs={'class': 'form-control'}
            )
        }

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'quantity']

        widgets = {
            'order': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'product': forms.Select(
                attrs={'class': 'form-control'}
            )
        }