from datetime import date
import inventario
import ventas
import reportes
import persistencia
from validaciones import leer_texto, leer_entero, leer_flotante


def submenu_inventario(productos):
    while True:
        print("\n--- GESTION DE INVENTARIO ---")
        print("1. Listar productos")
        print("2. Registrar producto")
        print("3. Buscar por codigo")
        print("4. Buscar por categoria")
        print("5. Modificar precio o stock")
        print("6. Eliminar producto")
        print("0. Volver")

        op = input("Opcion: ").strip()

        if op == "1":
            inventario.mostrar_tabla_productos(list(productos.values()))

        elif op == "2":
            codigo = leer_texto("Codigo: ")
            nombre = leer_texto("Nombre: ")
            categoria = leer_texto("Categoria: ")
            precio = leer_flotante("Precio: ")
            stock = leer_entero("Stock inicial: ")
            stock_min = leer_entero("Stock minimo: ")
            proveedor = leer_texto("Proveedor: ")

            try:
                inventario.registrar_producto(
                    productos, codigo, nombre, categoria, precio, stock, stock_min, proveedor
                )
                print("Producto registrado correctamente.")
            except ValueError as e:
                print("Error:", e)

        elif op == "3":
            codigo = leer_texto("Codigo a buscar: ")
            prod = inventario.buscar_por_codigo(productos, codigo)
            if prod is None:
                print("No existe un producto con ese codigo.")
            else:
                inventario.mostrar_tabla_productos([prod])

        elif op == "4":
            categoria = leer_texto("Categoria a buscar: ")
            encontrados = inventario.buscar_por_categoria(productos, categoria)
            if len(encontrados) == 0:
                print("No hay productos registrados en esa categoria.")
            else:
                inventario.mostrar_tabla_productos(encontrados)

        elif op == "5":
            codigo = leer_texto("Codigo del producto: ")
            prod = inventario.buscar_por_codigo(productos, codigo)
            if prod is None:
                print("No existe un producto con ese codigo.")
                continue

            inventario.mostrar_tabla_productos([prod])
            print("1. Cambiar precio")
            print("2. Cambiar stock")
            sub = input("Opcion: ").strip()

            try:
                if sub == "1":
                    nuevo_precio = leer_flotante("Nuevo precio: ")
                    inventario.modificar_precio(productos, codigo, nuevo_precio)
                    print("Precio actualizado.")
                elif sub == "2":
                    nuevo_stock = leer_entero("Nuevo stock: ")
                    inventario.modificar_stock(productos, codigo, nuevo_stock)
                    print("Stock actualizado.")
                else:
                    print("Opcion no valida.")
            except ValueError as e:
                print("Error:", e)

        elif op == "6":
            codigo = leer_texto("Codigo del producto a eliminar: ")
            try:
                eliminado = inventario.eliminar_producto(productos, codigo)
                print(f"Producto '{eliminado['nombre']}' eliminado.")
            except ValueError as e:
                print("Error:", e)

        elif op == "0":
            break
        else:
            print("Opcion no valida.")


def submenu_ventas(productos, lista_ventas):
    if len(productos) == 0:
        print("El inventario esta vacio.")
        return

    carrito = {}
    while True:
        print("\n--- REGISTRO DE VENTA ---")
        print("1. Agregar producto al carrito")
        print("2. Ver carrito")
        print("3. Confirmar venta y pagar")
        print("0. Cancelar venta")

        op = input("Opcion: ").strip()

        if op == "1":
            codigo = leer_texto("Codigo del producto: ")
            prod = inventario.buscar_por_codigo(productos, codigo)
            if prod is None:
                print("El producto no existe.")
                continue

            print(f"{prod['nombre']} - Precio: ${prod['precio']:,.2f} - Disponible: {prod['stock']}")
            cantidad = leer_entero("Cantidad: ")

            try:
                ventas.agregar_al_carrito(productos, carrito, codigo, cantidad)
                print("Producto agregado al carrito.")
            except ValueError as e:
                print("Error:", e)

        elif op == "2":
            ventas.mostrar_carrito(productos, carrito)

        elif op == "3":
            if len(carrito) == 0:
                print("Debe agregar al menos un producto.")
                continue

            print("\nDetalle de la compra:")
            ventas.mostrar_carrito(productos, carrito)
            subtotal, descuento, total = ventas.calcular_totales(productos, carrito)

            while True:
                pago = leer_flotante("Pago recibido: ")
                try:
                    cambio = ventas.calcular_cambio(total, pago)
                    break
                except ValueError as e:
                    print("Error:", e)

            try:
                nueva_venta = ventas.confirmar_venta(productos, carrito)
                persistencia.registrar_venta_archivo(nueva_venta)
                persistencia.guardar_inventario(productos)
                lista_ventas.append(nueva_venta)
                print(f"Venta confirmada. Cambio a entregar: ${cambio:,.2f}")
                break
            except ValueError as e:
                print("Error al confirmar:", e)

        elif op == "0":
            print("Venta cancelada.")
            break
        else:
            print("Opcion no valida.")


def menu_principal():
    productos = persistencia.cargar_inventario()
    lista_ventas = persistencia.cargar_ventas()

    while True:
        print("\n--- TIENDAPY - TIENDA DON AURELIO ---")
        print("1. Gestion de inventario")
        print("2. Registrar venta")
        print("3. Alertas de stock")
        print("4. Cierre del dia")
        print("5. Guardar inventario")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            submenu_inventario(productos)
        elif opcion == "2":
            submenu_ventas(productos, lista_ventas)
        elif opcion == "3":
            print("\n--- ALERTAS DE STOCK ---")
            reportes.mostrar_alertas_stock(productos)
        elif opcion == "4":
            hoy = str(date.today())
            print(f"\n--- CIERRE DEL DIA ({hoy}) ---")
            entrada = input("Enter para hoy o escriba 'todas' para el historial: ").strip()
            if entrada.lower() == "todas":
                reportes.mostrar_cierre_dia(productos, lista_ventas)
            else:
                reportes.mostrar_cierre_dia(productos, lista_ventas, hoy)
        elif opcion == "5":
            persistencia.guardar_inventario(productos)
            print("Inventario guardado.")
        elif opcion == "0":
            persistencia.guardar_inventario(productos)
            print("Cambios guardados. Saliendo...")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu_principal()
