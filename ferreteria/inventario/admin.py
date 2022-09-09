from django.contrib import admin
from .models import *
# Register your models here.


# Register your models here.


admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Medida)
admin.site.register(Bodega)

admin.site.register(Producto)
admin.site.register(ProductoDNiveles)
#admin.site.register(ProductoMedidas)

admin.site.register(Compra)
admin.site.register(CompraDetalle)