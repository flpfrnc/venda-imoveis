from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionBase
from django.db.models import Q, F
from .models import *
from .forms import *

#Funções auxiliares contidas em utils
from .utils import *

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
@csrf_protect
def submit_login(request):
    logged_user = auth_user_login(request)

    if logged_user is not None:
        request.session['user_id'] = logged_user.id
        login(request, logged_user)
        if logged_user.is_superuser:
            return redirect('/imoveis/')
        
        #Criação/Update de dados do corretor conforme o mesmo realiza login
        corretor = Corretor.objects.get_or_create(nome=logged_user.get_full_name() , defaults={'senha': logged_user.password})
        return redirect('/imoveis/')
    else:
        messages.error(request, "Usuario ou senha invalidos. Tente novamente")
    return redirect('/login/')


#Manage logout usuário
@login_required(login_url='/login/')
def user_logout(request):
    if request.method == "GET":
        if request.GET.get('logout') == 'logout':
            logout(request)
            return redirect('/login/')
        else:
            return redirect('/imoveis/')


@login_required(login_url='/login/')
def imoveis(request):
    #Variaveis para manage de dados do imovel
    identifier = "Imóvel"    
    form = ImoveisForm()
    imoveis = Imovel.objects.all()
    context = {'form': form, 'identifier': identifier, 'imoveis': imoveis}

    #Pesquisa de imoveis atraves do campo Search
    if 'srch' in request.GET:
        srch = request.GET.get('srch')
        if srch is not None:            
            imoveis = Imovel.objects.filter(Q(tipo__icontains=srch) | Q(localizacao__icontains=srch))
            if imoveis.exists():
                context['srch'] = srch
                context['imoveis'] = imoveis 
            else:
                imoveis = Imovel.objects.all()
            return render(request, 'pages/imoveis.html', context)

    if request.method == "POST":
        #Testa através dessa função se um request de cadastro/edit foi enviado 
        create_or_update_imovel(request)

        #Filtro de imoveis através do campo select/option
        select = request.POST.get('option')
        if select == "remover" or select is None:
            imoveis = Imovel.objects.all()
            return redirect("/imoveis/")
        else:
            imoveis = Imovel.objects.all().order_by(select)
            context['imoveis'] = imoveis
            context['select'] = select 
        return render(request, 'pages/imoveis.html', context)

    return render(request, 'pages/imoveis.html', context)


@login_required(login_url='/login/')
def clientes(request):
    #Variaveis para manage de dados do cliente
    identifier = "Cliente"
    form = ClientesForm()
    clientes = Cliente.objects.all()
    context = {'form': form, 'identifier': identifier, 'clientes': clientes}
    
    #Pesquisa de clientes atraves do campo Search
    srch = request.GET.get('srch')
    if srch is not None:
        clientes = Cliente.objects.filter(Q(nome__icontains=srch) | Q(email__icontains=srch))
        if clientes.exists():
            context['srch'] = srch
            context['clientes'] = clientes
        else:
            clientes = Cliente.objects.all()
        return render(request, 'pages/clientes.html', context)

    if request.method == "POST":
        #Testa através dessa função se um request de cadastro/edit foi enviado 
        create_or_update_cliente(request)   

        #Filtro de clientes através do campo select/option
        select = request.POST.get('option')
        if select == "remover" or select is None:
            clientes = Cliente.objects.all()
            return redirect("/clientes/")
        else:
            clientes = Cliente.objects.all().order_by(select)
            context['clientes'] = clientes
            context['select'] = select 
        return render(request, 'pages/clientes.html', context)     
        
    return render(request, 'pages/clientes.html', context)


@login_required(login_url='/login/')
def simulacao(request, pk):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes }

    if request.method == "POST":
        #Coleta os dados de imovel escolhido para simulação e seus valores
        imovel_simulacao = Imovel.objects.get(pk=pk)
        parcelas = (imovel_simulacao.valor.amount / 180)
        context['imovel_simulacao'] = imovel_simulacao
        context['parcelas'] = parcelas
        return render(request, 'pages/simulacao.html', context)

    return render(request, 'pages/simulacao.html', context)


@login_required(login_url='/login/')
def resumo(request, pk):
    if request.method == "POST":
        id_imovel = request.POST.get("id_imovel")
        pagamento = request.POST.get("formaPagamento")
        id_cliente = request.POST.get("cliente_compra")

        
        # Testa se um cliente foi escolhido para exibir o resumo 
        # de dados a serem enviados para o cadastro de venda
        if id_cliente is not None and id_cliente != '':
            imovel = Imovel.objects.get(pk=id_imovel)
            cliente = Cliente.objects.get(pk=id_cliente)
            parcelas = (imovel.valor.amount / 180)
            corretor = Corretor.objects.get(nome=request.user.get_full_name())
            context = {
                'imovel': imovel, 
                'cliente': cliente, 
                'pagamento': pagamento, 
                'parcelas': parcelas, 
                'corretor': corretor 
                }

            return render(request, 'pages/resumo.html', context)
        messages.info(request, 'Comprador não selecionado. Escolha o comprador na simulacao!')
        return redirect("/imoveis/")
    return render(request, 'pages/resumo.html')


@login_required(login_url='/login/')
def cadastro_venda(request):
    if request.method == "POST":
        #Instâncias para cadastro das FKs
        id_imovel = request.POST.get("id_imovel")
        instance_imovel = Imovel.objects.get(pk=id_imovel)        
        id_corretor = request.POST.get("vendedor_imovel")
        instance_corretoor = Corretor.objects.get(pk=id_corretor)

        #Dados restantes do model
        valor = request.POST.get("valor_imovel")        
        cliente = request.POST.get("cliente_imovel")       
        pagamento = request.POST.get("condicao_pagamento_imovel")
        
        #Verifica se venda já existe e cria uma nova caso não exista
        venda = Venda.get_or_create(imovel=imovel, valor=valor, corretor=corretor, cliente=cliente, condicao_pagamento=pagamento)
        return redirect("/imoveis/")


@login_required(login_url='/login/')
def delete_cliente(request, pk):
    if request.method == 'POST':
        cliente = Cliente.objects.get(pk=pk)
        cliente.delete()    
    return redirect('/clientes/')
    

@login_required(login_url='/login/')
def delete_imovel(request, pk):
    if request.method == 'POST':
        imovel = Imovel.objects.get(pk=pk)
        imovel.delete()
    return redirect('/imoveis/')