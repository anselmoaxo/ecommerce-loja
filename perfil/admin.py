from django.contrib import admin
from .models import Perfil, Endereco


class PerfilAdmin(admin.ModelAdmin):
    model = Perfil
    list_display = ["usuario", "cpf", "idade", "sexo", "telefone_celular"]
    search_fields = ["usuario"]


admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Endereco)

# Register your models here.
