from flask import Flask, jsonify, request
from flask_cors import CORS 
import os
import struct
import json
from process_data import TelemetryProcessClass
# Aquí importarías tus clases: CarTelemetryDataClass, etc.

app = Flask(__name__)
CORS(app)

CARPETA_READ = "../DataUDPF12021"

procesador = TelemetryProcessClass()

# 1. Obtener nombres de archivos
@app.route('/get_files', methods=['GET'])
def get_files():
    archivos = [f for f in os.listdir(CARPETA_READ) if f.endswith('.dat')]
    return json.dumps(archivos)



# 2. Obtener sesiones de un archivo
@app.route('/sessions/<name_file>', methods=['GET'])
def get_sesiones(name_file):

    n_f = os.path.join(CARPETA_READ, f"{name_file}")

    data = procesador.get_data_laps( n_f )
    return json.dumps(data)


# # 3. Obtener pistas (Tracks)
# @app.route('/pistas/<id_sesion>', methods=['GET'])
# def obtener_pistas(id_sesion):
    # # Lógica para mapear el ID de pista del juego al nombre real
    # pistas = ["Interlagos", "Monza"]
    # return jsonify(pistas)

# 4. Obtener vueltas (Laps) y sectores
@app.route('/get_telemetry/<name_file>/<int:session_id>/<int:lap_id>', methods=['GET'])
def get_telemetry( name_file, session_id, lap_id ) :

    n_f = os.path.join(CARPETA_READ, f"{name_file}")

    data = procesador.get_data_telemetry( n_f, session_id, lap_id )
    
    return json.dumps(data)

# # 5. Datos de telemetría detallados de una vuelta
# @app.route('/telemetria/<lap_id>', methods=['GET'])
# def detalle_telemetria(lap_id):
    # # Aquí devolverías el array de velocidades, temperaturas, etc.
    # # que procesaste con tus clases.
    # datos = {"velocidad": [200, 205, 210], "freno": [0, 0, 100]}
    # return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True, port=8000)