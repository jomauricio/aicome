from django.contrib import admin
from .models import Produto, Restaurante, Pedido, ItemPedido
from .forms import RestauranteForm, ProdutoForm, PedidoForm, ItemPedidoForm
# Register your models here.

class ProdutoAdminStackedInline(admin.StackedInline):
    model = Produto
    form = ProdutoForm
    search_fields = ['nome', 'restaurante__nome']
    extra = 1

class RestauranteAdmin(admin.ModelAdmin):
    model = Restaurante
    form = RestauranteForm
    list_display = ('nome', 'endereco', 'fone')
    search_fields = ['nome', 'endereco__raw', 'fone']
    inlines = [ProdutoAdminStackedInline]

class ItemPedidoAdminStackedInline(admin.StackedInline):
    model = ItemPedido
    form = ItemPedidoForm
    autocomplete_fields = ['produto']
    extra = 1
    readonly_fields=('valor_total',)

class PedidoAdmin(admin.ModelAdmin):
    model = Pedido
    form = PedidoForm
    list_display = ('cod', 'user', 'end_entrega', 'status', 'valor_total')
    search_fields = ['cod', 'end_entrega__raw ']
    list_filter = ['status']
    autocomplete_fields = ['user']
    readonly_fields=('valor_total',)
    inlines = [ItemPedidoAdminStackedInline]

class ProdutoAdminModelAdmin(admin.ModelAdmin):
    model = Produto
    form = ProdutoForm
    search_fields = ['nome', 'restaurante__nome']
    autocomplete_fields = ['restaurante']
    list_display = ('nome', 'restaurante', 'valor')
    list_filter = ['restaurante']

admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Produto, ProdutoAdminModelAdmin)