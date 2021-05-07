from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('home/', index, name="index"),
    path('login/', user_login, name="login"),
    path('login/submit', submit_login),
]