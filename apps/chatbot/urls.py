from django.urls import path, include
from .views import (
    chat, clear_history, home,
    user_login, user_logout
)


urlpatterns = [
    path('', view=home, name='home'),
    path('chat', view=chat, name='chat'),
    path('clear_history', view=clear_history, name='clear_history'),
    path('login', view=user_login, name='login'),
    path('logout', view=user_logout, name='logout'),
]
