"""Test del patron Repository."""

import pytest

from cotizador.modelos import Producto
from cotizador.repositorios import RepositorioProductosMemoria


@pytest.fixture
def repo() -> RepositorioProductosMemoria:
    """Fixture: crea un repositorio limpio para cada test."""
    return RepositorioProductosMemoria()


@pytest.fixture
def producto_ejemplo() -> Producto:
    """Fixture: producto de prueba."""
    return Producto(id="P-1", nombre="Laptop", precio_unitario=1500.0, stock=10)


class TestRepositorioProductosMemoria:
    def test_guardar_y_obtener(
        self, repo: RepositorioProductosMemoria, producto_ejemplo: Producto
    ) -> None:
        repo.guardar(producto_ejemplo)
        recuperado = repo.obtener("P-1")

        assert recuperado is not None
        assert recuperado.nombre == "Laptop"
        assert recuperado.precio_unitario == 1500.0

    def test_obtener_inexistente_retorna_none(
        self, repo: RepositorioProductosMemoria
    ) -> None:
        assert repo.obtener("NO-EXISTE") is None

    def test_listar_vacio(self, repo: RepositorioProductosMemoria) -> None:
        assert repo.listar() == []

    def test_listar_con_productos(
        self, repo: RepositorioProductosMemoria, producto_ejemplo: Producto
    ) -> None:
        repo.guardar(producto_ejemplo)
        lista = repo.listar()

        assert len(lista) == 1
        assert lista[0].id == "P-1"

    def test_guardar_actualiza_si_ya_existe(
        self, repo: RepositorioProductosMemoria, producto_ejemplo: Producto
    ) -> None:
        repo.guardar(producto_ejemplo)

        # Modificamos el producto (mismo ID)
        producto_modificado = Producto(
            id="p-1", nombre="Laptop Pro", precio_unitario=2000.0, stock=5
        )
        repo.guardar(producto_modificado)

        assert len(repo.listar()) == 1
        producto_recuperado = repo.obtener("P-1")
        assert producto_recuperado is not None, (
            "El producto deberia existir en el repositorio"
        )
        assert producto_recuperado.nombre == "Laptop Pro"
