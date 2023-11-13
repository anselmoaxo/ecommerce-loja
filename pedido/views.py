from typing import Any
from django import http
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView

from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from produto.models import Variacao
from pedido.models import Pedido, ItemPedido
from utils import utils
from pixqrcodegen import Payload


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args: Any, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("perfil:criar")
        return super().dispatch(*args, **kwargs)


class PagarPedido(DispatchLoginRequiredMixin, DetailView):
    template_name = "pagar.html"
    model = Pedido
    pk_url_kwarg = "pk"
    context_object_name = "pedido"

    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(usuario=self.request.user)
        return query


class SalvarPedido(View):
    template_name = "pagar.html"

    def get(self, *args, **kwargs):
        # Se Usuário não estiver logado será direcionado a tela de Login/cadastro.
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Você precisa fazer Login.")
            return redirect("perfil:criar")
        # Carrinho de compras esteja vazio será direcionado para tela incial
        # com a mesnagem de erro
        if not self.request.session.get("carrinho"):
            messages.error(self.request, "Carrinho está vazio.")
            return redirect("produto:lista")

        carrinho = self.request.session.get("carrinho")
        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacao = list(
            Variacao.objects.select_related("produto").filter(
                id__in=carrinho_variacao_ids
            )
        )

        for variacao in bd_variacao:
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]["quantidade"]
            preco_unt = carrinho[vid]["preco_unitario"]
            preco_unt_promo = carrinho[vid]["preco_unitario_promocional"]
            produto = carrinho[vid]["produto_nome"]

        erro_msg_estoque = ""
        # Verificar quando o estoque estiver zerado.
        if estoque < qtd_carrinho:
            carrinho[vid]["quantidade"] = estoque
            carrinho[vid]["preco_quantitativo"] = estoque * preco_unt
            carrinho[vid]["preco_quantitativo_promocional"] = estoque * preco_unt_promo

            erro_msg_estoque = (
                "Estoque insuficiente para alguns produtos do seu carrinho."
                "Reduzimos a quantidade desses produtos .Pro favor , verifique"
                " quais produtos foram afetados a seguir."
            )
        if erro_msg_estoque:
            messages.error(self.request, erro_msg_estoque)

            self.request.session.save()
            return redirect("produto:carrinho")

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status="C",
        )
        pedido.save()
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v["produto_nome"],
                    produto_id=v["produto_id"],
                    variacao=v["variacao_nome"],
                    variacao_id=v["variacao_id"],
                    preco=v["preco_quantitativo"],
                    preco_promocional=v["preco_quantitativo_promocional"],
                    quantidade=v["quantidade"],
                    imagem=v["imagem"],
                )
                for v in carrinho.values()
            ]
        )

        del self.request.session["carrinho"]
        return redirect(reverse("pedido:pagar", kwargs={"pk": pedido.pk}))


class DetalhePedido(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = "pedido"
    template_name = "detalhar.html"
    pk_url_kwarg = "pk"


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = "pedidos"
    template_name = "listar.html"
    paginate_by = 10
    ordering = ["-id"]

    def get_queryset(self):
        # Obtém o usuário atualmente autenticado
        user = self.request.user

        # Filtra os pedidos do usuário atual
        queryset = Pedido.objects.filter(usuario=user)

        return queryset


def gerador_pix(nome, chave_pix, valor, cidade, txt_id):
    # Crie a payload PIX
    payload = Payload(
        nome=nome, chave=chave_pix, valor=valor, cidade=cidade, txid=txt_id
    )

    # Gere a Payload e retorne
    return payload.gerarPayload()


def pagar_pix(request):
    resultado = None
    pix = None

    if request.method == "POST":
        carrinho = request.session.get("carrinho", None)
        resultado = utils.cart_totals(carrinho)

        # Parâmetros para o gerador_pix
        nome = "Anselmo Xavier"
        chave_pix = "anselmo.cstecnologia@gmail.com"
        valor = "1.00"
        cidade = "Guarulhos"
        txt_id = "Ecommerce_AXO"

        # Chame a função gerador_pix
        pix = gerador_pix(nome, chave_pix, valor, cidade, txt_id)

    contexto = {
        "resultado": resultado,
        "pix": pix,
    }

    return render(request, "pagamento_pix.html", contexto)
