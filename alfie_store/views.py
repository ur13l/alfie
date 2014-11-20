#-*-coding:utf-8 -*-
from systemd import login
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.datastructures import MultiValueDictKeyError
from alfie_store.models import Producto, DetalleProducto, Talla, Color, Categoria, Subcategoria, Perfil
from alfie_store import forms
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
_usuario=AnonymousUser()

def home(request):
	return render_to_response('index.html',{'param':parametros()},RequestContext(request))


def iniciar_sesion(request):
    errors=[]
    if not request.user.is_authenticated():
        if 'user' in request.POST and 'cont' in request.POST:
            user=request.POST['user']
            cont=request.POST['cont']
            acceso=authenticate(username=user,password=cont)

            if not user:
                errors.append("Introduzca un nombre de usuario")
            elif not cont:
                errors.append('Escriba su contraseña')
            else:
                if not cont:
                    errors.append("Escriba su contraseña")

                else:
                    if acceso is not None:
                        if acceso.is_active:
                            login(request,acceso)
                            return render_to_response('index.html',{'param':parametros()},context_instance=RequestContext(request))
                        else:
                            errors.append("El usuario no se encuentra activo")
                    else:
                        errors.append("Error de usuario o contraseña")
        return render_to_response('iniciar_sesion.html',{'errors':errors, 'param':parametros()},RequestContext(request))
    else:
        return HttpResponseRedirect("/perfil/resumen")

def registro(request):
    if request.method == 'POST':
        registro_form=forms.RegistroForm(request.POST)
        if registro_form.is_valid():
            registro_form.save()
            acceso=authenticate(username=request.POST['username'],password=request.POST['password1'])
            login(request, acceso)
            return render_to_response('index.html',{'param':parametros()},context_instance=RequestContext(request))
        else:
            return render_to_response('registro_form.html',{'registro_form':registro_form,'param':parametros()},context_instance=RequestContext(request))
    else:
        registro_form=forms.RegistroForm()

    return render_to_response('registro_form.html',{'registro_form':registro_form,'param':parametros()},context_instance=RequestContext(request))

def busqueda(request):
    if 'q' in request.GET:
        q=request.GET['q']
        prod=Producto.objects.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        return render_to_response('busqueda.html',{'prod':prod,'param':parametros()},context_instance=RequestContext(request))
    else:
		return render_to_response("index.html",{'param':parametros()},context_instance=RequestContext(request))



def producto(request,offset):
    errors=[]
    try:
        offset=int(offset)
    except ValueError:
	    return render_to_response('producto_no_encontrado.html',{'param':parametros()},context_instance=RequestContext(request))

    try:
        producto=Producto.objects.get(id=offset);
        color=""
        talla=""
        cantidad=""

        if request.method=='POST':
            try:
                talla=request.POST['talla']
                color=request.POST['color']
                cantidad=int(request.POST['cantidad'])


                if 'color' in request.POST and 'cantidad' in request.POST and 'talla' in request.POST:
                    detalleProd=DetalleProducto.objects.get(Q(producto_id=producto.id) & Q( talla_id=talla) & Q(color_id=color))
                    if cantidad>detalleProd.unidades:
                        errors.append("Solo quedan %d unidades"%(detalleProd.unidades))
                    else:
                        return HttpResponse("HOLA MUNDO"+str(detalleProd.unidades+int(cantidad)))
            except MultiValueDictKeyError:
                if not color:
                    errors.append("Debe especificar algún color")
                if not talla:
                    errors.append("Debe especificar una talla")
            except ValueError:
                errors.append("Debe especificar una cantidad")
            except ObjectDoesNotExist:
                errors.append("El producto se encuentra agotado")

        return render_to_response('producto.html',{'producto':producto,'errors':errors,'param':parametros()},context_instance=RequestContext(request))
    except:
        return render_to_response('producto_no_encontrado.html',{'param':parametros()},context_instance=RequestContext(request))

def carrito(request):
    param=parametros()
    return render_to_response('carrito.html',{'param':parametros()},context_instance=RequestContext(request))



def inventario(request):
    mensaje="Hola entrando a inventario"
    return render_to_response('inventario.html',{'mensaje':mensaje,'param':parametros()}, context_instance=RequestContext(request))

def cerrar_sesion(request):
    logout(request)
    return render_to_response('index.html',{'param':parametros()},context_instance=RequestContext(request))


def ver_inventario(request):
    param=parametros()
    lisproductos = []
    lisproductos=Producto.objects.order_by('SKU')
    return render_to_response('ver_inventario.html',{'productos':lisproductos,'param':parametros()}, context_instance=RequestContext(request))

#def add_existencias(request):
    #if 'e' in request.GET:
     #   e=request.GET['e']
        prod=Producto.objects.filter(Q(nombre__icontains=e) | Q(SKU__icontains=e))

        #return render_to_response('add_existencias.html.html',{'prod':prod,'param':parametros()},context_instance=RequestContext(request))

    #else:
		#return render_to_response("index.html",{'param':parametros()},context_instance=RequestContext(request))



def perfil(request,offset):
    if offset=="resumen":
        return resumen(request)
    elif offset=="modificar":
        return modificar(request)
    else:
        return Http404()

def resumen(request):
    return render_to_response('resumen.html',{'param':parametros()},context_instance=RequestContext(request))

def modificar(request):
    u=request.user
    p=u.perfil
    user={'us':u.username,'imagen':p.foto_perfil,'nombre':u.first_name,'apellido':u.last_name,'sexo':p.sexo,'domicilio':p.domicilio,'cp':p.cp,'municipio':p.municipio,'estado':p.estado,'telefono1':p.telefono1,'telefono2':p.telefono2}

    if request.method=='POST':
        form_modificar=forms.ModificarUsuarioForm(request.POST,user)
        if form_modificar.is_valid():
            cd=form_modificar.cleaned_data
            us=User.objects.get(id=request.user.id)
            per=Perfil.objects.get(user=us)
            us.first_name=cd['nombre']
            us.last_name=cd['apellido']
            per.sexo=cd['sexo']
            per.domicilio=cd['domicilio']
            per.cp=cd['cp']
            per.municipio=cd['municipio']
            per.estado=cd['estado']
            per.telefono1=cd['telefono1']
            per.telefono2=cd['telefono2']
            per.foto_perfil=cd['imagen']
            us.save()
            per.save()
            return render_to_response('resumen.html',{'param':parametros()},context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    else:
        form_modificar=forms.ModificarUsuarioForm(user)
        return render_to_response('modificar_perfil.html',{'form_modificar':form_modificar,'param':parametros()},context_instance=RequestContext(request))
#----------------------------------------------------------------------------------------------------------------------------------------

def parametros():
    list_tallas=Talla.objects.all()
    list_colores=Color.objects.all()
    list_categoria=Categoria.objects.all()
    list_subcategoria=Subcategoria.objects.all()
    return {'list_tallas':list_tallas,'list_colores':list_colores,'list_categoria':list_categoria,'list_subcategoria':list_subcategoria}
