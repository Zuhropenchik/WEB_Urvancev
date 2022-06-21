from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import User, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 3:
            raise ValidationError("Password length must be > 3 characters")

        return data
