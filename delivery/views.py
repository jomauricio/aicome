from django.views.generic import ListView, DetailView, DeleteView
from .models import Restaurante, Pedido, Produto, ItemPedido
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .serializers import RestauranteSerializer, ProdutoSerializer, PedidoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from django.http import Http404

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

# ViewSets define the view behavior.
class RestauranteViewSet(viewsets.ModelViewSet):
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_pedido_api(request, pk_restaurente, pk_produto):
    restaurante = get_object_or_404(Restaurante, pk=pk_restaurente)
    produto = get_object_or_404(Produto, pk=pk_produto)

    if 'pedido_cod' in request.session:

        pedido = get_object_or_404(Pedido, cod=request.session['pedido_cod'])

        if restaurante == pedido.itempedido_set.first().produto.restaurante:
            
            if ItemPedido.objects.filter(produto__pk=pk_produto):
                return Response("Produto ja adicionado no pedido!", status=status.HTTP_304_NOT_MODIFIED)
            else:
                item_pedido = ItemPedido(
                    pedido=pedido, produto=produto, quantidade=1)
                item_pedido.valor_total = item_pedido.cal_valor_total()
                item_pedido.save()
                pedido.valor_total = pedido.cal_valor_total()
                pedido.save()
                serializer = PedidoSerializer(instance=pedido)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Produto inexistente no restaurante!", status=status.HTTP_304_NOT_MODIFIED)
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
        serializer = PedidoSerializer(instance=pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# # @permission_classes([IsAuthenticated])
# def restaurante_list_create(request):
#     """
#     List all code restaurantes, or create a new restaurante.
#     """
#     if request.method == 'GET':
#         restaurantes = Restaurante.objects.all()
#         serializer = RestauranteSerializer(restaurantes, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = RestauranteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# # @permission_classes([IsAuthenticated])
# def restaurante_detail_update_delete(request, pk):
#     """
#     Retrieve, update or delete a code restaurante.
#     """
#     try:
#         restaurante = Restaurante.objects.get(pk=pk)
#     except Restaurante.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = RestauranteSerializer(restaurante)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = RestauranteSerializer(restaurante, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         restaurante.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class RestauranteListCreateAPIView(APIView):
#     """
#     List all restaurantes, or create a new restaurante.
#     """
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request, format=None):
#         restaurantes = Restaurante.objects.all()
#         serializer = RestauranteSerializer(restaurantes, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = RestauranteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RestauranteDetailUpdataDeleteAPIView(APIView):
#     """
#     Retrieve, update or delete a restaurante instance.
#     """
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return Restaurante.objects.get(pk=pk)
#         except Restaurante.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         restaurante = self.get_object(pk)
#         serializer = RestauranteSerializer(restaurante)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         restaurante = self.get_object(pk)
#         serializer = RestauranteSerializer(restaurante, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         restaurante = self.get_object(pk)
#         restaurante.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class RestauranteGenericListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Restaurante.objects.all()
#     serializer_class = RestauranteSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class RestauranteGenericRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Restaurante.objects.all()
#     serializer_class = RestauranteSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]