"""
Plik views.py – definiuje widoki aplikacji FleetMind.
Każda funkcja widoku odpowiada za obsługę różnych stron aplikacji.
"""

import os
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy

from .forms import PostForm, RegisterForm
from .models import Post

# Pobranie ustawienia środowiska
ENV = os.environ.get('ENV', 'dev')


def home(request):
    """
    Widok strony startowej (HOME).
    Jeśli użytkownik jest zalogowany, może przejść do listy przejazdów,
    w przeciwnym razie zachęcamy do logowania/rejestracji.
    """
    return render(request, "Fleet/home.html")


class CustomLoginView(LoginView):
    """
    Niestandardowy widok logowania użytkownika.
    Możesz tutaj dostosować wygląd strony logowania lub jej zachowanie.
    """
    template_name = "Fleet/Auth/login.html"  # Upewnij się, że ten plik istnieje
    redirect_authenticated_user = True
    success_url = reverse_lazy("post_list")  # Przekierowanie po zalogowaniu

@login_required
def post_list(request):
    """
    Widok listy przejazdów.
    - Użytkownik musi być zalogowany (`@login_required`).
    - Pobiera wszystkie posty z bazy danych.
    - Obsługuje sortowanie po różnych polach (tytuł, data, dystans).
    - Przekazuje dane do `post_list.html`.
    """
    sort_field = request.GET.get('sort', 'title')  # Domyślnie sortujemy po tytule
    direction = request.GET.get('direction', 'asc')  # Kierunek sortowania (asc/desc)

    order_prefix = '' if direction == 'asc' else '-'
    posts = Post.objects.all().order_by(order_prefix + sort_field)

    return render(request, 'Fleet/post_list.html', {
        'posts': posts,
        'current_sort': sort_field,
        'current_direction': direction,
    })


@login_required
def create_post(request):
    """
    Widok dodawania nowego przejazdu.
    - Pobiera dane z formularza.
    - Ustawia autora na zalogowanego użytkownika.
    - Zapisuje przejazd do bazy.
    """
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("post_list")
    return render(request, "Fleet/post_form.html", {"form": form, "title": "Dodaj przejazd"})


@login_required
def update_post(request, post_id):
    """
    Widok edycji postu.
    Pobiera istniejący post (lub zwraca błąd 404, jeśli post nie istnieje),
    wyświetla formularz z aktualnymi danymi, a przy poprawnym zatwierdzeniu zapisuje zmiany.
    """
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "Fleet/post_form.html", {"form": form, "title": "Edytuj post"})


@login_required
def delete_post(request, post_id):
    """
    Widok usuwania postu.
    Przyjmuje żądanie HTTP DELETE – jeśli metoda się zgadza, usuwa post,
    w przeciwnym wypadku zwraca komunikat o niedozwolonej metodzie.

    UWAGA: W przeglądarce może być konieczne wywoływanie tego widoku poprzez AJAX,
    gdyż standardowy formularz HTML nie obsługuje metody DELETE.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post usunięty"}, status=204)
    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)


@login_required
def register(request):
    """
    Widok rejestracji użytkownika.
    Przy GET wyświetla formularz rejestracyjny, przy POST tworzy nowe konto
    i automatycznie loguje nowego użytkownika.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = RegisterForm()
    return render(request, "Fleet/Auth/register.html", {"form": form})


@login_required
def user_panel(request):
    """
    Panel użytkownika – wyświetla aktualnego użytkownika oraz jego posty.
    """
    user_posts = Post.objects.filter(author=request.user)
    return render(request, "Fleet/Auth/user_panel.html", {"user": request.user, "posts": user_posts})


@login_required
def user_posts(request):
    """
    Widok listy postów zalogowanego użytkownika z możliwością sortowania.
    Dozwolone pola sortowania: 'title', 'content', 'create_at'.
    Jeśli w zapytaniu GET podano nieobsługiwane pole, domyślnie sortuje po 'create_at'.
    """
    valid_sort_fields = ['title', 'content', 'create_at']
    sort_field = request.GET.get('sort', 'create_at')
    direction = request.GET.get('direction', 'asc')

    if sort_field not in valid_sort_fields:
        sort_field = 'create_at'

    if direction == 'desc':
        sort_field = f'-{sort_field}'

    posts = Post.objects.filter(author=request.user).order_by(sort_field)

    return render(request, "Fleet/user_posts.html", {
        "posts": posts,
        "current_sort": request.GET.get('sort', 'create_at'),
        "current_direction": request.GET.get('direction', 'asc')
    })


@login_required
def post_detail_json(request, post_id):
    """
    Widok zwracający szczegóły postu w formacie JSON.
    Dostępny tylko dla autora postu.
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)
    data = {
        "title": post.title,
        "content": post.content,
        "create_at": post.create_at.strftime("%Y-%m-%d %H:%M"),
        "distance": post.distance,
        "start_location": post.start_location,
        "end_location": post.end_location,
        "travel_time": str(post.travel_time) if post.travel_time else None,
        "vehicle": post.vehicle,
        "edit_url": reverse("update_post", args=[post.id]),
        "delete_id": post.id,
    }
    return JsonResponse(data)
