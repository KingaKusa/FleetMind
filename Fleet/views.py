"""
Plik views.py – definiuje widoki (views) aplikacji FleetMind.
Każda funkcja lub klasa widoku odpowiada za pewien fragment logiki aplikacji,
np. wyświetlanie listy postów, tworzenie nowych, rejestrację użytkowników itp.
"""

import os

# Importy z Django – moduły odpowiedzialne za obsługę HTTP, renderowanie szablonów, przekierowania itp.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# Importy lokalne – formularze i modele z aplikacji
from .forms import PostForm, RegisterForm, CustomLoginForm
from .models import Post

# Import modelu Task z innej aplikacji – Fleet, jeśli potrzebujemy łączyć dane między aplikacjami.
from Fleet.models import Task

# Pobieramy informacje o środowisku (domyślnie byłoby 'dev' ale jest ustawiona zmienna ENV)
ENV = os.environ.get('ENV', 'dev')


@csrf_exempt  # UWAGA: wyłączenie ochrony CSRF – niezalecane w produkcji!
def hello_users(request):
    """
    Prosty widok demonstracyjny, który wyświetla:
    - listę zadań z bazy danych,
    - formularz umożliwiający dodanie nowego zadania,
    - komunikaty o statusie połączenia z bazą danych.

    Dla żądania POST tworzy nowe zadanie na podstawie przesłanych danych.
    """
    try:
        # Pobieramy wszystkie zadania z bazy danych
        tasks = Task.objects.all()
        # Tworzymy listę tekstową z identyfikatorem i tytułem zadania
        task_list = "<br>".join([f"{task.id}. {task.title}" for task in tasks])
        db_status = "Połączenie z bazą danych działa poprawnie!"
    except Exception as e:
        # W przypadku błędu przy pobieraniu danych
        task_list = ""
        db_status = f"Błąd bazy danych: {str(e)}"

    if request.method == 'POST':
        # Obsługa dodawania nowego zadania przy wysłaniu formularza
        try:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            if title:
                # Tworzymy nowe zadanie tylko, jeśli podany jest tytuł
                Task.objects.create(title=title, description=description)
                return redirect('hello_users')
        except Exception as e:
            # Rozszerzamy komunikat o możliwość błędu przy dodawaniu zadania
            db_status += f"<br>Błąd podczas dodawania zadania: {str(e)}"

    # Prosty formularz HTML do dodawania zadania – można rozważyć jego przeniesienie do szablonu
    form_html = """
        <form method="post">
          <div>
            <label for="title">Tytuł zadania:</label>
            <input type="text" id="title" name="title" required>
          </div>
          <div>
            <label for="description">Opis:</label>
            <textarea id="description" name="description"></textarea>
          </div>
          <button type="submit">Dodaj zadanie</button>
        </form>
        """

    # Składamy końcowy HTML przy użyciu f-stringa. W produkcji warto korzystać z szablonów.
    return HttpResponse(f"""
        <h1>Hello, World!</h1>
        <p>Środowisko: {ENV}</p>
        <p>Status bazy danych: {db_status}</p>
        <h2>Dodaj nowe zadanie:</h2>
        {form_html}
        <h2>Lista zadań:</h2>
        <p>{task_list if task_list else "Brak zadań"}</p>
        """)


def hello_name(request, name):
    """
    Widok wyświetlający stronę powitalną dedykowaną dla konkretnej osoby.
    Przekazuje do szablonu nazwę użytkownika.
    """
    return render(request, 'Fleet/hello_name.html', {'name': name})


@login_required
def post_list(request):
    """
    Widok listy postów.
    Umożliwia sortowanie postów poprzez parametry GET:
    - sort: pole, po którym sortujemy (domyślnie 'title')
    - direction: kierunek sortowania ('asc' dla rosnąco, 'desc' dla malejąco)
    """
    # Odczytujemy wartości sortowania z zapytania GET
    current_sort = request.GET.get('sort', 'title')
    current_direction = request.GET.get('direction', 'asc')

    # Ustalamy prefiks "-" dla malejącego sortowania, pusty dla rosnącego
    order_prefix = '' if current_direction == 'asc' else '-'
    order_by = order_prefix + current_sort

    # Pobieramy wszystkie posty posortowane według ustalonego kryterium
    posts = Post.objects.all().order_by(order_by)

    context = {
        'posts': posts,
        'current_sort': current_sort,
        'current_direction': current_direction,
    }
    return render(request, 'Fleet/post_list.html', context)


@login_required
def create_post(request):
    """
    Widok tworzenia nowego postu.
    Przy żądaniu GET wyświetla formularz, a przy POST zapisuje nowy post.
    Ustawia autora postu na aktualnie zalogowanego użytkownika.
    """
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Tworzymy obiekt postu, ale jeszcze go nie zapisujemy (commit=False)
        post = form.save(commit=False)
        # Ustawiamy autora postu na aktualnie zalogowanego użytkownika
        post.author = request.user
        post.save()
        return redirect("post_list")
    return render(request, "Fleet/post_form.html", {"form": form, "title": "Dodaj przejazd"})


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


def register(request):
    """
    Widok rejestracji użytkownika.
    Przy GET wyświetla formularz rejestracyjny, przy POST tworzy nowe konto
    i automatycznie loguje nowego użytkownika.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Tworzymy użytkownika, ustawiając wcześniej hasło (metoda set_password hashuje wartość)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = RegisterForm()
    return render(request, "Fleet/Auth/register.html", {"form": form})


class CustomLoginView(LoginView):
    """
    Widok logowania.
    Dziedziczy po wbudowanym widoku Django, używając własnego formularza logowania.
    """
    form_class = CustomLoginForm


@login_required
def user_panel(request):
    """
    Panel użytkownika – wyświetla aktualnego użytkownika oraz jego posty.
    """
    # Pobieramy posty, których autorem jest aktualnie zalogowany użytkownik
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

    # Upewniamy się, że pole sortowania jest dozwolone
    if sort_field not in valid_sort_fields:
        sort_field = 'create_at'

    # Ustawiamy kierunek sortowania; dla 'desc' dodajemy znak minus '-'
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
    Dostępny tylko dla autora postu (sprawdzenie poprzez get_object_or_404 z filtrem author=request.user).
    Zwraca dane niezbędne m.in. do dynamicznego edytowania czy usuwania postu przez JavaScript.
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)
    data = {
        "title": post.title,
        "content": post.content,
        "create_at": post.create_at.strftime("%Y-%m-%d %H:%M"),  # Formatowanie daty
        "distance": post.distance,
        "start_location": post.start_location,
        "end_location": post.end_location,
        "travel_time": str(post.travel_time) if post.travel_time else None,
        "vehicle": post.vehicle,
        # URL do edycji postu – dzięki funkcji reverse uzyskujemy adres URL po nazwie ścieżki
        "edit_url": reverse("update_post", args=[post.id]),
        # Identyfikator posta przydatny przy wywołaniu akcji usuwania za pomocą JavaScript
        "delete_id": post.id,
    }
    return JsonResponse(data)

# def get_api_key():
#     """Pobiera klucz API z pliku openai_key.txt"""
#     try:
#         with open('../openai_key.txt', 'r') as f:
#             return f.read().strip()
#     except FileNotFoundError:
#         print("Błąd: Plik openai_key.txt nie został znaleziony.")
#         return None
#     except Exception as e:
#         print(f"Błąd odczytu pliku z kluczem API: {str(e)}")
#         return None


# def chat(request):
#     preprompt = """Jesteś asystentem mojej witryny FleetMind. Służy do obsługi użytkowania pojazdów danego użytkownika. Masz za zadanie odpowiadać klientom na temat naszych produktów i usług.
# FIRMA ZAJMUJE SIĘ:
# 1. Tylko i wyłącznie sprzedaż programu: Fleet
# 2. Tylko i wyłącznie zajmujemy się: przechowywaniem danych wprowadzonych od użytkowników, przetwarzaniem ich na potrzeby użytkowników oraz analizą danych zebranych od użytkowników.
# 3. Niczym poza tym nie handlujemy i nie doradzamy
#
# DORADZAJ klientowi zakup TYLKO naszych produktów!
# NIE proponuj innych. Sprzedajemy tylko nasze.
#
# WAŻNE:
# 1. Jak klient zapyta o produkt innym niż nasz (nawet kuchenkę mikrofalową), zaproponuj, że potrezbuje do tego programu, który sprzedajemy.
# 2. Zachwalaj nasze usługi!
# 3. Na dzień dobry przedstaw naszą oefrtę, niezależnie co chce klient.
#
# OFERTA:
# 1. Rejestracja floty samochodowej.
# 2. Dodawanie danych o pojazdach - data zakupu, tankowania, podróże, drogi, eksploatacja, naprawy, wymiany,
# koszty powiązane, ilość przewożonych osób, rodzaj paliwa, rodzaj opon, pogoda na trasie.
# 3. Aplikacja oferuje analizę danych, wyciąganie wniosków, przedstawianie ich w formie graficznej, na przykład analiza
# kosztów przejazdu danej trasy z uwzględnieniem ceny paliwa oraz rodzaju opon czy obciążenia pojazdu.
#
#     Tu jest pierwsze pytanie klienta:
#     """
#     messages = []
#     api_key = get_api_key()
#     error_message = None
#     model = "gpt-3.5-turbo"
#     assistant_response = None
#     response = None
#
#     if not api_key:
#         error_message = "Błędna konfiguracja aplikacji. Skontaktuj się z administratorem."
#
#     form = ChatForm(request.POST or None)
#
#     if request.method == 'POST' and form.is_valid() and api_key:
#
#         try:
#             user_prompt = form.cleaned_data["prompt"]
#             history_json = form.cleaned_data.get("conversation_history") or "[]"
#             messages = json.loads(history_json)
#             if messages == []:
#                 messages.append({"role": "user", "content": preprompt})
#
#             client = OpenAI(api_key=api_key)
#             messages.append({"role": "user", "content": user_prompt})
#             response = client.chat.completions.create(
#                 model=model,
#                 messages=messages,
#                 temperature=0.7
#             )
#             assistant_response = response.choices[0].message.content
#             messages.append({"role": "assistant", "content": assistant_response})
#
#             form = ChatForm(initial={"conversation_history": json.dumps(messages)})
#
#         except Exception as e:
#             error_message = f"Wystąpił błąd: {str(e)}"
#
#     return render(request, "FleetMind/chat.html",
#                   {"form": form, "error_message": error_message,
#                    "assistant_response": assistant_response, "response": response, "messages": messages})