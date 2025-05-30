"""
Plik auth_views.py – zawiera widoki związane z autoryzacją użytkownika.
Obsługuje logowanie, rejestrację oraz panel użytkownika.
"""

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from Fleet.forms import RegisterForm, UserUpdateForm
from ..models import Profile


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

            # ✅ Zawsze przypisujemy `display_name`, jeśli jest podany
            display_name = form.cleaned_data.get("display_name", "")
            if display_name:  # Sprawdzamy, czy użytkownik rzeczywiście podał nick
                profile.display_name = display_name
                profile.save()

            login(request, user)
            return redirect("post_list")
    else:
        form = RegisterForm()

    return render(request, "Fleet/Auth/register.html", {"form": form})


@login_required
def user_panel(request):
    """
    Panel użytkownika – pozwala edytować Nick, e-mail oraz hasło.
    Jeśli wystąpią błędy, modal pozostanie otwarty zamiast odświeżyć stronę.
    """

    profile, created = Profile.objects.get_or_create(user=request.user)
    form = UserUpdateForm(instance=request.user, initial={"display_name": profile.display_name})
    success_message = None  # Zmienna przechowująca komunikat o powodzeniu zmian

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user.email = form.cleaned_data["email"]
            profile.display_name = form.cleaned_data["display_name"]
            profile.save()

            new_password = form.cleaned_data.get("password1")
            if new_password:  # Sprawdzamy, czy nowe hasło zostało podane
                request.user.set_password(new_password)

            request.user.save()

            # Automatyczne ponowne zalogowanie po zmianie danych użytkownika
            login(request, request.user)

            success_message = "Dane zostały pomyślnie zmienione!"  # Komunikat o powodzeniu zmian

        # Jeśli są błędy, modal pozostanie otwarty, a użytkownik zobaczy komunikaty
        return render(request, "Fleet/Auth/user_panel.html", {"user": request.user, "profile": profile, "form": form, "success_message": success_message})

    return render(request, "Fleet/Auth/user_panel.html", {"user": request.user, "profile": profile, "form": form})
