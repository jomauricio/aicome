from delivery.models import Restaurante
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView

# from .forms simport SearchForm

# Create your views here.


class IndexView(ListView):
    template_name = 'base.html'
    context_object_name = 'restaurantes'
    model = Restaurante

    def get_queryset(self, **kwargs):

        if 'formatted_address' not in self.request.GET:
            return Restaurante.objects.all()
        elif self.request.GET.get('sublocality', ''):
            bairro = self.request.GET.get('sublocality')
            return Restaurante.objects.filter(endereco__locality__name=bairro)
        else:
            messages.error(
                self.request, 'Não foi possivel determinar sua localização!')
            return Restaurante.objects.all()

def index(request):
    if 'formatted_address' not in request.GET:
        q = Restaurante.objects.all()
    elif request.GET.get('sublocality', ''):
        bairro = request.GET.get('sublocality')
        q = Restaurante.objects.filter(endereco__locality__name=bairro)
    else:
        messages.error(
            request, 'Não foi possivel determinar sua localização!')
        q = Restaurante.objects.all()
    
    contexto = {'restaurantes': q}
    return render(request, 'base.html', contexto)