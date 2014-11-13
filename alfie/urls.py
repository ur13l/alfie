from django.conf.urls import patterns, include, url, static

from django.contrib import admin
from alfie import settings
from settings import MEDIA_ROOT
admin.autodiscover();


urlpatterns = patterns('alfie_store.views',url(r'^$','busqueda'), url(r'^busqueda/$','busqueda'),
	url(r'^login/$','iniciar_sesion'),
	url(r'^registro/$','registro'),
	url(r'^inventario/$','inventario'),
	url(r'^ver_inventario/$','ver_inventario'),
	url(r'^add_existencias/$','add_existencias'),
    url(r'^producto/(\d{1,8})/$','producto'),
    url(r'^carrito/$','carrito')

	)

urlpatterns += patterns('',url(r'^admin/', include(admin.site.urls)))

urlpatterns += patterns('',url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':MEDIA_ROOT}))

    # Examples:
    # url(r'^$', 'alfie.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#urlpatterns +=  patterns(url(r'css/(?P<path>.*)$', 'django.views.static.serve',
#{'document_root': settings.STATIC_ROOT + 'templates/css'}),)

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)