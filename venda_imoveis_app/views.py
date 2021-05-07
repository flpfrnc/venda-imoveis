from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionBase


#Tela de login de usuário
def user_login(request):
    session = request.session.session_key
    if session:
        return redirect('/home/')
    else:
        return render(request, 'pages/login.html')

#Autenticação de usuário e senha
def auth_user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        return user

#Manage de login para usuário autenticado
def submit_login(request):
    logged_user = auth_user_login(request)

    if logged_user is not None:
        request.session['user_id'] = logged_user.id
        login(request, logged_user)
        return redirect('/home/')
    else:
        messages.error(request, "Usuario ou senha invalidos. Tente novamente")
    return redirect('/login/')


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')