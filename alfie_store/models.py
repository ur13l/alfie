from django.db import models
from django.forms import ModelForm, PasswordInput
from datetime import datetime
from alfie.settings import MEDIA_URL

class Usuario(models.Model):

	SEXO=(('H', str('Hombre')),('M',str('Mujer')))

	id_user=models.CharField(max_length=25,verbose_name='Nombre de usuario')
	nombre=models.CharField(max_length=30)
	apellido=models.CharField(max_length=30,verbose_name='Apellido')
	contrasena=models.CharField(max_length=32)
	fecha_nacimiento=models.CharField(max_length=30,verbose_name='Fecha de nacimiento')
	sexo=models.CharField(max_length=1,null=True,blank=True, choices=SEXO)
	domicilio=models.CharField(max_length=60)
	cp=models.CharField(max_length=8,verbose_name='Codigo Postal')
	municipio=models.CharField(max_length=30,verbose_name='Ciudad')
	estado=models.CharField(max_length=19)
	telefono1=models.CharField(max_length=20,verbose_name='Telefono',blank=True,null=True)
	telefono2=models.CharField(max_length=20,verbose_name='Telefono secundario',blank=True,null=True)
	num_tarjeta=models.IntegerField(blank=True,null=True)
	email=models.EmailField(verbose_name='Correo electronico')
	administrador=models.BooleanField(default=False);


	def __unicode__(self):
		return self.nombre + ' ' + self.apellido

	class Meta:
		ordering=["id_user"]

class Proveedor(models.Model):
	nombre=models.CharField(max_length=50)
	domicilio=models.CharField(max_length=60)
	cp=models.CharField(max_length=8,verbose_name='Codigo Postal')
	municipio=models.CharField(max_length=30)
	estado=models.CharField(max_length=19)
	telefono=models.IntegerField(blank=True,null=True)
	email=models.EmailField(blank=True,null=True,verbose_name='Correo electronico')
	website=models.URLField(blank=True,null=True)

class Promocion(models.Model):
	nombre=models.CharField(max_length=50)
	tipo=models.CharField(max_length=30)
	descuento=models.FloatField();


class Categoria(models.Model):
	nombre=models.CharField(max_length=40)

	def __unicode__(self):
		return self.nombre


class Subcategoria(models.Model):
	nombre=models.CharField(max_length=40)
	categoria=models.ForeignKey(Categoria)
	def __unicode__(self):
		return self.nombre + " | " + self.categoria.nombre

class Talla(models.Model):
	talla=models.FloatField()
	def __unicode__(self):
		return str(self.talla)

class Color(models.Model):
	nombre=models.CharField(max_length=40)
	def __unicode__(self):
		return self.nombre



class Producto(models.Model):
	SKU=models.CharField(max_length=50)
	nombre=models.CharField(max_length=100)
	modelo=models.CharField(max_length=15)
	precio_compra=models.FloatField(verbose_name='Precio de compra')
	precio_venta=models.FloatField(verbose_name='Precio de venta')
	descripcion=models.CharField(max_length=500,null=True,blank=True)
	subcategoria=models.ForeignKey(Subcategoria)
	foto_principal=models.ImageField(upload_to='media/')
	foto_frente=models.ImageField(upload_to="media/")
	foto_derecha=models.ImageField(upload_to='media/')
	foto_izquierda=models.ImageField(upload_to='media/')
	foto_trasera=models.ImageField(upload_to='media/')
	foto_suela=models.ImageField(upload_to='media/')
	talla=models.ManyToManyField(Talla)
	color=models.ManyToManyField(Color)
	promocion=models.ManyToManyField(Promocion, blank=True, null=True)
	proveedor=models.ManyToManyField(Proveedor)

	def __unicode__(self):
		return self.nombre


class DetalleProducto(models.Model):
	producto=models.ForeignKey(Producto)
	talla=models.ForeignKey(Talla)
	color=models.ForeignKey(Color)
	unidades=models.IntegerField()



class Carrito(models.Model):
	cliente=models.ForeignKey(Usuario)
	cantidad_total=models.FloatField()

class Venta(models.Model):
	cliente=models.ForeignKey(Usuario)
	cantidad_total=models.FloatField()



class DetalleCarrito(models.Model):
	producto=models.ForeignKey(Producto)
	carrito=models.ForeignKey(Carrito)
	cantidad=models.FloatField()
	descuento=models.FloatField()



class DetalleVenta(models.Model):
	producto=models.ForeignKey(Producto)
	carrito=models.ForeignKey(Venta)
	cantidad=models.FloatField()
	descuento=models.FloatField()







