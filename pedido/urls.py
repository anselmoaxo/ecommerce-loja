from django.urls import path
from . import views

app_name = "pedido"

urlpatterns = [
    path("pagar/<int:pk>", views.PagarPedido.as_view(), name="pagar"),
    path("salvarpedido", views.SalvarPedido.as_view(), name="salvarpedido"),
    path("listar", views.Lista.as_view(), name="listar"),
    path(
        "detalhar<int:pk>",
        views.DetalhePedido.as_view(),
        name="detalhar",
    ),
    path("pagamento", views.pagar_pix, name="pagamento"),
]
