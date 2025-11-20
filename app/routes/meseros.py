"""
Routes for Meseros endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/meseros", tags=["Meseros"])


@router.get("/", response_model=List[schemas.MeseroResponse])
def get_meseros(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all meseros with pagination.
    """
    meseros = crud.get_meseros(db, skip=skip, limit=limit)
    return meseros


@router.get("/{mesero_id}", response_model=schemas.MeseroResponse)
def get_mesero(
    mesero_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific mesero by ID.
    """
    mesero = crud.get_mesero(db, mesero_id=mesero_id)
    if mesero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mesero con ID {mesero_id} no encontrado"
        )
    return mesero


@router.post("/", response_model=schemas.MeseroResponse, status_code=status.HTTP_201_CREATED)
def create_mesero(
    mesero: schemas.MeseroCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new mesero.
    """
    try:
        return crud.create_mesero(db=db, mesero=mesero)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear mesero: {str(e)}"
        )


@router.put("/{mesero_id}", response_model=schemas.MeseroResponse)
def update_mesero(
    mesero_id: int,
    mesero: schemas.MeseroUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing mesero.
    """
    db_mesero = crud.update_mesero(db, mesero_id=mesero_id, mesero=mesero)
    if db_mesero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mesero con ID {mesero_id} no encontrado"
        )
    return db_mesero


@router.delete("/{mesero_id}", response_model=schemas.MessageResponse)
def delete_mesero(
    mesero_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a mesero.
    """
    try:
        mesero = crud.delete_mesero(db, mesero_id=mesero_id)
        if mesero is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mesero con ID {mesero_id} no encontrado"
            )
        return {"message": f"Mesero {mesero.Nombre} eliminado exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el mesero porque tiene órdenes asociadas"
        )
