# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django import forms 
from datetime import datetime
from django.core.context_processors import request
from alfie_store import models 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
import datetime


class RegistroForm(UserCreationForm):
    SEXO=(('H', str('Hombre')),('M',str('Mujer')))
    nombre=forms.CharField(max_length=30)
    apellido=forms.CharField(max_length=30)
    email=forms.EmailField()
    fecha_nacimiento=forms.CharField(widget=forms.DateInput(attrs={'placeholder':'mm/dd/aaaa'}))
    sexo=forms.ChoiceField(choices=SEXO)
    domicilio= forms.CharField(max_length=60)
    cp= forms.CharField(max_length=8)
    municipio=forms.CharField(max_length=30)
    estado= forms.CharField(max_length=19)
    telefono1= forms.CharField(max_length=20)


    class Meta:
        model=User
        fields=['username', 'password1','password2','nombre','apellido', 'fecha_nacimiento','email',  'sexo','domicilio',
            'cp','municipio','estado','telefono1']


    def clean_password1(self):
        data=self.cleaned_data['password1']
        tamano=len(str(data))

        if tamano<8:
            raise forms.ValidationError("La contraseña debe ser mayor a ocho caracteres")

        return data

    def save(self,commit=True):
        cd=self.cleaned_data
        user=super(RegistroForm,self).save(commit=False)
        user.email=cd['email']
        user.first_name=cd['nombre']
        user.last_name=cd['apellido']
        user.save()
        #user_profile=models.Perfil.create_user_profile(user=user)
        #sexo=cd['sexo'],domicilio=cd['domicilio'],cp=cd['cp'],municipio=cd['municipio'],estado=cd['estado'],telefono1=cd['telefono1'])
        d=datetime.datetime.strptime(cd['fecha_nacimiento'],'%m/%d/%Y')
        user.perfil.fecha_nacimiento=d.strftime('%Y-%m-%d')
        user.perfil.sexo=cd['sexo']
        user.perfil.domicilio=cd['domicilio']
        user.perfil.cp=cd['cp']
        user.perfil.municipio=cd['municipio']
        user.perfil.estado=cd['estado']
        user.perfil.telefono1=cd['telefono1']

        if commit:
            user.perfil.save()

        return user

class ExistenciaForm(forms.Form):
	#CADA VARIABLE QUE CREES REPRESENTA UN CAMPO, NO TIENES QUE HACER EL HTML
	exis=forms.CharField(max_length=30,label='',widget=forms.widgets.TextInput(attrs={'placeholder':'Introduzca código o nombre del producto '}))


class ModificarUsuarioForm(forms.Form):
    imagen=forms.ImageField(label="Cambiar imágen",required=False)
    SEXO=(('H', str('Hombre')),('M',str('Mujer')))
    nombre=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'nombre'}))
    apellido=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'nombre'}))
    sexo=forms.ChoiceField(choices=SEXO)
    domicilio= forms.CharField(max_length=60)
    cp= forms.CharField(max_length=8,label="Código Postal")
    municipio=forms.CharField(max_length=30)
    estado= forms.CharField(max_length=19)
    telefono1= forms.CharField(max_length=20, label="Teléfono")
    telefono2=forms.CharField(max_length=20,label="Teléfono secundario",required=False)

    class Meta:
        model = User

        fields=['imagen','nombre','apellido', 'fecha_nacimiento','sexo','domicilio',
                'cp','municipio','estado','telefono1']

