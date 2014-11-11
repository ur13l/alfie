from django.contrib import admin
from alfie_store import models

admin.site.register(models.Proveedor)
admin.site.register(models.Producto)
admin.site.register(models.Subcategoria)
admin.site.register(models.Color)
admin.site.register(models.Talla)
admin.site.register(models.Categoria)