from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from . import models
from . import forms

# Importações necessárias para o funcionamento da aplicação Django


class BasePerfil(View):
    template_name = "criar.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        # Copia profunda do carrinho da sessão do usuário
        self.carrinho = copy.deepcopy(self.request.session.get("carrinho", {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            # Se o usuário estiver autenticado, tenta obter o perfil associado
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

        # Configuração dos formulários com base na autenticação do usuário
        if self.request.user.is_authenticated:
            self.contexto = {
                "userform": forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                "perfilform": forms.PerfilForm(
                    data=self.request.POST or None, instance=self.perfil
                ),
            }
        else:
            self.contexto = {
                "userform": forms.UserForm(data=self.request.POST or None),
                "perfilform": forms.PerfilForm(data=self.request.POST or None),
            }

        self.userform = self.contexto["userform"]
        self.perfilform = self.contexto["perfilform"]

        if self.request.user.is_authenticated:
            self.template_name = "atualizar.html"

        # Renderiza a página com base nas configurações
        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        # Retorna a página renderizada
        return self.renderizar


class CriarPerfil(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            # Se os formulários não forem válidos, exibe uma mensagem de erro
            messages.error(
                self.request,
                "Existem erros no formulário de cadastro. Verifique se todos "
                "os campos foram preenchidos corretamente.",
            )

            # Retorna a página com os erros
            return self.renderizar

        username = self.userform.cleaned_data.get("username")
        password = self.userform.cleaned_data.get("password")
        email = self.userform.cleaned_data.get("email")
        first_name = self.userform.cleaned_data.get("first_name")
        last_name = self.userform.cleaned_data.get("last_name")

        # Se o usuário já estiver logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                # Se o perfil não existe, cria um novo com os dados do formulário
                self.perfilform.cleaned_data["usuario"] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                # Se o perfil existe, atualiza-o com os novos dados
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # Se for um novo usuário (não autenticado)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            # Se uma senha foi fornecida, tenta autenticar o usuário
            autentica = authenticate(self.request, username=usuario, password=password)

            if autentica:
                # Se a autenticação for bem-sucedida, faz login no usuário
                login(self.request, user=usuario)

        self.request.session["carrinho"] = self.carrinho
        self.request.session.save()

        # Mensagens de sucesso
        messages.success(
            self.request, "Seu cadastro foi criado ou atualizado com sucesso."
        )

        messages.success(self.request, "Você fez login e pode concluir sua compra.")

        # Redireciona o usuário para a página de carrinho
        return redirect("produto:carrinho")


class AtualizarPerfil(View):
    def get(self, *args, **kwargs):
        # Retorna uma resposta "Atualizar", mas pode ser necessário implementar a lógica aqui
        return HttpResponse("Atualizar")


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get("carrinho"))

        # Realiza o logout do usuário
        logout(self.request)

        # Restaura o carrinho na sessão do usuário
        self.request.session["carrinho"] = carrinho
        self.request.session.save()

        # Redireciona o usuário para a lista de produtos
        return redirect("produto:lista")
