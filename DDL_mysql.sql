CREATE DATABASE ptferreteria_db; 
USE ptferreteria_db;

CREATE TABLE Proveedor(
    nit VARCHAR(15) NOT NULL,
    nombre VARCHAR(75) NOT NULL,
    direccion VARCHAR(150),
    PRIMARY KEY (nit)
);

CREATE TABLE Cliente(
    nit VARCHAR(15) NOT NULL,
    nombre VARCHAR(75) NOT NULL,
    direccion VARCHAR(150),
    PRIMARY KEY (nit)
);

CREATE TABLE Medida(
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(75) UNIQUE not null,
    PRIMARY KEY (id)
);

CREATE TABLE Bodega(
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(75) UNIQUE not null,
    PRIMARY KEY (id)
);

CREATE TABLE Producto(
    id INT NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(75) not null, 
    tipo CHAR(1), /*('P','Producto'),('S','Servicios'), default='P'*/
    tipo_producto CHAR(1), /*('E','Embalaje'),('N','Nivel')), default='N'*/
    fecha_vencimiento DATETIME,
    medida INT,
    PRIMARY KEY (id),
    FOREIGN KEY (medida)
    REFERENCES Medida(id)
);

CREATE TABLE ProductoDNiveles(
    id INT NOT NULL AUTO_INCREMENT,
    producto INT,
    bodega INT,
    
    producto_nivel INT,
    unidadxmedida DECIMAL(9, 2),
    
	precio DECIMAL(9, 2),
    costo DECIMAL(9, 2),
    salidas DECIMAL(9, 2),
    entradas DECIMAL(9, 2),
    stock DECIMAL(9, 2),
    PRIMARY KEY (id),
    UNIQUE u_producto_bodega (producto, bodega),
    CONSTRAINT fk_producto
    FOREIGN KEY (producto)
    REFERENCES Producto(id),
    FOREIGN KEY (bodega)
    REFERENCES Bodega(id),
    CONSTRAINT fk_producto_nivel
    FOREIGN KEY (producto_nivel)
    REFERENCES Producto(id)
);

CREATE TABLE Compra(
    numero VARCHAR(10) NOT NULL,
    fecha DATETIME,
    proveedor VARCHAR(15),
    descripcion VARCHAR(150),
    PRIMARY KEY (numero),
    FOREIGN KEY (proveedor)
    REFERENCES Proveedor(nit)
);

CREATE TABLE CompraDetalle(
    id INT NOT NULL AUTO_INCREMENT,
    compra VARCHAR(10) NOT NULL,
    productodetalle INT,
    
	unidades DECIMAL(9, 2),
    costo DECIMAL(9, 2),
    PRIMARY KEY (id),
    FOREIGN KEY (compra)
    REFERENCES Compra(numero),
    FOREIGN KEY (productodetalle)
    REFERENCES ProductoDNiveles(id)
);

CREATE TABLE Venta(
    numero VARCHAR(10) NOT NULL,
    fecha DATETIME,
    cliente VARCHAR(15),
    descripcion VARCHAR(150),
    PRIMARY KEY (numero),
    FOREIGN KEY (cliente)
    REFERENCES Cliente(nit)
);

CREATE TABLE VentaDetalle(
    id INT NOT NULL AUTO_INCREMENT,
    venta VARCHAR(10) NOT NULL,
    productodetalle INT,
    
	unidades DECIMAL(9, 2),
    precio DECIMAL(9, 2),
    PRIMARY KEY (id),
    FOREIGN KEY (venta)
    REFERENCES Venta(numero),
    FOREIGN KEY (productodetalle)
    REFERENCES ProductoDNiveles(id)
);
