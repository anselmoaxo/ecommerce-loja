from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

from django.core.validators import RegexValidator

from utils.validacpf import valida_cpf
import re


class Perfil(models.Model):
    SEXO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField(blank=True)
    telefone_celular = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Nº telefone celular",
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Número de telefone deve estar no formato internacional. Exemplo: +123456789",
            ),
        ],
    )
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)

    def __str__(self):
        return self.usuario.last_name

    """
    Função clean faz a validações dos campos CPF e CEP , 
    cpf utiliza a função Valida_cpf , CEP e validado pelo regex e
    caso for mais de 8 digitos.
    """

    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        # Pegando o primeiro cpf
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages["cpf"] = "CPF ja existe. !"

        if not valida_cpf(self.cpf):
            error_messages["cpf"] = "Digite um CPF valido"

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"


Tipo_endereco = (
    ("Padrão", "Padrão"),
    ("Entrega", "Entrega"),
)

UF = (
    ("AC", "Rio Branco"),
    ("AL", "Maceió"),
    ("AM", "Manaus"),
    ("AP", "Macapá"),
    ("BA", "Salvador"),
    ("CE", "Fortaleza"),
    ("DF", "Brasília"),
    ("ES", "Vitória"),
    ("GO", "Goiânia"),
    ("MA", "São Luís"),
    ("MG", "Belo Horizonte"),
    ("MS", "Campo Grande"),
    ("MT", "Cuiabá"),
    ("PA", "Belém"),
    ("PB", "João Pessoa"),
    ("PE", "Recife"),
    ("PI", "Teresina"),
    ("PR", "Curitiba"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Natal"),
    ("RO", "Porto Velho"),
    ("RR", "Boa Vista"),
    ("RS", "Porto Alegre"),
    ("SC", "Florianópolis"),
    ("SE", "Aracaju"),
    ("SP", "São Paulo"),
    ("TO", "Palmas"),
)


class Endereco(models.Model):
    tp_endereco = models.CharField(
        max_length=15, choices=Tipo_endereco, verbose_name="UF"
    )
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=100)
    complemento = models.CharField(max_length=250, blank=True)
    numero = models.PositiveIntegerField()
    bairro = models.CharField(max_length=250)
    municipio = models.CharField(max_length=250)
    uf = models.CharField(max_length=15, choices=UF, verbose_name="UF")
    usuario = models.ForeignKey(
        Perfil, related_name="endereco", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Logradouro  : {self.logradouro} municipio {self.municipio}"

    def clean(self):
        error_messages = {}

        if re.search(r"[^0-9]", self.cep) or len(self.cep) > 8:
            error_messages["cep"] = "CEP invalido !"

        if error_messages:
            raise ValidationError(error_messages)
