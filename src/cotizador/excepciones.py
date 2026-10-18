"""Excepciones personalizadas del dominio del cotizador."""


class ProductoNoEncontradoError(Exception):
    """Se lanza cuando se busca un producto que no existe en el repositorio."""

    pass
