def validar_positivo(valor, campo):
    if valor <= 0:
        raise ValueError(f"El {campo} debe ser mayor a cero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("El campo no puede estar vacio.")
        elif "|" in texto or ";" in texto or ":" in texto:
            print("El texto contiene caracteres no permitidos.")
        else:
            return texto


def leer_entero(mensaje):
    while True:
        dato = input(mensaje).strip()
        try:
            return int(dato)
        except ValueError:
            print("Entrada invalida. Ingrese un numero entero.")


def leer_flotante(mensaje):
    while True:
        dato = input(mensaje).strip()
        try:
            return float(dato)
        except ValueError:
            print("Entrada invalida. Ingrese un numero valido.")
