from tabulate import tabulate


def mostrar_alertas_stock(inventario):
    por_proveedor = {}

    for prod in inventario.values():
        if prod["stock"] <= prod["stock_minimo"]:
            prov = prod["proveedor"]
            if prov not in por_proveedor:
                por_proveedor[prov] = []
            por_proveedor[prov].append(prod)

    if len(por_proveedor) == 0:
        print("No hay productos con stock bajo o agotados.")
        return

    for prov in sorted(por_proveedor.keys()):
        print(f"\nProveedor: {prov}")
        filas = []
        for p in por_proveedor[prov]:
            if p["stock"] == 0:
                estado = "Agotado"
            else:
                estado = "Bajo stock"

            filas.append([
                p["codigo"],
                p["nombre"],
                p["stock"],
                p["stock_minimo"],
                estado
            ])

        encabezados = ["Codigo", "Producto", "Stock", "Minimo", "Estado"]
        print(tabulate(filas, headers=encabezados, tablefmt="grid"))


def mostrar_cierre_dia(inventario, ventas, fecha_filtro=None):
    if fecha_filtro is not None:
        lista_ventas = [v for v in ventas if v["fecha"] == fecha_filtro]
    else:
        lista_ventas = ventas

    numero_ventas = len(lista_ventas)
    total_vendido = 0.0
    unidades_por_codigo = {}

    for v in lista_ventas:
        total_vendido += v["total"]
        for cod, cant in v["items"].items():
            unidades_por_codigo[cod] = unidades_por_codigo.get(cod, 0) + cant

    if numero_ventas > 0:
        ticket_promedio = total_vendido / numero_ventas
    else:
        ticket_promedio = 0.0

    if len(unidades_por_codigo) > 0:
        ordenados = sorted(unidades_por_codigo.items(), key=lambda x: x[1], reverse=True)
        cod_top, cant_top = ordenados[0]
        if cod_top in inventario:
            nombre_top = inventario[cod_top]["nombre"]
        else:
            nombre_top = cod_top
        mas_vendido = f"{nombre_top} ({cant_top} unidades)"
    else:
        mas_vendido = "Ninguno"

    codigos_inventario = set(inventario.keys())
    codigos_vendidos = set(unidades_por_codigo.keys())
    codigos_sin_venta = codigos_inventario - codigos_vendidos

    categorias_movimiento = {
        inventario[c]["categoria"]
        for c in codigos_vendidos
        if c in inventario
    }

    if len(categorias_movimiento) > 0:
        texto_categorias = ", ".join(sorted(categorias_movimiento))
    else:
        texto_categorias = "Ninguna"

    resumen = [
        ["Numero de ventas", numero_ventas],
        ["Total vendido", f"${total_vendido:,.2f}"],
        ["Ticket promedio", f"${ticket_promedio:,.2f}"],
        ["Producto mas vendido", mas_vendido],
        ["Categorias con movimiento", texto_categorias]
    ]
    print(tabulate(resumen, headers=["Dato", "Resultado"], tablefmt="grid"))

    print("\nProductos sin ventas:")
    if len(codigos_sin_venta) == 0:
        print("Todos los productos tuvieron al menos una venta.")
    else:
        filas_sin_venta = []
        for cod in sorted(codigos_sin_venta):
            p = inventario[cod]
            filas_sin_venta.append([p["codigo"], p["nombre"], p["categoria"], p["stock"]])
        print(tabulate(filas_sin_venta, headers=["Codigo", "Producto", "Categoria", "Stock"], tablefmt="grid"))
