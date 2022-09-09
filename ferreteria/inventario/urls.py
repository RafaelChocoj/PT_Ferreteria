from django.urls import path
from . import views

urlpatterns = [

    #productos
    path('', views.list_proveedores),
    path('eliminarProveedor/<nit>', views.eliminar_proveedor, name='eliminarProveedor'),
    path('vnewProveedor/', views.vnewProveedor, name='vnewProveedor'),
    path('newProveedor/', views.newProveedor, name='newProveedor'),
    path('edicionProveedor/<nit>', views.vistaEditProveedor, name='vistaEditProveedor'),
    path('editarProveedor/', views.editarProveedor, name='editarProveedor'),
    
    #producto
    path('homeProducto/', views.list_productos, name='homeProducto'),
    path('vistaProducto/<id>', views.vistaProducto, name='vistaProducto'),

    #compras
    path('homeCompras/', views.list_compras, name='homeCompras'),
    path('eliminar_compra/<numero>', views.eliminar_compra, name='eliminar_compra'),
    path('vnewCompra/', views.vnewCompra, name='vnewCompra'),
    path('newCompra/', views.newCompra, name='newCompra'),
    path('vistaCompra/<numero>', views.vistaCompra, name='vistaCompra'),

    path('addProductoCompra/<numero>', views.addProductoCompra, name='addProductoCompra'),
    path('eliminar_detCompra/<id>', views.eliminar_detCompra, name='eliminar_detCompra'),

    #Ventas
    path('homeVentas/', views.list_ventas, name='homeVentas'),
    path('eliminar_venta/<numero>', views.eliminar_venta, name='eliminar_venta'),
    path('vnewVenta/', views.vnewVenta, name='vnewVenta'),
    path('newVenta/', views.newVenta, name='newVenta'),
    path('vistaVenta/<numero>', views.vistaVenta, name='vistaVenta'),

    path('addProductoVenta/<numero>', views.addProductoVenta, name='addProductoVenta'),
    path('eliminar_detVenta/<id>', views.eliminar_detVenta, name='eliminar_detVenta'),
]