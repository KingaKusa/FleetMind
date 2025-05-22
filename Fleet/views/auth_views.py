"""
Plik auth_views.py – zawiera widoki związane z autoryzacją użytkownika.
Obsługuje logowanie, rejestrację oraz panel użytkownika.
"""

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from Fleet.forms import RegisterForm
from ..models import Post  # Dwie krpki oznaczają import z katalogu wyżej (nadrzędnego)

class CustomLoginView(LoginView):
    """
    Niestandardowy widok logowania użytkownika.
    Możesz tutaj dostosować wygląd strony logowania lub jego zachowanie.
    """
    template_name = "Fleet/Auth/login.html"
    redirect_authenticated_user = True
    success_url = "/posts/"  # Przekierowanie po zalogowaniu

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
