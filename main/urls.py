# main/urls.py

from django.urls import path
from .views import login_view, sign_up_view, logout_view, main_page, clear_history

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', sign_up_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('', main_page, name='main_page'),
    path('clear-history/', clear_history, name='clear_history'),
]
