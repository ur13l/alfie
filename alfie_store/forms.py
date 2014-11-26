# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django import forms 
from datetime import datetime
from django.core.context_processors import request
from django.utils.safestring import mark_safe
from alfie_store import models 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from alfie_store.models import DireccionEnvio, DireccionEnvioAdicional


class RegistroForm(UserCreationForm):
    SEXO=(('H', str('Hombre')),('M',str('Mujer')))
    nombre=forms.CharField(max_length=30)
    apellido=forms.CharField(max_length=30)
    email=forms.EmailField()
    fecha_nacimiento=forms.CharField(widget=forms.DateInput(attrs={'placeholder':'mm/dd/aaaa'}))
    sexo=forms.ChoiceField(choices=SEXO)
    domicilio= forms.CharField(max_length=60)
    colonia= forms.CharField(max_length=60)
    cp= forms.CharField(max_length=8)
    municipio=forms.CharField(max_length=30)
    estado= forms.CharField(max_length=19)
    telefono1= forms.CharField(max_length=20)


    class Meta:
        model=User
        fields=['username', 'password1','password2','nombre','apellido', 'fecha_nacimiento','email',  'sexo','domicilio','colonia',
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
        user.perfil.colonia=cd['colonia']
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
    colonia= forms.CharField(max_length=60)
    cp= forms.CharField(max_length=8,label="Código Postal")
    municipio=forms.CharField(max_length=30)
    estado= forms.CharField(max_length=19)
    telefono1= forms.CharField(max_length=20, label="Teléfono")
    telefono2=forms.CharField(max_length=20,label="Teléfono secundario",required=False)

    class Meta:
        model = User

        fields=['imagen','nombre','apellido', 'fecha_nacimiento','sexo','domicilio', 'colonia',
                'cp','municipio','estado','telefono1','telefono2']


class DireccionEnvioForm(forms.ModelForm):
    class Meta:
        model=DireccionEnvio
        fields=['domicilio','colonia','cp','municipio','estado']


class DireccionEnvio2Form(forms.ModelForm):
    class Meta:
        model=DireccionEnvioAdicional
        fields=['domicilio2','colonia2','cp2','municipio2','estado2']

class PagoForm(forms.Form):
    a=" <img src='/static/img/visa_code.jpg' style='display:none' id='img_visa' width=262 height=179><img src='/static/img/mc_code.jpg' style='display:none' id='img_mc' width=262 height=179><img src='/static/img/ae_code.jpg' style='display:none' id='img_ae' width='262' height='179'><br>"

    CHOICES=(('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('09','09'),('10','10'),('11','11'),('12','12'))
    ANIO=(('2014','14'),('2015','15'),('2016','16'),('2017','17'),('2018','18'),('2019','19'),('2020','20'),('2021','21'),('2022','22'))
    no_tarjeta=forms.CharField(widget=forms.TextInput(attrs={'style':'display:none;','placeholder':'No. de tarjeta'}),label='')
    codigo_tarj_ae=forms.CharField(max_length=16, widget=forms.TextInput(attrs={'style':'display:none;','placeholder':'Código de 4 dígitos '}),label='',required=False)
    codigo_tarj=forms.CharField(max_length=3,widget=forms.TextInput(attrs={'style':'display:none;','placeholder':'Código de 3 dígitos'}),label='',required=False)
    mes=forms.ChoiceField(choices=CHOICES,label=mark_safe(a+'<br>Vencida en: <br> <label>Mes:'))
    anio=forms.ChoiceField(choices=ANIO,label="/  Año:")
    nom=forms.CharField(max_length=90,widget=forms.TextInput(attrs={'style':'display:none;','placeholder':'Nombre y apellido impreso en la tarjeta'}),label="")

    def clean_no_tarjeta(self):
        data=self.cleaned_data['no_tarjeta']
        tamano=len(str(data))

        if tamano!=16:
            raise forms.ValidationError("Número de tarjeta no válido")

        return data

    def clean_codigo_tarj(self):
        data=self.cleaned_data['codigo_tarj']
        tamano=len(str(data))

        if tamano!=3 and tamano!=0:
            raise forms.ValidationError("Código de seguridad inválido")

        return data

    def clean_codigo_tarj_ae(self):
        data=self.cleaned_data['codigo_tarj_ae']
        tamano=len(str(data))

        if tamano!=4 and tamano!=0:
            raise forms.ValidationError("Código de seguridad no válido")

        return data

