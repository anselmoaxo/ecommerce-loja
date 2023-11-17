from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view

app_name = "perfil"

urlpatterns = [
    path("", views.CriarPerfil.as_view(), name="criar"),
    path("endereco/", views.EnderecoCreate.as_view(), name="endereco"),
    path("atualizar/", views.AtualizarPerfil.as_view(), name="atualizar"),
    path(
        "login/",
        auth_view.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", views.Logout.as_view(), name="logout"),
]
