from django.forms import ModelForm
from .models import *

#Form para cadastro/edit dos dados do model Imovel
class ImoveisForm(ModelForm):
    class Meta:
        model = Imovel
        fields = '__all__'

#Form para cadastro/edit dos dados do model Cliente
class ClientesForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'email', 'telefone']