"""Implementación de repositorio usando SQlite."""

import sqlite3

from cotizador.modelos import Producto
from cotizador.repositorios import RepositorioProductos


class RepositorioProductosSQlite(RepositorioProductos):
    def __init__(self, ruta_db: str = "cotizador.db") -> None:
        # Conectamos el archivo(si no existe ,SQlite lo crea)
        self.conn = sqlite3.connect(ruta_db)
        # Esto nos permite leer los resultados como diccionarios (más fácil)
        self.conn.row_factory = sqlite3.Row
        self._crear_tabla()

    def _crear_tabla(self) -> None:
        """crea la tabla si es la primera vez que se ejecuta."""
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS productos(
                       id TEXT PRIMARY KEY,
                       nombre TEXT NOT NULL,
                       precio_unitario REAL NOT NULL,
                       stock INTEGER NOT NULL)""")
        self.conn.commit()

    def guardar(self, producto: Producto) -> None:
        """Inserta o actualiza un producto."""
        cursor = self.conn.cursor()
        # INSERT O REPLACE: Si el ID ya existe, lo actualiza. Si no, lo crea.
        cursor.execute(
            """INSERT OR REPLACE INTO productos (id,nombre,precio_unitario,stock)
                       VALUES (?, ?, ?, ?)
                       """,
            (producto.id, producto.nombre, producto.precio_unitario, producto.stock),
        )
        self.conn.commit()

    def obtener(self, id_producto: str) -> Producto | None:
        """Busca un producto po ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM productos WHERE id = ?", (id_producto.strip().upper(),)
        )
        fila = cursor.fetchone()

        if fila is None:
            return None

        # Convertimos la filade la base de datos en un objeto Pydantic
        return Producto(**dict(fila))

    def listar(self) -> list[Producto]:
        """Retorna todos los productos guardados."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()

        return [Producto(**dict(fila)) for fila in filas]
