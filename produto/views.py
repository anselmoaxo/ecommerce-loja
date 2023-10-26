from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from .models import Produto, Variacao


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
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get("HTTP_REFERER", reverse("produto:lista"))
        variacao_id = self.request.GET.get("vid")

        if not variacao_id:
            messages.error(self.request, "Produto não existe.")
            return redirect(http_referer)
        variacao = get_object_or_404(Variacao, id=variacao_id)

        if not self.request.session.get("carrinho"):
            self.request.session["carrinho"] = {}
            self.request.session.save()

        carrinho = self.request.session["carrinho"]

        if variacao_id in carrinho:
            pass
        else:
            pass
        return HttpResponse(f"{variacao.produto} {variacao.nome}")


class RemoverDoCarrinho(View):
    pass


class Carrinho(View):
    pass


class Finalizar(View):
    pass
