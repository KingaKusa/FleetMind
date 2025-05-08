import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, ChatForm

def hello_users(request):
    # return HttpResponse ('Hello world!')
    return render (request, 'Fleet/hello_users.html')

def hello_name(request, name):
    # return HttpResponse(f'Hello {name}!')
    return render (request, 'Fleet/hello_name.html', {'name': name})

def table(request):
    posts = [
        {"id": 1, "title": "Praca", "content": "Dom - Żmigrodzka - Dom", "create_at": "2025-04-01", "distance": "24"},
        {"id": 2, "title": "Siłownia", "content": "Dom - Fitstrefa - Dom", "create_at": "2025-04-01", "distance": "7"},
        {"id": 3, "title": "Praca", "content": "Dom - Żmigrodzka - Dom", "create_at": "2025-04-02", "distance": "24"},
        {"id": 4, "title": "Praca, zakupy", "content": "Dom - Żmigrodzka - Lidl - Dom", "create_at": "2025-04-03", "distance": "27"},
    ]

    return render(request, 'Fleet/table.html', {'posts': posts})

from .models import Post
def post_list(request):
    sort = request.GET.get('sort', 'id')
    posts = Post.objects.all().order_by(sort)
    return render(request, 'Fleet/table.html', {'posts': posts})

def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "Fleet/post_form.html",
                  {"form": form, "title": "Dodaj post"})

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(requst, "Fleet/post_form.html",
                  {"form": form, "title": "Edytuj post"})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post usunięty"}, status=204)
    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)