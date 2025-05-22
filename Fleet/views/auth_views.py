"""
Plik auth_views.py – zawiera widoki związane z autoryzacją użytkownika.
Obsługuje logowanie, rejestrację oraz panel użytkownika.
"""

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from Fleet.forms import RegisterForm
from ..models import Profile  # Usunięto import Post, bo nie wyświetlamy już przejazdów


class CustomLoginView(LoginView):
    """
    Niestandardowy widok logowania użytkownika.
    Możesz tutaj dostosować wygląd strony logowania lub jego zachowanie.
    """
    template_name = "Fleet/Auth/login.html"
    redirect_authenticated_user = True
    success_url = "/posts/"  # Przekierowanie po zalogowaniu


def register(request):
    """
    Widok rejestracji użytkownika.
    Przy GET wyświetla formularz rejestracyjny, przy POST tworzy konto,
    dodaje Nick (`display_name`) i automatycznie loguje nowego użytkownika.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            # Sprawdzamy, czy użytkownik już ma profil
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.display_name = form.cleaned_data.get("display_name", "")
                profile.save()

            login(request, user)
            return redirect("post_list")
    else:
        form = RegisterForm()

    return render(request, "Fleet/Auth/register.html", {"form": form})


@login_required
def user_panel(request):
    """
    Panel użytkownika – wyświetla aktualnego użytkownika oraz pozwala na edycję jego danych.
    """

    # Pobieramy lub tworzymy profil użytkownika
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Obsługa formularza zmiany danych użytkownika
    if request.method == "POST":
        profile.display_name = request.POST.get("display_name", profile.display_name)
        request.user.email = request.POST.get("email", request.user.email)

        new_password = request.POST.get("password")
        if new_password:  # Jeśli wpisano nowe hasło, aktualizujemy je
            request.user.set_password(new_password)

        profile.save()
        request.user.save()

    # Przekazujemy dane do szablonu `user_panel.html`, wraz z odwołaniem do `_edit_user_modal.html`
    return render(request, "Fleet/Auth/user_panel.html", {"user": request.user, "profile": profile})
