from django.contrib import admin
from alfie_store import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model=models.Perfil
    can_delete=False
    verbose_name_plural='profile'

class UserAdmin(UserAdmin):
    inlines=(UserProfileInline,)

admin.site.register(models.Proveedor)
admin.site.register(models.Producto)
admin.site.register(models.Subcategoria)
admin.site.register(models.Color)
admin.site.register(models.Talla)
admin.site.register(models.Categoria)
admin.site.register(models.DetalleProducto)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)