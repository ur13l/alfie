#-*-coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.datastructures import MultiValueDictKeyError
from alfie_store.models import Usuario, Producto, DetalleProducto, Talla, Color, Categoria, Subcategoria
from alfie_store import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
_id_us=''
_usuario=''

def home(request):
	return render_to_response('index.html',{'param':parametros()},RequestContext(request))


def iniciar_sesion(request):
	errors=[]
	var_us=''
	if 'q' in request.GET:
			return busqueda(request)

	if 'user' in request.POST and 'cont' in request.POST:
		user=request.POST['user']
		cont=request.POST['cont']
		if not user:
			errors.append("Introduzca un nombre de usuario")
		elif not cont:
			errors.append('Escriba su contraseña');
		else:
			if not cont:
				errors.append("Escriba su contraseña")

			else:
				try:
					_usuario=Usuario.objects.get(id_user__exact=user)
					if _usuario:
						if _usuario.contrasena==cont:
							return HttpResponseRedirect("/")
						else:
							errors.append("Contraseña incorrecta")
				except:
					errors.append("El usuario especificado no existe")
		var_us=user

	return render_to_response('iniciar_sesion.html',{'errors':errors,'param':parametros(),'us':var_us},RequestContext(request))

def registro(request):
	if request.method == 'POST':
		form=forms.RegistroForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			us=Usuario(id_user=cd['id_user'], nombre=cd['nombre'], apellido=cd['apellido'], contrasena=cd['contrasena'],
				fecha_nacimiento=cd['fecha_nacimiento'], sexo=cd['sexo'], domicilio=cd['domicilio'],cp=cd['cp'],
				municipio=cd['municipio'], estado=cd['estado'], telefono1=cd['telefono1'], email=cd['email'], administrador=False)
			us.save()
			return HttpResponseRedirect("/")
	else:
		if 'q' in request.GET:
			return busqueda(request)
		form = forms.RegistroForm()

	return render_to_response('registro_form.html',{'form':form,'param':parametros()},context_instance=RequestContext(request))

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
		raise Http404()

    if 'q' in request.GET:
		return busqueda(request)

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

def carrito(request):
    param=parametros()
    return render_to_response('carrito.html',context_instance=RequestContext(request))



def inventario(request):
    mensaje="Hola entrando a inventario"
    return render_to_response('inventario.html',{'mensaje':mensaje}, context_instance=RequestContext(request))

def ver_inventario(request):
    param=parametros()
    lisproductos = []
    lisproductos=Producto.objects.order_by('SKU')
    return render_to_response('ver_inventario.html',{'productos':lisproductos,'param':parametros()}, context_instance=RequestContext(request))

def add_existencias(request):
	errors = []
	productos = []
	if request.method == 'POST':
		exis = request.POST['exis']
		form = forms.ExistenciaForm(request.POST)
		if form.is_valid():
			productos=Producto.objects.filter(Q(SKU=exis)|Q(nombre__icontains=exis))

	elif request.method=='GET':
		form=forms.ExistenciaForm()
		try:
			for elem in request.GET.keys():
				p=Producto.objects.get(SKU=elem)
				p.cantidad+=int(request.GET[elem])
				p.save()

		except ObjectDoesNotExist:
			form=forms.ExistenciaForm()


	else:
		form = forms.ExistenciaForm()


	return render_to_response('add_existencias.html',{'form':form,'productos': productos,'param':parametros()},context_instance = RequestContext(request))

#----------------------------------------------------------------------------------------------------------------------------------------

def parametros():
    list_tallas=Talla.objects.all()
    list_colores=Color.objects.all()
    list_categoria=Categoria.objects.all()
    list_subcategoria=Subcategoria.objects.all()
    return {'list_tallas':list_tallas,'list_colores':list_colores,'list_categoria':list_categoria,'list_subcategoria':list_subcategoria}
