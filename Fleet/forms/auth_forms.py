"""
Plik auth_forms.py – zawiera formularze związane z autoryzacją użytkownika.
Obsługuje rejestrację, edycję danych użytkownika oraz logowanie, wraz z walidacją.
"""

from django import forms
from django.contrib.auth.models import User
from Fleet.models import Profile
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """
    Formularz logowania użytkownika.
    Rozszerza wbudowany formularz logowania Django, dostosowując komunikaty błędów.
    """
    error_messages = {
        "invalid_login": "Niepoprawny login lub hasło. Spróbuj ponownie.",
        "inactive": "Twoje konto jest nieaktywne.",
    }


class RegisterForm(forms.ModelForm):
    """
    Formularz rejestracji użytkownika.
    Pozwala wprowadzić nazwę użytkownika, adres e-mail oraz hasło (dwukrotnie).
    Sprawdza, czy nazwa użytkownika i e-mail są unikalne oraz czy hasła są zgodne.
    """

    username = forms.CharField(label="Nazwa użytkownika", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Potwierdź hasło", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    display_name = forms.CharField(label="Nick", required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean(self):
        """
        Globalna walidacja formularza:
        - Sprawdza, czy hasła są identyczne.
        - Sprawdza unikalność nazwy użytkownika i e-maila.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Hasła muszą być identyczne!")

        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error("username", "Nazwa użytkownika już istnieje. Wybierz inną.")

        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error("email", "Użytkownik z tym adresem e-mail już istnieje.")

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    """
    Formularz edycji danych użytkownika – zawiera tę samą walidację co `RegisterForm`.
    """
    display_name = forms.CharField(label="Nick", required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Adres e-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Nowe hasło", required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Powtórz nowe hasło", required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["email"]

    def clean(self):
        """
        Globalna walidacja formularza edycji:
        - Sprawdza, czy nowe hasła są identyczne.
        - Sprawdza unikalność Nicku.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:  # Jeśli jedno z pól hasła jest wypełnione
            if password1 != password2:
                self.add_error("password2", "Hasła muszą być identyczne!")

        display_name = cleaned_data.get("display_name")
        if display_name and Profile.objects.filter(display_name=display_name).exists():
            self.add_error("display_name", "Ten Nick jest już zajęty. Wybierz inny.")

        return cleaned_data
