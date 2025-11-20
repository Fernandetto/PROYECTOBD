"""
Routes for MenuProductos endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/menu-productos", tags=["Menu Productos"])


@router.get("/", response_model=List[schemas.MenuProductoResponse])
def get_menu_productos(
    skip: int = 0,
    limit: int = 100,
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    """
    Get all menu productos with pagination and optional filters.
    """
    productos = crud.get_menu_productos(db, skip=skip, limit=limit, categoria_id=categoria_id, activo=activo)
    return productos


@router.get("/{producto_id}", response_model=schemas.MenuProductoResponse)
def get_menu_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific menu producto by ID.
    """
    producto = crud.get_menu_producto(db, producto_id=producto_id)
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto


@router.post("/", response_model=schemas.MenuProductoResponse, status_code=status.HTTP_201_CREATED)
def create_menu_producto(
    producto: schemas.MenuProductoCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new menu producto.
    """
    try:
        # Validate that categoria exists
        categoria = crud.get_categoria(db, producto.CategoriaId)
        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría con ID {producto.CategoriaId} no existe"
            )
        return crud.create_menu_producto(db=db, producto=producto)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear producto: {str(e)}"
        )


@router.put("/{producto_id}", response_model=schemas.MenuProductoResponse)
def update_menu_producto(
    producto_id: int,
    producto: schemas.MenuProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing menu producto.
    """
    try:
        # Validate categoria if provided
        if producto.CategoriaId is not None:
            categoria = crud.get_categoria(db, producto.CategoriaId)
            if categoria is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Categoría con ID {producto.CategoriaId} no existe"
                )

        db_producto = crud.update_menu_producto(db, producto_id=producto_id, producto=producto)
        if db_producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return db_producto
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar producto: {str(e)}"
        )


@router.delete("/{producto_id}", response_model=schemas.MessageResponse)
def delete_menu_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a menu producto.
    """
    try:
        producto = crud.delete_menu_producto(db, producto_id=producto_id)
        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return {"message": f"Producto {producto.Nombre} eliminado exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el producto porque está en detalles de órdenes"
        )
