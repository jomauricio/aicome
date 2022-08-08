from django.views.generic import ListView, DetailView
from .models import Restaurante, Pedido
# Create your views here.

class RestauranteListView(ListView):
    model = Restaurante
    context_object_name = 'restaurantes'
    template_name = 'restaurante/listar.html'


class RestauranteDetailView(DetailView):
    model = Restaurante
    context_object_name = 'restaurante'
    template_name = 'restaurante/detalhe.html'

class PedidoListView(ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/listar.html'


class PedidoDetailView(DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
