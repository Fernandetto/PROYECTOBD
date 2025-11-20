"""
CRUD operations for all database entities.
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

import models
import schemas


# ==================== CATEGORIAS ====================
def get_categoria(db: Session, categoria_id: int):
    """Get a single categoria by ID."""
    return db.query(models.Categoria).filter(models.Categoria.CategoriaId == categoria_id).first()


def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    """Get all categorias with pagination."""
    return db.query(models.Categoria).offset(skip).limit(limit).all()


def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """Create a new categoria."""
    db_categoria = models.Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaUpdate):
    """Update an existing categoria."""
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria is None:
        return None

    update_data = categoria.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_categoria, key, value)

    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def delete_categoria(db: Session, categoria_id: int):
    """Delete a categoria."""
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria is None:
        return None

    db.delete(db_categoria)
    db.commit()
    return db_categoria


# ==================== MESEROS ====================
def get_mesero(db: Session, mesero_id: int):
    """Get a single mesero by ID."""
    return db.query(models.Mesero).filter(models.Mesero.MeseroId == mesero_id).first()


def get_meseros(db: Session, skip: int = 0, limit: int = 100):
    """Get all meseros with pagination."""
    return db.query(models.Mesero).offset(skip).limit(limit).all()


def create_mesero(db: Session, mesero: schemas.MeseroCreate):
    """Create a new mesero."""
    db_mesero = models.Mesero(**mesero.model_dump(exclude_none=True))
    db.add(db_mesero)
    db.commit()
    db.refresh(db_mesero)
    return db_mesero


def update_mesero(db: Session, mesero_id: int, mesero: schemas.MeseroUpdate):
    """Update an existing mesero."""
    db_mesero = get_mesero(db, mesero_id)
    if db_mesero is None:
        return None

    update_data = mesero.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_mesero, key, value)

    db.commit()
    db.refresh(db_mesero)
    return db_mesero


def delete_mesero(db: Session, mesero_id: int):
    """Delete a mesero."""
    db_mesero = get_mesero(db, mesero_id)
    if db_mesero is None:
        return None

    db.delete(db_mesero)
    db.commit()
    return db_mesero


# ==================== MESAS ====================
def get_mesa(db: Session, mesa_id: int):
    """Get a single mesa by ID."""
    return db.query(models.Mesa).filter(models.Mesa.MesaId == mesa_id).first()


def get_mesas(db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None):
    """Get all mesas with pagination and optional estado filter."""
    query = db.query(models.Mesa)
    if estado:
        query = query.filter(models.Mesa.Estado == estado)
    return query.offset(skip).limit(limit).all()


def create_mesa(db: Session, mesa: schemas.MesaCreate):
    """Create a new mesa."""
    db_mesa = models.Mesa(**mesa.model_dump())
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa


def update_mesa(db: Session, mesa_id: int, mesa: schemas.MesaUpdate):
    """Update an existing mesa."""
    db_mesa = get_mesa(db, mesa_id)
    if db_mesa is None:
        return None

    update_data = mesa.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_mesa, key, value)

    db.commit()
    db.refresh(db_mesa)
    return db_mesa


def delete_mesa(db: Session, mesa_id: int):
    """Delete a mesa."""
    db_mesa = get_mesa(db, mesa_id)
    if db_mesa is None:
        return None

    db.delete(db_mesa)
    db.commit()
    return db_mesa


# ==================== MENU PRODUCTOS ====================
def get_menu_producto(db: Session, producto_id: int):
    """Get a single menu producto by ID."""
    return db.query(models.MenuProducto).filter(models.MenuProducto.ProductoId == producto_id).first()


def get_menu_productos(db: Session, skip: int = 0, limit: int = 100, categoria_id: Optional[int] = None, activo: Optional[bool] = None):
    """Get all menu productos with pagination and optional filters."""
    query = db.query(models.MenuProducto)
    if categoria_id:
        query = query.filter(models.MenuProducto.CategoriaId == categoria_id)
    if activo is not None:
        query = query.filter(models.MenuProducto.Activo == activo)
    return query.offset(skip).limit(limit).all()


def create_menu_producto(db: Session, producto: schemas.MenuProductoCreate):
    """Create a new menu producto."""
    db_producto = models.MenuProducto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_menu_producto(db: Session, producto_id: int, producto: schemas.MenuProductoUpdate):
    """Update an existing menu producto."""
    db_producto = get_menu_producto(db, producto_id)
    if db_producto is None:
        return None

    update_data = producto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete_menu_producto(db: Session, producto_id: int):
    """Delete a menu producto."""
    db_producto = get_menu_producto(db, producto_id)
    if db_producto is None:
        return None

    db.delete(db_producto)
    db.commit()
    return db_producto


# ==================== ORDENES ====================
def get_orden(db: Session, orden_id: int):
    """Get a single orden by ID with detalles."""
    return db.query(models.Orden).options(joinedload(models.Orden.detalles)).filter(models.Orden.OrdenId == orden_id).first()


def get_ordenes(db: Session, skip: int = 0, limit: int = 100, mesa_id: Optional[int] = None, estado: Optional[str] = None):
    """Get all ordenes with pagination and optional filters."""
    query = db.query(models.Orden).options(joinedload(models.Orden.detalles))
    if mesa_id:
        query = query.filter(models.Orden.MesaId == mesa_id)
    if estado:
        query = query.filter(models.Orden.Estado == estado)
    return query.offset(skip).limit(limit).all()


def create_orden(db: Session, orden: schemas.OrdenCreate):
    """Create a new orden with detalles."""
    # Create the orden
    orden_data = orden.model_dump(exclude={'Detalles'})
    db_orden = models.Orden(**orden_data)
    db.add(db_orden)
    db.flush()  # Flush to get the OrdenId

    # Add detalles if provided
    total = Decimal('0.00')
    if orden.Detalles:
        for detalle in orden.Detalles:
            # Validate that the product is active
            producto = get_menu_producto(db, detalle.ProductoId)
            if producto is None:
                db.rollback()
                raise ValueError(f"Producto {detalle.ProductoId} no existe")
            if not producto.Activo:
                db.rollback()
                raise ValueError(f"Producto {producto.Nombre} no está activo")

            # Calculate subtotal
            subtotal = detalle.Cantidad * detalle.PrecioUnitario
            total += subtotal

            # Create detalle
            db_detalle = models.DetalleOrden(
                OrdenId=db_orden.OrdenId,
                ProductoId=detalle.ProductoId,
                Cantidad=detalle.Cantidad,
                PrecioUnitario=detalle.PrecioUnitario,
                Subtotal=subtotal,
                Estado=detalle.Estado
            )
            db.add(db_detalle)

    # Update total
    db_orden.Total = total

    db.commit()
    db.refresh(db_orden)
    return db_orden


def update_orden(db: Session, orden_id: int, orden: schemas.OrdenUpdate):
    """Update an existing orden."""
    db_orden = get_orden(db, orden_id)
    if db_orden is None:
        return None

    update_data = orden.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_orden, key, value)

    db.commit()
    db.refresh(db_orden)
    return db_orden


def close_orden(db: Session, orden_id: int, comentarios: Optional[str] = None):
    """Close an orden and calculate final total."""
    db_orden = get_orden(db, orden_id)
    if db_orden is None:
        return None

    if db_orden.Estado == "Cerrada":
        raise ValueError("La orden ya está cerrada")

    # Calculate total from detalles
    total = Decimal('0.00')
    for detalle in db_orden.detalles:
        if detalle.Subtotal:
            total += detalle.Subtotal

    # Update orden
    db_orden.Total = total
    db_orden.Estado = "Cerrada"
    db_orden.FechaCierre = datetime.utcnow()
    if comentarios:
        db_orden.Comentarios = comentarios

    db.commit()
    db.refresh(db_orden)
    return db_orden


def delete_orden(db: Session, orden_id: int):
    """Delete an orden (cascade deletes detalles)."""
    db_orden = get_orden(db, orden_id)
    if db_orden is None:
        return None

    db.delete(db_orden)
    db.commit()
    return db_orden


# ==================== DETALLES ORDEN ====================
def get_detalle_orden(db: Session, detalle_id: int):
    """Get a single detalle orden by ID."""
    return db.query(models.DetalleOrden).filter(models.DetalleOrden.DetalleId == detalle_id).first()


def get_detalles_orden(db: Session, orden_id: int):
    """Get all detalles for a specific orden."""
    return db.query(models.DetalleOrden).filter(models.DetalleOrden.OrdenId == orden_id).all()


def create_detalle_orden(db: Session, detalle: schemas.DetalleOrdenCreate):
    """Create a new detalle orden and update orden total."""
    # Validate orden exists
    orden = get_orden(db, detalle.OrdenId)
    if orden is None:
        raise ValueError(f"Orden {detalle.OrdenId} no existe")

    # Validate product is active
    producto = get_menu_producto(db, detalle.ProductoId)
    if producto is None:
        raise ValueError(f"Producto {detalle.ProductoId} no existe")
    if not producto.Activo:
        raise ValueError(f"Producto {producto.Nombre} no está activo")

    # Calculate subtotal
    subtotal = detalle.Cantidad * detalle.PrecioUnitario

    # Create detalle
    db_detalle = models.DetalleOrden(
        **detalle.model_dump(exclude_none=True),
        Subtotal=subtotal
    )
    db.add(db_detalle)

    # Update orden total
    if orden.Total is None:
        orden.Total = Decimal('0.00')
    orden.Total += subtotal

    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def update_detalle_orden(db: Session, detalle_id: int, detalle: schemas.DetalleOrdenUpdate):
    """Update an existing detalle orden and recalculate totals."""
    db_detalle = get_detalle_orden(db, detalle_id)
    if db_detalle is None:
        return None

    # Store old subtotal
    old_subtotal = db_detalle.Subtotal or Decimal('0.00')

    # Update detalle
    update_data = detalle.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_detalle, key, value)

    # Recalculate subtotal if cantidad or precio changed
    if 'Cantidad' in update_data or 'PrecioUnitario' in update_data:
        db_detalle.Subtotal = db_detalle.Cantidad * db_detalle.PrecioUnitario

    # Update orden total
    orden = get_orden(db, db_detalle.OrdenId)
    if orden:
        new_subtotal = db_detalle.Subtotal or Decimal('0.00')
        if orden.Total is None:
            orden.Total = Decimal('0.00')
        orden.Total = orden.Total - old_subtotal + new_subtotal

    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def delete_detalle_orden(db: Session, detalle_id: int):
    """Delete a detalle orden and update orden total."""
    db_detalle = get_detalle_orden(db, detalle_id)
    if db_detalle is None:
        return None

    # Update orden total
    orden = get_orden(db, db_detalle.OrdenId)
    if orden and orden.Total and db_detalle.Subtotal:
        orden.Total -= db_detalle.Subtotal

    db.delete(db_detalle)
    db.commit()
    return db_detalle
