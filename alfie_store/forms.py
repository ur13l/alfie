# -*- coding:utf-8 -*-
from models import Usuario
from django import forms 
from datetime import datetime
from alfie_store import models 

class RegistroForm(forms.ModelForm):
	confirmar_contrasena = forms.CharField(max_length=45,widget=forms.PasswordInput())
	class Meta:
		
		model=Usuario
		fields=['nombre','apellido','id_user','contrasena','confirmar_contrasena','email','fecha_nacimiento', 'sexo','domicilio',
			'cp','municipio','estado','telefono1']
		widgets = {
			'contrasena': forms.PasswordInput(),
			'fecha_nacimiento': forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date','min':'01-01-1900','max':str(datetime.now),'placeholder':'dd-mm-aaaa'}),
			'telefono1':forms.TextInput(attrs={'placeholder':'Opcional'}),
			'email':forms.EmailInput(attrs={'placeholder':'ej. example@alfie.com'})
		}

	def clean_id_user(self):
		data=self.cleaned_data['id_user']
		try:
			u=models.Usuario.objects.get(id_user=data)
		except Usuario.DoesNotExist:
			return data
		raise forms.ValidationError("Usuario ya existe")

	def clean_contrasena(self):
		data=self.cleaned_data['contrasena']
		tamano=len(str(data))
		
		if tamano<8:
			raise forms.ValidationError("La contraseña debe ser mayor a ocho caracteres")

		return data

	def clean_confirmar_contrasena(self):
		cc=self.cleaned_data['confirmar_contrasena']
		try:
			c=self.cleaned_data['contrasena']

			if c!=cc:
				raise forms.ValidationError("Las contraseñas no coinciden")
		except KeyError:
			return cc


class ExistenciaForm(forms.Form):
	#CADA VARIABLE QUE CREES REPRESENTA UN CAMPO, NO TIENES QUE HACER EL HTML
	exis=forms.CharField(max_length=30,label='',widget=forms.widgets.TextInput(attrs={'placeholder':'Introduzca código o nombre del producto '}))

#	def clean_exis(self):
#		data=self.cleaned_data['exis']
#		try:
#			p=Producto.objects.get(SKU=data)
#		except Producto.DoesNotExist:
#			raise forms.ValidationError("Producto no encontrado")
#
#		return data
