"""
Plik models.py – Definicja modeli dla aplikacji FleetMind.
Zawiera definicję modelu Post, który reprezentuje wpisy użytkowników.
"""

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, blank=True, null=True)


class Post(models.Model):
    """
    Model Post reprezentuje wpis użytkownika.
    Zawiera informacje takie jak: tytuł, treść, data utworzenia,
    autor oraz dodatkowe dane związane z podróżą (np. dystans, lokalizacje, czas podróży, pojazd).
    """
    title = models.CharField(
        max_length=200,
        help_text="Tytuł posta (maks. 200 znaków)"
    )
    content = models.TextField(
        help_text="Treść posta"
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data i czas utworzenia posta (ustawiane automatycznie)"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Autor posta (odniesienie do modelu User)"
    )
    distance = models.FloatField(
        blank=True,
        null=True,
        help_text="Dystans (np. w kilometrach); pole opcjonalne"
    )
    start_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Punkt początkowy podróży; pole opcjonalne"
    )
    end_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Punkt końcowy podróży; pole opcjonalne"
    )
    travel_time = models.DurationField(
        blank=True,
        null=True,
        help_text="Czas podróży; pole opcjonalne"
    )
    vehicle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Informacja o pojeździe; pole opcjonalne"
    )

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu jako tytuł posta.
        """
        return self.title
