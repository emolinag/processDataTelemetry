import struct
from .HeaderClass import HeaderClass

class CarTelemetryDataClass :

    sizeBytes = 60
    
    FORMAT = '<HfffBbHBBH'
    # 'HBBHfB'
    
    m_brakesTemperature = []
    m_tyresSurfaceTemperature = []
    m_tyresInnerTemperature = []
    m_tyresPressure = []
    m_surfaceType = []

    FIELDS = [	
                'm_speed',                    # Speed of car in kilometres per hour
                'm_throttle',                 # Amount of throttle applied (0.0 to 1.0)
                'm_steer',                    # Steering (-1.0 (full lock left) to 1.0 (full lock right))
                'm_brake',                    # Amount of brake applied (0.0 to 1.0)
                'm_clutch',                   # Amount of clutch applied (0 to 100)
                'm_gear',                     # Gear selected (1-8, N=0, R=-1)
                'm_engineRPM',                # Engine RPM
                'm_drs',                      # 0 = off, 1 = on
                'm_revLightsPercent',         # Rev lights indicator (percentage)
                'm_revLightsBitValue',        # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
                'm_brakesTemperature',        # Brakes temperature (celsius)
                'm_tyresSurfaceTemperature',  # Tyres surface temperature (celsius)
                'm_tyresInnerTemperature',    # Tyres inner temperature (celsius)
                'm_engineTemperature',        # Engine temperature (celsius)
                'm_tyresPressure',            # Tyres pressure (PSI)
                'm_surfaceType'               # Driving surface, see appendices
            ]
            
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload_data ) :
    
        try :
            offset = 0
        
            unpacked_values = struct.unpack_from(self.FORMAT, payload_data, offset )
            offset += struct.calcsize( self.FORMAT )
            
            for name, value in zip(self.FIELDS, unpacked_values):
                setattr(self, name, value)
            
            unpacked_values = struct.unpack_from( '<HHHHBBBBBBBBHffffBBBB', payload_data, offset )
            offset += struct.calcsize( '<HHHHBBBBBBBBHffffBBBB' )
            
            self.m_tyresSurfaceTemperature = list( unpacked_values[ : 4 ] )
            self.m_tyresInnerTemperature = list( unpacked_values[ 4 : 8 ] )
            self.m_engineTemperature = unpacked_values[9]
            self.m_tyresPressure = list( unpacked_values[ 10 : 12 ] )
            self.m_surfaceType = list( unpacked_values[ 12 : 16 ] )

            if offset != self.sizeBytes :
                raise validatePayload( f"Se espera {self.sizeBytes} y se leyó {offset}" )
            
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")
            
            
            
            
class PacketCarTelemetryDataClass :

    sizeBytes = 1347
    
    FORMAT = '<BBB'

    FIELDS = [	
        'm_header',                         # Header
        'm_carTelemetryData',
        'm_mfdPanelIndex',                  # Index of MFD panel open - 255 = MFD closed
                                            # Single player, race – 0 = Car setup, 1 = Pits
                                            # 2 = Damage, 3 =  Engine, 4 = Temperatures
                                            # May vary depending on game mode
        'm_mfdPanelIndexSecondaryPlayer',   # See above
        'm_suggestedGear'                   # Suggested gear for the player (1-8)
                                            # 0 if no gear suggested
    ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
    
        try :
    
            offset = 0
        
            setattr(self, self.FIELDS[0], header )
            
            self.m_carTelemetryData = []
        
            for i in range(22):
                self.m_carTelemetryData.append( CarTelemetryDataClass( payload[offset:offset + CarTelemetryDataClass.sizeBytes ] ) )
                offset += CarTelemetryDataClass.sizeBytes

            unpacked_values = struct.unpack_from( self.FORMAT, payload, offset )
            offset += struct.calcsize( self.FORMAT )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            for name, value in zip(self.FIELDS[ 2 : ], unpacked_values):
                setattr(self, name, value)
            
            if offset != self.len_payload( ) :
                raise validatePayload( f"Se espera {self.sizeBytes} y se leyó {offset}" )
            
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")