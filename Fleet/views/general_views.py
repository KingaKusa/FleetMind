"""
Plik general_views.py – zawiera widoki ogólne, np. stronę główną.
"""

from django.shortcuts import render

def home(request):
    """
    Widok strony startowej (HOME).
    Jeśli użytkownik jest zalogowany, może przejść do listy przejazdów.
    """
    return render(request, "Fleet/home.html")
