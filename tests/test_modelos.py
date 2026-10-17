"""Tests de los modelos de dominio"""

import pytest
from pydantic import ValidationError

from cotizador.modelos import Cotizacion, EstadoCotizacion, ItemCotizacion, Producto


class TestProducto:
    def test_crear_producto_valido(self) -> None:
        producto = Producto(
            id="prod-01", nombre="Laptop", precio_unitario=1500.0, stock=5
        )
        assert producto.id == "PROD-01"  # se normalizó
        assert producto.nombre == "Laptop"
        assert producto.precio_unitario == 1500.0
        assert producto.stock == 5

    def test_precio_debe_ser_positivo(self) -> None:
        with pytest.raises(ValidationError):
            Producto(id="p1", nombre="X", precio_unitario=-10, stock=1)

    def test_nombre_demasiado_corto(self) -> None:
        with pytest.raises(ValidationError):
            Producto(id="p1", nombre="X", precio_unitario=10, stock=1)


class TestItemCotizacion:
    def test_cantidad_minima(self) -> None:
        with pytest.raises(ValidationError):
            ItemCotizacion(producto_id="p1", cantidad=0)


class TestCotizacion:
    def test_cotizacion_vacia_falla(self) -> None:
        with pytest.raises(ValidationError):
            Cotizacion(id="c1", cliente_id="cli1", items=[])

    def test_cotizacion_valida(self) -> None:
        cot = Cotizacion(
            id="c1",
            cliente_id="cli1",
            items=[ItemCotizacion(producto_id="p1", cantidad=2)],
        )
        assert cot.estado == EstadoCotizacion.BORRADOR
        assert cot.total == 0.0
        assert cot.fecha_creacion is not None
