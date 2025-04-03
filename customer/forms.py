from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "0",
            'min': 0,
        }))

    class Meta:
        model = Order
        fields = ['title', 'full_description', 'price', 'category', 'deadline']
