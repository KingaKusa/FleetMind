"""
Plik post_views.py – zawiera widoki do zarządzania postami użytkowników.
Obsługuje ich tworzenie, edycję, usuwanie i wyświetlanie szczegółów.
"""

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from ..models import Post
from Fleet.forms import PostForm

@login_required
def post_list(request):
    """
    Widok listy przejazdów.
    Pobiera wszystkie posty z bazy danych, obsługuje sortowanie.
    Dodany filtr sprawdzający czy post należy do zalogowanego użytkownika- by móc wejść w szczegóły posta
    """
    sort_field = request.GET.get('sort', 'title')
    direction = request.GET.get('direction', 'asc')

    order_prefix = '' if direction == 'asc' else '-'
    posts = Post.objects.all().order_by(order_prefix + sort_field)

    for post in posts:
        post.show_details = post.author == request.user

    return render(request, 'Fleet/post_list.html', {
        'posts': posts,
        'current_sort': sort_field,
        'current_direction': direction,
    })

@login_required
def create_post(request):
    """
    Widok dodawania nowego przejazdu.
    Pobiera dane z formularza, przypisuje autora i zapisuje post.
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
    Pobiera istniejący post, wyświetla formularz z aktualnymi danymi.
    """
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "Fleet/post_detail.html", {"post": post, "form": form})

@login_required
def delete_post(request, post_id):
    """
    Widok usuwania postu.
    Obsługuje żądanie HTTP DELETE – jeśli metoda się zgadza, usuwa post.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post usunięty"}, status=204)
    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)


@login_required
def post_detail_view(request, post_id):
    """
    Widok renderujący `post_detail.html`, aby poprawnie wyświetlić szczegóły posta.
    """
    post = get_object_or_404(Post, id=post_id)

    return render(request, "Fleet/post_detail.html", {"post": post})


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
