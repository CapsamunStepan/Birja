from django import forms
from .models import Order, Comment


class OrderForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
        })
    )
    price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': "0",
            'min': 0,
        }))
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = Order
        fields = ['title', 'full_description', 'price', 'category', 'deadline']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
