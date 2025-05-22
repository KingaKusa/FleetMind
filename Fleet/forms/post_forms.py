"""
Plik post_forms.py – zawiera formularze do tworzenia i edycji postów.
Obsługuje pola dotyczące podróży, takie jak dystans, lokalizacje i czas podróży.
"""

from django import forms
from ..models import Post


class PostForm(forms.ModelForm):
    """
    Formularz do tworzenia lub edycji postów.
    Umożliwia wprowadzenie tytułu, treści oraz dodatkowych pól podróży.
    """

    # Pole czasu podróży (format hh:mm:ss) z odpowiednim widgetem
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
        fields = ["title", "content", "distance", "start_location", "end_location", "travel_time", "vehicle"]
        labels = {
            "title": "Tytuł posta",
            "content": "Treść posta",
            "distance": "Dystans (km)",
            "start_location": "Miejsce początkowe",
            "end_location": "Miejsce końcowe",
            "vehicle": "Pojazd"
        }
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
