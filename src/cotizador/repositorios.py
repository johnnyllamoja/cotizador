"""Repositorios de datos del cotizador"""

from abc import ABC, abstractmethod

from cotizador.modelos import Producto


class RepositorioProductos(ABC):
    """Interfaz que define las operaciones de datos para Productos"""

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        """Guarda o actualiza un producto."""
        pass

    @abstractmethod
    def obtener(self, id_producto: str) -> Producto | None:
        """Busca un producto por su ID. Retorna None si no existe."""
        pass

    @abstractmethod
    def listar(self) -> list[Producto]:
        """Retorna todos los productos."""
        pass


class RepositorioProductosMemoria(RepositorioProductos):
    """Implementación de memoria(ideal para test y desarrollo temprano)."""

    def __init__(self) -> None:
        # Usamos un diccionario porque la búsqueda por ID es 0(1)
        self._productos: dict[str, Producto] = {}

    def guardar(self, producto: Producto) -> None:
        self._productos[producto.id] = producto

    def obtener(self, id_producto: str) -> Producto | None:
        # Normalizamos el ID por si el usuario lo pasa en minúsculas
        return self._productos.get(id_producto.strip().upper())

    def listar(self) -> list[Producto]:
        return list(self._productos.values())
