import random

import pymysql
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "escribe-aqui-una-frase-tuya"   # necesaria para usar session
def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ejercicios_py",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
def guardar(ejercicio, entrada, resultado):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO historial (ejercicio, entrada, resultado) "
                "VALUES (%s, %s, %s)",
                (ejercicio, str(entrada), resultado),
            )
        conexion.commit()
    finally:
        conexion.close()
def listar(limite=20):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT ejercicio, entrada, resultado, fecha "
                "FROM historial ORDER BY id DESC LIMIT %s",
                (limite,),
            )
            return cursor.fetchall()
    finally:
        conexion.close()

def par_o_impar(n):
    if n % 2 == 0:
        return f"{n} es par"
    else:
        return f"{n} es impar"
def generar_tabla(n):
    filas = []
    for i in range(1, 11):
        filas.append((n, i, n * i))
    return filas
def numero_secreto():
    return random.randint(1, 100)


def comparar(intento, secreto):
    if intento == secreto:
        return "acierto"
    elif intento < secreto:
        return "mayor"
    else:
        return "menor"
@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/par-impar", methods=["GET", "POST"])
def par_impar():
    resultado = None
    clase = None
    error = None
    pares = 0
    sobra = 0
    recortado = False

    if request.method == "POST":
        try:
            n = int(request.form["numero"])
            resultado = par_o_impar(n)
            if n % 2 == 0:
                clase = "par"
            else:
                clase = "impar"
            guardar("par_impar", n, resultado)

            pares = abs(n) // 2          # parejas completas
            sobra = abs(n) % 2           # 0 o 1 punto sin pareja
            recortado = pares > 10       # no dibujar cientos de puntos
            pares = min(pares, 10)
        except ValueError:
            error = "Escribe un número entero."

    return render_template("par_impar.html", resultado=resultado,
                           clase=clase, error=error, pares=pares,
                           sobra=sobra, recortado=recortado)


@app.route("/tabla", methods=["GET", "POST"])
@app.route("/tabla/<int:n>")
def tabla(n=None):
    error = None

    if request.method == "POST":
        try:
            n = int(request.form["numero"])
            guardar("tabla", n, f"Tabla del {n}")
        except ValueError:
            error = "Escribe un número entero."

    filas = []
    if n is not None:
        filas = generar_tabla(n)

    return render_template("tabla.html", n=n, filas=filas, error=error)


@app.route("/adivina", methods=["GET", "POST"])
def adivina():
    if "secreto" not in session or request.args.get("reiniciar"):
        session["secreto"] = numero_secreto()
        session["intentos"] = 0

    mensaje = None
    error = None
    acerto = False

    if request.method == "POST":
        try:
            intento = int(request.form["intento"])
        except ValueError:
            error = "Escribe un número entero."
        else:
            session["intentos"] += 1
            resultado = comparar(intento, session["secreto"])

            if resultado == "acierto":
                mensaje = f"¡Acertaste en {session['intentos']} intentos!"
                acerto = True
                guardar("adivina", intento, mensaje)
                session.pop("secreto")
            elif resultado == "mayor":
                mensaje = "El número secreto es mayor"
            else:
                mensaje = "El número secreto es menor"

    return render_template("adivina.html", mensaje=mensaje, error=error,
                           acerto=acerto, intentos=session.get("intentos", 0))


@app.route("/historial")
def historial():
    filas = listar(30)
    return render_template("historial.html", filas=filas)


if __name__ == "__main__":
    app.run(debug=True)