"""Lógica de negocio del cotizador"""

from cotizador.excepciones import ProductoNoEncontradoError
from cotizador.modelos import Cotizacion, ItemCotizacion
from cotizador.repositorios import RepositorioProductos


class ServicioCotizacion:
    """Servicio encargado de calcular y generar cotizaciones."""

    def __init__(self, repositorio: RepositorioProductos) -> None:
        # Aquí ocurre la Inyección de Dependencias: nos pasan el repositorio por fuera.
        self.repo = repositorio

    def calcular_total(self, items: list[ItemCotizacion]) -> float:
        """Calcula el subtotal de una lista de items sin aplicar descuentos."""
        subtotal: float = 0.0
        for item in items:
            # Buscamos el producto usando el contrato(no sabemos de dónde viene)
            producto = self.repo.obtener(item.producto_id)

            if producto is None:
                raise ProductoNoEncontradoError(
                    f"El producto con ID '{item.producto_id}' no existe"
                )
            # So existe, sumamos su precio por la cantidad
            subtotal += producto.precio_unitario * item.cantidad
        return subtotal

    def generar_cotizacion(
        self, id_cotizacion: str, cliente_id: str, items: list[ItemCotizacion]
    ) -> Cotizacion:
        """Genera una entidad Cotizacion completa con descuentos aplicados."""

        subtotal: float = self.calcular_total(items)
        descuento: float = self._calcular_descuento(subtotal)
        total: float = subtotal - descuento

        # Retomamos el modelo Pydantic validado
        return Cotizacion(
            id=id_cotizacion,
            cliente_id=cliente_id,
            items=items,
            subtotal=subtotal,
            descuento=descuento,
            total=total,
        )

    def _calcular_descuento(self, subtotal: float) -> float:
        """Regla de negocio: descuentos basados en el monto."""

        if subtotal > 500:
            return subtotal * 0.15  # 15% de descuento
        if subtotal > 100:
            return subtotal * 0.10  # 10% de descuento
        return 0.0
