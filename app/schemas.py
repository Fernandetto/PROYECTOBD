"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator


# ==================== CATEGORIAS ====================
class CategoriaBase(BaseModel):
    Nombre: str = Field(..., max_length=100, description="Nombre de la categoría")
    Descripcion: Optional[str] = Field(None, max_length=250, description="Descripción de la categoría")


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    Nombre: Optional[str] = Field(None, max_length=100)
    Descripcion: Optional[str] = Field(None, max_length=250)


class CategoriaResponse(CategoriaBase):
    CategoriaId: int

    class Config:
        from_attributes = True


# ==================== MESEROS ====================
class MeseroBase(BaseModel):
    Nombre: str = Field(..., max_length=150, description="Nombre del mesero")
    Telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del mesero")
    Email: Optional[str] = Field(None, max_length=150, description="Email del mesero")


class MeseroCreate(MeseroBase):
    FechaIngreso: Optional[date] = Field(None, description="Fecha de ingreso (default: hoy)")


class MeseroUpdate(BaseModel):
    Nombre: Optional[str] = Field(None, max_length=150)
    Telefono: Optional[str] = Field(None, max_length=20)
    Email: Optional[str] = Field(None, max_length=150)


class MeseroResponse(MeseroBase):
    MeseroId: int
    FechaIngreso: date

    class Config:
        from_attributes = True


# ==================== MESAS ====================
class MesaBase(BaseModel):
    Numero: int = Field(..., description="Número de la mesa")
    Capacidad: int = Field(..., gt=0, description="Capacidad de la mesa (debe ser > 0)")
    Estado: str = Field(default="Libre", max_length=20, description="Estado: Libre/Ocupada/Reservada")

    @field_validator('Estado')
    @classmethod
    def validate_estado(cls, v):
        valid_estados = ['Libre', 'Ocupada', 'Reservada']
        if v not in valid_estados:
            raise ValueError(f'Estado debe ser uno de: {", ".join(valid_estados)}')
        return v


class MesaCreate(MesaBase):
    pass


class MesaUpdate(BaseModel):
    Numero: Optional[int] = None
    Capacidad: Optional[int] = Field(None, gt=0)
    Estado: Optional[str] = Field(None, max_length=20)

    @field_validator('Estado')
    @classmethod
    def validate_estado(cls, v):
        if v is not None:
            valid_estados = ['Libre', 'Ocupada', 'Reservada']
            if v not in valid_estados:
                raise ValueError(f'Estado debe ser uno de: {", ".join(valid_estados)}')
        return v


class MesaResponse(MesaBase):
    MesaId: int

    class Config:
        from_attributes = True


# ==================== MENU PRODUCTOS ====================
class MenuProductoBase(BaseModel):
    Nombre: str = Field(..., max_length=200, description="Nombre del producto")
    Descripcion: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    Precio: Decimal = Field(..., ge=0, description="Precio del producto (>= 0)")
    CategoriaId: int = Field(..., description="ID de la categoría")
    Activo: bool = Field(default=True, description="Producto activo/inactivo")


class MenuProductoCreate(MenuProductoBase):
    pass


class MenuProductoUpdate(BaseModel):
    Nombre: Optional[str] = Field(None, max_length=200)
    Descripcion: Optional[str] = Field(None, max_length=500)
    Precio: Optional[Decimal] = Field(None, ge=0)
    CategoriaId: Optional[int] = None
    Activo: Optional[bool] = None


class MenuProductoResponse(MenuProductoBase):
    ProductoId: int

    class Config:
        from_attributes = True


# ==================== DETALLES ORDEN ====================
class DetalleOrdenBase(BaseModel):
    ProductoId: int = Field(..., description="ID del producto")
    Cantidad: int = Field(..., gt=0, description="Cantidad (> 0)")
    PrecioUnitario: Decimal = Field(..., ge=0, description="Precio unitario (>= 0)")
    Estado: str = Field(default="Pendiente", max_length=30, description="Estado del detalle")


class DetalleOrdenCreate(DetalleOrdenBase):
    OrdenId: Optional[int] = Field(None, description="ID de la orden (se asigna automáticamente)")


class DetalleOrdenUpdate(BaseModel):
    Cantidad: Optional[int] = Field(None, gt=0)
    PrecioUnitario: Optional[Decimal] = Field(None, ge=0)
    Estado: Optional[str] = Field(None, max_length=30)


class DetalleOrdenResponse(DetalleOrdenBase):
    DetalleId: int
    OrdenId: int
    Subtotal: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ==================== ORDENES ====================
class OrdenBase(BaseModel):
    MesaId: int = Field(..., description="ID de la mesa")
    MeseroId: int = Field(..., description="ID del mesero")
    Estado: str = Field(default="Abierta", max_length=30, description="Estado de la orden")
    Comentarios: Optional[str] = Field(None, max_length=500, description="Comentarios adicionales")


class OrdenCreate(OrdenBase):
    Detalles: Optional[List[DetalleOrdenCreate]] = Field(default=[], description="Detalles de la orden")


class OrdenUpdate(BaseModel):
    MesaId: Optional[int] = None
    MeseroId: Optional[int] = None
    Estado: Optional[str] = Field(None, max_length=30)
    Comentarios: Optional[str] = Field(None, max_length=500)
    FechaCierre: Optional[datetime] = None


class OrdenClose(BaseModel):
    """Schema for closing an order."""
    Comentarios: Optional[str] = Field(None, max_length=500, description="Comentarios al cerrar")


class OrdenResponse(OrdenBase):
    OrdenId: int
    FechaCreacion: datetime
    FechaCierre: Optional[datetime] = None
    Total: Optional[Decimal] = None
    Detalles: List[DetalleOrdenResponse] = []

    class Config:
        from_attributes = True


# ==================== GENERIC RESPONSES ====================
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    database: str
    timestamp: datetime
