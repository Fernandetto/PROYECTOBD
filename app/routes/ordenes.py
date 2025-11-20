"""
Routes for Ordenes endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/ordenes", tags=["Ordenes"])


@router.get("/", response_model=List[schemas.OrdenResponse])
def get_ordenes(
    skip: int = 0,
    limit: int = 100,
    mesa_id: Optional[int] = Query(None, description="Filtrar por mesa"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """
    Get all ordenes with pagination and optional filters.
    """
    ordenes = crud.get_ordenes(db, skip=skip, limit=limit, mesa_id=mesa_id, estado=estado)
    return ordenes


@router.get("/{orden_id}", response_model=schemas.OrdenResponse)
def get_orden(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific orden by ID with all detalles.
    """
    orden = crud.get_orden(db, orden_id=orden_id)
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con ID {orden_id} no encontrada"
        )
    return orden


@router.post("/", response_model=schemas.OrdenResponse, status_code=status.HTTP_201_CREATED)
def create_orden(
    orden: schemas.OrdenCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new orden with optional detalles.
    Validates that mesa and mesero exist, and that products are active.
    """
    try:
        # Validate mesa exists
        mesa = crud.get_mesa(db, orden.MesaId)
        if mesa is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mesa con ID {orden.MesaId} no existe"
            )

        # Validate mesero exists
        mesero = crud.get_mesero(db, orden.MeseroId)
        if mesero is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mesero con ID {orden.MeseroId} no existe"
            )

        # Create orden (validation of products happens in crud)
        return crud.create_orden(db=db, orden=orden)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear orden: {str(e)}"
        )


@router.put("/{orden_id}", response_model=schemas.OrdenResponse)
def update_orden(
    orden_id: int,
    orden: schemas.OrdenUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing orden.
    """
    try:
        # Validate mesa if provided
        if orden.MesaId is not None:
            mesa = crud.get_mesa(db, orden.MesaId)
            if mesa is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Mesa con ID {orden.MesaId} no existe"
                )

        # Validate mesero if provided
        if orden.MeseroId is not None:
            mesero = crud.get_mesero(db, orden.MeseroId)
            if mesero is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Mesero con ID {orden.MeseroId} no existe"
                )

        db_orden = crud.update_orden(db, orden_id=orden_id, orden=orden)
        if db_orden is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Orden con ID {orden_id} no encontrada"
            )
        return db_orden
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar orden: {str(e)}"
        )


@router.post("/{orden_id}/cerrar", response_model=schemas.OrdenResponse)
def close_orden(
    orden_id: int,
    close_data: schemas.OrdenClose,
    db: Session = Depends(get_db)
):
    """
    Close an orden, calculating the final total from all detalles.
    """
    try:
        orden = crud.close_orden(db, orden_id=orden_id, comentarios=close_data.Comentarios)
        if orden is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Orden con ID {orden_id} no encontrada"
            )
        return orden
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{orden_id}", response_model=schemas.MessageResponse)
def delete_orden(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an orden (cascade deletes all detalles).
    """
    orden = crud.delete_orden(db, orden_id=orden_id)
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con ID {orden_id} no encontrada"
        )
    return {"message": f"Orden {orden.OrdenId} eliminada exitosamente"}
