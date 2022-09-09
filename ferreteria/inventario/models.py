from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nit = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=75)
    direccion = models.CharField(max_length=150, null=True,blank=True)

    def __str__(self):
        texto = "{0} | {1}"
        return texto.format(self.nombre, self.nit)

class Cliente(models.Model):
    nit = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=75)
    direccion = models.CharField(max_length=150, null=True,blank=True)

    def __str__(self):
        texto = "{0} | {1}"
        return texto.format(self.nombre, self.nit)

class Medida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=75)

    def __str__(self):
        texto = "{0} | {1}"
        return texto.format(self.id, self.nombre)

    def get_medida(self):
        return self

    def get_etiquetamed(self):
        texto = "{0} | {1}"
        return texto.format(self.id, self.nombre)

class Bodega(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=75)

    def __str__(self):
        texto = "{0} | {1}"
        return texto.format(self.id, self.nombre)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=75)
    tipo = models.CharField(max_length=1,choices=(('P','Producto'),('S','Servicios')), default='P')
    tipo_producto = models.CharField(max_length=1,choices=(('E','Embalaje'),('N','Nivel')), default='N')
    fecha_vencimiento = models.DateTimeField(null=True)
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT,null=True)

    def __str__(self):
        texto = "{0} | {1} - {2}"
        return texto.format(self.id, self.nombre, self.medida)
    
    def get_idmed(self):
        return self.medida


class ProductoDNiveles(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='producto')
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    #medida = models.ForeignKey(Medida, on_delete=models.PROTECT)

    producto_nivel = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='producto_nivel', null=True,blank=True)
    unidadxmedida = models.DecimalField(max_digits=9, decimal_places=2, default=1)
    
    precio = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    costo = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    salidas = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    entradas = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    stock = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        texto = "{0} - {1}     [{2}]"
        return texto.format(self.producto, self.bodega, self.stock)
        
    class Meta:
        unique_together = (('producto', 'bodega'),)

#class ProductoMedidas(models.Model):
#    id = models.AutoField(primary_key=True)
#    producto_detalle = models.ForeignKey(ProductoDetalle, on_delete=models.PROTECT, null=True)
    
#    medida = models.ForeignKey(Medida, on_delete=models.PROTECT)

#    precio = models.DecimalField(max_digits=9, decimal_places=2)
#    stock = models.DecimalField(max_digits=9, decimal_places=2)

#    producto_medidas = models.ForeignKey('self', null=True,blank=True, on_delete=models.PROTECT)
#    unidadxmedida = models.DecimalField(max_digits=9, decimal_places=2, default=1)

#    def __str__(self):
#            texto = "{0} - {1}"
#            return texto.format(self.producto_detalle, self.medida)

#    class Meta:
#        unique_together = (('producto_detalle', 'medida'),)

class Compra(models.Model):
    numero = models.CharField(primary_key=True, max_length=10)
    fecha = models.DateTimeField(null=True,blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True,blank=True)
    descripcion = models.CharField(max_length=150, null=True,blank=True)

    def __str__(self):
        texto = "{0} - {1}"
        return texto.format(self.numero, self.proveedor)

class CompraDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    productodetalle = models.ForeignKey(ProductoDNiveles, on_delete=models.PROTECT)

    unidades = models.DecimalField(max_digits=9, decimal_places=2)
    costo = models.DecimalField(max_digits=9, decimal_places=2,null=True)

#    def __str__(self):
#            texto = "{0} ({1})"
#            return texto.format(self.productomedidas, self.unidades)