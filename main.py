from flask import Flask, jsonify

app = Flask( __name__)

from lista import datos

from products import productos
 
@app.route('/datos')
def diego():
    return jsonify (datos)

@app.route('/hola')
def hola():
    return "Hola Mundo"

@app.route('/datos/<string:datos_nombre>')
def diego2(nombre):
    print(nombre)
    return 'recibido'

@app.route('/mundo')
def mundo():
    return jsonify ({"mensaje": "Hola Mundo"})

@app.route('/productos')
def ListaDeLosProductos():
    return jsonify (productos)

@app.route('/productos/<string:nombre>') 
def Producto(nombre):
    for producto in productos:
       if producto["nombre"] == nombre:
           return jsonify(producto)
    return jsonify({"mensaje": "Producto no encontrado"})   


if __name__ == '__main__' : 
    app.run(debug = True) 
    

