"""
Plik urls.py – Definicja tras URL dla aplikacji FleetMind.
Każda ścieżka związana jest z konkretnym widokiem, który odpowiada za obsługę żądania.
"""

from django.urls import path
# Importujemy widoki, które będą obsługiwać poszczególne ścieżki URL.
from .views import (
    hello_users,
    hello_name,
    post_list,
    create_post,
    update_post,
    delete_post,
    register,
    user_panel,
    CustomLoginView,
    user_posts,
    post_detail_json
)
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    # Ścieżka demonstracyjna: wyświetlanie listy użytkowników ("hello_users").
    path('hello/', hello_users, name='hello_users'),

    # Ścieżka powitalna z dynamicznie przekazywaną nazwą.
    # Dodano nazwę "hello_name" dla spójności (możesz usunąć, jeśli nie jest potrzebna).
    path('hello/<str:name>/', hello_name, name='hello_name'),

    # Rejestracja nowych użytkowników.
    path('register/', register, name='register'),

    # Logowanie – wykorzystanie klasy CustomLoginView, która korzysta z własnego szablonu logowania.
    path('login/', CustomLoginView.as_view(template_name='Fleet/Auth/login.html'), name='login'),

    # Wylogowanie – po wylogowaniu przekierowujemy użytkownika do strony logowania.
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Panel użytkownika – widok, w którym wyświetlane są dane aktualnie zalogowanego użytkownika oraz jego posty.
    path('user-panel/', user_panel, name='user_panel'),

    # Widok z listą postów zalogowanego użytkownika, z możliwością sortowania.
    path('user_posts/', user_posts, name='user_posts'),

    # Przykładowe, zakomentowane ścieżki – możesz je odkomentować, kiedy będą potrzebne.
    # path('table/', table, name='table'),

    # Widok listy wszystkich postów (z możliwością sortowania poprzez parametry GET).
    path('posts/', post_list, name='post_list'),

    # Widok do tworzenia nowego posta.
    path('posts/create/', create_post, name='create_post'),

    # Widok do edycji istniejącego posta.
    path('posts/update/<int:post_id>/', update_post, name='update_post'),

    # Widok do usuwania posta – operacja wykonywana (najczęściej przez AJAX) metodą DELETE.
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),

    # Widok zwracający szczegóły posta w formacie JSON – przydatny przy dynamicznych operacjach na poście.
    path('posts/detail/<int:post_id>/', post_detail_json, name='post_detail_json'),

    # Zakomentowana ścieżka do widoku "chat" – na przyszłość, kiedy chcesz ją wdrożyć.
    # path('chat/', chat, name='chat'),
]
