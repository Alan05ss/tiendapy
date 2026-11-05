from datetime import date
from tabulate import tabulate
from validaciones import validar_positivo

UMBRAL_DESC_5 = 50000.0
UMBRAL_DESC_10 = 100000.0


def agregar_al_carrito(inventario, carrito, codigo, cantidad):
    codigo = codigo.strip().upper()
    if codigo not in inventario:
        raise ValueError("El codigo ingresado no existe en el inventario.")

    validar_positivo(cantidad, "cantidad")

    producto = inventario[codigo]
    en_carrito = carrito.get(codigo, 0)
    nuevo_total = en_carrito + cantidad

    if nuevo_total > producto["stock"]:
        raise ValueError(f"Stock insuficiente. Disponible: {producto['stock']}.")

    carrito[codigo] = nuevo_total


def calcular_totales(inventario, carrito):
    subtotal = 0.0
    for codigo, cantidad in carrito.items():
        precio = inventario[codigo]["precio"]
        subtotal += precio * cantidad

    if subtotal >= UMBRAL_DESC_10:
        descuento = subtotal * 0.10
    elif subtotal >= UMBRAL_DESC_5:
        descuento = subtotal * 0.05
    else:
        descuento = 0.0

    total = subtotal - descuento
    return round(subtotal, 2), round(descuento, 2), round(total, 2)


def calcular_cambio(total, pago):
    validar_positivo(pago, "pago recibido")
    if pago < total:
        raise ValueError(f"Pago insuficiente. El total a pagar es ${total:,.2f}.")
    return round(pago - total, 2)


def confirmar_venta(inventario, carrito):
    if len(carrito) == 0:
        raise ValueError("El carrito esta vacio.")

    for codigo, cantidad in carrito.items():
        if cantidad > inventario[codigo]["stock"]:
            raise ValueError(f"No hay suficiente stock para {codigo}.")

    subtotal, descuento, total = calcular_totales(inventario, carrito)

    for codigo, cantidad in carrito.items():
        inventario[codigo]["stock"] -= cantidad

    venta = {
        "fecha": str(date.today()),
        "total": total,
        "items": dict(carrito)
    }
    return venta


def mostrar_carrito(inventario, carrito):
    if len(carrito) == 0:
        print("El carrito esta vacio.")
        return

    filas = []
    for codigo, cantidad in carrito.items():
        prod = inventario[codigo]
        valor = prod["precio"] * cantidad
        filas.append([
            codigo,
            prod["nombre"],
            cantidad,
            f"${prod['precio']:,.2f}",
            f"${valor:,.2f}"
        ])

    encabezados = ["Codigo", "Producto", "Cantidad", "Precio Unit.", "Valor"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))

    subtotal, descuento, total = calcular_totales(inventario, carrito)
    print(f"Subtotal : ${subtotal:,.2f}")
    print(f"Descuento: ${descuento:,.2f}")
    print(f"Total    : ${total:,.2f}")
