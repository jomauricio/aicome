from address.models import AddressField
from django.conf import settings
from django.db import models
from django_extensions.db.fields import RandomCharField
# Create your models here.

class Restaurante(models.Model):

    nome = models.CharField('Nome', max_length=255)
    endereco = AddressField()
    fone = models.CharField('Telefone', max_length=15)

    def __str__(self):
        return self.nome

class Produto(models.Model):

    nome = models.CharField('Nome', max_length=255)
    descricao = models.CharField('Descrição', max_length=255)
    valor = models.DecimalField('Valor', max_digits=5, decimal_places=2)
    estoque = models.PositiveIntegerField('Estoque')
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, verbose_name='Restaurante')

    def __str__(self):
        return self.nome


class Pedido(models.Model):

    PEDIDO_STATUS = [
        ('Aberto', 'Aberto'),
        ('Recebido', 'Recebido'),
        ('Em preparo', 'Em preparo'),
        ('Saiu para entrega', 'Saiu para entrega'),
    ]

    cod = RandomCharField(length=6, include_alpha=False)
    end_entrega = AddressField()
    valor_total = models.DecimalField('Total', max_digits=5, decimal_places=2, null=True)
    status = models.CharField('Descrição', max_length=25, choices=PEDIDO_STATUS)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='Usuário')

    def __str__(self):
        return 'Pedido nº: %d - Status: %s' % (self.pk, self.status)

class ItemPedido(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, verbose_name='Pedido')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, verbose_name='Produto')
    quantidade = models.IntegerField('Quantidade')
    valor_total = models.DecimalField('Total', max_digits=5, decimal_places=2, null=True)
    obs = models.CharField('Observação', max_length=255)

    def __str__(self):
        return 'Item: %s - Quant.: %d' % (self.produto.nome, self.quantidade)
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Itens de Pedido'