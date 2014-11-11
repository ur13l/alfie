# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_cliente', models.CharField(max_length=25, verbose_name=b'Nombre de usuario')),
                ('nombre', models.CharField(max_length=30)),
                ('ap_pat', models.CharField(max_length=30, verbose_name=b'Apellido Paterno')),
                ('ap_mat', models.CharField(max_length=30, verbose_name=b'Apellido Materno')),
                ('contrasena', models.CharField(max_length=32)),
                ('domicilio', models.CharField(max_length=60)),
                ('cp', models.CharField(max_length=8, verbose_name=b'Codigo Postal')),
                ('municipio', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=19)),
                ('telefono1', models.IntegerField(null=True, verbose_name=b'Telefono principal', blank=True)),
                ('telefono2', models.IntegerField(null=True, verbose_name=b'Telefono secundario', blank=True)),
                ('num_tarjeta', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['id_cliente'],
            },
            bases=(models.Model,),
        ),
    ]
