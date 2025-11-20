"""
SQLAlchemy models for restaurant database.
Maps to the 'restaurante' schema in Azure SQL Server.
"""
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Date, Boolean, ForeignKey, CheckConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Categoria(Base):
    """Model for Categorias table."""
    __tablename__ = "Categorias"
    __table_args__ = {'schema': 'restaurante'}

    CategoriaId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False, unique=True)
    Descripcion = Column(String(250), nullable=True)

    # Relationships
    productos = relationship("MenuProducto", back_populates="categoria")


class Mesero(Base):
    """Model for Meseros table."""
    __tablename__ = "Meseros"
    __table_args__ = {'schema': 'restaurante'}

    MeseroId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(150), nullable=False)
    Telefono = Column(String(20), nullable=True)
    Email = Column(String(150), nullable=True)
    FechaIngreso = Column(Date, nullable=False, server_default=text('GETDATE()'))

    # Relationships
    ordenes = relationship("Orden", back_populates="mesero")


class Mesa(Base):
    """Model for Mesas table."""
    __tablename__ = "Mesas"
    __table_args__ = (
        CheckConstraint('Capacidad > 0', name='CK_Mesas_Capacidad'),
        {'schema': 'restaurante'}
    )

    MesaId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Numero = Column(Integer, nullable=False, unique=True)
    Capacidad = Column(Integer, nullable=False)
    Estado = Column(String(20), nullable=False, server_default="'Libre'")

    # Relationships
    ordenes = relationship("Orden", back_populates="mesa")


class MenuProducto(Base):
    """Model for MenuProductos table."""
    __tablename__ = "MenuProductos"
    __table_args__ = (
        CheckConstraint('Precio >= 0', name='CK_MenuProductos_Precio'),
        {'schema': 'restaurante'}
    )

    ProductoId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(200), nullable=False)
    Descripcion = Column(String(500), nullable=True)
    Precio = Column(DECIMAL(10, 2), nullable=False)
    CategoriaId = Column(Integer, ForeignKey('restaurante.Categorias.CategoriaId'), nullable=False, index=True)
    Activo = Column(Boolean, nullable=False, server_default='1')

    # Relationships
    categoria = relationship("Categoria", back_populates="productos")
    detalles_orden = relationship("DetalleOrden", back_populates="producto")


class Orden(Base):
    """Model for Ordenes table."""
    __tablename__ = "Ordenes"
    __table_args__ = {'schema': 'restaurante'}

    OrdenId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    MesaId = Column(Integer, ForeignKey('restaurante.Mesas.MesaId'), nullable=False, index=True)
    MeseroId = Column(Integer, ForeignKey('restaurante.Meseros.MeseroId'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text('SYSUTCDATETIME()'))
    FechaCierre = Column(DateTime, nullable=True)
    Total = Column(DECIMAL(12, 2), nullable=True)
    Estado = Column(String(30), nullable=False, server_default="'Abierta'")
    Comentarios = Column(String(500), nullable=True)

    # Relationships
    mesa = relationship("Mesa", back_populates="ordenes")
    mesero = relationship("Mesero", back_populates="ordenes")
    detalles = relationship("DetalleOrden", back_populates="orden", cascade="all, delete-orphan")


class DetalleOrden(Base):
    """Model for DetallesOrden table."""
    __tablename__ = "DetallesOrden"
    __table_args__ = (
        CheckConstraint('Cantidad > 0', name='CK_DetallesOrden_Cantidad'),
        CheckConstraint('PrecioUnitario >= 0', name='CK_DetallesOrden_PrecioUnitario'),
        {'schema': 'restaurante'}
    )

    DetalleId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    OrdenId = Column(Integer, ForeignKey('restaurante.Ordenes.OrdenId', ondelete='CASCADE'), nullable=False, index=True)
    ProductoId = Column(Integer, ForeignKey('restaurante.MenuProductos.ProductoId'), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    PrecioUnitario = Column(DECIMAL(10, 2), nullable=False)
    # Subtotal is a computed column in SQL Server, we'll calculate it in the application
    Subtotal = Column(DECIMAL(12, 2), nullable=True)
    Estado = Column(String(30), nullable=False, server_default="'Pendiente'")

    # Relationships
    orden = relationship("Orden", back_populates="detalles")
    producto = relationship("MenuProducto", back_populates="detalles_orden")
