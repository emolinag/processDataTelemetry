import datetime
import os
import struct

#https://github.com/raweceek-temeletry/f1-2021-udp?tab=readme-ov-file#motion-packet

# Tipos de paquete incluyendo la cabecera
# Si estás analizando el flujo:
packets = {
    0: 1464,    # Motion
    1: 625,     # Session
    2: 970,     # Lap Data
    3: 36,      # Event
    4: 1257,    # Participants
    5: 1102,    # Car Setups
    6: 1347,    # Car Telemetry
    7: 1058,    # Car Status
    8: 839,     # Final Classification
    9: 1191,    # Lobby Info
    10: 882,    # Car Damage
    11: 1155    # Session History
}

packets_out = [
    3,  # Event
    4,  # Participants
    8,  # Final Classification
    9,  # Lobby Info
    10, # Car Damage
    11  # Session History
]

#longitud de la cabecera, todo paquete lo tiene
lengthHeader = 24

# H=uint16, B=uint8, Q=uint64, f=float, I=uint32
header_format = '<HBBBBQfIBB'
lapDataFormat = '<IIHHfffBBBBBBBBBBBBBBHHB'

CARPETA_READ = "DataUDPF12021"

CARPETA_LOGS = "processData"

# Crear la carpeta si no existe
if not os.path.exists(CARPETA_LOGS):
    os.makedirs(CARPETA_LOGS)

def get_file_read():
    # Crea un nombre basado en la fecha y hora actual
    return os.path.join(CARPETA_READ, f"session_2026-04-15_18-38-25.dat")
    
def obtener_nombre_archivo():
    # Crea un nombre basado en la fecha y hora actual
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(CARPETA_LOGS, f"processMain_{fecha_hora}.dat")

def iniciar():

    fileRead = get_file_read()
    
    file_size = os.path.getsize(fileRead)

    print(f"Leyendo archivo: {fileRead}")
    
    lastTime = 0
    lastNumLap = 0

    try:
        # Abrir el archivo inicial
        with open(fileRead, "rb") as file:

            while file.tell() < file_size:
                
                header_data = file.read( lengthHeader )
                
                if len(header_data) < lengthHeader: break
                
                header = struct.unpack( header_format, header_data[:24] )
                
                packet_id = header[4]
                
                # print( f"packet_id: {packet_id}" )
                # print( f"session_id: {header[7]}" )
                
                
                
                if packet_id in packets:
                    
                    payload_size = packets[packet_id] - lengthHeader
                    payload_data = file.read(payload_size)
                    
                    if packet_id == 2 :
                        # print( f"Entrando a LapData" )
                        packetLapData = struct.unpack( lapDataFormat, payload_data[:43] )
                        
                        
                        if packetLapData[8] > lastNumLap or ( packetLapData[8] == lastNumLap and lastTime > packetLapData[1] ):
                        
                            print( f"Lap #: {packetLapData[8]} - {packetLapData[0]}" )
                        
                        lastTime = packetLapData[1]
                        lastNumLap = packetLapData[8]
                else :
                    print( f"Error leyendo packet_id... No existe" )
                    break
                
    except KeyboardInterrupt:
        print("\nCaptura detenida manualmente.")
    except Exception as e:
        print(f"Error en el servicio: {e}")
    #finally:
    #    sock.close()

if __name__ == "__main__":
    iniciar()