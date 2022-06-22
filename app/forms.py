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
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="login", max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group mb-3"}), label="Email", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Password',
                               max_length=50)
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}),
                                      label='Repeat password', max_length=50)

    avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Avatar", required=False)

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


class AskForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3",
                                                         "placeholder": "Specify one or more tags"}),
                           label="Tags")

    class Meta:
        model = Question
        fields = ("title", "text",)
        labels = {
            "title": "Header",
            "text": "Question wording",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-group mb-3", "placeholder": "Ask your question"}),
            "text": forms.Textarea(
                attrs={"class": "form-group mb-3", "placeholder": "Describe the problem in more details"})
        }

    def clean_tags(self):
        data = self.data['tags']
        if len(data) > 49:
            raise ValidationError("Tags should be less then 50 symbols.")
        return data

    def clean_title(self):
        data = self.data['title']
        if len(data) > 255:
            raise ValidationError("Title should be less then 256 symbols.")
        return data

    def clean_content(self):
        data = self.data['text']
        if len(data) > 999:
            raise ValidationError("Description should be less then 1000 symbols.")
        return data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            "content": forms.Textarea(
                attrs={'rows': 4, 'cols': 5, "class": "form-group mb-3", "placeholder": "Input your answer"})
        }

    def clean_text(self):
        data = self.data['content']
        if len(data) > 499:
            raise ValidationError("Description should be less then 500 symbols.")
        return data

    def save_fun(self, profile, question):
        ans = Answer.objects.create(author=profile, question=question, text=self.cleaned_data['content'])
        ans.save()
        return self
