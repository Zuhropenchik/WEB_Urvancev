from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Login", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=64)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 3:
            raise ValidationError("Password should be more then 2 symbols.")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 3:
            raise ValidationError("Username should be more then 2 symbols.")
        return data

