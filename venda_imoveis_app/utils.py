from .models import *
from .views import *

def create_or_update_cliente(request):
    # Variaveis para manage de dados do cliente
    identifier = "Cliente"
    form = ClientesForm()
    clientes = Cliente.objects.all()
    context = {'form': form, 'identifier': identifier, 'clientes': clientes}

    # Checa se o formulário enviado é edit ou cadastro
    # para que o formulário de cadastro não dê update

    checkIsEdit = request.POST.get("check_edit")
    instance_id = request.POST.get("id_cliente")
    if checkIsEdit == "true":
        if instance_id:        
            try:
                instance = Cliente.objects.get(pk=instance_id)
                formFilled = ClientesForm(request.POST, instance=instance)
                if formFilled.is_valid():
                    formFilled.save()
                    return redirect("/clientes/")
                else:
                    context['form'] = formFilled
                    return context
            except Cliente.DoesNotExist:
                formFilled =ClientesForm(request.POST)
                if formFilled.is_valid():
                    formFilled.save()
                    return redirect("/clientes/")

    # Caso o formulário seja de cadastro, checa se existe algum 
    # cliente com o mesmo cpf e impede a criação caso exista   
    instance_cpf = request.POST.get("cpf")
    if instance_cpf:
        try:
            instance = Cliente.objects.get(cpf=instance_cpf)
            return redirect("/clientes/")
        except Cliente.DoesNotExist:
            formFilled =ClientesForm(request.POST)
            if formFilled.is_valid():
                formFilled.save()
                return redirect("/clientes/")


def create_or_update_imovel(request):
    #Objetos para manage de dados do imovel
    identifier = "Imóvel"    
    form = ImoveisForm()
    imoveis = Imovel.objects.all()
    context = {'form': form, 'identifier': identifier, 'imoveis': imoveis}

    # Checa se o formulário enviado é edit ou cadastro
    # para que o formulário de cadastro não dê update
    checkIsEdit = request.POST.get("check_edit")
    instance_id = request.POST.get("id_imovel")
    if checkIsEdit == "true":
        if instance_id:        
            try:
                instance = Imovel.objects.get(pk=instance_id)
                formFilled = ImoveisForm(request.POST, instance=instance)
                if formFilled.is_valid():
                    formFilled.save()
                    return redirect("/imoveis/")
                else:
                    context['form'] = formFilled
                    return context
            except Imovel.DoesNotExist:
                formFilled =ImoveisForm(request.POST)
                if formFilled.is_valid():
                    formFilled.save()
                    context['form'] = form
                    return redirect("/imoveis/")
    
    # Caso o formulário seja de cadastro, checa se existe um imovel
    # com exatamente a mesma localização e impede a criação caso exista
    instance_localizacao = request.POST.get("localizacao")
    if instance_localizacao:
        try:
            instance = Imovel.objects.get(localizacao=instance_localizacao)
            return redirect("/imoveis/")
        except Imovel.DoesNotExist:
            formFilled = ImoveisForm(request.POST)
            if formFilled.is_valid():
                formFilled.save()
                context['form'] = form
                return redirect("/imoveis/")
    