# Generated by Django 4.2.6 on 2023-11-16 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cpf',
            field=models.CharField(max_length=11, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='idade',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tp_endereco', models.CharField(choices=[('Padrão', 'Padrão'), ('Entrega', 'Entrega')], max_length=15)),
                ('cep', models.CharField(max_length=8)),
                ('logradouro', models.CharField(max_length=100)),
                ('complemento', models.CharField(blank=True, max_length=250)),
                ('numero', models.PositiveIntegerField()),
                ('bairro', models.CharField(max_length=250)),
                ('municipio', models.CharField(max_length=250)),
                ('uf', models.CharField(choices=[('AC', 'Rio Branco'), ('AL', 'Maceió'), ('AM', 'Manaus'), ('AP', 'Macapá'), ('BA', 'Salvador'), ('CE', 'Fortaleza'), ('DF', 'Brasília'), ('ES', 'Vitória'), ('GO', 'Goiânia'), ('MA', 'São Luís'), ('MG', 'Belo Horizonte'), ('MS', 'Campo Grande'), ('MT', 'Cuiabá'), ('PA', 'Belém'), ('PB', 'João Pessoa'), ('PE', 'Recife'), ('PI', 'Teresina'), ('PR', 'Curitiba'), ('RJ', 'Rio de Janeiro'), ('RN', 'Natal'), ('RO', 'Porto Velho'), ('RR', 'Boa Vista'), ('RS', 'Porto Alegre'), ('SC', 'Florianópolis'), ('SE', 'Aracaju'), ('SP', 'São Paulo'), ('TO', 'Palmas')], max_length=15)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endereco', to='perfil.perfil')),
            ],
        ),
    ]