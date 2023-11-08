from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from perfil.models import Perfil
from django.db.models import Q

from .models import Produto, Variacao


class ListaProduto(ListView):
    model = Produto
    template_name = "lista.html"
    context_object_name = "lista_produtos"
    paginate_by = 9
    ordering = ["-id"]


class Busca(ListaProduto):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get("termo") or self.request.session["termo"]
        query = super().get_queryset(*args, **kwargs)

        if not termo:
            return query

        self.request.session["termo"] = termo

        query = query.filter(
            Q(nome__icontains=termo)
            | Q(descricao_curta__icontains=termo)
            | Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()
        return query


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
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ""
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ""

        if variacao.estoque < 1:
            messages.error(self.request, "Saldo Insuficiente")

        if not self.request.session.get("carrinho"):
            self.request.session["carrinho"] = {}
            self.request.session.save()

        carrinho = self.request.session["carrinho"]

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]["quantidade"]
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f"Saldo Insuficiente para {quantidade_carrinho}x"
                    f"no produto {produto_nome}.Adicionamos"
                    f"{variacao_estoque}x no seu carrinho.",
                )
                quantidade_carrinho = variacao_estoque
            carrinho[variacao_id]["quantidade"] = quantidade_carrinho
            carrinho[variacao_id]["preco_quantitativo"] = (
                preco_unitario * quantidade_carrinho
            )
            carrinho[variacao_id]["preco_quantitativo_promocional"] = (
                preco_unitario_promocional * quantidade_carrinho
            )

        else:
            carrinho[variacao_id] = {
                "produto_id": produto_id,
                "produto_nome": produto_nome,
                "variacao_nome": variacao.nome,
                "variacao_id": variacao_id,
                "preco_unitario": preco_unitario,
                "preco_unitario_promocional": preco_unitario_promocional,
                "preco_quantitativo": preco_unitario,
                "preco_quantitativo_promocional": preco_unitario_promocional,
                "quantidade": 1,
                "slug": slug,
                "imagem": imagem,
            }
        self.request.session.save()

        messages.success(
            self.request,
            f"Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho",
        )

        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get("HTTP_REFERER", reverse("produto:lista"))
        variacao_id = self.request.GET.get("vid")

        if not variacao_id:
            return redirect(http_referer)
        if not self.request.session.get("carrinho"):
            return redirect(http_referer)

        if variacao_id not in self.request.session["carrinho"]:
            return redirect(http_referer)

        carrinho = self.request.session["carrinho"][variacao_id]

        messages.success(
            self.request,
            f' {carrinho["produto_nome"]} ({carrinho["variacao_nome"]})'
            f" foi removido do seu carrinho.",
        )

        del self.request.session["carrinho"][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        context = {"carrinho": self.request.session.get("carrinho", {})}
        return render(self.request, "carrinho.html", context)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("perfil:criar")

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(self.request, "Usuário sem Perfil.")
            return redirect("perfil:criar")

        if not self.request.session.get("carrinho"):
            messages.error(self.request, "Carrinho Vazio.")
            return redirect("produto:lista")

        contexto = {
            "usuario": self.request.user,
            "carrinho": self.request.session["carrinho"],
        }

        return render(self.request, "resumodacompra.html", contexto)
