# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alfie_store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_total', models.FloatField()),
                ('cliente', models.ForeignKey(to='alfie_store.Cliente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleCarrito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.FloatField()),
                ('descuento', models.FloatField()),
                ('carrito', models.ForeignKey(to='alfie_store.Carrito')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.FloatField()),
                ('descuento', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SKU', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=100)),
                ('precio_compra', models.FloatField(verbose_name=b'Precio de compra')),
                ('precio_venta', models.FloatField(verbose_name=b'Precio de venta')),
                ('imagen', models.FileField(upload_to=b'')),
                ('cantidad', models.IntegerField()),
                ('talla', models.IntegerField()),
                ('color', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=30)),
                ('descuento', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('domicilio', models.CharField(max_length=60)),
                ('cp', models.CharField(max_length=8, verbose_name=b'Codigo Postal')),
                ('municipio', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=19)),
                ('telefono', models.IntegerField(null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name=b'Correo electronico', blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_total', models.FloatField()),
                ('cliente', models.ForeignKey(to='alfie_store.Cliente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='producto',
            name='promocion',
            field=models.ManyToManyField(to='alfie_store.Promocion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ManyToManyField(to='alfie_store.Proveedor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='carrito',
            field=models.ForeignKey(to='alfie_store.Venta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='producto',
            field=models.ForeignKey(to='alfie_store.Producto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detallecarrito',
            name='producto',
            field=models.ForeignKey(to='alfie_store.Producto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=75, null=True, verbose_name=b'Correo electronico', blank=True),
            preserve_default=True,
        ),
    ]
