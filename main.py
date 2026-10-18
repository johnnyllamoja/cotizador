"""Punto de entrada de la aplicación (CLI)"""

from pydantic import ValidationError

from cotizador.excepciones import ProductoNoEncontradoError
from cotizador.modelos import ItemCotizacion, Producto
from cotizador.repositorios import RepositorioProductosMemoria
from cotizador.servicios import ServicioCotizacion


def mostrar_menu() -> None:
    print("\n--- SISTEMA DE COTIZACIONES ---")
    print("1. Agregar producto al inventario")
    print("2. Crear una cotización")
    print("3. Salir")


def agregar_producto(repo: RepositorioProductosMemoria) -> None:
    print("\n--- NUEVO PRODUCTO ---")
    try:
        id_prod: str = input("ID del producto (ej. P1): ")
        nombre: str = input("Nombre del producto: ")
        precio: float = float(input("Precio unitario: "))
        stock = int(input("Stock disponoble: "))

        # El modelo valida automáticamnete si los datos sin correctos
        nuevo_producto: Producto = Producto(
            id=id_prod, nombre=nombre, precio_unitario=precio, stock=stock
        )
        repo.guardar(nuevo_producto)
        print(f"Producto '{nuevo_producto.nombre}' agregado correctamente.")

    except ValidationError as e:
        print("\n Error de validación: Revisa los datos ingresados.")
        print(e.errors())
    except ValueError:
        print("Error: El precio debe ser un númeroy el stock un entero.")


def crear_cotizacion(servicio: ServicioCotizacion) -> None:
    print("\n ---NUEVA COTIZACIÓN---")
    try:
        id_cot = input("ID de la cotización (ej. C1)")
        cliente = input("ID del cliente (ej. CLI1)")

        items: list[ItemCotizacion] = []
        while True:
            prod_id = input("ID del producto a cotizar (o 'fin' para terminar): ")
            if prod_id.lower() == "fin":
                break
            cantidad = int(input(f"Cantidad de {prod_id}: "))
            items.append(ItemCotizacion(producto_id=prod_id, cantidad=cantidad))

        if not items:
            print("No agregaste ningún producto a la cotización")
            return

        # El servicio hace la magia (inyectado con la repo)
        cotizacion = servicio.generar_cotizacion(
            id_cotizacion=id_cot, cliente_id=cliente, items=items
        )

        print("\n" + "=" * 30)
        print(f"COTIZACIÓN {cotizacion.id}")
        print(f"CLIENTE: {cotizacion.cliente_id}")
        print(f"Subtotal: ${cotizacion.subtotal:.2f}")
        print(f"Descuento: ${cotizacion.descuento:.2f}")
        print(f"TOTAL A PAGAR: ${cotizacion.total:.2f}")
        print("=" * 30)

    except ProductoNoEncontradoError as e:
        print(f"\n{e}")
    except ValidationError as e:
        print("\n  Error de validación en los datos de la cotización.")
        print(e.errors())
    except ValueError:
        print("\n Error: La cantidad debe ser un número entero.")


def main() -> None:
    print("¡El programa ha arrancado correctamente!")  # <--- AGREGA ESTA LÍNEA
    # 1. Instanciamos el repositorio (Infraestructura)
    repo = RepositorioProductosMemoria()

    # 2. Inyectamos el repositorio en el servicio (Lógica de negocio)
    servicio = ServicioCotizacion(repositorio=repo)

    # Precargamos un par de productos para no empezar vacíos
    repo.guardar(Producto(id="P1", nombre="Teclado", precio_unitario=50.0, stock=10))
    repo.guardar(Producto(id="P2", nombre="Monitor", precio_unitario=200.0, stock=5))
    print("Se han precargado 2 productos: P1(Teclado $50) y P2(Monitor $200)")

    # 3. Bucle principal de la interfaz
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-3): ")

        if opcion == "1":
            agregar_producto(repo)
        elif opcion == "2":
            crear_cotizacion(servicio)
        elif opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
