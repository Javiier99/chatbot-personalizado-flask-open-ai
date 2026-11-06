from flask import Flask, render_template, request

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
                datos = request.form['ia-escogida']
                ia_escogida = "qwen2.5-coder-7b-instruct"
            case "gemma":
                datos = request.form['ia-escogida']
                ia_escogida = "google/gemma-4-e4b"

        # file = request.form['file'], ""
        # print(file)
        # if(file):
        #     print(f"Archivo recibido {file}")
        
        print(f"Este es el promt {promt}")
        print(datos)
        print(ia_escogida)

    
    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)