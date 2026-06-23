# Este script se encarga de leer los datos puros desde una fuente y guardarlos en un archivo
# Siempre debe estar corriendo este script para obtener los datos

import json
import socket
import datetime
import os

# --- CONFIGURACIÓN ---
# IP_ESCUCHA = "127.0.0.1"
# PUERTO_UDP = 20777
# CARPETA_LOGS = "DataUDPF12021"

# Obteniendo datos de configuración
with open('./config.json', 'r') as file:
    config = json.load(file)

#Obteniendo los datos desde dónde se obtiene los datos de la telemetría desde la fuente (f1 2021, f1 2025, iracing, etc )
IP_ESCUCHA   = config[ 'rawData' ][ 'ip' ]
PUERTO_UDP   = config[ 'rawData' ][ 'portUdp' ]
CARPETA_LOGS = config[ 'rawData' ][ 'folder' ]

# Crear la carpeta si no existe
if not os.path.exists(CARPETA_LOGS):
    os.makedirs(CARPETA_LOGS)

def obtener_nombre_archivo():
    # Crea un nombre basado en la fecha y hora actual
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(CARPETA_LOGS, f"session_{fecha_hora}.dat")

def iniciar_captura():
    # Configurar socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_ESCUCHA, PUERTO_UDP))
    
    archivo_actual = obtener_nombre_archivo()
    
    print(f"Servicio activo. Guardando en: {archivo_actual}")

    try:
        # Abrir el archivo inicial
        with open(archivo_actual, "ab") as f:
            while True:
                # Recibir paquete (máximo 2048 bytes para F1 2021)
                data, addr = sock.recvfrom(2048)
                
                # Escribir en binario (máxima velocidad, mínimo CPU)
                f.write(data)
                
    except KeyboardInterrupt:
        print("\nCaptura detenida manualmente.")
    except Exception as e:
        print(f"Error en el servicio: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    iniciar_captura()