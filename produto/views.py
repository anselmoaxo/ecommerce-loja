from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

from .models import Produto


class ListaProduto(ListView):
    model = Produto
    template_name = "lista.html"
    context_object_name = "lista_produtos"
    paginate_by = 9


class DetalheProduto(DetailView):
    model = Produto
    template_name = "detalhe.html"
    context_object_name = "produto"
    slug_url_kwarg = "slug"


class AdicionarAoCarrinho(View):
    pass


class RemoverDoCarrinho(View):
    pass


class Carrinho(View):
    pass


class Finalizar(View):
    pass
