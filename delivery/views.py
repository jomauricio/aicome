from django.views.generic import ListView, DetailView, DeleteView
from .models import Restaurante, Pedido, Produto, ItemPedido
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

class RestauranteListView(ListView):
    model = Restaurante
    context_object_name = 'restaurantes'
    template_name = 'restaurante/listar.html'


class RestauranteDetailView(DetailView):
    model = Restaurante
    context_object_name = 'restaurante'
    template_name = 'restaurante/detalhe.html'

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/listar.html'

    def get_queryset(self):
        queryset = Pedido.objects.filter(user=self.request.user)
        return queryset


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'

@login_required
def add_item_pedido(request, pk_restaurente, pk_produto):
    restaurante = get_object_or_404(Restaurante, pk=pk_restaurente)
    produto = get_object_or_404(Produto, pk=pk_produto)

    if 'pedido_cod' in request.session:

        pedido = get_object_or_404(Pedido, cod=request.session['pedido_cod'])

        if restaurante == pedido.itempedido_set.first().produto.restaurante:
            
            if ItemPedido.objects.filter(produto__pk=pk_produto):
                messages.error(request, "Produto ja adicionado no pedido!")
                return redirect('restaurante-detalhe', pk=pk_restaurente)
            else:
                item_pedido = ItemPedido(
                    pedido=pedido, produto=produto, quantidade=1)
                item_pedido.valor_total = item_pedido.cal_valor_total()
                item_pedido.save()
                messages.success(request, "Item adicionado com sucesso!")
                pedido.valor_total = pedido.cal_valor_total()
                pedido.save()
                return redirect('pedido-detalhe', pk=pedido.pk)
        else:
            messages.error(request, "Produto inexistente no restaurante!")
            return redirect('restaurante-detalhe', pk=pk_restaurente)
    else:
        pedido = Pedido.objects.create(
            user=request.user, status=Pedido.PEDIDO_STATUS[0][0])
        request.session['pedido_cod'] = pedido.cod
        item_pedido = ItemPedido(
            pedido=pedido, produto=produto, quantidade=1)
        item_pedido.valor_total = item_pedido.cal_valor_total()
        item_pedido.save()
        pedido.valor_total = pedido.cal_valor_total()
        pedido.save()
        messages.success(request, "Item adicionado com sucesso!")
        return redirect('pedido-detalhe', pk=pedido.pk)

class PedidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pedido
    context_object_name = 'pedido'
    template_name_suffix = ''
    success_url = reverse_lazy('pedido-listar')
    template_name = 'pedido/delete.html'

    def post(self, *args, **kwargs):
        if 'pedido_cod' in self.request.session:
            del self.request.session['pedido_cod']
        return super(PedidoDeleteView, self).post(*args, **kwargs)

@login_required
def deletar_item_pedido(request, pk):
    item_pedido = get_object_or_404(ItemPedido, pk=pk)
    messages.success(request, 'Item de pedido removido!')
    pedido = item_pedido.pedido
    item_pedido.delete()
    pedido.valor_total = pedido.cal_valor_total()
    pedido.save()
    if not pedido.itempedido_set.all():
        return redirect('pedido-delete', pk=pedido.pk)
    else:
        return redirect('pedido-detalhe', pk=pedido.pk)