from django.db import models
from djmoney.models.fields import MoneyField

class Imovel(models.Model):
    tipo = models.CharField(max_length=255, default="")
    localizacao = models.CharField(max_length=255, default="")
    valor = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    comissao_vendedor = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')


class Corretor(models.Model):
    nome = models.CharField(max_length=255, default="")
    senha = models.CharField(max_length=255, default="")


class Cliente(models.Model):
    nome = models.CharField(max_length=255, default="")
    cpf = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    telefone = models.CharField(max_length=255, default="")
    cadastro = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.nome
    

class Venda(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    valor = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=255, default="")
    condicao_pagamento = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.corretor.nome