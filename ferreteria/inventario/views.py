from multiprocessing.connection import Client
from multiprocessing.dummy import Array
from django.shortcuts import render, redirect
from .models import Cliente, Compra, CompraDetalle, Medida, Producto, ProductoDNiveles, Proveedor, Venta, VentaDetalle
from django.contrib import messages
from datetime import datetime
from decimal import Decimal

# Create your views here.
def list_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, "list_proveedores.html", {"proveedores": proveedores})

def eliminar_proveedor(request, nit):
    proveedor = Proveedor.objects.get(nit=nit)
    proveedor.delete()

    messages.success(request, 'Se eliminó el Proveedor ' + nit)

    return redirect('/')


def vnewProveedor(request):
    return render(request, "vnewProveedor.html", {"proveedores": "proveedores"})

def newProveedor(request):
    nit = request.POST['nit']
    nombre = request.POST['nombre']
    direccion = request.POST['direccion']

    try:
        provee = Proveedor.objects.create(
        nit=nit, nombre=nombre, direccion=direccion)
        messages.success(request, 'Proveedor Registrado')
        return redirect('/')
    except:
        messages.error(request, "error al insertar proveedor")

def vistaEditProveedor(request, nit):
    provee = Proveedor.objects.get(nit=nit)
    return render(request, "edicionProveedor.html", {"provee": provee})

def vistaProducto(request, id):
    producto = Producto.objects.get(id=id)
    #producto.med = producto.medida
    #print(producto.medida.id)
    medidas = Medida.objects.all()

    productoDet = ProductoDNiveles.objects.filter(producto=id)
    return render(request, "vistaProducto.html", {"producto": producto, 
    "productoDet": productoDet, "medidas": medidas})

def editarProveedor(request):
    nit = request.POST['nit']
    nombre = request.POST['nombre']
    direccion = request.POST['direccion']

    prov = Proveedor.objects.get(nit=nit)
    prov.nombre = nombre
    prov.direccion = direccion
    prov.save()

    messages.success(request, 'Dato actualizado')

    return redirect('/')
   
# Productos
def list_productos(request):
    productos = Producto.objects.all()
    return render(request, "list_productos.html", {"productos": productos})

# Compras
def list_compras(request):
    compras = Compra.objects.all()
    return render(request, "list_compras.html", {"compras": compras})

# Venta
def list_ventas(request):
    ventas = Venta.objects.all()
    return render(request, "list_ventas.html", {"compras": ventas})

def eliminar_compra(request, numero):
    compra = Compra.objects.get(numero=numero)
    compra.delete()
    messages.success(request, 'Se eliminó el Compra ' + numero)
    return redirect('/homeCompras')

def eliminar_venta(request, numero):
    venta = Venta.objects.get(numero=numero)
    venta.delete()
    messages.success(request, 'Se eliminó la venta ' + numero)
    return redirect('/homeVentas')

def vnewCompra(request):
    proveedores = Proveedor.objects.all()
    return render(request, "vnewCompra.html", {"proveedores": proveedores})

def vnewVenta(request):
    clientes = Cliente.objects.all()
    return render(request, "vnewVenta.html", {"proveedores": clientes})

def newCompra(request):
    numero = request.POST['numero']
    fecha = request.POST['fecha']
    proveedor = request.POST['proveedor']
    descripcion = request.POST['descripcion']

    provobj =  Proveedor.objects.get(nit=proveedor)

    try:
        comp = Compra.objects.create(
        numero=numero, fecha=fecha,proveedor =provobj, descripcion=descripcion)
        #print("comp")
        #print(comp)
        messages.success(request, 'Compra Registrada')
        #return redirect('/homeCompras/')
        return redirect('/vistaCompra/'+numero)
    except:
        messages.success(request, 'Error al Registradar Compra')

def newVenta(request):
    numero = request.POST['numero']
    fecha = request.POST['fecha']
    cliente = request.POST['cliente']
    descripcion = request.POST['descripcion']
    
    provobj =  Cliente.objects.get(nit=cliente)

    try:
        comp = Venta.objects.create(
        numero=numero, fecha=fecha,cliente =provobj, descripcion=descripcion)
        #print("comp")
        #print(comp)
        messages.success(request, 'Venta Registrada')
        #return redirect('/homeCompras/')
        return redirect('/vistaVenta/'+numero)
    except:
        messages.success(request, 'Error al Registradar Compra')
        
def vistaCompra(request, numero):
    compra = Compra.objects.get(numero=numero)
    proveedores = Proveedor.objects.all()
    product = ProductoDNiveles.objects.all()

    CompraDet = CompraDetalle.objects.filter(compra=numero)
    return render(request, "edicionCompra.html", {"compra": compra, 
    "CompraDet": CompraDet, "proveedores": proveedores, "product": product})

def vistaVenta(request, numero):
    venta = Venta.objects.get(numero=numero)
    clientes = Cliente.objects.all()
    product = ProductoDNiveles.objects.all()

    VentaDet = VentaDetalle.objects.filter(venta=numero)
    return render(request, "edicionVenta.html", {"compra": venta, 
    "CompraDet": VentaDet, "proveedores": clientes, "product": product})

def addProductoCompra(request, numero):
    productodetalle = request.POST['productodetalle']
    costo = request.POST['costo']
    unidades = request.POST['unidades']

    productodetalleobj =  ProductoDNiveles.objects.get(id=productodetalle)
    compraobj =  Compra.objects.get(numero=numero)

    ##try:
    comp = CompraDetalle.objects.create(
    compra=compraobj, productodetalle=productodetalleobj, costo=costo,unidades =unidades)
    messages.success(request, 'Producto Ingresado')

    #existencias
    productodetalleobj.stock = productodetalleobj.stock + Decimal(unidades)
    productodetalleobj.entradas = productodetalleobj.entradas + Decimal(unidades)
    #costo
    productodetalleobj.costo = Decimal(costo)

    #existencia_niveles
    #print(productodetalleobj.producto_nivel.id) # el producto en detella prod
    #print(productodetalleobj.bodega.id) # bodega del producto
    #Model.objects.filter(x=1, y=2)
    if productodetalleobj.producto_nivel is not None:
        #print("xx----", productodetalleobj.producto_nivel)
        nivelProducto = ProductoDNiveles.objects.get(producto=productodetalleobj.producto_nivel.id, bodega =productodetalleobj.bodega.id)
        nivelProducto.stock = nivelProducto.stock  + (productodetalleobj.unidadxmedida * Decimal(unidades))
        nivelProducto.entradas = nivelProducto.entradas  + (productodetalleobj.unidadxmedida * Decimal(unidades))
        nivelProducto.save()

    if productodetalleobj.producto.tipo_producto == 'N': 
        print(productodetalleobj.producto.tipo_producto)
        embalajeProducto = ProductoDNiveles.objects.get(producto_nivel=productodetalleobj.producto.id, bodega =productodetalleobj.bodega.id)
        embalajeProducto.stock = embalajeProducto.stock  + (Decimal(unidades) / embalajeProducto.unidadxmedida)
        embalajeProducto.entradas = embalajeProducto.entradas  + (Decimal(unidades) / embalajeProducto.unidadxmedida)
        embalajeProducto.save()
    


    productodetalleobj.save()
    messages.success(request, 'Se actualizó Stock')

    return redirect('/vistaCompra/'+numero)
    #except:
    #   messages.success(request, 'Error al Ingresar Producto')
    #   productodetalleobj.roll
    #   return redirect('/vistaCompra/'+numero)


def addProductoVenta(request, numero):
    productodetalle = request.POST['productodetalle']
    costo = request.POST['costo']
    unidades = request.POST['unidades']

    productodetalleobj =  ProductoDNiveles.objects.get(id=productodetalle)
    compraobj =  Venta.objects.get(numero=numero)

    ##try:
    comp = VentaDetalle.objects.create(
    venta=compraobj, productodetalle=productodetalleobj, costo=costo,unidades =unidades)
    messages.success(request, 'Producto Ingresado')

    #existencias
    productodetalleobj.stock = productodetalleobj.stock - Decimal(unidades)
    productodetalleobj.salidas = productodetalleobj.salidas + Decimal(unidades)
    #precio
    productodetalleobj.precio = Decimal(costo)

    #existencia_niveles
    #print(productodetalleobj.producto_nivel.id) # el producto en detella prod
    #print(productodetalleobj.bodega.id) # bodega del producto
    #Model.objects.filter(x=1, y=2)
    if productodetalleobj.producto_nivel is not None:
        #print("xx----", productodetalleobj.producto_nivel)
        nivelProducto = ProductoDNiveles.objects.get(producto=productodetalleobj.producto_nivel.id, bodega =productodetalleobj.bodega.id)
        nivelProducto.stock = nivelProducto.stock  - (productodetalleobj.unidadxmedida * Decimal(unidades))
        nivelProducto.salidas = nivelProducto.salidas  + (productodetalleobj.unidadxmedida * Decimal(unidades))
        nivelProducto.save()

    if productodetalleobj.producto.tipo_producto == 'N': 
        print(productodetalleobj.producto.tipo_producto)
        embalajeProducto = ProductoDNiveles.objects.get(producto_nivel=productodetalleobj.producto.id, bodega =productodetalleobj.bodega.id)
        embalajeProducto.stock = embalajeProducto.stock  - (Decimal(unidades) / embalajeProducto.unidadxmedida)
        embalajeProducto.salidas = embalajeProducto.salidas  + (Decimal(unidades) / embalajeProducto.unidadxmedida)
        embalajeProducto.save()
    


    productodetalleobj.save()
    messages.success(request, 'Se actualizó Stock')

    return redirect('/vistaVenta/'+numero)
    #except:
    #   messages.success(request, 'Error al Ingresar Producto')
    #   productodetalleobj.roll
    #   return redirect('/vistaCompra/'+numero)

def eliminar_detCompra(request, id):
    compradet = CompraDetalle.objects.get(id=id)

    #print(compradet.unidades, "-", type(compradet.unidades))
    #print(compradet.productodetalle.stock, "-",type(compradet.productodetalle.stock))
    #print(compradet.productodetalle.stock - compradet.unidades)
    #print(compradet.productodetalle.id)

    productodetalleobj =  ProductoDNiveles.objects.get(id=compradet.productodetalle.id)
    productodetalleobj.stock = productodetalleobj.stock - compradet.unidades
    productodetalleobj.entradas = productodetalleobj.entradas - compradet.unidades
    
    #existencia_niveles
    #print(productodetalleobj.producto_nivel.id) # el producto en detella prod
    #print(productodetalleobj.bodega.id) # bodega del producto
    ##Model.objects.filter(x=1, y=2)
    if productodetalleobj.producto_nivel is not None:
        #print("xx----", productodetalleobj.producto_nivel)
        nivelProducto = ProductoDNiveles.objects.get(producto=productodetalleobj.producto_nivel.id, bodega =productodetalleobj.bodega.id)

        nivelProducto.stock = nivelProducto.stock  - (productodetalleobj.unidadxmedida * compradet.unidades)
        nivelProducto.entradas = nivelProducto.entradas  - (productodetalleobj.unidadxmedida * compradet.unidades)
        #print("stock: ", nivelProducto.stock)
        nivelProducto.save()

    if productodetalleobj.producto.tipo_producto == 'N': 
        print(productodetalleobj.producto.tipo_producto)
        embalajeProducto = ProductoDNiveles.objects.get(producto_nivel=productodetalleobj.producto.id, bodega =productodetalleobj.bodega.id)
        embalajeProducto.stock = embalajeProducto.stock  - (compradet.unidades / embalajeProducto.unidadxmedida)
        embalajeProducto.entradas = embalajeProducto.entradas  - (compradet.unidades / embalajeProducto.unidadxmedida)
        embalajeProducto.save()
    

    productodetalleobj.save()
    messages.success(request, 'Se actualizó Stock')

    compradet.delete()
    messages.success(request, 'Se eliminó item')
    

    return redirect('/vistaCompra/'+compradet.compra.numero)

def eliminar_detVenta(request, id):
    compradet = VentaDetalle.objects.get(id=id)

    #print(compradet.unidades, "-", type(compradet.unidades))
    #print(compradet.productodetalle.stock, "-",type(compradet.productodetalle.stock))
    #print(compradet.productodetalle.stock - compradet.unidades)
    #print(compradet.productodetalle.id)

    productodetalleobj =  ProductoDNiveles.objects.get(id=compradet.productodetalle.id)
    productodetalleobj.stock = productodetalleobj.stock + compradet.unidades
    productodetalleobj.salidas = productodetalleobj.salidas - compradet.unidades
    
    #existencia_niveles
    #print(productodetalleobj.producto_nivel.id) # el producto en detella prod
    #print(productodetalleobj.bodega.id) # bodega del producto
    ##Model.objects.filter(x=1, y=2)
    if productodetalleobj.producto_nivel is not None:
        #print("xx----", productodetalleobj.producto_nivel)
        nivelProducto = ProductoDNiveles.objects.get(producto=productodetalleobj.producto_nivel.id, bodega =productodetalleobj.bodega.id)

        nivelProducto.stock = nivelProducto.stock  + (productodetalleobj.unidadxmedida * compradet.unidades)
        nivelProducto.salidas = nivelProducto.salidas  - (productodetalleobj.unidadxmedida * compradet.unidades)
        #print("stock: ", nivelProducto.stock)
        nivelProducto.save()

    if productodetalleobj.producto.tipo_producto == 'N': 
        print(productodetalleobj.producto.tipo_producto)
        embalajeProducto = ProductoDNiveles.objects.get(producto_nivel=productodetalleobj.producto.id, bodega =productodetalleobj.bodega.id)
        embalajeProducto.stock = embalajeProducto.stock  + (compradet.unidades / embalajeProducto.unidadxmedida)
        embalajeProducto.salidas = embalajeProducto.salidas  - (compradet.unidades / embalajeProducto.unidadxmedida)
        embalajeProducto.save()
    

    productodetalleobj.save()
    messages.success(request, 'Se actualizó Stock')

    compradet.delete()
    messages.success(request, 'Se eliminó item')
    

    return redirect('/vistaVenta/'+compradet.venta.numero)