from django.db import models
from djmoney.models.fields import MoneyField

class Corretor(models.Model):
    nome = models.CharField(max_length=255, default="")
    senha = models.CharField(max_length=255, default="")

    def __str__(self):
        return self

class Cliente(models.Model):
    nome = models.CharField(max_length=255, default="")
    cpf = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    telefone = models.CharField(max_length=255, default="")

    def __str__(self):
        return self
    
class Venda(models.Model):
    #Dúvida se imovel seria uma fk ou apenas um charfield com (Apartamento ou Lote)
    imovel = models.CharField(max_length=255, default="")
    valor = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    corretor = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    condicao_pagamento = models.CharField(max_length=255, default="")

    def __str__(self):
        return self