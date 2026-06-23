# data_sessions {
#       id  : "",
#       fecini  : ""
#       fecfin  : ""
#       data_tracks : [  {
#                       id : "",
#                       name : "",
#                       data_laps : [{
#                               laps : [],
#                               car_setup : []
#                               car_telemetry : []
#                               motions : []
#                       },]
#                   },] 
# }


import datetime
import os
import struct
from packets import *
import json
import mmap
import datetime

# https://github.com/raweceek-temeletry/f1-2021-udp?tab=readme-ov-file#motion-packet

CARPETA_READ = "../DataUDPF12021"

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



def save_file_idx( name_file, data ) :
    with open( name_file , "w") as f:
        f.write( data )



def load_file_idx( name_file ) :
    with open( name_file , "r" ) as f:
        return json.load( f )



def listar_archivos():
    archivos = [f for f in os.listdir(CARPETA_READ) if f.endswith('.dat')]
    return json.dumps(archivos) 



def format_f1_time( ms_total ):
    # 1. Calcular minutos, segundos y milisegundos restantes
    minutos = ms_total // 60000
    segundos = (ms_total % 60000) // 1000
    milis = ms_total % 1000
    
    # 2. Formatear con ceros a la izquierda (zfill)
    # %01d: 1 dígito para minutos
    # %02d: 2 dígitos para segundos
    # %03d: 3 dígitos para milisegundos
    return f"{minutos}:{segundos:02d}.{milis:03d}"


# Se creará un index con todos los datos para poder leer más rapido los datos requeridos
# params
# file, el archivo a leer los datos
def create_sessions_idx( file, file_size ) :
     
    data_sessions = []
               
    offset = 0
    lastHeader = HeaderClass( bytes.fromhex('00'*24) )
    
    lastTime = 0
    lastNumLap = 0
    
    while offset < file_size:
       
        header_data = file.read( HeaderClass.len_payload(HeaderClass) )
                
        if len(header_data) < HeaderClass.len_payload(HeaderClass): break
        
        header = HeaderClass( header_data )
        
        # payload_data = file.read( MAPPER[header.m_packetId].len_payload(MAPPER[header.m_packetId]) )
        
                        
        match header.m_packetId:
        
        
            #Procesando Session
            case 1 : 
               
                if lastHeader.m_sessionUID != header.m_sessionUID :
                    data_sessions.append({
                                            "id"                : header.m_sessionUID,
                                            "start_timestamp"   : header.m_sessionTime,
                                            "end_timestamp"     : header.m_sessionTime,
                                            "offsets"           : [],
                                            "data_laps"         : []
                                        })
                
                data_sessions[-1]['end_timestamp'] = header.m_sessionTime
                data_sessions[-1]['offsets'].append( offset )
                
            # Procesando LapsData
            case 2 : 
                # packetClass = get_packet( header.m_packetId, header, payload_data )
                
                # Leyendo tiempo actual de la vuelta
                file.seek(offset + 28 )
                currentLapTime = int.from_bytes( file.read(4), byteorder='little', signed=False )
                
                # Leyendo Lap Actual
                file.seek( offset + 49 )
                currentLapNum = int.from_bytes( file.read(1), byteorder='little', signed=False )

                if currentLapNum > lastNumLap or ( currentLapNum == lastNumLap and lastTime > currentLapTime ):

                    data_sessions[-1][ 'data_laps' ].append({
                                                    "numLap"        : currentLapNum,
                                                    "laps"          : [],
                                                    "car_setup"     : [],
                                                    "car_telemetry" : [],
                                                    "motions"       : []
                                               })
               
                data_sessions[-1][ 'data_laps' ][-1][ 'laps' ].append(offset)
                
                lastTime    = currentLapTime
                lastNumLap  = currentLapNum

            # Procesando CarTelemetry
            case 6 :
                if lastHeader.m_frameIdentifier == header.m_frameIdentifier :
                    data_sessions[-1][ 'data_laps' ][-1]['car_telemetry'].append( offset )
                
            # Procesando MotionData
            case 0 :
                if lastHeader.m_frameIdentifier == header.m_frameIdentifier :
                    data_sessions[-1][ 'data_laps' ][-1]['motions'].append( offset )
            
            # Procesando CarSetup
            case 5 :
                try :
                    if lastHeader.m_frameIdentifier == header.m_frameIdentifier :
                        data_sessions[-1][ 'data_laps' ][-1]['car_setup'].append( offset )
                except :
                    pass
        
        match header.m_packetId:
            case 1 |2 | 6 | 0 | 5 :
                lastHeader = header
                
        offset += MAPPER[header.m_packetId].sizeBytes
        file.seek(offset)
        
    print( json.dumps(data_sessions, indent=4) )
    return data_sessions



# Obtener las vueltas de la vista con la siguiete información
# Nro de vuelta
# Tiempo Total
# Tiempo del sector 1
# Tiempo del sector 2
def get_laps( sessions, file_path ) :

    file = open( file_path, 'rb')
    # Mapeamos el archivo en memoria (Solo lectura)
    mm = mmap.mmap( file.fileno(), 0, access=mmap.ACCESS_READ)
    
    session_data = []
    
    try :
        for session in sessions :
        
            object_session_data = MAPPER[1]( HeaderClass( mm[ session['offsets'][0] : session['offsets'][0] + HeaderClass.sizeBytes ] ), 
                                             mm[ session['offsets'][0] + HeaderClass.sizeBytes : session['offsets'][0] + MAPPER[1].sizeBytes ] )
            
            session_data.append({
                                    'track'         : object_session_data.m_trackId,
                                    'dataTimeLaps'  : []
                                })
        
            data_time_laps = session_data[-1]['dataTimeLaps']
        
            for lap in session['data_laps'] :
            
                offset = lap['laps'][-1]
            
                header = HeaderClass( mm[ offset : offset+HeaderClass.sizeBytes ] ) 
                
                object_lap_data = MAPPER[2]( header, mm[ offset + HeaderClass.sizeBytes : offset + MAPPER[2].sizeBytes ] )
                
                if lap['numLap'] > 1 and lap['numLap'] != data_time_laps[-1]['numLap']: 
                    data_time_laps[-1]['totalTime'] = object_lap_data.m_lapData[0].m_lastLapTimeInMS
                
                data_time_laps.append({ 
                                        'numLap'      : lap['numLap'],
                                        'totalTime'   : object_lap_data.m_lapData[0].m_currentLapTimeInMS,
                                        'timeSector1' : object_lap_data.m_lapData[0].m_sector1TimeInMS,
                                        'timeSector2' : object_lap_data.m_lapData[0].m_sector2TimeInMS
                                     })
                
            # for lap in data_time_laps :
                # print( f" LAP # : {lap['numLap']} - {format_f1_time(lap['totalTime'])} - {lap['timeSector1']} - {lap['timeSector2']} - {lap['totalTime'] - lap['timeSector1'] -lap['timeSector2']}" )
            
        print( json.dumps( session_data, indent=4) )
            
        return session_data
             
    except :
        print( "paso algo en get_laps" )
        mm.close()
        file.close()
    finally :
        mm.close()
        file.close()
        
        
# Obtener las vueltas de la vista con la siguiete información
# Nro de vuelta
# Tiempo Total
# Tiempo del sector 1
# Tiempo del sector 2
def get_telemetry( sessions, file_path, session_id, lap_id, meters_min = 0, meters_max = 100000 ) :

    file = open( file_path, 'rb')
    # Mapeamos el archivo en memoria (Solo lectura)
    mm = mmap.mmap( file.fileno(), 0, access=mmap.ACCESS_READ)
    
    try :
    
        # laps_telemetry tendría las posiciones car_setup car_telemetry motions
        laps_telemetry = sessions[session_id]['data_laps']
        
        # print( len( laps_telemetry[ lap_id ]['laps'] ) )
        # print( len( laps_telemetry[ lap_id ]['car_telemetry'] ) )
        # print( len( laps_telemetry[ lap_id ]['motions'] ) )
        
        for i, pos in zip ( [2], ['laps'] ) :
        
            data_telemetry = []
            
            for idx, offset in enumerate( laps_telemetry[ lap_id ][ pos] ) :
            
                header = HeaderClass( mm[ offset : offset+HeaderClass.sizeBytes ] ) 
                
                object_data = MAPPER[i]( header, mm[ offset + HeaderClass.sizeBytes : offset + MAPPER[i].sizeBytes ] )

                i_telemetry = {}

                # Solo se leerán los 3 primeros carros, esto puede tener fallas (la primera posición es el player, el segundo el fantasma del player, y el tercero el fantasma del oponente)
                # Según documentación no es 100% fiable que las posiciones siempre sean iguales
                for pos_car in range(3) :
                    
                    if object_data.m_lapData[pos_car].m_lapDistance > meters_min and object_data.m_lapData[pos_car].m_lapDistance < meters_max : 
                    
                        data = { 'lapDistance' : object_data.m_lapData[pos_car].m_lapDistance }
                        
                        # Leyendo los dato de telemetría
                        for ti, tpos in zip ( [ 6, 0 ], [ 'car_telemetry', 'motions' ] ) :
                            
                            o_tel = laps_telemetry[ lap_id ][ tpos ][ idx ]
                            
                            h_telemetry = HeaderClass( mm[ o_tel : o_tel+HeaderClass.sizeBytes ] ) 

                            o_telemetry = MAPPER[ti]( header, mm[ o_tel + HeaderClass.sizeBytes : o_tel + MAPPER[ti].sizeBytes ] )
                            
                            f_tel = o_telemetry.FIELDS[1]
                            
                            for k, v in getattr( o_telemetry, f_tel )[pos_car].__dict__.items() :
                                data[ k[2:] ] = v
                                # print( f"-- {k[2:]} - {v}" )
                                
                        i_telemetry[ pos_car ] = data
                
                data_telemetry.append( i_telemetry )
                
            # print( f"{json.dumps( data_telemetry )}" )
            return data_telemetry

    except:
        print( "paso algo en get_laps" )
        mm.close()
        file.close()
    finally :
        mm.close()
        file.close()



def iniciar() :

    fileRead = get_file_read()
    
    fileRead = fileRead[:-3]+'json'
    
    # print( fileRead )
    
    data_idx = load_file_idx( fileRead )
    
    # print( len( data_idx[0]['data_laps'] ) )
    
    # get_laps( data_idx, get_file_read() )
    
    data = get_telemetry( data_idx, get_file_read(), 0 , 0 )
    
    print( f"{json.dumps( data )}")
    
    # listar_archivos()
    
    # return None

    # fileRead = get_file_read()
    
    # file_size = os.path.getsize(fileRead)

    # print(f"Leyendo archivo: {fileRead}")
    
    # lastTime = 0
    # lastNumLap = 0

    # try:
    
        # # Abrir el archivo inicial
        # with open(fileRead, "rb") as file:

            # data_idx = create_sessions_idx( file, file_size )
            # save_file_idx( fileRead[:-3]+'json', json.dumps(data_idx, indent=4)  )

    # except KeyboardInterrupt:
        # print("\nCaptura detenida manualmente.")
    # except Exception as e:
        # print(f"Error en el servicio: {e}")

    
    
    
# def iniciar():

    # fileRead = get_file_read()
    
    # file_size = os.path.getsize(fileRead)

    # print(f"Leyendo archivo: {fileRead}")
    
    # lastTime = 0
    # lastNumLap = 0

    # try:
    
        # # Abrir el archivo inicial
        # with open(fileRead, "rb") as file:

            # while file.tell() < file_size:
                
                # header_data = file.read( HeaderClass.len_payload(HeaderClass) )
                
                # if len(header_data) < HeaderClass.len_payload(HeaderClass): break
                
                # header = HeaderClass( header_data )
                # packet_id = header.m_packetId
                
                # payload_data = file.read( MAPPER[packet_id].len_payload(MAPPER[packet_id]) )
                                
                # match packet_id:
                
                    # case 2 : 
                        # packetClass = get_packet( packet_id, header, payload_data )

                        # if packetClass.m_lapData[0].m_currentLapNum > lastNumLap or ( packetClass.m_lapData[0].m_currentLapNum == lastNumLap and lastTime > packetClass.m_lapData[0].m_currentLapTimeInMS ):
                            # print( f"Lap #: {packetClass.m_lapData[0].m_currentLapNum} - {packetClass.m_lapData[0].m_currentLapTimeInMS} - {header.m_playerCarIndex}" )
                        
                        # for i in range( 22 ):
                            # if( packetClass.m_lapData[0].m_carPosition != 0 ): 
                                # print( f"-- # pos: {i} {packetClass.m_lapData[0].m_carPosition}" )
                        
                        # lastTime = packetClass.m_lapData[0].m_currentLapTimeInMS
                        # lastNumLap = packetClass.m_lapData[0].m_currentLapNum
                    
                        # # return None
                    # # case 4 :
                        # # print(f"Si hay participantes")

    # except KeyboardInterrupt:
        # print("\nCaptura detenida manualmente.")
    # except Exception as e:
        # print(f"Error en el servicio: {e}")
    # #finally:
    # #    sock.close()

if __name__ == "__main__":
    iniciar()