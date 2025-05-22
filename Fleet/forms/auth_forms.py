"""
Plik auth_forms.py – zawiera formularze związane z autoryzacją użytkownika.
Obsługuje rejestrację oraz logowanie, wraz z walidacją danych użytkownika.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    """
    Formularz rejestracji użytkownika.
    Pozwala wprowadzić nazwę użytkownika, adres e-mail oraz hasło (dwukrotnie).
    Sprawdza, czy nazwa użytkownika i e-mail są unikalne oraz czy hasła są zgodne.
    """

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

    def clean_username(self):
        """ Sprawdza, czy nazwa użytkownika już istnieje. """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nazwa użytkownika już istnieje. Wybierz inną.")
        return username

    def clean_email(self):
        """ Sprawdza, czy adres e-mail jest unikalny. """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik z tym adresem e-mail już istnieje.")
        return email

    def clean_password2(self):
        """ Sprawdza, czy oba hasła są identyczne. """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Hasła muszą być identyczne!")
        return password2


class CustomLoginForm(AuthenticationForm):
    """
    Formularz logowania użytkownika.
    Rozszerza wbudowany formularz logowania Django, dostosowując komunikaty błędów.
    """
    error_messages = {
        "invalid_login": "Niepoprawny login lub hasło. Spróbuj ponownie.",
        "inactive": "Twoje konto jest nieaktywne.",
    }
