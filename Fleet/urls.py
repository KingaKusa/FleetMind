"""
Plik urls.py – Definicja tras URL dla aplikacji FleetMind.
Każda ścieżka URL jest powiązana z odpowiednim widokiem obsługującym żądania użytkownika.
Zostały podzielone widoki na osobne moduły (`auth_views.py`, `post_views.py`, `general_views.py`),
co ułatwia zarządzanie kodem.
"""

from django.urls import path
# Importujemy widoki z `views/__init__.py`, co upraszcza importy
from .views import *
from Fleet import views

from django.contrib.auth.views import LogoutView

# Definicja tras URL aplikacji FleetMind
urlpatterns = [
    # Strona startowa – dostępna zarówno pod `/` jak i `/home/`
    path('', home, name='home'),
    path('home/', home, name='home'),

    # Rejestracja nowych użytkowników
    path('register/', views.register, name='register'),

    # Logowanie – używamy `CustomLoginView`, które korzysta z własnego szablonu logowania
    path('login/', CustomLoginView.as_view(), name='login'),

    # Wylogowanie – po wylogowaniu użytkownik zostanie przekierowany na stronę logowania
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Panel użytkownika – wyświetla dane aktualnie zalogowanego użytkownika oraz jego posty
    path('user-panel/', user_panel, name='user_panel'),

    # Lista wszystkich postów – użytkownik może je sortować za pomocą parametrów GET
    path('posts/', post_list, name='post_list'),

    # Tworzenie nowego posta – użytkownik może dodać nowy wpis do systemu
    path('posts/create/', create_post, name='create_post'),

    # Edycja istniejącego posta – dostępne tylko dla autora wpisu
    path('posts/update/<int:post_id>/', update_post, name='update_post'),

    # Usuwanie posta – operacja wykonywana metodą DELETE (najczęściej przez AJAX)
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),

    # Szczegóły posta – zwraca dane w formacie JSON (np. dla dynamicznych operacji w frontendzie)
    path('posts/detail/<int:post_id>/', post_detail_json, name='post_detail_json'),
]

