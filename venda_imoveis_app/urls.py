from django.urls import path, include
from .views import *

urlpatterns = [
    path('', imoveis, name="imoveis"),
    path('login/', user_login, name="login"),
    path('login/submit', submit_login),
    path('imoveis/', imoveis, name="imoveis"),
    path('imoveis/<int:pk>', delete_imovel, name="delete_imovel"),
    path('clientes/', clientes, name="clientes"),    
    path('clientes/<int:pk>', delete_cliente, name="delete_cliente"),
    path('simulacao/', simulacao, name="simulacao"),
    path('simulacao/imovel/<int:pk>', simulacao, name="simulacao"),
    path('resumo/', resumo, name="resumo"),    
    path('resumo/<int:pk>', resumo, name="resumo"),    
    path('cadastro/', cadastro_venda, name="cadastro_venda"),    
    path('logout/', user_logout, name='logout'),
    path('login/submit', submit_login),
]