
from django.urls import path
from .views import RestauranteDetailView, RestauranteListView, PedidoDetailView, PedidoListView, add_item_pedido, PedidoDeleteView, deletar_item_pedido

urlpatterns = [
    path('restaurantes/', RestauranteListView.as_view(),
         name='restaurante-listar'),
    path('pedidos/', PedidoListView.as_view(),
         name='pedido-listar'),
    path('restaurantes/<int:pk>/', RestauranteDetailView.as_view(),
         name='restaurante-detalhe'),
    path('pedidos/<str:pk>/', PedidoDetailView.as_view(),
         name='pedido-detalhe'),
     path('pedidos/add/<int:pk_restaurente>/<int:pk_produto>/', add_item_pedido, name='add-item-pedido'),
     path('pedidos/delete/<str:pk>/', PedidoDeleteView.as_view(), name='pedido-delete'),
     path('items/delete/<str:pk>/', deletar_item_pedido, name='item-delete'),
     
]