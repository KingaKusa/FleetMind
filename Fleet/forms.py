"""
Plik forms.py – Definicja formularzy dla aplikacji FleetMind.
Zawiera formularze służące do tworzenia postów, rejestracji użytkownika oraz logowania.
"""

from django import forms                        # Import modułu formularzy w Django
from .models import Post                        # Import modelu Post (dla formularza tworzenia/edycji postów)
from django.contrib.auth.models import User       # Import modelu użytkownika
from django.contrib.auth.forms import AuthenticationForm  # Import wbudowanego formularza logowania


class PostForm(forms.ModelForm):
    """
    Formularz do tworzenia lub edycji postów.
    Używa modelu Post i umożliwia wprowadzenie tytułu, treści posta oraz dodatkowych pól:
      - dystans,
      - miejsce początkowe,
      - miejsce końcowe,
      - czas podróży,
      - pojazd.
    Korzysta z dedykowanych widgetów, aby nadać formularzowi styl (Bootstrap 'form-control')
    oraz pomocnicze placeholdery, które ułatwiają użytkownikowi wprowadzanie danych.
    """
    # Pole travel_time/czas podróży definiujemy jako DurationField z widgetem TimeInput
    # Format hh:mm:ss. Pole jest opcjonalne oraz posiada pomocniczy tekst.
    travel_time = forms.DurationField(
        widget=forms.TimeInput(format='%H:%M:%S', attrs={
            'class': 'form-control',
            'placeholder': 'hh:mm:ss'
        }),
        required=False,
        help_text="Wprowadź czas w formacie hh:mm:ss (np. 01:30:00)"
    )

    class Meta:
        model = Post
        # Definiujemy, które pola modelu mają być użyte w formularzu.
        # Dodaliśmy nowe pola: distance, start_location, end_location, travel_time, vehicle.
        fields = ["title", "content", "distance", "start_location", "end_location", "travel_time", "vehicle"]
        # Etykiety wyświetlane przy poszczególnych polach
        labels = {
            "title": "Tytuł posta",
            "content": "Treść posta",
            "distance": "Dystans (km)",
            "start_location": "Miejsce początkowe",
            "end_location": "Miejsce końcowe",
            "vehicle": "Pojazd"
        }
        # Widgety umożliwiają dostosowanie wyglądu pól formularza (np. dodanie klas CSS i placeholderów)
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Podaj tytuł"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Podaj treść posta",
                "rows": 5
            }),
            "distance": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Podaj dystans w km",
                "step": "any"
            }),
            "start_location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Podaj miejsce początkowe"
            }),
            "end_location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Podaj miejsce końcowe"
            }),
            "vehicle": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Podaj pojazd"
            }),
        }


class RegisterForm(forms.ModelForm):
    """
    Formularz rejestracji użytkownika.
    Pozwala wprowadzić nazwę użytkownika, adres e-mail oraz hasło (dwukrotnie).
    W procesie walidacji sprawdzamy:
      - czy użytkownik o podanej nazwie już nie istnieje,
      - czy e-mail nie jest już używany,
      - czy oba hasła są identyczne.
    """
    # Definiujemy pola niestandardowe, dzięki czemu możemy precyzyjnie ustalić widgety i etykiety
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
        # Formularz oparty jest o model wbudowanego użytkownika
        model = User
        # Określamy, które pola będą dostępne w formularzu
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        """
        Walidacja nazwy użytkownika.
        Sprawdza, czy nazwa użytkownika jest unikalna – jeżeli już istnieje, zwraca błąd walidacji.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nazwa użytkownika już istnieje. Wybierz inną.")
        return username

    def clean_email(self):
        """
        Walidacja adresu e-mail.
        Upewnia się, że dany adres e-mail nie jest już używany przez innego użytkownika.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik z tym adresem e-mail już istnieje.")
        return email

    def clean_password2(self):
        """
        Walidacja zgodności haseł.
        Porównuje wprowadzone hasła – jeżeli się różnią, zwraca błąd walidacji.
        """
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

