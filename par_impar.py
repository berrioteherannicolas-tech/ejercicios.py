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

            pares = abs(n) // 2        
            sobra = abs(n) % 2          
            recortado = pares > 10      
            pares = min(pares, 10)
        except ValueError:
            error = "Escribe un número entero."

    return render_template("par_impar.html", resultado=resultado,
                           clase=clase, error=error, pares=pares,
                           sobra=sobra, recortado=recortado)