"""
Routes for Mesas endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/mesas", tags=["Mesas"])


@router.get("/", response_model=List[schemas.MesaResponse])
def get_mesas(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = Query(None, description="Filtrar por estado: Libre, Ocupada, Reservada"),
    db: Session = Depends(get_db)
):
    """
    Get all mesas with pagination and optional estado filter.
    """
    mesas = crud.get_mesas(db, skip=skip, limit=limit, estado=estado)
    return mesas


@router.get("/{mesa_id}", response_model=schemas.MesaResponse)
def get_mesa(
    mesa_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific mesa by ID.
    """
    mesa = crud.get_mesa(db, mesa_id=mesa_id)
    if mesa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mesa con ID {mesa_id} no encontrada"
        )
    return mesa


@router.post("/", response_model=schemas.MesaResponse, status_code=status.HTTP_201_CREATED)
def create_mesa(
    mesa: schemas.MesaCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new mesa.
    """
    try:
        return crud.create_mesa(db=db, mesa=mesa)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una mesa con ese número"
        )


@router.put("/{mesa_id}", response_model=schemas.MesaResponse)
def update_mesa(
    mesa_id: int,
    mesa: schemas.MesaUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing mesa.
    """
    try:
        db_mesa = crud.update_mesa(db, mesa_id=mesa_id, mesa=mesa)
        if db_mesa is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mesa con ID {mesa_id} no encontrada"
            )
        return db_mesa
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una mesa con ese número"
        )


@router.delete("/{mesa_id}", response_model=schemas.MessageResponse)
def delete_mesa(
    mesa_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a mesa.
    """
    try:
        mesa = crud.delete_mesa(db, mesa_id=mesa_id)
        if mesa is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mesa con ID {mesa_id} no encontrada"
            )
        return {"message": f"Mesa {mesa.Numero} eliminada exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la mesa porque tiene órdenes asociadas"
        )
