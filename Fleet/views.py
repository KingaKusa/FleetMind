import os
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, RegisterForm, CustomLoginForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post
# from .forms import ChatForm
# from openai import OpenAI

from Fleet.models import Task

ENV = os.environ.get('ENV', 'dev')

@csrf_exempt
def hello_users(request):
    try:
        tasks = Task.objects.all()
        task_list = "<br>".join([f"{task.id}. {task.title}" for task in tasks])
        db_status = "Połączenie z bazą danych działa poprawnie!"
    except Exception as e:
        task_list = ""
        db_status = f"Błąd bazy danych: {str(e)}"

    if request.method == 'POST':
        try:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            if title:
                Task.objects.create(title=title, description=description)
                return redirect('hello_users')
        except Exception as e:
            db_status += f"<br>Błąd podczas dodawania zadania: {str(e)}"

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
    return render (request, 'Fleet/hello_name.html', {'name': name})

def table(request):
    posts = []
    return render(request, 'Fleet/table.html', {'posts': posts})

@login_required
def post_list(request):
    current_sort = request.GET.get('sort', 'title')           # domyślnie sortuj po tytule
    current_direction = request.GET.get('direction', 'asc')   # domyślnie rosnąco

    order_prefix = '' if current_direction == 'asc' else '-'
    order_by = order_prefix + current_sort

    posts = Post.objects.all().order_by(order_by)

    context = {
        'posts': posts,
        'current_sort': current_sort,
        'current_direction': current_direction,
    }
    return render(request, 'Fleet/post_list.html', context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("post_list")
    return render(request, "Fleet/post_form.html", {"form": form, "title": "Dodaj przejazd"})


def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "Fleet/post_form.html",
                  {"form": form, "title": "Edytuj post"})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post usunięty"}, status=204)
    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)

def register(request):
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

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

@login_required
def user_panel(request):
    user_posts = Post.objects.filter(author=request.user)  # Pobieramy posty użytkownika
    return render(request, "Fleet/Auth/user_panel.html", {"user": request.user, "posts": user_posts})

@login_required
def user_posts(request):
    valid_sort_fields = ['title', 'content', 'create_at']
    sort_field = request.GET.get('sort', 'create_at')
    direction = request.GET.get('direction', 'asc')

    # zabezpieczenie: tylko dozwolone pola
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