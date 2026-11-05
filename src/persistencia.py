from pathlib import Path

RUTA_INVENTARIO = Path("data") / "inventario.txt"
RUTA_VENTAS = Path("data") / "ventas.txt"


def cargar_inventario():
    inventario = {}
    try:
        with RUTA_INVENTARIO.open("r", encoding="utf-8") as f:
            numero_linea = 0
            for linea in f:
                numero_linea += 1
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue

                partes = linea_limpia.split("|")
                if len(partes) != 7:
                    print(f"Advertencia: linea {numero_linea} corrupta omitida.")
                    continue

                try:
                    codigo = partes[0].strip().upper()
                    nombre = partes[1].strip()
                    categoria = partes[2].strip()
                    precio = float(partes[3].strip())
                    stock = int(partes[4].strip())
                    stock_minimo = int(partes[5].strip())
                    proveedor = partes[6].strip()

                    if codigo == "" or precio <= 0 or stock < 0 or stock_minimo < 0:
                        print(f"Advertencia: datos invalidos en linea {numero_linea}, omitida.")
                        continue

                    inventario[codigo] = {
                        "codigo": codigo,
                        "nombre": nombre,
                        "categoria": categoria,
                        "precio": precio,
                        "stock": stock,
                        "stock_minimo": stock_minimo,
                        "proveedor": proveedor
                    }
                except ValueError:
                    print(f"Advertencia: valores no numericos en linea {numero_linea}, omitida.")
    except FileNotFoundError:
        print("No se encontro inventario.txt. Se inicia con el inventario vacio.")
        RUTA_INVENTARIO.parent.mkdir(parents=True, exist_ok=True)
        with RUTA_INVENTARIO.open("w", encoding="utf-8") as f:
            f.write("")

    return inventario


def guardar_inventario(inventario):
    RUTA_INVENTARIO.parent.mkdir(parents=True, exist_ok=True)
    with RUTA_INVENTARIO.open("w", encoding="utf-8") as f:
        for p in inventario.values():
            linea = (
                p["codigo"] + "|" +
                p["nombre"] + "|" +
                p["categoria"] + "|" +
                str(p["precio"]) + "|" +
                str(p["stock"]) + "|" +
                str(p["stock_minimo"]) + "|" +
                p["proveedor"] + "\n"
            )
            f.write(linea)


def cargar_ventas():
    ventas = []
    if not RUTA_VENTAS.exists():
        RUTA_VENTAS.parent.mkdir(parents=True, exist_ok=True)
        with RUTA_VENTAS.open("w", encoding="utf-8") as f:
            f.write("")
        return ventas

    with RUTA_VENTAS.open("r", encoding="utf-8") as f:
        numero_linea = 0
        for linea in f:
            numero_linea += 1
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue

            partes = linea_limpia.split("|")
            if len(partes) != 3:
                print(f"Advertencia: venta corrupta en linea {numero_linea} omitida.")
                continue

            try:
                fecha = partes[0].strip()
                total = float(partes[1].strip())
                detalle_texto = partes[2].strip()

                if fecha == "" or total <= 0 or detalle_texto == "":
                    print(f"Advertencia: venta invalida en linea {numero_linea} omitida.")
                    continue

                items = {}
                for item in detalle_texto.split(";"):
                    datos_item = item.split(":")
                    if len(datos_item) != 2:
                        raise ValueError("formato de item incorrecto")
                    cod = datos_item[0].strip().upper()
                    cant = int(datos_item[1].strip())
                    if cod == "" or cant <= 0:
                        raise ValueError("cantidad invalida")
                    items[cod] = items.get(cod, 0) + cant

                ventas.append({
                    "fecha": fecha,
                    "total": total,
                    "items": items
                })
            except ValueError:
                print(f"Advertencia: error leyendo venta en linea {numero_linea}, omitida.")

    return ventas


def registrar_venta_archivo(venta):
    RUTA_VENTAS.parent.mkdir(parents=True, exist_ok=True)
    lista_items = []
    for cod, cant in venta["items"].items():
        lista_items.append(f"{cod}:{cant}")

    detalle = ";".join(lista_items)
    linea = f"{venta['fecha']}|{venta['total']}|{detalle}\n"

    with RUTA_VENTAS.open("a", encoding="utf-8") as f:
        f.write(linea)
