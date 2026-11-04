from flask import Flask, render_template, request

app = Flask(__name__)




@app.route("/", methods=['POST', 'GET'])
def inicio():
    if(request.method == "POST"):

        accion_usuario = request.form['accion-usuario']
        print(accion_usuario)
        match(accion_usuario):
            case "img":
                datos = request.form['img']
            case "promt":
                datos = request.form['pront']
            case "create_img":
                datos = request.form['create-img']
    
    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)