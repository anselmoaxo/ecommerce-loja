from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path("", views.ListaProduto.as_view(), name="lista"),
    path("<slug>", views.DetalheProduto.as_view(), name="detalhe"),
    path(
        "adicionarcarrinho",
        views.AdicionarAoCarrinho.as_view(),
        name="adicionarcarrinho",
    ),
    path(
        "removerdocarrinho", views.RemoverDoCarrinho.as_view(), name="removerdocarrinho"
    ),
    path("carrinho", views.Carrinho.as_view(), name="lista"),
    path("finalizar", views.Finalizar.as_view(), name="finalizar"),
]
