"""Test de la lógica de negocio(Servicios)."""

import pytest

from cotizador.excepciones import ProductoNoEncontradoError
from cotizador.modelos import ItemCotizacion, Producto
from cotizador.repositorios import RepositorioProductosMemoria
from cotizador.servicios import ServicioCotizacion


@pytest.fixture
def repo() -> RepositorioProductosMemoria:
    """Repositorio con algunos productos precargados."""
    repo = RepositorioProductosMemoria()
    repo.guardar(Producto(id="P1", nombre="Teclado", precio_unitario=50.0, stock=10))
    repo.guardar(Producto(id="P2", nombre="Monitor", precio_unitario=200.0, stock=5))
    return repo


@pytest.fixture
def servicio(repo: RepositorioProductosMemoria) -> ServicioCotizacion:
    """Inyectamos el repositorio en el servicio."""
    return ServicioCotizacion(repositorio=repo)


class TestServicioCotizacion:
    def test_calcular_total_sin_descuento(self, servicio: ServicioCotizacion) -> None:
        items = [ItemCotizacion(producto_id="P1", cantidad=1)]  # 50
        assert servicio.calcular_total(items) == 50

    def test_calcular_total_con_varios_items(
        self, servicio: ServicioCotizacion
    ) -> None:
        items = [
            ItemCotizacion(producto_id="P1", cantidad=2),  # 100
            ItemCotizacion(producto_id="P2", cantidad=1),  # 200
        ]
        assert servicio.calcular_total(items) == 300

    def test_producto_inexistente_lanza_error(
        self, servicio: ServicioCotizacion
    ) -> None:
        items = [ItemCotizacion(producto_id="NO EXISTE", cantidad=1)]
        with pytest.raises(ProductoNoEncontradoError):
            servicio.calcular_total(items)

    def test_generar_cotizacion_sin_descuento(
        self, servicio: ServicioCotizacion
    ) -> None:
        items = [ItemCotizacion(producto_id="P1", cantidad=1)]  # subtotal 50.0
        cotizacion = servicio.generar_cotizacion(
            id_cotizacion="C1", cliente_id="CLI1", items=items
        )

        assert cotizacion.subtotal == 50.0
        assert cotizacion.descuento == 0.0
        assert cotizacion.total == 50.0

    def test_generar_cotizacion_con_descuento_10(
        self, servicio: ServicioCotizacion
    ) -> None:
        items = [ItemCotizacion(producto_id="P2", cantidad=1)]  # Subtotal 200
        cotizacion = servicio.generar_cotizacion(
            id_cotizacion="C2", cliente_id="CLI1", items=items
        )

        assert cotizacion.subtotal == 200.0
        assert cotizacion.descuento == 20.0  # 10% de 200
        assert cotizacion.total == 180.0

    def test_generar_cotizacion_con_descuento_15(
        self, servicio: ServicioCotizacion
    ) -> None:
        items = [
            ItemCotizacion(producto_id="P1", cantidad=2),  # 100
            ItemCotizacion(producto_id="P2", cantidad=2),  # 400
        ]  # Subtotal 500 (NO aplica 15% porque debe ser mayor a 500, aplica 10%)
        cotizacion = servicio.generar_cotizacion(
            id_cotizacion="C3", cliente_id="CLI1", items=items
        )
        assert cotizacion.descuento == 50.0
        assert cotizacion.total == 450.0

        items_2 = [
            ItemCotizacion(producto_id="P2", cantidad=3),  # 600
        ]
        cotizacion_2 = servicio.generar_cotizacion(
            id_cotizacion="C4", cliente_id="CLI1", items=items_2
        )

        assert cotizacion_2.subtotal == 600.0
        assert cotizacion_2.descuento == 90.0  # 15% descuento
        assert cotizacion_2.total == 510.0
