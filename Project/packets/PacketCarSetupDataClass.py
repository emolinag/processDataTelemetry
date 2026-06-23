import struct
from .HeaderClass import HeaderClass

class CarSetupDataClass :

    sizeBytes = 49
    
    FORMAT = '<BBBBffffBBBBBBBBffffBf'

    FIELDS = [	
                'm_frontWing',                # Front wing aero
                'm_rearWing',                 # Rear wing aero
                'm_onThrottle',               # Differential adjustment on throttle (percentage)
                'm_offThrottle',              # Differential adjustment off throttle (percentage)
                'm_frontCamber',              # Front camber angle (suspension geometry)
                'm_rearCamber',               # Rear camber angle (suspension geometry)
                'm_frontToe',                 # Front toe angle (suspension geometry)
                'm_rearToe',                  # Rear toe angle (suspension geometry)
                'm_frontSuspension',          # Front suspension
                'm_rearSuspension',           # Rear suspension
                'm_frontAntiRollBar',         # Front anti-roll bar
                'm_rearAntiRollBar',          # Front anti-roll bar
                'm_frontSuspensionHeight',    # Front ride height
                'm_rearSuspensionHeight',     # Rear ride height
                'm_brakePressure',            # Brake pressure (percentage)
                'm_brakeBias',                # Brake bias (percentage)
                'm_rearLeftTyrePressure',     # Rear left tyre pressure (PSI)
                'm_rearRightTyrePressure',    # Rear right tyre pressure (PSI)
                'm_frontLeftTyrePressure',    # Front left tyre pressure (PSI)
                'm_frontRightTyrePressure',   # Front right tyre pressure (PSI)
                'm_ballast',                  # Ballast
                'm_fuelLoad'                  # Fuel load
            ]
            
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload_data ) :
    
        try :
            offset = 0
        
            # 2. Desempaquetamos los datos en una tupla
            unpacked_values = struct.unpack_from( self.FORMAT, payload_data, offset )
            offset += struct.calcsize( self.FORMAT )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            for name, value in zip(self.FIELDS, unpacked_values):
                setattr(self, name, value)
                
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")
            
            
            
            
            
class PacketCarSetupDataClass :

    sizeBytes = 1102
    
    FORMAT = ''
    
    m_carSetups = []

    FIELDS = [	
        'm_header',            # Header
        'm_carSetups'
    ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
        
        try :
            offset = 0
            
            setattr(self, self.FIELDS[0], header )
        
            for i in range(22):
                self.m_carSetups.append( CarSetupDataClass( payload[offset:offset+CarSetupDataClass.sizeBytes] ) )
                offset += CarSetupDataClass.sizeBytes
            
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
            
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")