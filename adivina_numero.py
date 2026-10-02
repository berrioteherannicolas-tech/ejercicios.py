import random


def numero_secreto():
    return random.randint(1, 100)


def comparar(intento, secreto):
    if intento == secreto:
        return "acierto"
    elif intento < secreto:
        return "mayor"
    else:
        return "menor"


def adivinar():
    secreto = numero_secreto()
    intentos = 0

    while True:
        intento = int(input("Adivina el número: "))
        intentos += 1
        resultado = comparar(intento, secreto)

        if resultado == "acierto":
            print("¡Acertaste en", intentos, "intentos!")
            break
        elif resultado == "mayor":
            print("El número secreto es mayor")
        else:
            print("El número secreto es menor")


if __name__ == "__main__":
    adivinar()
