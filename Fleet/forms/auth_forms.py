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

    def clean_display_name(self):
        """ Sprawdza, czy Nick jest unikalny. """
        display_name = self.cleaned_data.get("display_name")
        if display_name and Profile.objects.filter(display_name=display_name).exists():
            raise forms.ValidationError("Ten Nick jest już zajęty. Wybierz inny.")
        return display_name


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

    def clean_password2(self):
        """ Sprawdza, czy nowe hasła są identyczne, jeśli zostały podane. """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Hasła muszą być identyczne!")
        return password2

    def clean_display_name(self):
        """ Sprawdza, czy Nick jest unikalny. """
        display_name = self.cleaned_data.get("display_name")
        if display_name and Profile.objects.filter(display_name=display_name).exists():
            raise forms.ValidationError("Ten Nick jest już zajęty. Wybierz inny.")
        return display_name
