from flask import Flask, render_template, request, jsonify
from ia import obtener_respuesta

app = Flask(__name__)




@app.route("/", methods=['POST', 'GET'])
def inicio():
    datos = ""
    ia_escogida = ""
    promt = ""
    file = ""
    if(request.method == "POST"):
        promt = request.form['prompt']
        accion_usuario = request.form['ia-escogida']
        match(accion_usuario):
            case "qwen":
                ia_escogida = "qwen2.5-coder-7b-instruct"
            case "gemma":
                ia_escogida = "google/gemma-4-e4b"
            case "openai":
                ia_escogida = "open_ai"
        file = request.form['files'], ""
        print(file)
            
        reply_ia = obtener_respuesta(promt, ia_escogida)
        print(reply_ia)
        return jsonify({"respuesta_ia" : reply_ia})

    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)