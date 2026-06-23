import datetime
import os
import struct
from packets import *
import json
import mmap
import datetime

# https://github.com/raweceek-temeletry/f1-2021-udp?tab=readme-ov-file#motion-packet

CARPETA_READ = "../DataUDPF12021"


class TelemetryProcessClass : 

    def get_file_read():
        # Crea un nombre basado en la fecha y hora actual
        return os.path.join(CARPETA_READ, f"session_2026-04-15_18-38-25.dat")

        
    def save_file_idx( self, name_file, data ) :
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
    def create_sessions_idx( self, file, file_size ) :
         
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
                case 1 | 11 : 
                   
                    if lastHeader.m_sessionUID != header.m_sessionUID :
                        data_sessions.append({
                                                "id"                : header.m_sessionUID,
                                                "start_timestamp"   : header.m_sessionTime,
                                                "end_timestamp"     : header.m_sessionTime,
                                                "offsets"           : [],
                                                "data_laps"         : []
                                            })
                                            
                        lastTime = 0
                        lastNumLap = 0
                    
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
            
        # print( json.dumps(data_sessions, indent=4) )
        return data_sessions



    # Obtener las vueltas de la vista con la siguiete información
    # Nro de vuelta
    # Tiempo Total
    # Tiempo del sector 1
    # Tiempo del sector 2
    def get_laps( self, sessions, file_path ) :

        print( f"nombre de archivo {file_path}")

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
                                            'timeSector2' : object_lap_data.m_lapData[0].m_sector2TimeInMS,
                                            'invalid'     : object_lap_data.m_lapData[0].m_currentLapInvalid
                                         })
                    
                # for lap in data_time_laps :
                    # print( f" LAP # : {lap['numLap']} - {format_f1_time(lap['totalTime'])} - {lap['timeSector1']} - {lap['timeSector2']} - {lap['totalTime'] - lap['timeSector1'] -lap['timeSector2']}" )
                
            # print( json.dumps( session_data, indent=4) )
                
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
    def get_telemetry( self, sessions, file_path, session_id, lap_id, meters_min = -1000000, meters_max = 1000000 ) :

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
                        
                        # if object_data.m_lapData[pos_car].m_lapDistance > meters_min and object_data.m_lapData[pos_car].m_lapDistance < meters_max : 
                        
                            data = { 
                                     'lapDistance'        : object_data.m_lapData[pos_car].m_lapDistance,
                                     'currentLapTimeInMS' : object_data.m_lapData[pos_car].m_currentLapTimeInMS
                                   }
                            
                            # Leyendo los dato de telemetría
                            for ti, tpos in zip ( [ 6, 0 ], [ 'car_telemetry', 'motions' ] ) :
                                
                                o_tel = laps_telemetry[ lap_id ][ tpos ][ idx ]
                                
                                h_telemetry = HeaderClass( mm[ o_tel : o_tel+HeaderClass.sizeBytes ] ) 

                                o_telemetry = MAPPER[ti]( header, mm[ o_tel + HeaderClass.sizeBytes : o_tel + MAPPER[ti].sizeBytes ] )
                                
                                f_tel = o_telemetry.FIELDS[1]
                                    
                                for k, v in getattr( o_telemetry, f_tel )[pos_car].__dict__.items() :
                                    data[ k[2:] ] = v
                                    
                            i_telemetry[ pos_car ] = data
                    
                    data_telemetry.append( i_telemetry )
                    
                # print( f"{json.dumps( data_telemetry )}" )
                return data_telemetry

        except Exception as e:
            print( f"paso algo en get_telemetry {e}" )
            mm.close()
            file.close()
        finally :
            mm.close()
            file.close()



    def load_index( self, name_file ) :
    
        ruta_idx = name_file.replace(".dat", ".idx")
        
        if os.path.exists(ruta_idx):
            print("Cargando índice desde archivo...")
            return self.load_file_idx( name_file )
            
        else:
            print("Índice no encontrado. Escaneando archivo binario (esto puede tardar)...")
            
            file_size = os.path.getsize(name_file)
            
            with open(name_file, "rb") as file:
                data_idx = self.create_sessions_idx( file, file_size )
            
                self.save_file_idx( name_file[:-3]+'json', json.dumps(data_idx)  )
            
            # Guardarlo para la próxima vez
            # with open(ruta_idx, "wb") as f:
                # pickle.dump(nuevo_indice, f)
                
            return data_idx

    def get_data_laps( self, name_file ) :
        
        idx = self.load_index( name_file )
        
        data = self.get_laps( idx, name_file )
        
        return data
        
        
    def get_data_telemetry( self, name_file, session_id, lap_id ) :
        # print( name_file, session_id, lap_id  )
        idx = self.load_index( name_file )
        
        data = self.get_telemetry( idx, name_file, session_id, lap_id )
        # print( json.dumps(data) )
        return data

