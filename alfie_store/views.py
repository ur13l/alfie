#-*-coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.templatetags.static import static
from django.utils.datastructures import MultiValueDictKeyError
from alfie.settings import MEDIA_ROOT
from alfie_store.models import Producto, DetalleProducto, Talla, Color, Categoria, Subcategoria, Perfil, Carrito, \
    DetalleCarrito, Venta, DetalleVenta
from alfie_store import forms
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
_usuario=AnonymousUser()

def home(request):
    p=Producto.objects.all()
    return render_to_response('index.html',{'prod':p,'param':parametros()},context_instance=RequestContext(request))


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
                            return HttpResponseRedirect("/")
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
            r=User.objects.get(username=request.POST['username'])
            r.perfil.foto_perfil=static('default.jpg')
            r.save()
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
                    p=request.POST['producto']
                    talla=request.POST['talla']
                    color=request.POST['color']
                    cantidad=int(request.POST['cantidad'])


                    if 'color' in request.POST and 'cantidad' in request.POST and 'talla' in request.POST:
                        detalleProd=DetalleProducto.objects.get(Q(producto_id=producto.id) & Q( talla_id=talla) & Q(color_id=color))
                        if cantidad>detalleProd.unidades:
                            errors.append("Solo quedan %d unidades"%(detalleProd.unidades))
                        else:

                            if request.user.is_anonymous():
                                return HttpResponseRedirect('/login/')
                            else:
                                try:
                                    car=Carrito.objects.get(cliente=request.user)
                                    car.save()

                                except ObjectDoesNotExist:
                                    car=Carrito(cliente=request.user)
                                    car.save()
                                try:
                                    dc=DetalleCarrito.objects.get(dproducto=detalleProd)
                                    dc.cantidad+=cantidad
                                    dc.precio=dc.dproducto.producto.precio_venta*dc.cantidad
                                    dc.save()
                                except ObjectDoesNotExist:
                                    dc=DetalleCarrito(dproducto=detalleProd,carrito=car,cantidad=cantidad,precio=(detalleProd.producto.precio_venta*cantidad))
                                    dc.save()
                                return HttpResponseRedirect('/perfil/carrito/')

                except MultiValueDictKeyError:
                    if not color:
                        errors.append("Debe especificar algún color")
                    if not talla:
                        errors.append("Debe especificar una talla")
               # except ValueError:
                #    errors.append("Debe especificar una cantidad")
                except ObjectDoesNotExist:
                    errors.append("El producto se encuentra agotado")

            return render_to_response('producto.html',{'producto':producto,'errors':errors,'param':parametros()},context_instance=RequestContext(request))
        except ValueError:
            return render_to_response('producto_no_encontrado.html',{'param':parametros()},context_instance=RequestContext(request))

def inventario(request):
    mensaje="Hola entrando a inventario"
    return render_to_response('inventario.html',{'mensaje':mensaje,'param':parametros()}, context_instance=RequestContext(request))

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect("/")

def ver_inventario(request):
    param=parametros()
    lisproductos = []
    lisproductos=Producto.objects.order_by('SKU')
    return render_to_response('ver_inventario.html',{'productos':lisproductos,'param':parametros()}, context_instance=RequestContext(request))

def add_existencias(request):
    if request.method=='GET':
        if 'e' in request.GET:
            e=request.GET.get('e','')
            prod=Producto.objects.filter(Q(nombre__icontains=e) | Q(SKU__icontains=e))
            return render_to_response('add_existencias.html',{'prod':prod,'param':parametros()},context_instance=RequestContext(request))
        return render_to_response('add_existencias.html',{'param':parametros()},context_instance=RequestContext(request))
    elif request.method=='POST':
        c=request.POST['sel_color']
        t=request.POST['sel_talla']
        p=request.POST['sel_producto']
        e=request.GET['e']
        prod=Producto.objects.filter(Q(nombre__icontains=e) | Q(SKU__icontains=e))
        _color=Color.objects.get(id=c)
        _talla=Talla.objects.get(id=t)
        _producto=Producto.objects.get(id=p)
        try:
            dp=DetalleProducto.objects.get(producto=_producto,color=_color,talla=_talla)
        except ObjectDoesNotExist:
            dp=DetalleProducto(color=_color,talla=_talla,producto=_producto)
            dp.unidades=0
            dp.save()
        if not 'unidades' in request.POST:
            return render_to_response("add_existencias.html",{'prod':prod,'dp':dp},context_instance=RequestContext(request))
        else:
            unid=request.POST['unidades']
            dp.unidades+=int(unid)
            dp.save()
            return render_to_response("add_existencias.html",{'prod':prod,'dp':dp},context_instance=RequestContext(request))
    else:
		return render_to_response("add_existencias.html",{'param':parametros()},context_instance=RequestContext(request))

def perfil(request,offset):
    if offset=="resumen":
        return resumen(request)
    elif offset=="modificar":
        return modificar(request)
    elif offset=="carrito":
        return carrito(request)
    elif offset=="compras":
        return compras(request)
    elif offset=="pedidos":
        return pedidos(request)
    else:
        return Http404()

def resumen(request):
    v=Venta.objects.filter(usuario=request.user)
    dv=DetalleVenta.objects.filter(venta=v)
    car=Carrito.objects.filter(cliente=request.user)
    dc=DetalleCarrito.objects.filter(carrito=car)

    return render_to_response('resumen.html',{'dv':dv,'dc':dc,'param':parametros()},context_instance=RequestContext(request))

@login_required
def modificar(request):
    u=request.user
    p=u.perfil
    user={'us':u.username,'imagen':p.foto_perfil,'nombre':u.first_name,'apellido':u.last_name,'sexo':p.sexo,'domicilio':p.domicilio,'colonia':p.colonia,'cp':p.cp,'municipio':p.municipio,'estado':p.estado,'telefono1':p.telefono1,'telefono2':p.telefono2}

    if request.method=='POST':
        form_modificar=forms.ModificarUsuarioForm(request.POST,request.FILES, user)
        if form_modificar.is_valid():
            us=User.objects.get(id=request.user.id)
            per=Perfil.objects.get(user=us)
            us.first_name=request.POST['nombre']
            us.last_name=request.POST['apellido']
            per.sexo=request.POST['sexo']
            per.domicilio=request.POST['domicilio']
            per.colonia=request.POST['colonia']
            per.cp=request.POST['cp']
            per.municipio=request.POST['municipio']
            per.estado=request.POST['estado']
            per.telefono1=request.POST['telefono1']
            per.telefono2=request.POST['telefono2']

            if 'imagen' in request.FILES:
                per.foto_perfil=request.FILES['imagen']
                save_file(request.FILES['imagen'])
            us.save()
            per.save()
            return HttpResponseRedirect("/perfil/resumen", request)

    else:
        form_modificar=forms.ModificarUsuarioForm(user)
        return render_to_response('modificar_perfil.html',{'form_modificar':form_modificar,'param':parametros()},context_instance=RequestContext(request))

@login_required
def carrito(request):

    try:
        car=Carrito.objects.get(cliente=request.user)
        car.save()

    except ObjectDoesNotExist:
        car=Carrito(cliente=request.user)
        car.save()

    dc=DetalleCarrito.objects.filter(carrito=car)
    total=0

    for elem in dc:
        total += elem.precio

    if 'actualizarCarrito' in request.POST:

        id_dcar=int(request.POST['id_dcar'])
        dcar=DetalleCarrito.objects.get(id=id_dcar)
        prec_un=dcar.dproducto.producto.precio_venta
        cant=float(request.POST['cantidad'])
        prec_total=prec_un*cant
        dcar.precio=prec_total
        dcar.cantidad=cant
        dcar.save()
        return HttpResponseRedirect("/perfil/carrito")

    elif 'eliminarCarrito' in request.POST:
        id_dcar=int(request.POST['id_dcar'])
        dcar=DetalleCarrito.objects.get(id=id_dcar)
        dcar.delete()
        return HttpResponseRedirect("/perfil/carrito")

    return render_to_response('carrito.html',{'carrito':car, 'dcar':dc, 'total':total, 'param':parametros()},context_instance=RequestContext(request))

@login_required
def envio(request):
    u=request.user
    p=u.perfil
    datos={'domicilio':p.domicilio,'colonia':p.colonia,'cp':p.cp,'municipio':p.municipio,'estado':p.estado}
    form2=forms.DireccionEnvio2Form()
    form=forms.DireccionEnvioForm(datos)

    return render_to_response('envio.html',{'form':form,'form2':form2,'param':parametros()},context_instance=RequestContext(request))

@login_required
def pago(request):


    if request.method=="POST":
        pago=forms.PagoForm(request.POST)
        if pago.is_valid():
            return HttpResponseRedirect("/confirmar/")
    else:
        pago=forms.PagoForm()
    return render_to_response('pago.html',{'pago_form':pago,'param':parametros()},context_instance=RequestContext(request))

@login_required
def exito(request):
    car=Carrito.objects.get(cliente=request.user)
    dc=DetalleCarrito.objects.filter(carrito=car)
    return render_to_response('exito.html',{'dc':dc,'param':parametros()},context_instance=RequestContext(request))

@login_required
def confirmar(request):
    car=Carrito.objects.get(cliente=request.user)
    dc=DetalleCarrito.objects.filter(carrito=car)
    total=0
    for elem in dc:
        total += elem.precio
    if request.method=="POST":
        v=Venta(usuario=request.user,cantidad_total=0,entrega=False);
        v.save()
        for elem in dc:
            dv=DetalleVenta(dproducto=elem.dproducto,venta=v,cantidad=elem.cantidad,precio=elem.precio,descuento=0)
            dv.save()
            elem.delete()
            dv.dproducto.unidades-=dv.cantidad
            dv.dproducto.save()


        return HttpResponseRedirect('/exito/')
    return render_to_response('detalle_envio.html',{'dc':dc,'total':total,'param':parametros()},context_instance=RequestContext(request))

@login_required
def compras(request):
    v=Venta.objects.filter(Q(usuario=request.user))
    dv=DetalleVenta.objects.filter(venta=v)

    return render_to_response('compras.html',{'dv':dv,'param':parametros()},context_instance=RequestContext(request))

@login_required
def pedidos(request):
    v=Venta.objects.filter(Q(usuario=request.user)&Q(entrega=False))
    dv=DetalleVenta.objects.filter(venta=v)

    return render_to_response('pedidos.html',{'dv':dv,'param':parametros()},context_instance=RequestContext(request))

#----------------------------------------------------------------------------------------------------------------------------------------

def save_file(file, path=""):
    filename=file._get_name()
    fd=open('%s%s'%(MEDIA_ROOT,str(path)+str(filename)),'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()


def parametros():
    list_tallas=Talla.objects.all()
    list_colores=Color.objects.all()
    list_categoria=Categoria.objects.all()
    list_subcategoria=Subcategoria.objects.all()
    return {'list_tallas':list_tallas,'list_colores':list_colores,'list_categoria':list_categoria,'list_subcategoria':list_subcategoria}
