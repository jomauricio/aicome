
from django.urls import path

from .views import RestauranteDetailView, RestauranteListView, PedidoDetailView, PedidoListView

urlpatterns = [
    path('restaurantes/', RestauranteListView.as_view(),
         name='restaurante-listar'),
    path('pedidos/', PedidoListView.as_view(),
         name='pedido-listar'),
    path('restaurantes/<int:pk>/', RestauranteDetailView.as_view(),
         name='restaurante-detalhe'),
    path('pedidos/<str:pk>/', PedidoDetailView.as_view(),
         name='pedido-detalhe'),
]