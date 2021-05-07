from django.urls import path, include
from .views import *

urlpatterns = [
    path('', imoveis, name="imoveis"),
    path('home/', imoveis, name="imoveis"),
    path('login/', user_login, name="login"),
    path('login/submit', submit_login),
]