from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Login", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=50)

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


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="login", max_length=50)
    email = forms.EmailField(widget=forms.EmailInput, label="Email", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=50)
    password_repeat = forms.CharField(widget=forms.PasswordInput, label='Repeat password', max_length=50)

    avatar = forms.FileField(widget=forms.FileInput, label="Avatar", required=False)

    def clean_password(self):
        data = self.data['password']
        if len(data) < 6:
            raise ValidationError("Password should be more then 5 symbols.")
        return data

    def clean_username(self):
        data = self.data['username']
        if len(data) < 6:
            raise ValidationError("Username should be more then 5 symbols.")
        return data

    def clean_password_repeat(self):
        passwd_one = self.data['password']
        passwd_two = self.data['password_repeat']
        if passwd_one != passwd_two:
            raise ValidationError("Passwords do not match")
