import pymysql


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


if __name__ == "__main__":
    guardar("prueba", "1", "conexión correcta")
    for fila in listar(5):
        print(fila)