from django import forms
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        # widget=forms.TextInput(attrs={
        #     'autocomplete': 'off',
        # })
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
        })
    )
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password dont\'t match')
        return cd['password2']
