# Generated by Django 4.2.6 on 2023-11-07 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_pedido_qtd_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='stauts',
            new_name='status',
        ),
    ]