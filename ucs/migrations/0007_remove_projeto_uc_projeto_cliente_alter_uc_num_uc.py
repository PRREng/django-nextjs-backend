# Generated by Django 5.0.6 on 2024-07-15 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('ucs', '0006_alter_modulosolar_potencia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projeto',
            name='uc',
        ),
        migrations.AddField(
            model_name='projeto',
            name='cliente',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uc',
            name='num_UC',
            field=models.CharField(max_length=50),
        ),
    ]
