"""
Routes for Categorias endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=List[schemas.CategoriaResponse])
def get_categorias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all categorias with pagination.
    """
    categorias = crud.get_categorias(db, skip=skip, limit=limit)
    return categorias


@router.get("/{categoria_id}", response_model=schemas.CategoriaResponse)
def get_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific categoria by ID.
    """
    categoria = crud.get_categoria(db, categoria_id=categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria


@router.post("/", response_model=schemas.CategoriaResponse, status_code=status.HTTP_201_CREATED)
def create_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new categoria.
    """
    try:
        return crud.create_categoria(db=db, categoria=categoria)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )


@router.put("/{categoria_id}", response_model=schemas.CategoriaResponse)
def update_categoria(
    categoria_id: int,
    categoria: schemas.CategoriaUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing categoria.
    """
    try:
        db_categoria = crud.update_categoria(db, categoria_id=categoria_id, categoria=categoria)
        if db_categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {categoria_id} no encontrada"
            )
        return db_categoria
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )


@router.delete("/{categoria_id}", response_model=schemas.MessageResponse)
def delete_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a categoria.
    """
    try:
        categoria = crud.delete_categoria(db, categoria_id=categoria_id)
        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {categoria_id} no encontrada"
            )
        return {"message": f"Categoría {categoria.Nombre} eliminada exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la categoría porque tiene productos asociados"
        )
