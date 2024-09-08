from django.contrib.auth.models import User
from django import forms
from .models import Hw


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # information about this class
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class HwForm(forms.ModelForm):

    class Meta:
        model = Hw
        fields = ['hw_title', 'hw_content', 'hw_object']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)