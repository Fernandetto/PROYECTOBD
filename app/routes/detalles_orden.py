"""
Routes for DetallesOrden endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/detalles-orden", tags=["Detalles Orden"])


@router.get("/orden/{orden_id}", response_model=List[schemas.DetalleOrdenResponse])
def get_detalles_by_orden(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all detalles for a specific orden.
    """
    # Validate orden exists
    orden = crud.get_orden(db, orden_id)
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con ID {orden_id} no encontrada"
        )

    detalles = crud.get_detalles_orden(db, orden_id=orden_id)
    return detalles


@router.get("/{detalle_id}", response_model=schemas.DetalleOrdenResponse)
def get_detalle_orden(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific detalle orden by ID.
    """
    detalle = crud.get_detalle_orden(db, detalle_id=detalle_id)
    if detalle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detalle con ID {detalle_id} no encontrado"
        )
    return detalle


@router.post("/", response_model=schemas.DetalleOrdenResponse, status_code=status.HTTP_201_CREATED)
def create_detalle_orden(
    detalle: schemas.DetalleOrdenCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new detalle orden.
    Validates that orden exists and product is active.
    Updates orden total automatically.
    """
    try:
        return crud.create_detalle_orden(db=db, detalle=detalle)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear detalle: {str(e)}"
        )


@router.put("/{detalle_id}", response_model=schemas.DetalleOrdenResponse)
def update_detalle_orden(
    detalle_id: int,
    detalle: schemas.DetalleOrdenUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing detalle orden.
    Recalculates subtotal and updates orden total automatically.
    """
    try:
        db_detalle = crud.update_detalle_orden(db, detalle_id=detalle_id, detalle=detalle)
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detalle con ID {detalle_id} no encontrado"
            )
        return db_detalle
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar detalle: {str(e)}"
        )


@router.delete("/{detalle_id}", response_model=schemas.MessageResponse)
def delete_detalle_orden(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a detalle orden.
    Updates orden total automatically.
    """
    detalle = crud.delete_detalle_orden(db, detalle_id=detalle_id)
    if detalle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detalle con ID {detalle_id} no encontrado"
        )
    return {"message": f"Detalle {detalle.DetalleId} eliminado exitosamente"}
