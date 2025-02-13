from flask import Flask, jsonify

app = Flask(__name__)


from products import productos
from lista import datos


@app.route('/')
def Inicio():
    return jsonify({"mensaje": "Bienvenido a la API de productos selecciona /productos. para ver la lista de productos y /productos/nombre para ver un producto en especifico"})

@app.route('/datos')
def ListaDeDatos():
    return jsonify(datos)


@app.route('/productos')
def ListaDeLosProductos():
    return jsonify (productos)

@app.route('/productos/<string:producto_nombre>')
def SeleccionDeProducto(producto_nombre):
    for producto in productos:
        if producto["nombre"] == producto_nombre:
            return jsonify(producto)
    return jsonify({"mensaje": "Producto no encontrado"})

@app.route('/datos/<string:datos_nombre>')
def SeleccionDeDato_lista(datos_nombre):
    for dato in datos:
        if dato["inventario"] == datos_nombre:
            return jsonify(dato)
    return jsonify({"mensaje": "Dato no encontrado"})   
    
@app.route("/datos/agregar,methods=['POST']")
def AgregarDato_lista():
    nuevo_dato = {
        "inventario": "papa",
        "cantidad": 10,
        "precio": 5
    }
    datos.append(nuevo_dato)
    return jsonify({"mensaje": "Dato agregado correctamente", "datos": datos})




if __name__ == '__main__' : 
    app.run(debug = True, port=4000) 

    