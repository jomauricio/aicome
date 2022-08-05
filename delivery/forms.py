from pyexpat import model
from django.forms import ModelForm
from .models import Restaurante, Produto, Pedido, ItemPedido

class RestauranteForm(ModelForm):
    model = Restaurante
    fields = '__all__'

class ProdutoForm(ModelForm):
    model = Produto
    fields = '__all__'

class PedidoForm(ModelForm):
    model = Pedido
    fields = '__all__'

class ItemPedidoForm(ModelForm):
    model = ItemPedido
    fields = '__all__'

