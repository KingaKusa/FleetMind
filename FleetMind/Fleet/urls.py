from django.urls import path
from .views import hello_users, hello_name, table, post_list, create_post, update_post, delete_post

urlpatterns = [
    path('hello/', hello_users),
    path('hello/<str:name>/', hello_name),
    path('table/', table),
    path('posts/', post_list, name='post_list'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/update/<int:post_id>', update_post, name='update_post'),
    path('posts/delete/<int:post_id>', delete_post, name='delete_post'),
]