from django import forms
from .models import Portfolio, CategorySubscription
from customer.models import Bid


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['image', 'github', 'introduction', 'education_or_courses', 'qualities', 'skills']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'custom-file-input'})
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['description']


class CategorySubscriptionForm(forms.ModelForm):
    class Meta:
        model = CategorySubscription
        fields = ['category']
