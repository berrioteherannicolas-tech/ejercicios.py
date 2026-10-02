
def generar_tabla(n):
    filas = []
    for i in range(1, 11):
        filas.append((n, i, n * i))
    return filas


if __name__ == "__main__":
    n = int(input("Número: "))
    for a, b, c in generar_tabla(n):
        print(a, "x", b, "=", c)