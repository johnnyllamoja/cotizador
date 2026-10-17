"""Modelos  de dominio de cotizador."""

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class EstadoCotizacion(StrEnum):
    """Estados posibles de una cotización."""

    BORRADOR = "borrador"
    ENVIADA = "enviada"
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"


class Producto(BaseModel):
    """Producto del catálogo"""

    id: str = Field(min_length=1, max_length=50, description="Identificador único")
    nombre: str = Field(min_length=2, max_length=100, description="Nombre del producto")
    precio_unitario: float = Field(gt=0, description="Precio unitario mayor a 0 ")
    stock: int = Field(ge=0, description="Unidades disponibles en stock")

    @field_validator("id")
    @classmethod
    def normalizar_id(cls, valor: str) -> str:
        return valor.strip().upper()


class Cliente(BaseModel):
    """Cliente al que se cotiza"""

    id: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=2, max_length=100)
    email: str | None = Field(default=None, max_length=120)
    telefono: str | None = Field(default=None, max_length=20)

    @field_validator("id")
    @classmethod
    def normalizar_id(cls, valor: str) -> str:
        return valor.strip().upper()

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, mail: str) -> str:
        if "@" not in mail:
            raise ValueError("Error: correo no válido")
        return mail.strip().lower()


class ItemCotizacion(BaseModel):
    """Línea de una cotización: un producto con su cantidad."""

    producto_id: str = Field(min_length=1, max_length=50)
    cantidad: int = Field(ge=1, description="Cantiadad mayor o igual a 1")


class Cotizacion(BaseModel):
    """Cotización completa."""

    id: str = Field(min_length=1, max_length=50)
    cliente_id: str = Field(min_length=1, max_length=50)
    items: list[ItemCotizacion] = Field(min_length=1, description="Al menos un item")
    estado: EstadoCotizacion = EstadoCotizacion.BORRADOR
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(UTC))
    subtotal: float = Field(default=0.0, ge=0)
    descuento: float = Field(default=0.0, ge=0)
    total: float = Field(default=0.0, ge=0)
