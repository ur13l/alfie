from django.db import models
from django.forms import ModelForm, PasswordInput
from datetime import datetime
from alfie.settings import MEDIA_URL
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Perfil(models.Model):
    SEXO=(('H', str('Hombre')),('M',str('Mujer')))
    user=models.OneToOneField(User)
    fecha_nacimiento=models.CharField(max_length=30,verbose_name='Fecha de nacimiento',blank=True,null=True)
    sexo=models.CharField(max_length=1,null=True,blank=True, choices=SEXO)
    domicilio= models.CharField(max_length=60,null=True)
    colonia= models.CharField(max_length=60,null=True)
    cp= models.CharField(max_length=8,verbose_name='Codigo Postal',null=True)
    municipio=models.CharField(max_length=30,verbose_name='Ciudad',null=True)
    estado= models.CharField(max_length=19,null=True)
    telefono1= models.CharField(max_length=20,verbose_name='Telefono',blank=True,null=True)
    telefono2= models.CharField(max_length=20,verbose_name='Telefono secundario',blank=True,null=True)
    num_tarjeta= models.IntegerField(blank=True,null=True)
    foto_perfil=models.ImageField(upload_to='media/')

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Perfil.objects.create(user=instance)

post_save.connect(create_user_profile,sender=User)


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
    class Meta:
        ordering=["talla"]


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
    cliente=models.ForeignKey(User)

    def __unicode__(self):
        return 'Carrito de %s'%(self.cliente)

class Venta(models.Model):
    usuario=models.ForeignKey(User)
    cantidad_total=models.FloatField()
    entrega=models.BooleanField()

    class Meta:
        ordering=['entrega']

class DetalleCarrito(models.Model):
    dproducto=models.ForeignKey(DetalleProducto)
    carrito=models.ForeignKey(Carrito)
    cantidad=models.IntegerField()
    precio=models.FloatField()

class DetalleVenta(models.Model):
    dproducto=models.ForeignKey(DetalleProducto)
    venta=models.ForeignKey(Venta)
    cantidad=models.IntegerField()
    precio=models.FloatField()
    descuento=models.FloatField(blank=True,null=True)
    class Meta:
        ordering=['venta']

class DireccionEnvio(models.Model):
    venta=models.ForeignKey(Venta,null=True,blank=True)
    domicilio= models.CharField(max_length=60,null=True)
    colonia= models.CharField(max_length=60,null=True)
    cp= models.CharField(max_length=8,verbose_name='Codigo Postal',null=True)
    municipio=models.CharField(max_length=30,verbose_name='Ciudad',null=True)
    estado= models.CharField(max_length=19,null=True)

class DireccionEnvioAdicional(models.Model):
    dir_envio=models.ForeignKey(DireccionEnvio,null=True,blank=True)
    domicilio2= models.CharField(max_length=60,null=True,blank=True,verbose_name='Domicilio')
    colonia2= models.CharField(max_length=60,null=True,verbose_name='Colonia',blank=True,)
    cp2= models.CharField(max_length=8,verbose_name='Codigo Postal',null=True,blank=True)
    municipio2=models.CharField(max_length=30,verbose_name='Ciudad',null=True,blank=True)
    estado2= models.CharField(max_length=19,null=True,verbose_name='Estado',blank=True)
