from tabulate import tabulate
from validaciones import validar_positivo


def registrar_producto(inventario, codigo, nombre, categoria, precio, stock, stock_minimo, proveedor):
    codigo = codigo.strip().upper()
    if codigo in inventario:
        raise ValueError("Ya existe un producto con ese codigo.")

    validar_positivo(precio, "precio")
    validar_positivo(stock, "stock")
    validar_positivo(stock_minimo, "stock minimo")

    producto = {
        "codigo": codigo,
        "nombre": nombre.strip(),
        "categoria": categoria.strip(),
        "precio": round(precio, 2),
        "stock": stock,
        "stock_minimo": stock_minimo,
        "proveedor": proveedor.strip()
    }
    inventario[codigo] = producto
    return producto


def buscar_por_codigo(inventario, codigo):
    return inventario.get(codigo.strip().upper())


def buscar_por_categoria(inventario, categoria):
    buscada = categoria.strip().lower()
    resultados = [p for p in inventario.values() if p["categoria"].lower() == buscada]
    return resultados


def modificar_precio(inventario, codigo, nuevo_precio):
    codigo = codigo.strip().upper()
    if codigo not in inventario:
        raise ValueError("El producto no existe.")

    validar_positivo(nuevo_precio, "precio")
    inventario[codigo]["precio"] = round(nuevo_precio, 2)


def modificar_stock(inventario, codigo, nuevo_stock):
    codigo = codigo.strip().upper()
    if codigo not in inventario:
        raise ValueError("El producto no existe.")

    validar_positivo(nuevo_stock, "stock")
    inventario[codigo]["stock"] = nuevo_stock


def eliminar_producto(inventario, codigo):
    codigo = codigo.strip().upper()
    if codigo not in inventario:
        raise ValueError("El producto no existe.")

    return inventario.pop(codigo)


def mostrar_tabla_productos(lista_productos):
    if len(lista_productos) == 0:
        print("No se encontraron productos.")
        return

    ordenados = sorted(lista_productos, key=lambda p: p["codigo"])
    filas = []
    for p in ordenados:
        filas.append([
            p["codigo"],
            p["nombre"],
            p["categoria"],
            f"${p['precio']:,.2f}",
            p["stock"],
            p["stock_minimo"],
            p["proveedor"]
        ])

    encabezados = ["Codigo", "Nombre", "Categoria", "Precio", "Stock", "Minimo", "Proveedor"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))
