from django.urls import path
from .views import hello_users, hello_name, table, post_list, create_post, update_post, delete_post, register, \
    user_panel, CustomLoginView, user_posts, serve_image
# from .views import chat
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('hello/', hello_users, name='hello_users'),
    path('hello/<str:name>/', hello_name),
    path('table/', table, name='table'),
    path('posts/', post_list, name='post_list'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/update/<int:post_id>/', update_post, name='update_post'),
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),
    # path('chat/', chat, name='chat'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='Fleet/Auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('user-panel/', user_panel, name='user_panel'),
    path('user_posts/', user_posts, name='user_posts'),
    path('posts/image/<int:post_id>/', serve_image, name='serve_image')
]