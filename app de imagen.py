from flask import Flask, request, jsonify, send_from_directory
import os
import shutil

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la carpeta donde se guardarán las imágenes subidas
CARPETA_DE_SUBIDAS = 'subidas'
if not os.path.exists(CARPETA_DE_SUBIDAS):
    os.makedirs(CARPETA_DE_SUBIDAS)

# Configurar la carpeta donde se guardarán las imágenes descargadas
CARPETA_DE_DESCARGAS = 'descargas'
if not os.path.exists(CARPETA_DE_DESCARGAS):
    os.makedirs(CARPETA_DE_DESCARGAS)

# Asignar las carpetas a la configuración de Flask
app.config['CARPETA_DE_SUBIDAS'] = CARPETA_DE_SUBIDAS
app.config['CARPETA_DE_DESCARGAS'] = CARPETA_DE_DESCARGAS

# Definir las extensiones de archivo permitidas
EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}

# Función para verificar si un archivo tiene una extensión permitida
def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

# Endpoint para subir imágenes
@app.route('/subir', methods=['POST'])
def subir_imagen():
    # Verificar si se ha enviado un archivo en la solicitud
    if 'archivo' not in request.files:
        return jsonify({"error": "No se ha enviado ningún archivo"}), 400

    archivo = request.files['archivo']

    # Verificar si el archivo tiene un nombre
    if archivo.filename == '':
        return jsonify({"error": "No se ha seleccionado ningún archivo"}), 400

    # Verificar si el archivo tiene una extensión permitida y guardarlo
    if archivo and archivo_permitido(archivo.filename):
        ruta_archivo = os.path.join(app.config['CARPETA_DE_SUBIDAS'], archivo.filename)
        archivo.save(ruta_archivo)
        return jsonify({"mensaje": "Archivo subido exitosamente", "ruta_archivo": ruta_archivo}), 200
    else:
        return jsonify({"error": "Tipo de archivo no permitido"}), 400

# Endpoint para ver una imagen subida
@app.route('/ver/<nombre_archivo>', methods=['GET'])
def ver_imagen(nombre_archivo):
    # Verificar si el archivo existe en la carpeta de subidas
    ruta_archivo = os.path.join(app.config['CARPETA_DE_SUBIDAS'], nombre_archivo)
    if not os.path.isfile(ruta_archivo):
        return jsonify({"error": "El archivo no existe"}), 404

    # Servir la imagen como un archivo estático
    return send_from_directory(app.config['CARPETA_DE_SUBIDAS'], nombre_archivo)

# Endpoint para descargar una imagen subida
@app.route('/descargar/<nombre_archivo>', methods=['GET'])
def descargar_imagen(nombre_archivo):
    # Verificar si el archivo existe en la carpeta de subidas
    ruta_archivo_subida = os.path.join(app.config['CARPETA_DE_SUBIDAS'], nombre_archivo)
    if not os.path.isfile(ruta_archivo_subida):
        return jsonify({"error": "El archivo no existe"}), 404

    # Copiar el archivo a la carpeta de descargas
    ruta_archivo_descarga = os.path.join(app.config['CARPETA_DE_DESCARGAS'], nombre_archivo)
    shutil.copy(ruta_archivo_subida, ruta_archivo_descarga)

    # Forzar la descarga del archivo
    return send_from_directory(
        app.config['CARPETA_DE_DESCARGAS'],
        nombre_archivo,
        as_attachment=True  # Esto fuerza la descarga del archivo
    )
    
# Endpoint para dar una lista y ver de las imagenes subidas en json
@app.route('/lista', methods=['GET'])
def lista_imagenes():
    # Obtener la lista de archivos en la carpeta de subidas
    archivos = os.listdir(app.config['CARPETA_DE_SUBIDAS'])
    return jsonify({"archivos": archivos})



# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)