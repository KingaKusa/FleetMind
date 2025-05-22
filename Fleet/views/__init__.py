"""
Plik __init__.py – umożliwia traktowanie katalogu views jako modułu Pythona.
Dzięki temu możemy importować widoki z różnych plików w jednym miejscu.
"""

from .auth_views import CustomLoginView, register, user_panel
from .post_views import post_list, create_post, update_post, delete_post, post_detail_json
from .general_views import home
