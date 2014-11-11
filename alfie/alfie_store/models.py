from django.db import models
from django.forms import ModelForm, PasswordInput

class Cliente(models.Model):
	id_cliente=models.CharField(max_length=25,verbose_name='Nombre de usuario')
	nombre=models.CharField(max_length=30)
	ap_pat=models.CharField(max_length=30,verbose_name='Apellido Paterno')
	ap_mat=models.CharField(max_length=30,verbose_name='Apellido Materno')
	contrasena=models.CharField(max_length=32) 
	domicilio=models.CharField(max_length=60)
	cp=models.CharField(max_length=8,verbose_name='Codigo Postal')
	municipio=models.CharField(max_length=30)
	estado=models.CharField(max_length=19)
	telefono1=models.IntegerField(verbose_name='Telefono principal',blank=True,null=True)
	telefono2=models.IntegerField(verbose_name='Telefono secundario',blank=True,null=True)
	num_tarjeta=models.IntegerField(blank=True,null=True)
	email=models.EmailField(blank=True,null=True,verbose_name='Correo electronico')
	


	def __unicode__(self):
		return self.nombre + ' ' + self.ap_pat + ' ' + self.ap_mat

	class Meta:
		ordering=["id_cliente"]

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
	descuento=models.IntegerField();


class Producto(models.Model):
	SKU=models.CharField(max_length=50)
	nombre=models.CharField(max_length=100)
	precio_compra=models.FloatField(verbose_name='Precio de compra')
	precio_venta=models.FloatField(verbose_name='Precio de venta')
	descripcion=models.CharField(max_length=200,null=True,blank=True)
	categoria=models.CharField(max_length=30,null=True,blank=True)
	imagen=models.FileField()
	cantidad=models.IntegerField();
	talla=models.IntegerField(blank=True, null=True);
	color=models.CharField(max_length=30,blank=True, null=True)
	promocion=models.ManyToManyField(Promocion, blank=True, null=True)
	proveedor=models.ManyToManyField(Proveedor)


class Carrito(models.Model):
	cliente=models.ForeignKey(Cliente)
	cantidad_total=models.FloatField()

class Venta(models.Model):
	cliente=models.ForeignKey(Cliente)
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







