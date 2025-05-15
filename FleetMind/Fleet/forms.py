from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {"title": "Tytuł posta", "content": "Treść posta"}
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Podaj tytuł"}),
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Podaj treść posta", "rows": 5}),
        }

class ChatForm(forms.Form):
    prompt = forms.CharField(label="Prompt")
    conversation_history = forms.CharField(required=False, widget=forms.HiddenInput())

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nazwa użytkownika"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="E-mail"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Hasło"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Potwierdź hasło"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Hasła muszą być identyczne!")
        return password2

class CustomLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Niepoprawny login lub hasło. Spróbuj ponownie.",
        "inactive": "Twoje konto jest nieaktywne.",
    }